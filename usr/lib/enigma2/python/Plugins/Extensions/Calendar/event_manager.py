#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
###########################################################
#  Calendar Planner for Enigma2 v1.6                      #
#  Created by: Lululla (based on Sirius0103)              #
###########################################################

MAIN FEATURES:
• Calendar with color-coded days (events/holidays/today)
• Event system with smart notifications & audio alerts
• Holiday import for 30+ countries with auto-coloring
• vCard import/export with contact management
• Database format converter (Legacy ↔ vCard)

NEW IN v1.6:
vCard EXPORT to /tmp/calendar.vcf
Database converter with progress tracking
Auto-conversion option in settings
Contact sorting in export (name/birthday/category)
Optimized import performance
Fixed holiday cache refresh

KEY CONTROLS - MAIN:
OK    - Main menu (Events/Holidays/Contacts/Import/Export/Converter)
RED   - Previous month
GREEN - Next month
YELLOW- Previous day
BLUE  - Next day
0     - Event management
MENU  - Configuration

EXPORT VCARD:
• Export contacts to /tmp/calendar.vcf
• Sorting: name, birthday, or category
• vCard 3.0 format compatible
• Progress tracking

DATABASE CONVERTER:
• Convert Legacy ↔ vCard formats
• Automatic backup creation
• Progress & statistics display
• Auto-conversion option

CONFIGURATION:
• Database format (Legacy/vCard)
• Auto-convert option
• Export sorting preference
• Event/holiday colors & indicators
• Audio notification settings

TECHNICAL:
• Python 2.7+ compatible
• Multi-threaded vCard import
• Smart cache system
• File-based storage
• Configurable via setup.xml

VERSION HISTORY:
v1.0 - Basic calendar
v1.1 - Event system
v1.2 - Holiday import
v1.3 - Code rewrite
v1.4 - Bug fixes
v1.5 - vCard import
v1.6 - vCard export & converter

