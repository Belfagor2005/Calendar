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
import shutil
from datetime import datetime
from os import makedirs, listdir
from os.path import exists, join, dirname, isdir
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ProgressBar import ProgressBar
from enigma import getDesktop

from . import _, PLUGIN_PATH


class DatabaseConverter(Screen):
    if (getDesktop(0).size().width() >= 1920):
        skin = """
            <screen name="DatabaseConverter" position="center,center" size="1200,800" title="Database Converter" flags="wfNoBorder">
                <widget name="title" position="10,10" size="1180,40" font="Regular;32" halign="center" valign="center" />
                <widget name="details" position="10,65" size="1180,578" font="Regular;28" />
                <widget name="status" position="10,672" size="1180,40" font="Regular;28" />
                <widget name="progress" position="10,648" size="1180,20" />
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="50,768" size="230,10" alphatest="blend" />
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_green.png" position="364,769" size="230,10" alphatest="blend" />
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_blue.png" position="944,770" size="230,10" alphatest="blend" />
                <widget name="key_red" position="50,725" size="230,40" font="Regular;28" halign="center" valign="center" />
                <widget name="key_green" position="365,725" size="230,40" font="Regular;28" halign="center" valign="center" />
                <widget name="key_blue" position="944,725" size="230,40" font="Regular;28" halign="center" valign="center" />
        </screen>
        """
    else:
        skin = """
            <screen name="DatabaseConverter" position="center,center" size="850,600" title="Database Converter" flags="wfNoBorder">
                <widget name="title" position="16,10" size="820,40" font="Regular;32" halign="center" valign="center" />
                <widget name="details" position="16,67" size="820,400" font="Regular;24" />
                <widget name="status" position="18,497" size="820,40" font="Regular;28" />
                <widget name="progress" position="15,473" size="820,20" />
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="35,571" size="150,10" alphatest="blend" />
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_green.png" position="213,572" size="150,10" alphatest="blend" />
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_blue.png" position="591,572" size="150,10" alphatest="blend" />
                <widget name="key_red" position="35,545" size="150,25" font="Regular;20" halign="center" valign="center" />
                <widget name="key_green" position="215,545" size="150,25" font="Regular;20" halign="center" valign="center" />
                <widget name="key_blue" position="595,545" size="150,25" font="Regular;20" halign="center" valign="center" />
            </screen>
        """

    def __init__(self, session, plugin_path, language):
        Screen.__init__(self, session)
        self.session = session
        self.plugin_path = plugin_path
        self.language = language

        self["title"] = Label(_("Database Converter"))
        self["status"] = Label(_("Ready"))
        self["details"] = Label("")
        self["progress"] = ProgressBar()
        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label(_("Convert to vCard"))
        self["key_blue"] = Label(_("Convert to Legacy"))

        self["actions"] = ActionMap(
            ["CalendarActions"],
            {
                "red": self.cancel,
                "green": self.convert_to_vcard,
                "blue": self.convert_to_legacy,
                "cancel": self.cancel,
                "ok": self.ok,
            }, -1
        )

        self.converter = Converter(plugin_path, language)
        self.update_status()

    def update_status(self):
        """Update status display"""
        legacy_count = self.converter.count_legacy_files()
        vcard_count = self.converter.count_vcard_files()

        status_text = _("Legacy: {0} files | vCard: {1} files").format(
            legacy_count, vcard_count
        )
        self["status"].setText(status_text)

        details = [
            _("Current format: {0}").format("Legacy" if legacy_count > vcard_count else "vCard"),
            _("Language: {0}").format(self.language)
        ]
        self["details"].setText("\n".join(details))

    def convert_to_vcard(self):
        """Convert from Legacy to vCard format"""
        if not self.converter.has_legacy_files():
            self.session.open(
                MessageBox,
                _("No legacy files found to convert"),
                MessageBox.TYPE_INFO
            )
            return

        self.session.openWithCallback(
            self.confirm_conversion,
            MessageBox,
            _("Convert all legacy files to vCard format?\n\n"
              "This will create new vCard files while keeping the original legacy files."),
            MessageBox.TYPE_YESNO
        )

    def convert_to_legacy(self):
        """Convert from vCard to Legacy format"""
        if not self.converter.has_vcard_files():
            self.session.open(
                MessageBox,
                _("No vCard files found to convert"),
                MessageBox.TYPE_INFO
            )
            return

        self.session.openWithCallback(
            self.confirm_conversion_back,
            MessageBox,
            _("Convert all vCard files to legacy format?\n\n"
              "This will create new legacy files while keeping the original vCard files."),
            MessageBox.TYPE_YESNO
        )

    def confirm_conversion(self, result=None):
        """Confirm conversion to vCard"""
        if result:
            self["status"].setText(_("Converting to vCard..."))
            self["progress"].setValue(0)

            def conversion_callback(progress, message, completed):
                self["progress"].setValue(int(progress * 100))
                self["details"].setText(message)

                if completed:
                    self.session.open(
                        MessageBox,
                        _("Conversion completed successfully!"),
                        MessageBox.TYPE_INFO
                    )
                    self.update_status()

            # Start conversion in background
            self.converter.convert_legacy_to_vcard(conversion_callback)

    def confirm_conversion_back(self, result=None):
        """Confirm conversion back to Legacy"""
        if result:
            self["status"].setText(_("Converting to Legacy..."))
            self["progress"].setValue(0)

            def conversion_callback(progress, message, completed):
                self["progress"].setValue(int(progress * 100))
                self["details"].setText(message)

                if completed:
                    self.session.open(
                        MessageBox,
                        _("Conversion completed successfully!"),
                        MessageBox.TYPE_INFO
                    )
                    self.update_status()

            # Start conversion in background
            self.converter.convert_vcard_to_legacy(conversion_callback)

    def ok(self):
        """OK button - show statistics"""
        legacy_count = self.converter.count_legacy_files()
        vcard_count = self.converter.count_vcard_files()

        stats = [
            _("Database Statistics"),
            _("Legacy files: {0}").format(legacy_count),
            _("vCard files: {0}").format(vcard_count),
            "",
            _("Paths:"),
            _("Legacy: {0}").format(self.converter.legacy_path),
            _("vCard: {0}").format(self.converter.vcard_path)
        ]

        self.session.open(
            MessageBox,
            "\n".join(stats),
            MessageBox.TYPE_INFO
        )

    def cancel(self):
        """Cancel and close"""
        self.close()

    # def close(self, result=None):
        # """Close the screen"""
        # Screen.close(self, result)


