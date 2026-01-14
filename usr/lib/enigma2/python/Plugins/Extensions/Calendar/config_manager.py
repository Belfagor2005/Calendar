#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
###########################################################
#  Calendar Planner for Enigma2 v1.8                      #
#  Created by: Lululla                                    #
###########################################################

Last Updated: 2026-01-02
Status: Stable with complete vCard & ICS support
Credits: Lululla
Homepage: www.corvoboys.org www.linuxsat-support.com
###########################################################
"""
from __future__ import print_function
from os.path import exists
from Components.config import (
    config,
    ConfigSubsection,
    ConfigSelection,
    ConfigYesNo,
    ConfigText,
    ConfigInteger
)
from . import _

OLD_DEFAULT_EVENT_TIME = "14:00"
LAST_CONFIGURED_TIME = None
_calendar_config_initialized = False


def init_last_used_time():
    """Get the last configured default time from settings"""
    global LAST_CONFIGURED_TIME
    try:
        settings_file = "/etc/enigma2/settings"
        if exists(settings_file):
            with open(settings_file, 'r') as f:
                for line in f:
                    if line.strip().startswith('config.plugins.calendar.default_event_time='):
                        parts = line.strip().split('=', 1)
                        if len(parts) == 2:
                            time_str = parts[1].strip()
                            if ':' in time_str and len(time_str) == 5:
                                LAST_CONFIGURED_TIME = time_str
                                return time_str
    except:
        pass
    LAST_CONFIGURED_TIME = OLD_DEFAULT_EVENT_TIME
    return OLD_DEFAULT_EVENT_TIME


def get_last_used_default_time():
    """Get last used default time from settings file"""
    try:
        settings_file = "/etc/enigma2/settings"
        if exists(settings_file):
            with open(settings_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('# Calendar_last_used_default_time='):
                        parts = line.split('=', 1)
                        if len(parts) == 2:
                            time_str = parts[1].strip()
                            if ':' in time_str and len(time_str) == 5:
                                return time_str
    except Exception as e:
        print("[ConfigManager] Error reading last used time:", str(e))

    return OLD_DEFAULT_EVENT_TIME


def update_last_used_default_time(new_time):
    """Update last used default time in settings file"""
    try:
        settings_file = "/etc/enigma2/settings"
        lines = []
        found = False

        if exists(settings_file):
            with open(settings_file, 'r') as f:
                for line in f:
                    if line.strip().startswith('# Calendar_last_used_default_time='):
                        lines.append('# Calendar_last_used_default_time=%s\n' % new_time)
                        found = True
                    else:
                        lines.append(line)

        # Add if not found
        if not found:
            lines.append('\n# Calendar_last_used_default_time=%s\n' % new_time)

        # Write back
        with open(settings_file, 'w') as f:
            f.writelines(lines)

        print("[ConfigManager] Updated last used default time to: %s" % new_time)
        return True

    except Exception as e:
        print("[ConfigManager] Error updating last used time: %s" % str(e))
        return False


def force_init_config():
    """FORCE configuration initialization - called on import"""
    global _calendar_config_initialized

    if not _calendar_config_initialized:
        print("[ConfigManager] FORCE: Initializing configuration...")
        init_calendar_config()
        init_export_config()
        _calendar_config_initialized = True
        print("[ConfigManager] FORCE: Configuration initialized")


def init_calendar_config():
    """Initialize all calendar configurations"""
    try:
        print("[ConfigManager] Initializing calendar config...")

        # Create config structure if not exists
        if not hasattr(config, 'plugins'):
            config.plugins = ConfigSubsection()
            print("[ConfigManager] Created config.plugins")

        if not hasattr(config.plugins, 'calendar'):
            config.plugins.calendar = ConfigSubsection()
            print("[ConfigManager] Created config.plugins.calendar")

        # ====== AUTOSTART CONFIG ======
        if not hasattr(config.plugins.calendar, 'autostart_enabled'):
            config.plugins.calendar.autostart_enabled = ConfigYesNo(default=True)
        if not hasattr(config.plugins.calendar, 'autostart_delay'):
            config.plugins.calendar.autostart_delay = ConfigInteger(default=30, limits=(5, 300))

        # ====== PERFORMANCE CONFIG ======
        if not hasattr(config.plugins.calendar, 'check_interval'):
            config.plugins.calendar.check_interval = ConfigInteger(default=60, limits=(10, 300))
        if not hasattr(config.plugins.calendar, 'auto_clean_notifications'):
            config.plugins.calendar.auto_clean_notifications = ConfigYesNo(default=True)
        if not hasattr(config.plugins.calendar, 'notification_cache_days'):
            config.plugins.calendar.notification_cache_days = ConfigInteger(default=7, limits=(1, 30))

        # ====== EVENTS CONFIG ======
        if not hasattr(config.plugins.calendar, 'events_enabled'):
            config.plugins.calendar.events_enabled = ConfigYesNo(default=True)
        if not hasattr(config.plugins.calendar, 'default_event_time'):
            config.plugins.calendar.default_event_time = ConfigText(default=OLD_DEFAULT_EVENT_TIME, fixed_size=False)
        if not hasattr(config.plugins.calendar, 'events_notifications'):
            config.plugins.calendar.events_notifications = ConfigYesNo(default=True)
        if not hasattr(config.plugins.calendar, 'events_show_indicators'):
            config.plugins.calendar.events_show_indicators = ConfigYesNo(default=True)
        if not hasattr(config.plugins.calendar, 'events_color'):
            config.plugins.calendar.events_color = ConfigSelection(
                choices=[
                    ("#0000FF", _("Blue")),
                    ("#FF0000", _("Red")),
                    ("#00FF00", _("Green")),
                    ("#FFA500", _("Orange")),
                    ("#FFFF00", _("Yellow")),
                    ("#FFFFFF", _("White")),
                    ("#00FFFF", _("Cyan")),
                ],
                default="#00FF00"
            )
        if not hasattr(config.plugins.calendar, 'events_play_sound'):
            config.plugins.calendar.events_play_sound = ConfigYesNo(default=True)
        if not hasattr(config.plugins.calendar, 'events_sound_type'):
            config.plugins.calendar.events_sound_type = ConfigSelection(
                choices=[
                    ("short", _("Short beep")),
                    ("notify", _("Notification tone")),
                    ("alert", _("Alert sound")),
                    ("none", _("No sound"))
                ],
                default="notify"
            )

        # ====== HOLIDAYS CONFIG ======
        if not hasattr(config.plugins.calendar, 'holidays_enabled'):
            config.plugins.calendar.holidays_enabled = ConfigYesNo(default=True)
        if not hasattr(config.plugins.calendar, 'holidays_show_indicators'):
            config.plugins.calendar.holidays_show_indicators = ConfigYesNo(default=True)
        if not hasattr(config.plugins.calendar, 'holidays_color'):
            config.plugins.calendar.holidays_color = ConfigSelection(
                choices=[
                    ("#0000FF", _("Blue")),
                    ("#FF0000", _("Red")),
                    ("#00FF00", _("Green")),
                    ("#FFA500", _("Orange")),
                    ("#FFFF00", _("Yellow")),
                    ("#FFFFFF", _("White")),
                    ("#00FFFF", _("Cyan")),
                ],
                default="#0000FF"
            )

        # ====== DATABASE CONFIG ======
        if not hasattr(config.plugins.calendar, 'database_format'):
            config.plugins.calendar.database_format = ConfigSelection(
                choices=[
                    ("legacy", _("Legacy format (text files)")),
                    ("vcard", _("vCard format (standard)")),
                    ("ics", _("ICS format (google calendar)")),
                ],
                default="legacy"
            )

        # ====== NOTIFICATION CONFIG ======
        if not hasattr(config.plugins.calendar, 'default_notify_minutes'):
            config.plugins.calendar.default_notify_minutes = ConfigInteger(default=5, limits=(0, 1440))

        # ====== DEBUG CONFIG ======
        if not hasattr(config.plugins.calendar, 'debug_enabled'):
            config.plugins.calendar.debug_enabled = ConfigYesNo(default=False)

        # ====== ADDITIONAL CONFIG ======
        # Menu position (like in your example)
        if not hasattr(config.plugins.calendar, 'menu'):
            config.plugins.calendar.menu = ConfigYesNo(default=True)

        # Auto-convert events
        if not hasattr(config.plugins.calendar, 'auto_convert_events'):
            config.plugins.calendar.auto_convert_events = ConfigYesNo(default=True)

        print("[ConfigManager] All config initialized successfully")
        return True

    except Exception as e:
        print("[ConfigManager] ERROR in init_calendar_config:", str(e))
        import traceback
        traceback.print_exc()
        return False


def validate_event_time(time_str):
    """Validate HH:MM format"""
    try:
        if not time_str or len(time_str) != 5:
            return False
        parts = time_str.split(':')
        if len(parts) != 2:
            return False
        hour = int(parts[0])
        minute = int(parts[1])
        return 0 <= hour <= 23 and 0 <= minute <= 59
    except:
        return False


def init_export_config():
    """Initialize export configuration"""
    try:
        print("[ConfigManager] Initializing export config...")
        # Ensure calendar config exists
        if not hasattr(config, 'plugins'):
            config.plugins = ConfigSubsection()
        if not hasattr(config.plugins, 'calendar'):
            config.plugins.calendar = ConfigSubsection()

        # Export location
        if not hasattr(config.plugins.calendar, 'export_location'):
            config.plugins.calendar.export_location = ConfigSelection(
                choices=[
                    ("/tmp/", _("Temporary Storage (/tmp)")),
                    ("/media/hdd/", _("Hard Disk (/media/hdd)")),
                    ("/media/usb/", _("USB Drive (/media/usb)")),
                    ("/home/root/", _("Root Home (/home/root)")),
                    ("/usr/lib/enigma2/python/Plugins/Extensions/Calendar/", _("Plugin Directory"))
                ],
                default="/tmp/"
            )

        # Export subdirectory
        if not hasattr(config.plugins.calendar, 'export_subdir'):
            config.plugins.calendar.export_subdir = ConfigText(
                default="Calendar_Export",
                fixed_size=False
            )

        # Add timestamp
        if not hasattr(config.plugins.calendar, 'export_add_timestamp'):
            config.plugins.calendar.export_add_timestamp = ConfigYesNo(default=True)

        # Export format
        if not hasattr(config.plugins.calendar, 'export_format'):
            config.plugins.calendar.export_format = ConfigSelection(
                choices=[
                    ("vcard", _("vCard format")),
                    ("ics", _("ICS format")),
                    ("csv", _("CSV format")),
                    ("txt", _("Text format"))
                ],
                default="vcard"
            )

        print("[ConfigManager] Export config initialized")
        return True

    except Exception as e:
        print("[ConfigManager] ERROR in init_export_config:", str(e))
        return False


def save_all_config():
    """Force save ALL configuration to disk"""
    try:
        print("=== CONFIG MANAGER: Saving ALL configuration ===")
        config.plugins.calendar.autostart_enabled.save()
        config.plugins.calendar.autostart_delay.save()
        config.plugins.calendar.check_interval.save()
        config.plugins.calendar.auto_clean_notifications.save()
        config.plugins.calendar.notification_cache_days.save()
        config.plugins.calendar.events_enabled.save()
        config.plugins.calendar.default_event_time.save()
        config.plugins.calendar.events_notifications.save()
        config.plugins.calendar.events_show_indicators.save()
        config.plugins.calendar.events_color.save()
        config.plugins.calendar.events_play_sound.save()
        config.plugins.calendar.events_sound_type.save()
        config.plugins.calendar.holidays_enabled.save()
        config.plugins.calendar.holidays_show_indicators.save()
        config.plugins.calendar.holidays_color.save()
        config.plugins.calendar.debug_enabled.save()
        config.plugins.calendar.database_format.save()
        config.plugins.calendar.default_notify_minutes.save()

        from Components.config import configfile
        # Ensure all config is initialized
        init_calendar_config()
        init_export_config()

        # Save to file
        configfile.save()
        print("SUCCESS: Config saved to /etc/enigma2/settings")

        settings_file = "/etc/enigma2/settings"
        if exists(settings_file):
            print("\n=== SAVED CONFIGURATIONS ===")
            with open(settings_file, 'r') as f:
                for line in f:
                    if 'calendar' in line.lower():
                        print(line.strip())
            print("=== END SAVED CONFIGURATIONS ===")
        return True
    except Exception as e:
        print("ERROR in save_all_config: %s" % str(e))
        import traceback
        traceback.print_exc()
        return False


def get_default_event_time():
    """Get default event time from configuration"""
    try:
        if (hasattr(config, 'plugins') and
                hasattr(config.plugins, 'calendar') and
                hasattr(config.plugins.calendar, 'default_event_time')):

            time_str = config.plugins.calendar.default_event_time.value.strip()
            if time_str and ':' in time_str:
                parts = time_str.split(':')
                if len(parts) == 2:
                    try:
                        hours = int(parts[0])
                        minutes = int(parts[1])
                        if 0 <= hours <= 23 and 0 <= minutes <= 59:
                            return "%02d:%02d" % (hours, minutes)
                    except ValueError:
                        pass

            return OLD_DEFAULT_EVENT_TIME

    except Exception as e:
        print("[ConfigManager] Error getting default event time:", e)

    return OLD_DEFAULT_EVENT_TIME


def get_default_notify_minutes():
    """Get default notification minutes before event"""
    try:
        if (hasattr(config, 'plugins') and
                hasattr(config.plugins, 'calendar') and
                hasattr(config.plugins.calendar, 'default_notify_minutes')):
            return config.plugins.calendar.default_notify_minutes.value
    except:
        pass
    return 5


def get_autostart_status():
    """Check autostart configuration"""
    try:
        if (hasattr(config, 'plugins') and
                hasattr(config.plugins, 'calendar') and
                hasattr(config.plugins.calendar, 'autostart_enabled')):
            return config.plugins.calendar.autostart_enabled.value
    except:
        pass
    return True


def get_debug():
    """Get debug status safely"""
    try:
        if (hasattr(config, 'plugins') and
                hasattr(config.plugins, 'calendar') and
                hasattr(config.plugins.calendar, 'debug_enabled')):
            return config.plugins.calendar.debug_enabled.value
    except:
        pass
    return False


def get_export_format():
    """Get export format"""
    try:
        if (hasattr(config, 'plugins') and
                hasattr(config.plugins, 'calendar') and
                hasattr(config.plugins.calendar, 'export_format')):
            return config.plugins.calendar.export_format.value
    except:
        pass
    return "vcard"


def get_check_interval():
    """Get check interval in seconds"""
    try:
        if (hasattr(config, 'plugins') and
                hasattr(config.plugins, 'calendar') and
                hasattr(config.plugins.calendar, 'check_interval')):
            return config.plugins.calendar.check_interval.value
    except:
        pass
    return 60


def get_all_config_values():
    """Debug function to get all config values"""
    values = {}
    try:
        if hasattr(config, 'plugins') and hasattr(config.plugins, 'calendar'):
            for attr_name in dir(config.plugins.calendar):
                if not attr_name.startswith('__'):
                    attr = getattr(config.plugins.calendar, attr_name)
                    if hasattr(attr, 'value'):
                        values[attr_name] = attr.value
    except Exception as e:
        print("[ConfigManager] Error getting all config values:", e)
    return values


def get_auto_refresh_interval():
    """Get auto refresh interval in seconds"""
    try:
        if (hasattr(config, 'plugins') and
                hasattr(config.plugins, 'calendar') and
                hasattr(config.plugins.calendar, 'auto_refresh_interval')):
            return config.plugins.calendar.auto_refresh_interval.value
    except:
        pass
    return 0


def get_upcoming_days():
    """Get number of days to show for upcoming events"""
    try:
        if (hasattr(config, 'plugins') and
                hasattr(config.plugins, 'calendar') and
                hasattr(config.plugins.calendar, 'upcoming_days')):
            return config.plugins.calendar.upcoming_days.value
    except:
        pass
    return 7


def get_max_events_per_day():
    """Get maximum events to display per day"""
    try:
        if (hasattr(config, 'plugins') and
                hasattr(config.plugins, 'calendar') and
                hasattr(config.plugins.calendar, 'max_events_per_day')):
            return config.plugins.calendar.max_events_per_day.value
    except:
        pass
    return 10


def init_all_config():
    """Initialize all configuration in correct order"""
    global _calendar_config_initialized
    
    if _calendar_config_initialized:
        print("[ConfigManager] Config already initialized, skipping")
        return True

    print("[ConfigManager] init_all_config called")

    # 1. Basic config first
    if not init_calendar_config():
        print("[ConfigManager] ERROR: Failed to init basic config")
        return False

    # 2. Export config
    init_export_config()

    # 3. Initialize last used default time
    init_last_used_time()

    _calendar_config_initialized = True

    print("[ConfigManager] All configuration initialized")
    # Debug: Print all config values
    print("\n=== CURRENT CONFIG VALUES ===")
    values = get_all_config_values()
    for key, value in sorted(values.items()):
        print("%s: %s" % (key, value))
    print("=== END CONFIG VALUES ===\n")
    return True
