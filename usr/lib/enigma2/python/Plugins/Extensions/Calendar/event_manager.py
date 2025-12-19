#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
###########################################################
#                                                         #
#  Calendar Plugin for Enigma2                            #
#  Created by: Lululla                                    #
#  Based on original work by: Sirius0103                  #
#                                                         #
#  FEATURES:                                              #
#  • Monthly calendar display with color-coded days       #
#  • Date information management with text files          #
#  • Event system with smart notifications                #
#  • Recurring events: daily, weekly, monthly, yearly     #
#  • Event browser and management interface               #
#  • Configurable notification settings                   #
#  • Multi-language support for date data                 #
#                                                         #
#  EVENT SYSTEM:                                          #
#  • Smart notifications (0-60 minutes before event)      #
#  • Background monitoring every 30 seconds               #
#  • Visual indicators on calendar for days with events   #
#  • Event persistence in JSON format                     #
#  • Configurable notification duration (3-15 seconds)    #
#  • Automatic cleanup of past event notifications        #
#                                                         #
#  DATE MANAGEMENT:                                       #
#  • Create, edit, remove date information                #
#  • Virtual keyboard for field editing                   #
#  • Automatic field navigation during editing            #
#  • File structure: base/[language]/day/YYYYMMDD.txt     #
#  • Sections: [day] for date info, [month] for people    #
#                                                         #
#  CALENDAR DISPLAY:                                      #
#  • Color coding: Today=green, Saturday=yellow, Sunday=red #
#  • Event days highlighted in blue/cyan (configurable)   #
#  • Asterisk (*) indicator for days with events          #
#  • Week numbers display                                 #
#  • Smooth month navigation                              #
#                                                         #
#  CONFIGURATION:                                         #
#  • Event system enable/disable                          #
#  • Notification settings (duration, advance time)       #
#  • Event color selection                                #
#  • Show event indicators toggle                         #
#  • Menu integration option                              #
#                                                         #
#  KEY CONTROLS - MAIN CALENDAR:                          #
#    OK          - Open main menu (New/Edit/Remove/Events)#
    RED         - Previous month                          #
    GREEN       - Next month                              #
    YELLOW      - Previous day                            #
    BLUE        - Next day                                #
    0 (ZERO)    - Open event management                   #
    LEFT/RIGHT  - Previous/Next day                       #
    UP/DOWN     - Previous/Next month                     #
    MENU        - Configuration                           #
    INFO/EPG    - About dialog                            #
#                                                         #
#  KEY CONTROLS - EVENT DIALOG:                           #
#    OK          - Edit current field                     #
    RED         - Cancel                                  #
    GREEN       - Save event                              #
    YELLOW      - Delete event (edit mode only)           #
    UP/DOWN     - Navigate between fields                 #
    LEFT/RIGHT  - Change selection options                #
#                                                         #
#  KEY CONTROLS - EVENTS VIEW:                            #
#    OK          - Edit selected event                    #
    RED         - Add new event                           #
    GREEN       - Edit selected event                     #
    YELLOW      - Delete selected event                   #
    BLUE        - Back to calendar                        #
    UP/DOWN     - Navigate event list                     #