class Converter:
    """Main converter class"""

    # MAPPING DEFINITIONS
    LEGACY_TO_VCARD = {
        'date': 'DATE',             # Date field
        'datepeople': 'FN',         # Formatted Name
        'sign': 'CATEGORIES',       # Tags/Categories
        'holiday': 'holiday',       # Holiday (stays same!)
        'description': 'NOTE',      # Notes/Description
        'monthpeople': 'CONTACTS'   # Contacts list
    }

    VCARD_TO_LEGACY = {
        'DATE': 'date',
        'FN': 'datepeople',
        'CATEGORIES': 'sign',
        'holiday': 'holiday',           # Holiday (stays same!)
        'NOTE': 'description',
        'DESCRIPTION': 'description',   # Alternative
        'CONTACTS': 'monthpeople',
        'ORG': 'monthpeople'            # Alternative mapping
    }

    def __init__(self, plugin_path, language):
        self.plugin_path = plugin_path
        self.language = language

        # Define paths
        self.legacy_path = join(plugin_path, "base", language, "day")
        self.vcard_path = join(plugin_path, "base", "vcard", language)

        # Ensure directories exist
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories"""
        if not exists(self.vcard_path):
            makedirs(self.vcard_path)

    def count_legacy_files(self):
        """Count legacy format files"""
        if not exists(self.legacy_path):
            return 0

        count = 0
        for filename in listdir(self.legacy_path):
            if filename.endswith(".txt") and len(filename) == 12:  # YYYYMMDD.txt
                count += 1
        return count

    def count_vcard_files(self):
        """Count vCard format files"""
        if not exists(self.vcard_path):
            return 0

        count = 0
        for filename in listdir(self.vcard_path):
            if filename.endswith(".txt") and len(filename) == 12:  # YYYYMMDD.txt
                count += 1
        return count

    def has_legacy_files(self):
        """Check if legacy files exist"""
        return self.count_legacy_files() > 0

    def has_vcard_files(self):
        """Check if vCard files exist"""
        return self.count_vcard_files() > 0

    def convert_legacy_to_vcard(self, callback=None):
        """Convert all legacy files to vCard format"""
        if not exists(self.legacy_path):
            if callback:
                callback(1.0, _("No legacy files found"), True)
            return

        files = []
        for filename in listdir(self.legacy_path):
            if filename.endswith(".txt") and len(filename) == 12:
                files.append(filename)

        total = len(files)
        if total == 0:
            if callback:
                callback(1.0, _("No legacy files found"), True)
            return

        converted = 0
        errors = 0

        for i, filename in enumerate(files):
            try:
                # Update progress
                progress = (i + 1) / total
                message = _("Converting: {0} ({1}/{2})").format(filename, i + 1, total)
                if callback:
                    callback(progress, message, False)

                # Convert single file
                legacy_file = join(self.legacy_path, filename)
                vcard_file = join(self.vcard_path, filename)

                if self._convert_file(legacy_file, vcard_file, "legacy_to_vcard"):
                    converted += 1
                else:
                    errors += 1

            except Exception as e:
                print("[Converter] Error converting {0}: {1}".format(filename, str(e)))
                errors += 1

        # Final callback
        if callback:
            message = _("Converted: {0} files, Errors: {1}").format(converted, errors)
            callback(1.0, message, True)

    def convert_vcard_to_legacy(self, callback=None):
        """Convert all vCard files to legacy format"""
        if not exists(self.vcard_path):
            if callback:
                callback(1.0, _("No vCard files found"), True)
            return

        files = []
        for filename in listdir(self.vcard_path):
            if filename.endswith(".txt") and len(filename) == 12:
                files.append(filename)

        total = len(files)
        if total == 0:
            if callback:
                callback(1.0, _("No vCard files found"), True)
            return

        converted = 0
        errors = 0

        for i, filename in enumerate(files):
            try:
                # Update progress
                progress = (i + 1) / total
                message = _("Converting: {0} ({1}/{2})").format(filename, i + 1, total)
                if callback:
                    callback(progress, message, False)

                # Convert single file
                vcard_file = join(self.vcard_path, filename)
                legacy_file = join(self.legacy_path, filename)

                if self._convert_file(vcard_file, legacy_file, "vcard_to_legacy"):
                    converted += 1
                else:
                    errors += 1

            except Exception as e:
                print("[Converter] Error converting {0}: {1}".format(filename, str(e)))
                errors += 1

        # Final callback
        if callback:
            message = _("Converted: {0} files, Errors: {1}").format(converted, errors)
            callback(1.0, message, True)

    def _convert_file(self, source_file, target_file, direction):
        """
        Convert single file between formats

        Args:
            source_file: Path to source file
            target_file: Path to target file
            direction: "legacy_to_vcard" or "vcard_to_legacy"
        """
        if not exists(source_file):
            return False

        try:
            # Read source file
            with open(source_file, 'r') as f:
                lines = f.readlines()

            # Parse file content
            data = self._parse_file_content(lines, direction)

            # Write target file
            self._write_converted_file(data, target_file, direction)

            return True

        except Exception as e:
            print("[Converter] Error converting {0}: {1}".format(source_file, str(e)))
            return False

    def _parse_file_content(self, lines, direction):
        """
        Parse file content and extract data

        Args:
            lines: List of lines from file
            direction: Conversion direction
        """
        data = {}
        current_section = None

        for line in lines:
            line = line.strip()

            # Detect sections
            if line in ["[day]", "[contact]"]:
                current_section = "main"
            elif line == "[month]":
                current_section = "month"
            elif line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1]

            # Parse key-value pairs
            elif current_section and ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                # Store data
                if current_section == "month":
                    data["month_" + key] = value
                else:
                    data[key] = value

        return data

    def _write_converted_file(self, data, target_file, direction):
        """
        Write converted data to target file

        Args:
            data: Dictionary with parsed data
            target_file: Path to target file
            direction: Conversion direction
        """
        # Create directory if needed
        target_dir = dirname(target_file)
        if not exists(target_dir):
            makedirs(target_dir)

        # Prepare content based on direction
        if direction == "legacy_to_vcard":
            content = self._create_vcard_content(data)
        else:  # vcard_to_legacy
            content = self._create_legacy_content(data)

        # Write to file
        with open(target_file, 'w') as f:
            f.write(content)

    def _create_vcard_content(self, data):
        """Create vCard format content from legacy data"""
        content = "[contact]\n"

        # Apply mapping
        for legacy_key, vcard_key in self.LEGACY_TO_VCARD.items():
            value = data.get(legacy_key, '')
            if value:
                content += "{0}: {1}\n".format(vcard_key, value)

        # Handle monthpeople
        month_value = data.get("month_monthpeople", '')
        if month_value:
            content += "CONTACTS: {0}\n".format(month_value)

        return content

    def _create_legacy_content(self, data):
        """Create legacy format content from vCard data"""
        # Build day section
        day_content = "[day]\n"

        # Apply reverse mapping
        for vcard_key, legacy_key in self.VCARD_TO_LEGACY.items():
            value = data.get(vcard_key, '')
            if value:
                day_content += "{0}: {1}\n".format(legacy_key, value)

        # Build month section
        month_content = "\n[month]\n"

        # Handle CONTACTS/ORG -> monthpeople
        contacts_value = data.get("CONTACTS", data.get("ORG", ''))
        if contacts_value:
            month_content += "monthpeople: {0}\n".format(contacts_value)

        return day_content + month_content

    def backup_database(self, backup_name=None):
        """
        Create backup of database

        Args:
            backup_name: Optional backup name (default: timestamp)
        """
        if backup_name is None:
            backup_name = "backup_" + datetime.now().strftime("%Y%m%d_%H%M%S")

        backup_path = join(self.plugin_path, "backups", backup_name)

        try:
            # Create backup directory
            makedirs(backup_path, exist_ok=True)

            # Copy legacy directory
            if exists(self.legacy_path):
                legacy_backup = join(backup_path, "legacy")
                if exists(legacy_backup):
                    shutil.rmtree(legacy_backup)
                shutil.copytree(self.legacy_path, legacy_backup)

            # Copy vcard directory
            if exists(self.vcard_path):
                vcard_backup = join(backup_path, "vcard")
                if exists(vcard_backup):
                    shutil.rmtree(vcard_backup)
                shutil.copytree(self.vcard_path, vcard_backup)

            return backup_path

        except Exception as e:
            print("[Converter] Backup error: {0}".format(str(e)))
            return None

    def restore_backup(self, backup_path):
        """
        Restore database from backup

        Args:
            backup_path: Path to backup directory
        """
        if not exists(backup_path) or not isdir(backup_path):
            return False

        try:
            # Restore legacy files
            legacy_backup = join(backup_path, "legacy")
            if exists(legacy_backup):
                # Clear existing
                if exists(self.legacy_path):
                    shutil.rmtree(self.legacy_path)
                # Restore from backup
                shutil.copytree(legacy_backup, self.legacy_path)

            # Restore vcard files
            vcard_backup = join(backup_path, "vcard")
            if exists(vcard_backup):
                # Clear existing
                if exists(self.vcard_path):
                    shutil.rmtree(self.vcard_path)
                # Restore from backup
                shutil.copytree(vcard_backup, self.vcard_path)

            return True

        except Exception as e:
            print("[Converter] Restore error: {0}".format(str(e)))
            return False


def auto_convert_database(plugin_path, language, target_format="vcard"):
    """
    Auto-convert database based on configuration

    Args:
        plugin_path: Plugin installation path
        language: Current language
        target_format: Target format ("vcard" or "legacy")
    """
    converter = Converter(plugin_path, language)

    if target_format == "vcard":
        # Check if conversion is needed
        if converter.has_legacy_files() and not converter.has_vcard_files():
            print("[AutoConvert] Converting database to vCard format")

            # Create backup
            backup_path = converter.backup_database()
            if backup_path:
                print("[AutoConvert] Backup created: {0}".format(backup_path))

            # Convert
            converter.convert_legacy_to_vcard()
            return True

    elif target_format == "legacy":
        # Check if conversion is needed
        if converter.has_vcard_files() and not converter.has_legacy_files():
            print("[AutoConvert] Converting database to legacy format")

            # Create backup
            backup_path = converter.backup_database()
            if backup_path:
                print("[AutoConvert] Backup created: {0}".format(backup_path))

            # Convert
            converter.convert_vcard_to_legacy()
            return True

    return False


def check_database_consistency(plugin_path, language):
    """
    Check database consistency between formats

    Args:
        plugin_path: Plugin installation path
        language: Current language

    Returns:
        Dictionary with consistency information
    """
    converter = Converter(plugin_path, language)

    legacy_files = set()
    vcard_files = set()

    # Get legacy files
    if exists(converter.legacy_path):
        for f in listdir(converter.legacy_path):
            if f.endswith(".txt") and len(f) == 12:
                legacy_files.add(f)

    # Get vcard files
    if exists(converter.vcard_path):
        for f in listdir(converter.vcard_path):
            if f.endswith(".txt") and len(f) == 12:
                vcard_files.add(f)

    # Find differences
    only_in_legacy = legacy_files - vcard_files
    only_in_vcard = vcard_files - legacy_files
    in_both = legacy_files & vcard_files

    return {
        'legacy_count': len(legacy_files),
        'vcard_count': len(vcard_files),
        'only_in_legacy': list(only_in_legacy),
        'only_in_vcard': list(only_in_vcard),
        'in_both': len(in_both),
        'consistent': len(only_in_legacy) == 0 and len(only_in_vcard) == 0
    }
