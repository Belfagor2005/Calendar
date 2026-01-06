#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
###########################################################
#  Calendar Planner for Enigma2 v1.7                      #
#  Created by: Lululla (based on Sirius0103)              #
###########################################################

Last Updated: 2026-01-02
Status: Stable with complete vCard & ICS support
Credits: Sirius0103 (original), Lululla (modifications)
Homepage: www.corvoboys.org www.linuxsat-support.com
###########################################################
"""
from __future__ import print_function
import time
import subprocess
import shutil
from os import makedirs, remove, rename, fsync, chmod
from os.path import exists, dirname, join, getsize
from json import load, dump
from datetime import datetime, timedelta
from enigma import eTimer, eServiceReference, eServiceCenter
from Components.config import config
from Screens.MessageBox import MessageBox
from Screens.InfoBar import InfoBar

from . import _, PLUGIN_PATH
from .config_manager import get_debug, get_default_event_time, OLD_DEFAULT_EVENT_TIME, get_last_used_default_time
from .formatters import get_EVENTS_JSON, get_SOUNDS_DIR

EVENTS_JSON = get_EVENTS_JSON()
SOUNDS_DIR = get_SOUNDS_DIR()


global DEBUG
DEBUG = get_debug()


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
        self.events_file = events_file or EVENTS_JSON
        self.sound_dir = SOUNDS_DIR

        self.events = []
        from .formatters import DATA_PATH
        self.notified_events = set()  # Events already notified in this session
        self.notified_events_file = join(DATA_PATH, "notified_events.json")
        self.load_notified_events()

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

        self.converted_events_file = EVENTS_JSON + ".converted"
        self.load_events()
        self.start_monitoring()

        # Initialize notification system if available
        if NOTIFICATION_AVAILABLE:
            init_notification_system(session)

    def load_events(self):
        """Load events from JSON file - convert old times"""
        try:
            if DEBUG:
                print("[EventManager] Loading events from: %s" % self.events_file)

            if not exists(self.events_file):
                if DEBUG:
                    print("[EventManager] No events file found")
                self.events = []
                return

            current_default = get_default_event_time()
            last_used = get_last_used_default_time()

            if DEBUG:
                print("[EventManager] Current default time: %s" % current_default)
                print("[EventManager] Last used default time: %s" % last_used)
                print("[EventManager] OLD_DEFAULT_EVENT_TIME: %s" % OLD_DEFAULT_EVENT_TIME)

            # CHECK IF WE ALREADY CONVERTED THIS FILE
            file_hash = self._get_file_hash()

            if self._is_already_converted(file_hash, current_default):
                if DEBUG:
                    print("[EventManager] Events already converted to %s" % current_default)
                # Load normally without conversion
                with open(self.events_file, 'r') as f:
                    data = load(f)
                self.events = [Event.from_dict(item) for item in data]
                return

            with open(self.events_file, 'r') as f:
                data = load(f)

            if DEBUG:
                print("[EventManager] Loaded %d events from file" % len(data))

            converted_count = 0
            self.events = []
            need_save = False

            for item in data:
                # Get time from event
                event_time = item.get('time', current_default)
                original_time = event_time

                # Check if conversion is needed
                convert_reason = None

                # Convert from last used default time
                if last_used and event_time == last_used and current_default != last_used:
                    event_time = current_default
                    converted_count += 1
                    need_save = True
                    convert_reason = "last_used_default"

                # Convert from old hardcoded default (14:00)
                elif event_time == OLD_DEFAULT_EVENT_TIME and current_default != OLD_DEFAULT_EVENT_TIME:
                    event_time = current_default
                    converted_count += 1
                    need_save = True
                    convert_reason = "old_hardcoded_default"

                # Fix invalid time format
                elif not event_time or len(event_time) != 5 or ':' not in event_time:
                    event_time = current_default
                    converted_count += 1
                    need_save = True
                    convert_reason = "invalid_format"

                # Log conversion if debug enabled
                if convert_reason and DEBUG:
                    print("[EventManager] Converted '%s' from %s to %s (reason: %s)" % (
                        item.get('title', 'N/A'), original_time, event_time, convert_reason))

                # Create event object
                event = create_event_from_data(
                    title=item.get('title', ''),
                    date=item.get('date', ''),
                    event_time=event_time,
                    description=item.get('description', ''),
                    repeat=item.get('repeat', 'none'),
                    notify_before=item.get('notify_before', 0),
                    enabled=item.get('enabled', True)
                )

                event.id = item.get('id', int(time.time() * 1000))
                event.created = item.get('created', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                event.labels = item.get('labels', [])

                self.events.append(event)

            if DEBUG:
                print("[EventManager] Total events loaded: %d" % len(self.events))
                print("[EventManager] Converted %d events" % converted_count)

            # Save if any conversions were made
            if need_save and converted_count > 0:
                if DEBUG:
                    print("[EventManager] Saving %d converted events to file" % converted_count)
                self.save_events()

                # MARK FILE AS CONVERTED
                self._mark_as_converted(file_hash, current_default)

                # Update last used default time after conversion
                from .config_manager import update_last_used_default_time
                update_last_used_default_time(current_default)
                if DEBUG:
                    print("[EventManager] Events updated to new default time: %s" % current_default)

        except Exception as e:
            print("[EventManager] Error loading events: %s" % str(e))
            import traceback
            traceback.print_exc()
            self.events = []

    def save_events(self):
        """Save events to JSON file"""
        try:
            current_default = get_default_event_time()

            if DEBUG:
                print("[EventManager] Saving events, current default: %s" % current_default)
                print("[EventManager] Number of events to save: %d" % len(self.events))

            data = []
            for event in self.events:
                data.append({
                    'id': event.id,
                    'title': event.title,
                    'description': event.description,
                    'date': event.date,
                    'time': event.time,  # Keep original time
                    'repeat': event.repeat,
                    'notify_before': event.notify_before,
                    'enabled': event.enabled,
                    'created': event.created,
                    'labels': event.labels
                })

                if DEBUG:
                    print("[EventManager]   Event '%s' time: %s" % (event.title, event.time))

            # Create directory if missing
            events_dir = dirname(self.events_file)
            if not exists(events_dir):
                try:
                    makedirs(events_dir, 0o755)
                    if DEBUG:
                        print("[EventManager] Created directory: %s" % events_dir)
                except Exception as e:
                    print("[EventManager] Error creating directory: %s" % str(e))

            # Save to temp file first
            temp_file = self.events_file + ".tmp"
            try:
                with open(temp_file, 'w') as f:
                    dump(data, f, indent=2)
                    f.flush()
                    fsync(f.fileno())

                if DEBUG:
                    print("[EventManager] Written to temp file: %s" % temp_file)

                # Rename temp to final
                if exists(self.events_file):
                    remove(self.events_file)
                rename(temp_file, self.events_file)

                if DEBUG:
                    print("[EventManager] File saved: %s" % self.events_file)
                    print("[EventManager] Save completed successfully")

                # Set file permissions
                try:
                    chmod(self.events_file, 0o644)
                except Exception as e:
                    print("[EventManager] Warning: Could not set permissions: %s" % str(e))
                # Verify file
                if DEBUG:
                    if exists(self.events_file):
                        file_size = getsize(self.events_file)
                        print("[EventManager] File saved successfully, size:", file_size, "bytes")
                        with open(self.events_file, 'r') as f:
                            test_data = load(f)
                            if test_data:
                                print("[EventManager] First event time after save:", test_data[0].get('time', 'N/A'))
                    else:
                        print("[EventManager] ERROR: File not created!")
            except Exception as e:
                print("[EventManager] Error in file operations: %s" % str(e))
                if exists(temp_file):
                    remove(temp_file)
                raise

        except Exception as e:
            print("[EventManager] Error saving events: %s" % str(e))
            raise

    def save_notified_events(self):
        """Save notified events cache to file"""
        try:
            if DEBUG:
                print("[EventManager] Saving notified events cache")

            # Create directory if needed
            events_dir = dirname(self.notified_events_file)
            if not exists(events_dir):
                makedirs(events_dir, 0o755)

            # Save to file
            with open(self.notified_events_file, 'w') as f:
                dump(list(self.notified_events), f, indent=2)
                f.flush()
                fsync(f.fileno())

            if DEBUG:
                print("[EventManager] Saved {} notified events".format(len(self.notified_events)))

        except Exception as e:
            print("[EventManager] Error saving notified events: {}".format(str(e)))


    def load_notified_events(self):
        """Load notified events cache from file"""
        try:
            if exists(self.notified_events_file):
                with open(self.notified_events_file, 'r') as f:
                    loaded_events = load(f)
                    self.notified_events = set(loaded_events)

                    if DEBUG:
                        print(
                            "[EventManager] Loaded {} previously notified events"
                            .format(len(self.notified_events))
                        )
            else:
                if DEBUG:
                    print("[EventManager] No notified events cache found")

        except Exception as e:
            print("[EventManager] Error loading notified events: {}".format(str(e)))
            self.notified_events = set()

    def _get_file_hash(self):
        """Get hash of events file for version tracking"""
        try:
            import hashlib
            if not exists(self.events_file):
                return "empty"

            with open(self.events_file, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except:
            return "error"

    def _is_already_converted(self, file_hash, target_time):
        """Check if file was already converted to target time"""
        try:
            if not exists(self.converted_events_file):
                return False

            with open(self.converted_events_file, 'r') as f:
                conversion_data = load(f)
                if file_hash in conversion_data:
                    return conversion_data[file_hash] == target_time
        except:
            pass

    def _mark_as_converted(self, file_hash, target_time):
        """Mark file as converted to specific time"""
        try:
            conversion_data = {}
            if exists(self.converted_events_file):
                try:
                    with open(self.converted_events_file, 'r') as f:
                        conversion_data = load(f)
                except:
                    conversion_data = {}

            conversion_data[file_hash] = target_time
            directory = dirname(self.converted_events_file)
            if not exists(directory):
                makedirs(directory)

            with open(self.converted_events_file, 'w') as f:
                dump(conversion_data, f, indent=2)

            if DEBUG:
                print("[EventManager] Successfully marked file as converted to: %s" % target_time)

        except Exception as e:
            print("[EventManager] Error marking conversion: %s" % str(e))
            import traceback
            traceback.print_exc()

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

    def add_event(self, event):
        """Add a new event"""
        self.events.append(event)
        self.save_events()
        if DEBUG:
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
                if DEBUG:
                    print("[EventManager] Event updated: {0}".format(event.title))
                return True
        return False

    def delete_event(self, event_id):
        """Delete an event"""
        self.events = [event for event in self.events if event.id != event_id]
        self.save_events()
        # Also remove from notified cache
        if event_id in self.notified_events:
            self.notified_events.remove(event_id)
            self.save_notified_events()

        if DEBUG:
            print(f"[EventManager] Event deleted: {event_id}")
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

    def convert_all_events_time(self, new_time=None):
        """Force convert all events to new time"""
        if new_time is None:
            new_time = get_default_event_time()

        if DEBUG:
            print("[EventManager] FORCE converting all events to: %s" % new_time)

        converted = 0
        for event in self.events:
            old_time = event.time
            event.time = new_time
            converted += 1
            if DEBUG:
                print("[EventManager]   %s: %s -> %s" % (event.title, old_time, new_time))

        if converted > 0:
            self.save_events()
            # Update conversion tracking
            file_hash = self._get_file_hash()
            self._mark_as_converted(file_hash, new_time)

        return converted

    def check_events(self):
        """Check events and show notifications if needed"""
        try:
            now = datetime.now()

            if DEBUG:
                print(
                    "\n[EventManager] === CHECK EVENTS at {} ==="
                    .format(now.strftime('%H:%M:%S'))
                )
                print("[EventManager] Total events: {}".format(len(self.events)))
                print(
                    "[EventManager] Enabled events: {}"
                    .format(sum(1 for e in self.events if e.enabled))
                )
                print(
                    "[EventManager] Recurring events: {}"
                    .format(sum(1 for e in self.events if e.repeat != 'none'))
                )
                print(
                    "[EventManager] Already notified: {}"
                    .format(len(self.notified_events))
                )

            events_checked = 0
            events_skipped = 0
            notifications_shown = 0

            for event in self.events:
                # Check if we should skip this event
                if not self._should_check_event(event, now):
                    events_skipped += 1
                    continue

                events_checked += 1

                if DEBUG:
                    print("\n[EventManager] Checking: '{}'".format(event.title))
                    print(
                        "[EventManager]   Date/Time: {} {}"
                        .format(event.date, event.time)
                    )
                    print("[EventManager]   Repeat: {}".format(event.repeat))
                    print(
                        "[EventManager]   Notify before: {}min"
                        .format(event.notify_before)
                    )

                next_occurrence = event.get_next_occurrence(now)

                if next_occurrence:
                    # Calculate notification window
                    notify_window_start = (
                        next_occurrence - timedelta(minutes=event.notify_before)
                    )
                    notify_window_end = next_occurrence + timedelta(minutes=5)

                    if DEBUG:
                        print("[EventManager]   Next: {}".format(next_occurrence))
                        print(
                            "[EventManager]   Notify window: {} to {}"
                            .format(notify_window_start, notify_window_end)
                        )

                    # Check if we should notify now
                    should_notify = notify_window_start <= now <= notify_window_end

                    if should_notify and event.id not in self.notified_events:
                        if DEBUG:
                            print("[EventManager]   >>> SHOWING NOTIFICATION!")

                        self.show_notification(event)
                        self.notified_events.add(event.id)
                        self.save_notified_events()  # <-- SALVA SUBITO
                        notifications_shown += 1

                    elif event.id in self.notified_events:
                        # Clean up if event is past notification window
                        if now > notify_window_end:
                            self.notified_events.remove(event.id)
                            self.save_notified_events()
                            if DEBUG:
                                print("[EventManager]   Removed from notified cache")

            if DEBUG:
                print("\n[EventManager] Summary:")
                print("[EventManager]   Checked: {}".format(events_checked))
                print("[EventManager]   Skipped: {}".format(events_skipped))
                print(
                    "[EventManager]   Notifications shown: {}"
                    .format(notifications_shown)
                )
                print(
                    "[EventManager]   Notified cache size: {}"
                    .format(len(self.notified_events))
                )
                print("[EventManager] === CHECK COMPLETE ===\n")

            # Reschedule next check
            self.check_timer.start(30000, True)

        except Exception as e:
            print(
                "[EventManager] Error in check_events: {}"
                .format(str(e))
            )
            import traceback
            traceback.print_exc()

    def _should_check_event(self, event, now):
        """
        Determine if an event should be checked for notifications

        Returns:
            bool: True if event should be checked, False otherwise
        """
        # Disabled events: skip
        if not event.enabled:
            if DEBUG:
                print("[EventManager]   SKIP: Event disabled")
            return False

        # Recurring events: always check
        if event.repeat != "none":
            return True

        # Non-recurring events
        event_dt = event.get_datetime()
        if not event_dt:
            if DEBUG:
                print("[EventManager]   SKIP: Invalid date/time")
            return False

        time_passed = now - event_dt

        # More than 1 day past: skip
        if time_passed > timedelta(days=1):
            if DEBUG:
                print(
                    "[EventManager]   SKIP: More than 1 day past ({})"
                    .format(time_passed)
                )
            return False

        # More than 30 minutes past and already notified: skip
        if (time_passed > timedelta(minutes=30) and
                event.id in self.notified_events):
            if DEBUG:
                print(
                    "[EventManager]   SKIP: Past & notified ({}min ago)"
                    .format(time_passed.seconds // 60)
                )
            return False

        # Check this event
        return True

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
                    if DEBUG:
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
            if DEBUG:
                print("[EventManager] Cleaned up {0} past events".format(removed_count))

        return removed_count

    def cleanup_duplicate_events_with_dialog(self, session, callback=None):
        """Clean up duplicates with user dialog"""
        from Screens.MessageBox import MessageBox

        def do_cleanup(result):
            if result:
                cleaned = self.cleanup_duplicate_events()
                message = _("Cleaned {0} duplicate events").format(cleaned) if cleaned > 0 else _("No duplicates found")
                session.open(MessageBox, message, MessageBox.TYPE_INFO)
                if callback:
                    callback()

        session.openWithCallback(
            do_cleanup,
            MessageBox,
            _("Clean up duplicate events?\n\nThis will remove exact duplicates from your events list."),
            MessageBox.TYPE_YESNO
        )

    def cleanup_duplicate_events(self):
        """Remove duplicate events from the list"""
        try:
            if not self.events:
                if DEBUG:
                    print("[EventManager] No events to cleanup")
                return 0
            if DEBUG:
                print("[EventManager] === STARTING DUPLICATE CLEANUP ===")
                print("[EventManager] Total events before: %d" % len(self.events))

            # DEBUG: Print all events
            if DEBUG:
                print("\n[EventManager] DEBUG - All events:")
            for i, event in enumerate(self.events):
                print("[%d] '%s' - %s %s" % (i, event.title, event.date, event.time))

            # Keep track of unique events
            unique_events = []
            seen_keys = set()
            removed_count = 0

            for event in self.events:
                # Create unique key for this event
                key = self._get_event_key(event)
                if DEBUG:
                    print("\n[EventManager] Checking: '%s'" % event.title)
                    print("[EventManager] Key: '%s'" % key)

                if key in seen_keys:
                    # Duplicate found - remove it
                    if DEBUG:
                        print("[EventManager] DUPLICATE FOUND! Removing: %s" % event.title)
                    removed_count += 1
                    continue

                # Not a duplicate - keep it
                seen_keys.add(key)
                unique_events.append(event)
                if DEBUG:
                    print("[EventManager] Added to unique list")

            # Update events if duplicates were found
            if removed_count > 0:
                self.events = unique_events
                self.save_events()
                if DEBUG:
                    print("\n[EventManager] Cleanup completed: removed %d duplicates" % removed_count)
                    print("[EventManager] Total events after: %d" % len(self.events))
            else:
                print("\n[EventManager] No duplicates found")
            if DEBUG:
                print("[EventManager] === CLEANUP FINISHED ===\n")
            return removed_count

        except Exception as e:
            print("[EventManager] Error in cleanup_duplicate_events: %s" % str(e))
            import traceback
            traceback.print_exc()
            return 0

    def _get_event_key(self, event):
        """Create unique key for event deduplication"""
        # Normalize the title
        if hasattr(self, '_normalize_event_title'):
            norm_title = self._normalize_event_title(event.title)
        else:
            # Fallback simple normalization
            norm_title = event.title.lower().strip() if event.title else ""

        key_parts = [
            norm_title,
            event.date if event.date else "",
            event.time if event.time else get_default_event_time()
        ]

        return "|".join(key_parts)

    def _normalize_event_title(self, title):
        """Normalize event title for comparison"""
        if not title:
            return ""

        # Lowercase
        normalized = title.lower()

        # Remove extra spaces
        normalized = " ".join(normalized.split())

        # Remove common suffixes
        suffixes = [
            ' - birthday', ' - compleanno', "'s birthday",
            ' - geburtstag', ' - anniversaire', ' - cumpleaños',
            ' birthday', ' compleanno'
        ]

        for suffix in suffixes:
            if normalized.endswith(suffix):
                normalized = normalized[:-len(suffix)].strip()

        return normalized

    def _is_birthday_event(self, event):
        """Check if event is a birthday"""
        if not event.title:
            return False

        title_lower = event.title.lower()
        birthday_keywords = ['birthday', 'compleanno', 'geburtstag', 'anniversaire', 'cumpleaños']

        return any(keyword in title_lower for keyword in birthday_keywords)

    def _extract_name_from_birthday(self, title):
        """Extract name from birthday title"""
        import re

        # Remove common birthday suffixes
        patterns = [
            r'\s*-\s*birthday\s*$',
            r'\s*-\s*compleanno\s*$',
            r"'s\s+birthday\s*$",
            r'\s*-\s*geburtstag\s*$',
            r'\s*-\s*anniversaire\s*$',
            r'\s*-\s*cumpleaños\s*$'
        ]

        clean_title = title.strip()
        for pattern in patterns:
            clean_title = re.sub(pattern, '', clean_title, flags=re.IGNORECASE)

        return clean_title.strip()

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
            time_str = event.time[:5] if event.time else get_default_event_time()
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
                self.save_notified_events()

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
                    notification_timer.timeout.connect(stop_sound_when_notification_ends)
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
            for test_dir in [PLUGIN_PATH + "sounds/", PLUGIN_PATH + "sound/", SOUNDS_DIR]:
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
                stop_timer.timeout.connect(stop_and_restore_tv)
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
                            if DEBUG:
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
                check_timer.timeout.connect(check_if_playing)
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
                infoBarInstance = InfoBar.instance

                if infoBarInstance and hasattr(infoBarInstance, 'session'):
                    # Stop current playback first
                    infoBarInstance.session.nav.stopService()
                    # Start playing the audio
                    infoBarInstance.session.nav.playService(service_ref)
                    if DEBUG:
                        print("[EventManager] Playing audio via session.nav.playService")

                    # Monitor playback to auto-remove when done
                    self._monitor_playback(infoBarInstance.session.nav, sound_path)
                    return True
            if DEBUG:
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
                    if DEBUG:
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
                if DEBUG:
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
def create_event_from_data(title, date, event_time=get_default_event_time(), description="",
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


import atexit


def cleanup_event_manager():
    """Cleanup function called on exit"""
    try:
        if 'manager' in globals():
            manager.save_notified_events()
            print("[EventManager] Cleanup completed")
    except:
        pass

atexit.register(cleanup_event_manager)


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