#                                                         #
#  FILE STRUCTURE:                                        #
#  • plugin.py - Main plugin entry point                  #
#  • event_manager.py - Event management core             #
#  • event_dialog.py - Event add/edit interface           #
#  • events_view.py - Events browser                      #
#  • notification_system.py - Notification display        #
#  • events.json - Event database (JSON format)           #
#  • base/ - Date information storage                     #
#  • buttons/ - Button images for UI                      #
#                                                         #
#  EVENT STORAGE FORMAT (events.json):                    #
#  [{                                                     #
#    "id": 1766153767369,                                 #
#    "title": "Meeting",                                  #
#    "description": "Team meeting",                       #
#    "date": "2025-12-19",                                #
#    "time": "14:30",                                     #
#    "repeat": "none",                                    #
#    "notify_before": 15,                                 #
#    "enabled": true,                                     #
#    "created": "2024-12-19 14:25:47"                     #
#  }]                                                     #
#                                                         #
#  DATE FILE FORMAT (YYYYMMDD.txt):                       #
#  [day]                                                  #
#  date: 2025-06-10                                       #
#  datepeople: John Doe                                   #
#  sign: Gemini                                           #
#  holiday: None                                          #
#  description: Special day description.                  #
#                                                         #
#  [month]                                                #
#  monthpeople: Important people of the month             #
#                                                         #
#  TECHNICAL DETAILS:                                     #
#  • Python 2.7+ compatible                               #
#  • Uses eTimer for background monitoring                #
#  • JSON storage for events                              #
#  • Virtual keyboard integration                         #
#  • Auto-skin detection (HD/FHD)                         #
#  • Configurable via setup.xml                           #
#                                                         #
#  PERFORMANCE:                                           #
#  • Efficient event checking algorithm                   #
#  • Skipped checks for past non-recurring events         #
#  • Minimal memory usage                                 #
#  • Fast loading of date information                     #
#                                                         #
#  DEBUGGING:                                             #
#  • Enable debug logs: check enigma2.log                 #
#  • Filter: grep EventManager /tmp/enigma2.log           #
#  • Event check interval: 30 seconds                     #
#  • Notification window: event time ± 5 minutes          #
#                                                         #
#  CREDITS:                                               #
#  • Original Calendar plugin: Sirius0103                 #
#  • Event system & modifications: Lululla                #
#  • Notification system: Custom implementation           #
#  • Testing & feedback: Enigma2 community                #
#                                                         #
#  VERSION HISTORY:                                       #
#  • v1.0 - Basic calendar functionality                  #
#  • v1.1 - Complete event system added                   #
#           (Current version)                             #
#                                                         #
#  Last Updated: 2025-12-19                               #
#  Status: Stable with event system                       #
###########################################################
"""

import json
import time
import subprocess
import shutil
from datetime import datetime, timedelta
from os import makedirs
from os.path import exists, dirname
from enigma import eTimer
from Components.config import config

try:
    from .notification_system import init_notification_system, quick_notify
    NOTIFICATION_AVAILABLE = True
except ImportError:
    NOTIFICATION_AVAILABLE = False
    print("[EventManager] Notification system not available")


class Event:
    """Class to represent a single event"""

    def __init__(self, title="", description="", date="", event_time="",  # event_time qui
                 repeat="none", notify_before=15, enabled=True):
        self.title = title
        self.description = description
        self.date = date  # Format: YYYY-MM-DD
        self.time = event_time  # Format: HH:MM - assegna a self.time
        self.repeat = repeat  # none, daily, weekly, monthly, yearly
        self.notify_before = notify_before  # minutes before
        self.enabled = enabled
        self.created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.id = int(time.time() * 1000)  # Unique ID

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
            'created': self.created
        }

    @classmethod
    def from_dict(cls, data):
        """Create event from dictionary"""
        event = cls()
        for key, value in data.items():
            if hasattr(event, key):
                setattr(event, key, value)
        return event

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
        self.events_file = events_file or "/usr/lib/enigma2/python/Plugins/Extensions/Calendar/events.json"
        self.sound_dir = "/usr/lib/enigma2/python/Plugins/Extensions/Calendar/sounds/"
        self.events = []
        self.notified_events = set()  # Events already notified in this session

        # Timer to check events
        self.check_timer = eTimer()
        self.check_timer.callback.append(self.check_events)

        # Timer to update current time
        self.time_timer = eTimer()
        self.time_timer.callback.append(self.update_time)

        self.load_events()
        self.start_monitoring()

        # Initialize notification system if available
        if NOTIFICATION_AVAILABLE:
            init_notification_system(session)

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

    def load_events(self):
        """Load events from JSON file"""
        try:
            if exists(self.events_file):
                with open(self.events_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.events = [Event.from_dict(event_data) for event_data in data]
                print("[EventManager] Loaded {0} events".format(len(self.events)))
            else:
                self.events = []
                print("[EventManager] No event file found, creating empty list")
        except Exception as e:
            print("[EventManager] Error loading events: {0}".format(e))
            self.events = []

    def save_events(self):
        """Save events to JSON file"""
        try:
            # Create directory if it doesn't exist
            makedirs(dirname(self.events_file), exist_ok=True)

            with open(self.events_file, 'w', encoding='utf-8') as f:
                json.dump([event.to_dict() for event in self.events], f,
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
        """Check events and show notifications if needed - OPTIMIZED VERSION"""
        try:
            now = datetime.now()
            print("[EventManager] Checking events at {0}".format(now.strftime('%H:%M:%S')))
            print("[EventManager] Total events: {0}".format(len(self.events)))

            # Clean up old non-recurring events first
            self._cleanup_old_events(now)

            events_checked = 0
            events_notified = 0

            # Check remaining events
            for event in self.events:
                if not event.enabled:
                    continue

                # Skip events that have already been notified and are past
                if event.id in self.notified_events and event.repeat == "none":
                    event_dt = event.get_datetime()
                    if event_dt and now > event_dt + timedelta(minutes=5):
                        continue

                events_checked += 1

                # Check if event should trigger notification
                if event.should_notify(now) and event.id not in self.notified_events:
                    print("[EventManager] >>> NOTIFYING: {0} at {1}".format(event.title, event.time))
                    self.show_notification(event)
                    self.notified_events.add(event.id)
                    events_notified += 1

                    # If it's a non-recurring event, mark it for immediate cleanup next time
                    if event.repeat == "none":
                        print("[EventManager] Non-recurring event notified - will cleanup soon")

            print("[EventManager] Checked: {0}, Notified: {1}, Total: {2}".format(
                events_checked, events_notified, len(self.events)))

            # Schedule next check
            self.check_timer.start(30000, True)

        except Exception as e:
            print("[EventManager] Error in check_events: {0}".format(e))
            self.check_timer.start(30000, True)

    def _cleanup_old_events(self, current_time=None):
        """Remove old non-recurring events that are no longer needed"""
        if current_time is None:
            current_time = datetime.now()

        removed_count = 0
        events_to_keep = []

        for event in self.events:
            keep_event = True

            # Non-recurring events that are past
            if event.repeat == "none" and event.enabled:
                event_dt = event.get_datetime()
                if event_dt:
                    time_passed = current_time - event_dt

                    # Remove if:
                    # 1. More than 30 minutes have passed
                    # OR 2. Event was notified and passed more than 5 minutes ago
                    if time_passed > timedelta(minutes=30) or (
                        event.id in self.notified_events and time_passed > timedelta(minutes=5)
                    ):
                        print("[EventManager] Removing old event: {0} (passed {1} min ago)".format(
                            event.title, time_passed.seconds // 60))
                        keep_event = False
                        removed_count += 1

                        # Remove from notified events
                        if event.id in self.notified_events:
                            self.notified_events.remove(event.id)

            if keep_event:
                events_to_keep.append(event)

        if removed_count > 0:
            self.events = events_to_keep
            self.save_events()
            print("[EventManager] Cleaned up {0} old events".format(removed_count))

    def show_notification(self, event):
        """Show notification with optional sound"""
        try:
            if not config.plugins.calendar.events_notifications.value:
                return

            # PLAY SOUND if configured
            sound_type = config.plugins.calendar.events_sound_type.value
            if sound_type != "none" and config.plugins.calendar.events_play_sound.value:
                # Choose sound based on priority
                if event.notify_before == 0:
                    sound_to_play = "alert"   # Event in progress
                elif event.notify_before <= 5:
                    sound_to_play = "notify"  # Event imminent
                else:
                    sound_to_play = sound_type  # User setting

                self.play_notification_sound(sound_to_play)

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
                quick_notify(message, seconds=15)
            else:
                print("[EventManager] NOTIFICATION: {0}".format(message))

        except Exception as e:
            print("[EventManager] Error in show_notification: {0}".format(e))

    def play_notification_sound(self, sound_type="notify"):
        """Play notification sound - supports WAV and MP3"""
        try:
            # Audio file paths inside the plugin
            sound_files = {
                "short": {
                    "wav": "/usr/lib/enigma2/python/Plugins/Extensions/Calendar/sounds/beep.wav",
                    "mp3": "/usr/lib/enigma2/python/Plugins/Extensions/Calendar/sounds/beep.mp3"
                },
                "notify": {
                    "wav": "/usr/lib/enigma2/python/Plugins/Extensions/Calendar/sounds/notify.wav",
                    "mp3": "/usr/lib/enigma2/python/Plugins/Extensions/Calendar/sounds/notify.mp3"
                },
                "alert": {
                    "wav": "/usr/lib/enigma2/python/Plugins/Extensions/Calendar/sounds/alert.wav",
                    "mp3": "/usr/lib/enigma2/python/Plugins/Extensions/Calendar/sounds/alert.mp3"
                }
            }

            sound_info = sound_files.get(sound_type, sound_files["notify"])

            # Look first for WAV, then MP3
            sound_path = None
            sound_format = None

            # Check WAV
            if exists(sound_info["wav"]):
                sound_path = sound_info["wav"]
                sound_format = "wav"
            # Check MP3
            elif exists(sound_info["mp3"]):
                sound_path = sound_info["mp3"]
                sound_format = "mp3"
            else:
                print("[EventManager] No sound file found for {0}".format(sound_type))
                return False

            print(
                "[EventManager] Playing {0}: {1}".format(
                    sound_format.upper(),
                    sound_path
                )
            )

            # METHOD 1: eServiceReference (works on many receivers)
            try:
                return self._play_via_eservicereference(sound_path, sound_format)
            except Exception as e1:
                print("[EventManager] eServiceReference failed: {0}".format(e1))

            # METHOD 2: System audio player
            try:
                return self._play_via_system_player(sound_path, sound_format)
            except Exception as e2:
                print("[EventManager] System player failed: {0}".format(e2))

            # METHOD 3: GStreamer (if available)
            try:
                return self._play_via_gstreamer(sound_path, sound_format)
            except Exception as e3:
                print("[EventManager] GStreamer failed: {0}".format(e3))

            print("[EventManager] All playback methods failed")
            return False

        except Exception as e:
            print("[EventManager] Error in play_notification_sound: {0}".format(e))
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
            check_timer.callback.append(check_if_playing)
            check_timer.start(1000, True)  # Check after 1 second

        except Exception as e:
            print("[EventManager] Playback monitor error: {0}".format(e))

    def _play_via_eservicereference(self, sound_path, sound_format):
        """Play using eServiceReference - ENIGMA2 CORRECT METHOD"""
        try:
            from enigma import eServiceReference, eServiceCenter
            # from Components.ServiceEventTracker import ServiceEventTracker
            # from enigma import iPlayableService

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
                           repeat="none", notify_before=15, enabled=True):
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

    print("Event created: {0}".format(test_event.title))
    print("Next occurrence: {0}".format(test_event.get_next_occurrence()))
    print("Should notify? {0}".format(test_event.should_notify()))
