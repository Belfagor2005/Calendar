#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
###########################################################
#                                                         #
#  Calendar Planner for Enigma2                           #
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
#  • Holiday import system with automatic coloring        #
#  • vCard (.vcf) import/export system                    #
#  • Contact management with birthdays                    #
#  • Database format converter (Legacy ↔ vCard)           #
#                                                         #
#  EVENT SYSTEM:                                          #
#  • Smart notifications (0-60 minutes before event)      #
#  • Background monitoring every 30 seconds               #
#  • Visual indicators on calendar for days with events   #
#  • Event persistence in JSON format                     #
#  • Configurable notification duration (3-15 seconds)    #
#  • Automatic cleanup of past event notifications        #
#                                                         #
#  AUDIO NOTIFICATION SYSTEM:                             #
#  • Built-in sound alerts (alert/notify/short tones)     #
#  • Support for WAV and MP3 formats                      #
#  • Priority-based sound selection                       #
#    - Alert: events in progress (notify_before=0)        #
#    - Notify: imminent events (≤5 min before)            #
#    - Short: regular notifications                       #
#  • Sound files location: /sounds/ directory             #
#  • Auto-stop after playback completion                  #
#                                                         #
#  HOLIDAY SYSTEM:                                        #
#  • Import holidays from Holidata.net                    #
#  • Support for 30+ countries and languages              #
#  • Automatic holiday coloring with configurable colors  #
#  • "H" indicator for holiday days                       #
#  • Smart cache system for fast loading                  #
#  • Today's and upcoming holidays display                #
#  • Integration with existing date files                 #
#                                                         #
#  VCARD & CONTACT SYSTEM:                                #
#  • Import thousands of contacts from .vcf files         #
#  • Multi-threaded import (no GUI freeze)                #
#  • Contact management with birthdays                    #
#  • Birthday tracking with age calculation               #
#  • Contact sorting (name, birthday, category)           #
#  • Search by name, phone, email, notes                  #
#  • Duplicate detection during import                    #
#  • Progress bar with cancel option                      #
#                                                         #
#  DATABASE MANAGEMENT:                                   #
#  • Convert between Legacy and vCard formats             #
#  • Creates automatic backups before conversion          #
#  • Preserves all data during conversion                 #
#  • Progress indicator during conversion                 #
#  • Consistency checking between formats                 #
#                                                         #
#  DATE MANAGEMENT:                                       #
#  • Create, edit, remove date information                #
#  • Virtual keyboard for field editing                   #
#  • Automatic field navigation during editing            #
#  • File structure: base/[language]/day/YYYYMMDD.txt     #
#  • Sections: [day] for date info, [month] for people    #
#                                                         #
#  CALENDAR DISPLAY:                                      #
#  • Color code: Today=green, Saturday=yellow, Sunday=red #
#  • Event days highlighted in blue/cyan (configurable)   #
#  • Holiday days highlighted in orange (configurable)    #
#  • Asterisk (*) indicator for days with events          #
#  • "H" indicator for holiday days                       #
#  • Birthday contacts display in description             #
#  • Week numbers display                                 #
#  • Smooth month navigation                              #
#  • Day selection with blue background                   #
#  • Color priority: Today > Selection > Holiday > Event  #
#                                                         #
#  CONFIGURATION:                                         #
#  • Event system enable/disable                          #
#  • Notification settings (duration, advance time)       #
#  • Audio notification type (short/notify/alert/none)    #
#  • Enable/disable sound playback                        #
#  • Event color selection                                #
#  • Show event indicators toggle                         #
#  • Holiday system enable/disable                        #
#  • Holiday color selection                              #
#  • Show holiday indicators toggle                       #
#  • Menu integration option                              #
#  • Database format selection (Legacy/vCard)             #
#                                                         #
#  KEY CONTROLS - MAIN CALENDAR:                          #
#   OK          - Open main menu                          #
#                 (New/Edit/Remove/Events/Holidays/       #
#                  Contacts/Import vCard/Converter)       #
#   RED         - Previous month                          #
#   GREEN       - Next month                              #
#   YELLOW      - Previous day                            #
#   BLUE        - Next day                                #
#   0 (ZERO)    - Open event management                   #
#   LEFT/RIGHT  - Previous/Next day                       #
#   UP/DOWN     - Previous/Next month                     #
#   MENU        - Configuration                           #
#   INFO/EPG    - About dialog                            #
#                                                         #
#  KEY CONTROLS - EVENT DIALOG:                           #
#   OK          - Edit current field                      #
#   RED         - Cancel                                  #
#   GREEN       - Save event                              #
#   YELLOW      - Delete event (edit mode only)           #
#   UP/DOWN     - Navigate between fields                 #
#   LEFT/RIGHT  - Change selection options                #
#                                                         #
#  KEY CONTROLS - EVENTS VIEW:                            #
#   OK          - Edit selected event                     #
#   RED         - Add new event                           #
#   GREEN       - Edit selected event                     #
#   YELLOW      - Delete selected event                   #
#   BLUE        - Back to calendar                        #
#   UP/DOWN     - Navigate event list                     #
#                                                         #
#  KEY CONTROLS - CONTACTS VIEW:                          #
#   OK          - Edit selected contact                   #
#   RED         - Add new contact                         #
#   GREEN       - Edit selected contact                   #
#   YELLOW      - Delete selected contact                 #
#   BLUE        - Toggle sort mode (Name/Birthday/Cat.)   #
#   UP/DOWN     - Navigate contact list                   #
#                                                         #
#  KEY CONTROLS - VCARD IMPORTER:                         #
#   OK          - Select file                             #
#   RED         - Cancel                                  #
#   GREEN       - Import selected file                    #
#   YELLOW      - View file info (size, contacts)         #
#   BLUE        - Refresh file list                       #
#                                                         #
#  KEY CONTROLS - DATABASE CONVERTER:                     #
#   OK          - Show statistics                         #
#   RED         - Cancel                                  #
#   GREEN       - Convert to vCard format                 #
#   BLUE        - Convert to legacy format                #
#                                                         #
#  FILE STRUCTURE:                                        #
#  • plugin.py - Main plugin entry point                  #
#  • event_manager.py - Event management core             #
#  • event_dialog.py - Event add/edit interface           #
#  • events_view.py - Events browser                      #
#  • notification_system.py - Notification display        #
#  • holidays.py - Holiday import and management          #
#  • vcard_importer.py - vCard import system              #
#  • birthday_manager.py - Contact management             #
#  • contacts_view.py - Contacts browser                  #
#  • birthday_dialog.py - Contact add/edit dialog         #
#  • database_converter.py - Format converter             #
#  • events.json - Event database (JSON format)           #
#  • base/ - Date information storage                     #
#  • base/contacts/ - vCard contact storage               #
#  • sounds/ - Audio files for notifications              #
#  • buttons/ - Button images for UI                      #
#                                                         #
#  AUDIO FILE REQUIREMENTS:                               #
#  • alert.wav / alert.mp3 - High priority events         #
#  • notify.wav / notify.mp3 - Normal notifications       #
#  • beep.wav / beep.mp3 - Short beeps                    #
#  • Location: /Calendar/sounds/                          #
#                                                         #
#  EVENT STORAGE FORMAT (events.json):                    #
#  [{                                                     #
#    "id": 1766153767369,                                 #
#    "title": "Meeting",                                  #
#    "description": "Team meeting",                       #
#    "date": "2025-12-19",                                #
#    "time": "14:30",                                     #
#    "repeat": "none",                                    #
#    "notify_before": 5,                                  #
#    "enabled": true,                                     #
#    "created": "2024-12-19 14:25:47"                     #
#  }]                                                     #
#                                                         #
#  CONTACT STORAGE FORMAT (contacts/*.txt):               #
#  [contact]                                              #
#  FN: John Doe                                           #
#  BDAY: 1990-05-15                                       #
#  TEL: +391234567890                                     #
#  EMAIL: john@example.com                                #
#  CATEGORIES: Family, Friends                            #
#  NOTE: Birthday reminder                                #
#  CREATED: 2024-12-25 10:30:00                           #
#                                                         #
#  DATE FILE FORMAT (YYYYMMDD.txt):                       #
#  [day]                                                  #
#  date: 2025-06-10                                       #
#  datepeople: John Doe                                   #
#  sign: Gemini                                           #
#  holiday: Christmas Day, New Year's Day                 #
#  description: Special day description.                  #
#                                                         #
#  [month]                                                #
#  monthpeople: Important people of the month             #
#                                                         #
#  HOLIDAY IMPORT:                                        #
#  • Source: Holidata.net                                 #
#  • Format: JSON Lines per country/year                  #
#  • Countries: Italy, Germany, France, UK, USA, etc.     #
#  • Languages: it, en, de, fr, es, etc.                  #
#  • Cache: Memory-based for performance                  #
#  • Integration: Updates holiday field in date files     #
#                                                         #
#  TECHNICAL DETAILS:                                     #
#  • Python 2.7+ compatible                               #
#  • Uses eTimer for background monitoring                #
#  • JSON storage for events                              #
#  • Threaded vCard import (no GUI freeze)                #
#  • Virtual keyboard integration                         #
#  • Auto-skin detection (HD/FHD)                         #
#  • Configurable via setup.xml                           #
#  • Uses eServiceReference for audio playback            #
#  • Holiday cache system for fast rendering              #
#  • File-based storage (no database)                     #
#                                                         #
#  PERFORMANCE:                                           #
#  • Efficient event checking algorithm                   #
#  • Skipped checks for past non-recurring events         #
#  • Holiday cache: 1 file read per month                 #
#  • Threaded import for large vCard files                #
#  • Minimal memory usage                                 #
#  • Fast loading of date information                     #
#                                                         #
#  DEBUGGING:                                             #
#  • Enable debug logs: check enigma2.log                 #
#  • Filter: grep EventManager /tmp/enigma2.log           #
#  • Holiday debug: grep Holidays /tmp/enigma2.log        #
#  • vCard debug: grep VCardImporter /tmp/enigma2.log     #
#  • Event check interval: 30 seconds                     #
#  • Notification window: event time ± 5 minutes          #
#  • Audio debug: check play_notification_sound() calls   #
#                                                         #
#  CREDITS:                                               #
#  • Original Calendar plugin: Sirius0103                 #
#  • Event system & modifications: Lululla                #
#  • Holiday system & enhancements: Custom implementation #
#  • vCard system & database converter: Lululla           #
#  • Notification system: Custom implementation           #
#  • Audio system: Enigma2 eServiceReference integration  #
#  • Testing & feedback: Enigma2 community                #
#                                                         #
#  VERSION HISTORY:                                       #
#  • v1.0 - Basic calendar functionality                  #
#  • v1.1 - Complete event system added                   #
#  • v1.2 - Holiday import and coloring system            #
#  • v1.3 - Rewrite complete code . screen and source..   #
#  • v1.4 - minor fix for update and timers py2           #
#  • v1.5 - vCard import/export & contact management      #
#                                                         #
#  Last Updated: 2025-12-25                               #
#  Status: Stable with all systems integrated             #
###########################################################
"""
from __future__ import print_function
import time
import shutil
import subprocess
from re import sub, search
from os import makedirs
from os.path import join, exists
from sys import version_info

from . import _, PLUGIN_VERSION, plugin_path

if version_info[0] == 3:
    from urllib.request import urlopen, Request
else:
    from urllib2 import urlopen, Request


USER_AGENT = "Calendar-Enigma2-Updater/%s" % PLUGIN_VERSION


class PluginUpdater:
    """Plugin update manager"""

    # Repository information
    REPO_OWNER = "Belfagor2005"
    REPO_NAME = "Calendar"
    REPO_BRANCH = "main"

    # GitHub URLs
    RAW_CONTENT = "https://raw.githubusercontent.com"
    INSTALLER_URL = "https://raw.githubusercontent.com/Belfagor2005/Calendar/main/installer.sh"

    # Backup directory
    BACKUP_DIR = "/tmp/Calendar_backup"

    def __init__(self):
        self.current_version = PLUGIN_VERSION
        self.user_agent = USER_AGENT
        self.backup_path = None

        # Create backup directory
        if not exists(self.BACKUP_DIR):
            makedirs(self.BACKUP_DIR, mode=0o755)

    def get_latest_version(self):
        """Get latest version from installer.sh - Python 2/3 compatible"""
        try:
            installer_url = "https://raw.githubusercontent.com/Belfagor2005/Calendar/main/installer.sh"

            print("Checking version from: %s" % installer_url)

            headers = {'User-Agent': self.user_agent}
            req = Request(installer_url, headers=headers)

            response = None
            try:
                response = urlopen(req, timeout=10)
                content = response.read().decode('utf-8')
            finally:
                if response:
                    response.close()

            patterns = [
                r"version\s*=\s*['\"](\d+\.\d+)['\"]",  # version='1.1' o version="1.1"
                r"version\s*:\s*['\"](\d+\.\d+)['\"]",  # version: '1.1'
                r"Version\s*=\s*['\"](\d+\.\d+)['\"]",  # Version='1.1'
            ]

            for pattern in patterns:
                match = search(pattern, content)
                if match:
                    version = match.group(1)
                    print("Found version %s using pattern: %s" % (version, pattern))
                    return version

            print("No version pattern found in installer.sh")
            fallback = search(r'(\d+\.\d+)', content)
            if fallback:
                version = fallback.group(1)
                print("Fallback found version: %s" % version)
                return version

            return None

        except Exception as e:
            print("Error getting latest version: %s" % e)
            return None

    def compare_versions(self, v1, v2):
        """Compare version strings"""
        try:
            # Clean version strings
            v1_clean = sub(r'[^\d.]', '', v1)
            v2_clean = sub(r'[^\d.]', '', v2)

            v1_parts = list(map(int, v1_clean.split('.')))
            v2_parts = list(map(int, v2_clean.split('.')))

            # Pad with zeros if needed
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts += [0] * (max_len - len(v1_parts))
            v2_parts += [0] * (max_len - len(v2_parts))

            for i in range(max_len):
                if v1_parts[i] > v2_parts[i]:
                    return 1
                elif v1_parts[i] < v2_parts[i]:
                    return -1
            return 0
        except Exception as e:
            print("Version compare error: %s" % e)
            return 0

    def check_update(self, callback=None):
        """Check if update is available - VERSIONE SINCROZINATA"""
        print("PluginUpdater.check_update called")

        try:
            latest = self.get_latest_version()
            print("get_latest_version returned: %s" % latest)
            print("Current version: %s" % self.current_version)

            if latest is None:
                print("Could not get latest version")
                if callback:
                    callback(None)
                return

            # Compare versions
            is_newer = self.compare_versions(latest, self.current_version) > 0
            print("Version comparison: is_newer = %s" % is_newer)

            if callback:
                print("Calling callback with: %s" % is_newer)
                callback(is_newer)

        except Exception as e:
            print("Error in check_update: %s" % e)
            if callback:
                callback(None)

    def download_update(self, callback=None):
        """Download and install update - VERSIONE SINCROZINATA"""
        print("Starting update process...")
        success = False
        message = ""

        try:
            # Step 1: Create backup
            if not self.create_backup():
                message = _("Failed to create backup. Update cancelled.")
                if callback:
                    callback(False, message)
                return

            # Step 2: Download and run installer
            if self.download_and_run_installer():
                success = True
                message = _("Update completed successfully!")
            else:
                # Step 3: Restore backup if failed
                if self.restore_backup():
                    message = _("Update failed. Restored from backup.")
                else:
                    message = _("Update failed and backup restore also failed!")

        except Exception as e:
            print("Update process error: %s" % e)
            # Try to restore backup
            try:
                self.restore_backup()
            except:
                pass
            message = _("Update error: %s") % str(e)

        if callback:
            callback(success, message)

    def download_and_run_installer(self):
        """Download and run installer script - USANDO WGET COME NELL'INSTALLER"""
        try:
            print("Running Calendar installer...")
            cmd = 'wget -q --no-check-certificate "https://raw.githubusercontent.com/Belfagor2005/Calendar/main/installer.sh" -O - | /bin/sh'
            print("Executing: %s" % cmd)
            result = subprocess.call(cmd, shell=True)

            if result == 0:
                print("Installer completed successfully")
                return True
            else:
                print("Installer failed with exit code: %d" % result)
                return False

        except Exception as e:
            print("Installer execution error: %s" % e)
            return False

    def create_backup(self):
        """Create backup of current plugin"""
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_name = "backup_v%s_%s" % (self.current_version, timestamp)
            self.backup_path = join(self.BACKUP_DIR, backup_name)

            if exists(plugin_path):
                print("Creating backup to: %s" % self.backup_path)
                shutil.copytree(plugin_path, self.backup_path)
                print("Backup created successfully")
                return True
            else:
                print("Plugin path not found: %s" % plugin_path)
                return False
        except Exception as e:
            print("Backup failed: %s" % e)
            return False

    def restore_backup(self):
        """Restore from backup"""
        try:
            if self.backup_path and exists(self.backup_path):
                print("Restoring from backup: %s" % self.backup_path)

                # Remove current plugin
                if exists(plugin_path):
                    shutil.rmtree(plugin_path)

                # Restore from backup
                shutil.copytree(self.backup_path, plugin_path)
                print("Restored successfully")
                return True
            else:
                print("Backup not found: %s" % self.backup_path)
                return False
        except Exception as e:
            print("Restore failed: %s" % e)
            return False


def perform_update(callback=None):
    """Simple update"""
    updater = PluginUpdater()
    return updater.download_update(callback)