Last Updated: 2025-12-26
Status: Stable with complete vCard support
Credits: Sirius0103 (original), Lululla (modifications)
Homepage: www.linuxsat-support.com
###########################################################
"""
from __future__ import print_function
import time
import subprocess
import shutil
from os import makedirs
from os.path import exists, dirname, join
from json import load, dump
from datetime import datetime, timedelta
from enigma import eTimer, eServiceReference, eServiceCenter
from Components.config import config
from Screens.MessageBox import MessageBox

from . import _, PLUGIN_PATH

events_json = join(PLUGIN_PATH, "events.json")
sounds_dir = join(PLUGIN_PATH, "sounds")
DEBUG = config.plugins.calendar.debug_enabled.value if hasattr(config.plugins, 'calendar') and hasattr(config.plugins.calendar, 'debug_enabled') else False


try:
    from .notification_system import init_notification_system, quick_notify
    NOTIFICATION_AVAILABLE = True
except ImportError:
    NOTIFICATION_AVAILABLE = False
    print("[EventManager] Notification system not available")


class Event:
    """Class to represent a single event"""

    def __init__(self, title="Event", description="Description", date="", event_time="",
                 repeat="none", notify_before=5, enabled=True):
        self.title = title
        self.description = description
        self.date = date  # Format: YYYY-MM-DD
        self.time = event_time  # Format: HH:MM - assegna a self.time
        self.repeat = repeat  # none, daily, weekly, monthly, yearly
        self.notify_before = notify_before  # minutes before
        self.enabled = enabled
        self.created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.id = int(time.time() * 1000)  # Unique ID

        # NEW FIELD: Labels for display
        self.labels = self._extract_labels()

    def _extract_labels(self):
        """Extract labels automatically from title and description"""
        labels = []

        # Extract keywords from title (minimum 3 letters)
        if self.title and self.title != "Event":
            words = self.title.split()
            for word in words:
                if len(word) > 2:  # Words with more than 2 characters
                    clean_word = ''.join(c for c in word if c.isalnum())
                    if clean_word:
                        labels.append(clean_word.lower())

        # Extract keywords from description
        if self.description and self.description != "Description":
            words = self.description.split()
            for word in words:
                if len(word) > 2:  # Words with more than 2 characters
                    clean_word = ''.join(c for c in word if c.isalnum())
                    if clean_word:
                        labels.append(clean_word.lower())

        # Add special labels based on event properties
        if self.repeat != "none":
            labels.append("recurring")
            labels.append("repeat-" + self.repeat)

        # Add status label
        if self.enabled:
            labels.append("active")
        else:
            labels.append("inactive")

        # Add time-based labels
        if self.time:
            try:
                hour = int(self.time.split(':')[0])
                if 5 <= hour < 12:
                    labels.append("morning")
                elif 12 <= hour < 17:
                    labels.append("afternoon")
                elif 17 <= hour < 22:
                    labels.append("evening")
                else:
                    labels.append("night")
            except:
                pass

        # Remove duplicates and return
        seen = set()
        unique_labels = []
        for label in labels:
            if label not in seen:
                seen.add(label)
                unique_labels.append(label)

        return unique_labels

    def to_dict(self):
        """Convert event to dictionary for JSON"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date,
            'time': self.time,
            'repeat': self.repeat,
            'notify_before': self.notify_before,
            'enabled': self.enabled,
            'created': self.created,
            'labels': self.labels  # Save labels
        }

    @classmethod
    def from_dict(cls, data):
        """Create event from dictionary"""
        event = cls()
        for key, value in data.items():
            if hasattr(event, key):
                setattr(event, key, value)
        return event

    def update_labels(self):
        """Update labels after editing"""
        self.labels = self._extract_labels()

    def get_datetime(self):
        """Return datetime object of the event"""
        try:
            return datetime.strptime("{0} {1}".format(self.date, self.time), "%Y-%m-%d %H:%M")
        except ValueError:
            return None

    def get_next_occurrence(self, from_date=None):
        if not self.enabled:
            return None

        event_dt = self.get_datetime()
        if not event_dt:
            return None

        if from_date is None:
            from_date = datetime.now()

        if self.repeat == "none":
            if event_dt >= from_date or (from_date - event_dt) <= timedelta(minutes=2):
                return event_dt
            return None

        elif self.repeat == "daily":
            # For daily events, find the next day
            test_date = datetime(from_date.year, from_date.month, from_date.day,
                                 event_dt.hour, event_dt.minute)
            if test_date < from_date:
                test_date += timedelta(days=1)
            return test_date

        elif self.repeat == "weekly":
            # For weekly events (same day of week)
            event_weekday = event_dt.weekday()
            current_weekday = from_date.weekday()

            days_ahead = event_weekday - current_weekday
            if days_ahead < 0 or (
                days_ahead == 0 and
                    (event_dt.hour < from_date.hour or
                        (event_dt.hour == from_date.hour and event_dt.minute <= from_date.minute))):
                days_ahead += 7

            next_date = from_date + timedelta(days=days_ahead)
            return datetime(next_date.year, next_date.month, next_date.day,
                            event_dt.hour, event_dt.minute)

        elif self.repeat == "monthly":
            # For monthly events (same day of month)
            test_date = datetime(from_date.year, from_date.month,
                                 min(event_dt.day, 28),  # Avoid February issues
                                 event_dt.hour, event_dt.minute)

            if test_date < from_date:
                # Move to next month
                if from_date.month == 12:
                    test_date = datetime(from_date.year + 1, 1,
                                         min(event_dt.day, 28),
                                         event_dt.hour, event_dt.minute)
                else:
                    test_date = datetime(from_date.year, from_date.month + 1,
                                         min(event_dt.day, 28),
                                         event_dt.hour, event_dt.minute)

            # Adjust for months with less than 31 days
            while True:
                try:
                    datetime(test_date.year, test_date.month, event_dt.day)
                    break
                except ValueError:
                    test_date = datetime(test_date.year, test_date.month,
                                         event_dt.day - 1,
                                         event_dt.hour, event_dt.minute)

            return test_date

        elif self.repeat == "yearly":
            # For yearly events (same day and month)
            test_date = datetime(from_date.year, event_dt.month, event_dt.day,
                                 event_dt.hour, event_dt.minute)

            if test_date < from_date:
                test_date = datetime(from_date.year + 1, event_dt.month, event_dt.day,
                                     event_dt.hour, event_dt.minute)

            return test_date

        return None

    def should_notify(self, current_time=None):
        """Check if it's time to notify about the event"""
        if not self.enabled:
            return False

        next_occurrence = self.get_next_occurrence(current_time)
        if not next_occurrence:
            return False

        if current_time is None:
            current_time = datetime.now()

        # Calculate when notification should be shown
        notify_time = next_occurrence - timedelta(minutes=self.notify_before)

        return notify_time <= current_time <= next_occurrence + timedelta(minutes=5)

    def is_active(self, current_time=None):
        """Check if event is active right now"""
        if not self.enabled:
            return False

        next_occurrence = self.get_next_occurrence(current_time)
        if not next_occurrence:
            return False

        if current_time is None:
            current_time = datetime.now()

        # Consider event active for 30 minutes after scheduled time
        event_end = next_occurrence + timedelta(minutes=30)

        return next_occurrence <= current_time <= event_end


class EventManager:
    """Central event manager with notification system"""

    def __init__(self, session, events_file=None):
        self.session = session
        self.events_file = events_file or events_json
        self.sound_dir = sounds_dir

        self.events = []

        self.notified_events = set()  # Events already notified in this session
        self.tv_service_backup = None  # For TV service backup
        self.sound_stop_timer = None   # For audio timer

        # Timer to check events
        self.check_timer = eTimer()
        try:
            self.check_timer_conn = self.check_timer.timeout.connect(self.check_events)
        except AttributeError:
            self.check_timer.callback.append(self.check_events)

        # Timer to update current time
        self.time_timer = eTimer()
        try:
            self.time_timer_conn = self.time_timer.timeout.connect(self.update_time)
        except AttributeError:
            self.time_timer.callback.append(self.update_time)

        self.load_events()
        self.start_monitoring()

        # Initialize notification system if available
        if NOTIFICATION_AVAILABLE:
            init_notification_system(session)

    def load_events(self):
        """Load events from JSON file"""
        try:
            if exists(self.events_file):
                with open(self.events_file, 'r', encoding='utf-8') as f:
                    data = load(f)
                    self.events = [Event.from_dict(event_data) for event_data in data]
                print("[EventManager] Loaded {0} events".format(len(self.events)))
            else:
                self.events = []
                print("[EventManager] No event file found, creating empty list")
        except Exception as e:
            print("[EventManager] Error loading events: {0}".format(e))
            self.events = []

    def start_monitoring(self):
        """Start event monitoring"""
        # Check events every 30 seconds
        self.check_timer.start(30000, True)
        # Update time every minute
        self.time_timer.start(60000, True)

    def stop_monitoring(self):
        """Stop event monitoring"""
        self.check_timer.stop()
        self.time_timer.stop()

    def save_events(self):
        """Save events to JSON file"""
        try:
            # Create directory if it doesn't exist
            makedirs(dirname(self.events_file), exist_ok=True)

            with open(self.events_file, 'w', encoding='utf-8') as f:
                dump([event.to_dict() for event in self.events], f,
                     indent=2, ensure_ascii=False)
            print("[EventManager] Saved {0} events".format(len(self.events)))
            return True
        except Exception as e:
            print("[EventManager] Error saving events: {0}".format(e))
            return False

    def add_event(self, event):
        """Add a new event"""
        self.events.append(event)
        self.save_events()
        print("[EventManager] Event added: {0}".format(event.title))
        return event.id

    def update_event(self, event_id, **kwargs):
        """Update an existing event"""
        for event in self.events:
            if event.id == event_id:
                for key, value in kwargs.items():
                    if key == 'event_time':
                        setattr(event, 'time', value)
                    elif hasattr(event, key):
                        setattr(event, key, value)

                # Update labels after modification
                event.update_labels()

                self.save_events()
                print("[EventManager] Event updated: {0}".format(event.title))
                return True
        return False

    def delete_event(self, event_id):
        """Delete an event"""
        self.events = [event for event in self.events if event.id != event_id]
        self.save_events()
        print("[EventManager] Event deleted: {0}".format(event_id))
        return True

    def get_event(self, event_id):
        """Get event by ID"""
        for event in self.events:
            if event.id == event_id:
                return event
        return None

    def get_events_for_date(self, date_str):
        """Get all events for a specific date (YYYY-MM-DD)"""
        result = []
        current_date = datetime.strptime(date_str, "%Y-%m-%d")

        for event in self.events:
            if not event.enabled:
                continue

            event_dt = event.get_datetime()
            if not event_dt:
                continue

            if event.repeat == "none":
                if event.date == date_str:
                    result.append(event)

            elif event.repeat == "daily":
                # Daily events are always included
                result.append(event)

            elif event.repeat == "weekly":
                # Same day of week
                event_weekday = event_dt.weekday()
                if current_date.weekday() == event_weekday:
                    result.append(event)

            elif event.repeat == "monthly":
                # Same day of month
                if current_date.day == event_dt.day:
                    result.append(event)

            elif event.repeat == "yearly":
                # Same day and month
                if current_date.month == event_dt.month and current_date.day == event_dt.day:
                    result.append(event)

        # Sort by time
        result.sort(key=lambda x: x.time)
        return result

    def get_upcoming_events(self, days=7):
        """Get upcoming events for the next N days"""
        result = []
        now = datetime.now()
        end_date = now + timedelta(days=days)

        current_date = now.date()
        while current_date <= end_date.date():
            date_str = current_date.strftime("%Y-%m-%d")
            daily_events = self.get_events_for_date(date_str)

            for event in daily_events:
                event_dt = event.get_datetime()
                if event_dt:
                    # For recurring events, calculate specific occurrence
                    if event.repeat != "none":
                        next_occurrence = event.get_next_occurrence(now)
                        if next_occurrence and next_occurrence.date() == current_date:
                            result.append((next_occurrence, event))
                    else:
                        if event_dt.date() == current_date:
                            result.append((event_dt, event))

            current_date += timedelta(days=1)

        # Sort by date/time
        result.sort(key=lambda x: x[0])
        return result

    def check_events(self):
        """Check events and show notifications if needed"""
        try:
            now = datetime.now()
            if DEBUG:
                print("[EventManager DEBUG] Checking events at {0}".format(now.strftime('%H:%M:%S')))
                print("[EventManager DEBUG] Total events: {0}".format(len(self.events)))

            events_checked = 0
            events_skipped = 0

            for event in self.events:
                # 1. If the event is disabled, skip it
                if not event.enabled:
                    if DEBUG:
                        print("[EventManager DEBUG] Event '{0}' is disabled - SKIP".format(event.title))
                    events_skipped += 1
                    continue

                # 2. For NON-recurring events already past by >5 minutes: SKIP CHECKING
                if event.repeat == "none":
                    event_dt = event.get_datetime()
                    if event_dt:
                        time_passed = now - event_dt

                        # Event passed more than 5 minutes ago AND already notified? SKIP
                        if time_passed > timedelta(minutes=5) and event.id in self.notified_events:
                            if DEBUG:
                                print("[EventManager DEBUG] Event '{0}' passed {1} min ago and already notified - SKIP CHECKING".format(
                                    event.title, time_passed.seconds // 60))
                            events_skipped += 1
                            continue

                        # Event passed more than 30 minutes ago (even if not notified)? SKIP
                        elif time_passed > timedelta(minutes=30):
                            if DEBUG:
                                print("[EventManager DEBUG] Event '{0}' passed {1} min ago - SKIP CHECKING".format(
                                    event.title, time_passed.seconds // 60))
                            events_skipped += 1
                            continue

                        # Event passed 2-30 minutes ago but not notified? Still check
                        elif time_passed > timedelta(minutes=2):
                            # Event passed but we might still be in notification window
                            pass

                events_checked += 1
                if DEBUG:
                    print("[EventManager DEBUG] Checking event: {0}".format(event.title))
                    print("[EventManager DEBUG]   Date/Time: {0} {1}".format(event.date, event.time))
                    print("[EventManager DEBUG]   Notify before: {0} min".format(event.notify_before))
                    print("[EventManager DEBUG]   Repeat: {0}".format(event.repeat))

                next_occurrence = event.get_next_occurrence(now)
                if next_occurrence:
                    if DEBUG:
                        print("[EventManager DEBUG]   Next occurrence: {0}".format(next_occurrence))

                    # Check if it's time to notify
                    notify_time = next_occurrence - timedelta(minutes=event.notify_before)
                    if DEBUG:
                        print("[EventManager DEBUG]   Notify time: {0}".format(notify_time))
                        print("[EventManager DEBUG]   Now: {0}".format(now))
                        print("[EventManager DEBUG]   Should notify window: {0} to {1}".format(
                            notify_time, next_occurrence + timedelta(minutes=5)))

                    should_notify = event.should_notify(now)
                    if DEBUG:
                        print("[EventManager DEBUG]   Should notify: {0}".format(should_notify))
                        print("[EventManager DEBUG]   Already notified: {0}".format(
                            event.id in self.notified_events))

                    if should_notify and event.id not in self.notified_events:
                        if DEBUG:
                            print("[EventManager DEBUG]   >>> SHOWING NOTIFICATION for {0}".format(event.title))
                        self.show_notification(event)
                        self.notified_events.add(event.id)
                        if DEBUG:
                            print("[EventManager DEBUG]   Added to notified events: {0}".format(event.id))
                    elif event.id in self.notified_events:
                        if DEBUG:
                            print("[EventManager DEBUG]   Already notified, checking if past...")
                        if (next_occurrence and
                                (next_occurrence - timedelta(minutes=event.notify_before)) >
                                now + timedelta(minutes=5)):
                            self.notified_events.remove(event.id)
                            if DEBUG:
                                print("[EventManager DEBUG]   Removed from notified events: {0}".format(event.id))
                else:
                    print("[EventManager DEBUG]   No next occurrence found")

                print("[EventManager DEBUG]   ---")
            if DEBUG:
                print("[EventManager DEBUG] Summary: {0} events checked, {1} skipped".format(
                    events_checked, events_skipped))
                print("[EventManager DEBUG] Notified events count: {0}".format(len(self.notified_events)))

            # Reschedule next check
            self.check_timer.start(30000, True)
            if DEBUG:
                print("[EventManager DEBUG] Next check in 30 seconds")

        except Exception as e:
            print("[EventManager] Error checking events: {0}".format(e))

    def cleanup_past_events(self):
        """Clean up past non-recurring events"""
        if not config.plugins.calendar.events_enabled.value:
            # No need to check self.event_manager anymore because self IS the EventManager
            return 0

        now = datetime.now()
        removed_count = 0
        events_to_keep = []

        for event in self.events:
            if event.repeat != "none":
                # Keep recurring events
                events_to_keep.append(event)
                continue

            # For non-recurring events, check if they are past
            event_dt = event.get_datetime()
            if event_dt:
                # If the event is more than 1 day past, remove it
                if (now - event_dt) > timedelta(days=1):
                    print("[EventManager] Removing past event: {0} ({1})".format(
                        event.title, event.date))
                    removed_count += 1
                    continue

            # Keep the event
            events_to_keep.append(event)

        # Update the event list if we removed any
        if removed_count > 0:
            self.events = events_to_keep
            self.save_events()
            print("[EventManager] Cleaned up {0} past events".format(removed_count))

        return removed_count

    def _execute_cleanup(self, result):
        """Execute cleanup after confirmation"""
        if result:
            removed = self.event_manager.cleanup_past_events()

            if removed > 0:
                message = _("Removed {0} past events").format(removed)
                self._paint_calendar()  # Reload calendar
            else:
                message = _("No past events to remove")

            self.session.open(MessageBox, message, MessageBox.TYPE_INFO)

    def show_notification(self, event):
        """Show notification with optional sound"""
        try:
            if not config.plugins.calendar.events_notifications.value:
                return

            # PLAY SOUND if configured
            if config.plugins.calendar.events_play_sound.value:
                sound_type = config.plugins.calendar.events_sound_type.value
                # PLAY SOUND if configured
                """
                sound_type = config.plugins.calendar.events_sound_type.value
                # if sound_type != "none" and config.plugins.calendar.events_play_sound.value:
                    # # Choose sound based on priority
                    # if event.notify_before == 0:
                        # sound_to_play = "alert"   # Event in progress
                    # elif event.notify_before <= 5:
                        # sound_to_play = "notify"  # Event imminent
                    # else:
                        # sound_to_play = sound_type  # User setting
                """
                if sound_type != "none":
                    # Store current service BEFORE playing sound
                    self.previous_service = self.session.nav.getCurrentlyPlayingServiceReference()

                    if DEBUG:
                        if self.previous_service:
                            print("[EventManager] Saved previous service before playing sound")
                        else:
                            print("[EventManager] No service currently playing")

                    # Use only the user's selected sound type
                    sound_to_play = sound_type

                    # Play sound and get the stop timer
                    sound_stop_timer = self.play_notification_sound(sound_to_play)

                    # Store the timer reference
                    if sound_stop_timer:
                        self.sound_stop_timer = sound_stop_timer

            # Build message
            time_str = event.time[:5] if event.time else "00:00"
            message = "Event: {0}\nTime: {1}".format(event.title, time_str)

            if event.description:
                desc = event.description
                if len(desc) > 50:
                    desc = desc[:47] + "..."
                message += "\n{0}".format(desc)

            # Show notification
            if NOTIFICATION_AVAILABLE:
                # Show notification for 5 seconds
                quick_notify(message, seconds=10)

                # Timer to stop the sound when the notification ends
                def stop_sound_when_notification_ends():
                    try:
                        if DEBUG:
                            print("[EventManager] Notification timer ended, stopping sound")

                        # Stop any active sound timer
                        if hasattr(self, 'sound_stop_timer') and self.sound_stop_timer:
                            if self.sound_stop_timer.isActive():
                                self.sound_stop_timer.stop()

                        # Call method to stop audio and restore TV
                        self.stop_notification_sound()

                    except Exception as e:
                        print("[EventManager] Error in notification end callback: " + str(e))

                # 10-second timer (notification duration)
                notification_timer = eTimer()
                try:
                    notification_timer_conn = notification_timer.timeout.connect(stop_sound_when_notification_ends)
                except AttributeError:
                    notification_timer.callback.append(stop_sound_when_notification_ends)
                notification_timer.start(10000, True)  # 10 seconds

            else:
                print("[EventManager] NOTIFICATION: {0}".format(message))

        except Exception as e:
            print("[EventManager] Error in show_notification: {0}".format(e))

    def play_notification_sound(self, sound_type="notify"):
        try:
            if DEBUG:
                print("[EventManager] === START play_notification_sound ===")
                print("[EventManager] Requested sound type: " + sound_type)

            # 1. SAVE the CURRENT service FIRST
            current_service = self.session.nav.getCurrentlyPlayingServiceReference()

            # SAVE to a SEPARATE attribute for security
            self.tv_service_backup = current_service

            if DEBUG:
                if self.tv_service_backup:
                    print("[EventManager] TV service saved: " + self.tv_service_backup.toString())
                else:
                    print("[EventManager] No TV service active (TV might be off)")

            # Try different possible sound directories
            sound_dir = None
            for test_dir in [PLUGIN_PATH + "sounds/", PLUGIN_PATH + "sound/", sounds_dir]:
                if exists(test_dir):
                    sound_dir = test_dir
                    break

            if not sound_dir:
                if DEBUG:
                    print("[EventManager] ERROR: No sound directory found!")
                return None

            if DEBUG:
                print("[EventManager] Using sound directory: " + sound_dir)

            # Audio file mapping
            sound_map = {
                "short": "beep",
                "notify": "notify",
                "alert": "alert"
            }

            filename_base = sound_map.get(sound_type)
            if not filename_base:
                if DEBUG:
                    print("[EventManager] ERROR: Unknown sound type: " + sound_type)
                return None

            if DEBUG:
                print("[EventManager] Looking for base filename: " + filename_base)

            # Look for the file (WAV first, then MP3)
            sound_path = None
            for ext in ['.wav', '.mp3']:
                test_path = join(sound_dir, filename_base + ext)
                if exists(test_path):
                    sound_path = test_path
                    break

            if not sound_path:
                if DEBUG:
                    print("[EventManager] ERROR: Sound file not found!")
                return None

            if DEBUG:
                print("[EventManager] Found sound file: " + sound_path)

            # 2. STOP the current service BEFORE playing audio
            self.session.nav.stopService()
            time.sleep(0.1)  # Piccola pausa

            # 3. Create eServiceReference for audio file
            # 4097 = isFile (1) + isAudio (4096)
            service_ref = eServiceReference(4097, 0, sound_path)
            service_ref.setName("Calendar Notification")

            if DEBUG:
                print("[EventManager] Playing sound: " + sound_path)

            self.session.nav.playService(service_ref)

            # 4. Timer STOP automatic
            def stop_and_restore_tv():
                if DEBUG:
                    print("[EventManager] Auto-stop timer triggered")

                try:
                    # Stop audio playback
                    self.session.nav.stopService()

                    # Wait a bit
                    time.sleep(0.2)

                    # Restore ORIGINAL service (TV/radio) if it exists
                    if hasattr(self, 'tv_service_backup') and self.tv_service_backup:
                        if DEBUG:
                            print("[EventManager] Restoring TV service: " +
                                  self.tv_service_backup.toString())

                        # Check it's not our audio file
                        if self.tv_service_backup.toString().find("Calendar Notification") == -1:
                            self.session.nav.playService(self.tv_service_backup)
                        else:
                            if DEBUG:
                                print("[EventManager] Skipping - backup is audio file")

                    # Clean up
                    if hasattr(self, 'tv_service_backup'):
                        self.tv_service_backup = None

                except Exception as e:
                    print("[EventManager] Error in stop_and_restore_tv: " + str(e))

            # Create and start the timer
            stop_timer = eTimer()
            try:
                stop_timer_conn = stop_timer.timeout.connect(stop_and_restore_tv)
            except AttributeError:
                stop_timer.callback.append(stop_and_restore_tv)
            stop_timer.start(10000, True)  # 10 seconds

            if DEBUG:
                print("[EventManager] Auto-stop timer set for 3000 ms")
                print("[EventManager] === END play_notification_sound ===")

            # Return the timer so it can be stopped if needed
            return stop_timer

        except Exception as e:
            print("[EventManager] CRITICAL ERROR in play_notification_sound: " + str(e))
            import traceback
            traceback.print_exc()
            return None

    def stop_notification_sound(self):
        try:
            if DEBUG:
                print("[EventManager] stop_notification_sound called")

            # Ferma audio
            self.session.nav.stopService()
            time.sleep(0.2)

            # Restore previous service if it exists AND is NOT the audio file
            if hasattr(self, 'tv_service_backup') and self.tv_service_backup:
                if DEBUG:
                    print("[EventManager] Restoring from backup: " +
                          self.tv_service_backup.toString())

                # Only restore if it's a TV/radio service, not audio file
                if self.tv_service_backup.toString().find("Calendar Notification") == -1:
                    self.session.nav.playService(self.tv_service_backup)

                # Clear the reference
                self.tv_service_backup = None

            return True

        except Exception as e:
            print("[EventManager] Error in stop_notification_sound: " + str(e))
            return False

    def _monitor_playback(self, nav, sound_path):
        """Monitor audio playback to clean up when done"""
        try:

            def check_if_playing():
                current = nav.getCurrentService()
                if current:
                    try:
                        # Check if still playing our file
                        ref = nav.getCurrentlyPlayingServiceReference()
                        if ref and ref.getPath() == sound_path:
                            # Still playing, check again in 1 second
                            check_timer.start(1000, True)
                        else:
                            print("[EventManager] Audio playback finished")
                            # Try to restore previous service if any
                            try:
                                # This would restore TV/radio if it was playing
                                # nav.playService(previous_service)
                                pass
                            except:
                                pass
                    except:
                        pass

            check_timer = eTimer()
            try:
                check_timer_conn = check_timer.timeout.connect(check_if_playing)
            except AttributeError:
                check_timer.callback.append(check_if_playing)
            check_timer.start(1000, True)  # Check after 1 second

        except Exception as e:
            print("[EventManager] Playback monitor error: {0}".format(e))

    def _play_via_eservicereference(self, sound_path, sound_format):
        """Play using eServiceReference - ENIGMA2 CORRECT METHOD"""
        try:
            # Create service reference for audio file
            # 4097 = 1 (isFile) + 4096 (isAudio)
            service_ref = eServiceReference(4097, 0, sound_path)
            service_ref.setName("Calendar Notification")

            # Get service center
            service_handler = eServiceCenter.getInstance()

            # Try to get the service
            service = service_handler.uniqueService(service_ref)
            if service:
                # This is the correct way to play a service in Enigma2
                from Screens.InfoBar import InfoBar
                infoBarInstance = InfoBar.instance

                if infoBarInstance and hasattr(infoBarInstance, 'session'):
                    # Stop current playback first
                    infoBarInstance.session.nav.stopService()
                    # Start playing the audio
                    infoBarInstance.session.nav.playService(service_ref)
                    print("[EventManager] Playing audio via session.nav.playService")

                    # Monitor playback to auto-remove when done
                    self._monitor_playback(infoBarInstance.session.nav, sound_path)
                    return True

            print("[EventManager] Could not get service instance")
            return False

        except Exception as e:
            print("[EventManager] eServiceReference error: {0}".format(e))
            return False

    def _play_via_system_player(self, sound_path, sound_format):
        """Play using system audio players"""
        players = [
            ["aplay", sound_path],
            ["paplay", sound_path],
            ["play", sound_path],
            ["mpg123", "-q", sound_path],
            ["madplay", "-Q", sound_path],
            ["mpg321", "-q", sound_path],
        ]

        for cmd in players:
            try:
                if shutil.which(cmd[0]) is None:
                    continue

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    timeout=2,
                    env={"DISPLAY": ":0"}
                )

                if result.returncode == 0:
                    print("[EventManager] Played via {0}".format(cmd[0]))
                    return True

            except subprocess.TimeoutExpired:
                print("[EventManager] {0} timeout".format(cmd[0]))
                continue
            except Exception as e:
                print("[EventManager] {0} error: {1}".format(cmd[0], e))
                continue

        return False

    def _play_via_gstreamer(self, sound_path, sound_format):
        """Play using GStreamer (if available)"""
        try:
            cmd = [
                "gst-launch-1.0",
                "filesrc",
                "location={0}".format(sound_path),
                "!",
                "decodebin",
                "!",
                "audioconvert",
                "!",
                "autoaudiosink"
            ]

            result = subprocess.run(cmd, capture_output=True, timeout=3)
            if result.returncode == 0:
                print("[EventManager] Played via GStreamer")
                return True

        except Exception as e:
            print("[EventManager] GStreamer error: {0}".format(e))

        return False

    def update_time(self):
        """Update current time (for recurring event handling)"""
        # For now just print, but can be extended
        # current_time = datetime.now().strftime("%H:%M")
        # Reschedule timer
        self.time_timer.start(60000, True)

    def get_todays_events(self):
        """Get today's events"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.get_events_for_date(today)

    def has_events_today(self):
        """Check if there are events today"""
        return len(self.get_todays_events()) > 0


# Helper functions for Calendar integration
def create_event_from_data(title, date, event_time="00:00", description="",
                           repeat="none", notify_before=5, enabled=True):
    """Create new event from provided data"""
    return Event(
        title=title,
        description=description,
        date=date,
        event_time=event_time,
        repeat=repeat,
        notify_before=notify_before,
        enabled=enabled
    )


def format_event_display(event):
    """Format event for display"""
    repeat_text = {
        "none": "",
        "daily": " (Daily)",
        "weekly": " (Weekly)",
        "monthly": " (Monthly)",
        "yearly": " (Yearly)"
    }.get(event.repeat, "")

    return "{0} - {1}{2}".format(event.time, event.title, repeat_text)


# Test the module
if __name__ == "__main__":
    # Example usage
    print("Test EventManager")

    # Create test event
    test_event = Event(
        title="Test Event",
        description="This is a test event",
        date=datetime.now().strftime("%Y-%m-%d"),
        time=(datetime.now() + timedelta(minutes=10)).strftime("%H:%M"),
        repeat="none",
        notify_before=5
    )
    if DEBUG:
        print("Event created: {0}".format(test_event.title))
        print("Next occurrence: {0}".format(test_event.get_next_occurrence()))
        print("Should notify? {0}".format(test_event.should_notify()))
