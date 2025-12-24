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
from datetime import datetime
from enigma import eTimer, getDesktop
from re import split, IGNORECASE, search
from os.path import basename, exists, getsize, join, getmtime
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Components.Label import Label
from Components.FileList import FileList
from Components.ActionMap import ActionMap
from Components.ProgressBar import ProgressBar

from . import _


class VCardImporter(Screen):
    if (getDesktop(0).size().width() >= 1920):
        skin = """
            <screen name="VCardImporter" position="center,center" size="1200,800" title="Import vCard" flags="wfNoBorder">
                <widget name="filelist" position="10,20" size="1170,600" itemHeight="30" font="Regular;24" scrollbarMode="showNever" />
                <widget name="status" position="12,641" size="1170,64" font="Regular;24" />
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="50,768" size="230,10" alphatest="blend" />
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_green.png" position="364,769" size="230,10" alphatest="blend" />
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_yellow.png" position="666,770" size="230,10" alphatest="blend" />
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_blue.png" position="944,770" size="230,10" alphatest="blend" />
                <widget name="key_red" position="50,725" size="230,40" font="Regular;28" halign="center" valign="center" />
                <widget name="key_green" position="365,725" size="230,40" font="Regular;28" halign="center" valign="center" />
                <widget name="key_yellow" position="665,725" size="230,40" font="Regular;28" halign="center" valign="center" />
                <widget name="key_blue" position="944,725" size="230,40" font="Regular;28" halign="center" valign="center" />
            </screen>
            """
    else:
        skin = """
            <screen name="VCardImporter" position="center,center" size="850,600" title="Import vCard" flags="wfNoBorder">
                <widget name="filelist" position="10,10" size="818,450" itemHeight="30" font="Regular;24" scrollbarMode="showNever" />
                <widget name="status" position="12,471" size="818,64" font="Regular;24" />
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="35,571" size="150,10" alphatest="blend" />
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_green.png" position="213,572" size="150,10" alphatest="blend" />
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_yellow.png" position="398,572" size="150,10" alphatest="blend" />
                <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_blue.png" position="591,572" size="150,10" alphatest="blend" />
                <widget name="key_red" position="35,545" size="150,25" font="Regular;20" halign="center" valign="center" />
                <widget name="key_green" position="215,545" size="150,25" font="Regular;20" halign="center" valign="center" />
                <widget name="key_yellow" position="400,545" size="150,25" font="Regular;20" halign="center" valign="center" />
                <widget name="key_blue" position="595,545" size="150,25" font="Regular;20" halign="center" valign="center" />
            </screen>
            """

    def __init__(self, session, birthday_manager):
        Screen.__init__(self, session)
        self.birthday_manager = birthday_manager
        print("[VCardImporter] Initializing...")

        # Start in /tmp directory
        start_path = "/tmp"
        if not exists(start_path):
            start_path = "/"

        print("[VCardImporter] Start path: {0}".format(start_path))

        matching_pattern = r".*\.(vcf|vcard)$"
        self["filelist"] = FileList(start_path, matchingPattern=matching_pattern)
        self["status"] = Label(_("Select vCard file to import"))
        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label(_("Import"))
        self["key_yellow"] = Label(_("View"))
        self["key_blue"] = Label(_("Refresh"))
        self["actions"] = ActionMap(
            ["CalendarActions"],
            {
                "red": self.cancel,
                "green": self.do_import,
                "yellow": self.view_file_info,
                "blue": self.refresh,
                "cancel": self.cancel,
                "ok": self.ok,
            }, -1
        )

        print("[VCardImporter] Initialization complete")

    def ok(self):
        """OK - select file"""
        selection = self["filelist"].getSelection()
        if selection and not selection[1]:  # selection[1] = True if directory
            filename = selection[0]
            self["status"].setText(_("Selected: {0}").format(filename))
            self.do_import()

    def refresh(self):
        """Refresh file list"""
        self["filelist"].refresh()
        self["status"].setText(_("Refreshed"))

    def view_file_info(self):
        """Show file information - VERSIONE VELOCE"""
        selection = self["filelist"].getSelection()
        if not selection or selection[1]:
            return

        filename = selection[0]
        current_dir = self["filelist"].getCurrentDirectory()
        filepath = join(current_dir, filename)

        if not exists(filepath):
            return

        try:
            size = getsize(filepath)
            size_kb = size / 1024
            size_mb = size_kb / 1024

            # File info only, no contact counting
            from time import ctime
            modified_time = ctime(getmtime(filepath))

            info = [
                _("File: {0}").format(filename),
                _("Size: {0:.1f} MB").format(size_mb),
                _("Modified: {0}").format(modified_time),
                "",
                _("Press GREEN to import")
            ]

            self.session.open(
                MessageBox,
                "\n".join(info),
                MessageBox.TYPE_INFO
            )

        except Exception as e:
            print("[VCardImporter] Error reading file info: {0}".format(str(e)))
            self.session.open(
                MessageBox,
                _("Error reading file:\n{0}").format(str(e)),
                MessageBox.TYPE_ERROR
            )

    def count_contacts_in_file(self, filepath):
        """Count contacts in vCard file using single method"""
        contact_count = 0
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                # Read file in chunks for efficiency
                chunk_size = 1024 * 1024  # 1MB chunks
                buffer = ''

                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break

                    buffer += chunk

                    # Count BEGIN:VCARD occurrences in buffer
                    while 'BEGIN:VCARD' in buffer.upper():
                        contact_count += 1
                        # Find position and remove counted part
                        pos = buffer.upper().find('BEGIN:VCARD')
                        # Move past this BEGIN:VCARD
                        buffer = buffer[pos + len('BEGIN:VCARD'):]

                # Count any remaining in final buffer
                contact_count += buffer.upper().count('BEGIN:VCARD')

            print("[VCardImporter] Counted {0} contacts in {1}".format(contact_count, filepath))
            return contact_count

        except Exception as e:
            print("[VCardImporter] Error counting contacts: {0}".format(e))
            # Fallback: quick count from file start
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(1000000)  # Read first 1MB
                    return max(content.count('BEGIN:VCARD'),
                               content.count('BEGIN:VCARD\r\n'),
                               content.count('BEGIN:VCARD\n'))
            except:
                return 0

    def do_import(self):
        """Import selected file - senza conteggio prima"""
        print("[VCardImporter] do_import() called - versione veloce")

        selection = self["filelist"].getSelection()
        if not selection:
            self["status"].setText(_("No file selected"))
            return

        if selection[1]:  # It's a directory
            self["status"].setText(_("Select a file, not a folder"))
            return

        filename = selection[0]
        current_dir = self["filelist"].getCurrentDirectory()
        filepath = join(current_dir, filename)

        print("[VCardImporter] Selected file: {0}".format(filename))

        if not exists(filepath):
            self.session.open(
                MessageBox,
                _("File not found:\n{0}").format(filepath),
                MessageBox.TYPE_ERROR
            )
            return

        # Quick check if file is valid vCard (solo primi 1KB)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                first_chunk = f.read(1024)
                if 'BEGIN:VCARD' not in first_chunk.upper():
                    self.session.open(
                        MessageBox,
                        _("File does not contain vCard data\n{0}").format(filename),
                        MessageBox.TYPE_WARNING
                    )
                    return
        except Exception as e:
            print("[VCardImporter] Error checking file: {0}".format(e))
            self.session.open(
                MessageBox,
                _("Error reading file:\n{0}").format(str(e)),
                MessageBox.TYPE_ERROR
            )
            return

        # Conferma import SENZA conteggio
        self.session.openWithCallback(
            lambda result: self.start_import_process(result, filepath) if result else None,
            MessageBox,
            _("Import contacts from:\n{0}?").format(filename),
            MessageBox.TYPE_YESNO
        )

    def start_import_process(self, result, filepath):
        """Start the actual import process"""
        if not result:
            return

        print("[VCardImporter] Starting import of: {0}".format(filepath))
        try:
            # Open import progress screen
            self.session.openWithCallback(
                self.import_completed,
                ImportProgressScreen,
                self.birthday_manager,
                filepath
            )
            print("[VCardImporter] ImportProgressScreen opened successfully")
        except Exception as e:
            print("[VCardImporter] ERROR opening ImportProgressScreen: {0}".format(e))
            import traceback
            traceback.print_exc()
            # Fallback: import directly
            self.import_directly(filepath)

    def import_directly(self, filepath):
        """Direct import without progress screen (fallback)"""
        try:
            # Use the unified file importer
            imported, skipped, errors = VCardFileImporter.import_file_sync(
                self.birthday_manager,
                filepath
            )

            message = [
                _("Import completed!"),
                _("Imported: {0} contacts").format(imported),
                _("Skipped: {0} (duplicates)").format(skipped),
                _("Errors: {0}").format(errors)
            ]

            self.session.open(
                MessageBox,
                "\n".join(message),
                MessageBox.TYPE_INFO
            )

            self.import_completed(True)

        except Exception as e:
            print("[VCardImporter] Direct import error: {0}".format(e))
            self.session.open(
                MessageBox,
                _("Import error: {0}").format(str(e)),
                MessageBox.TYPE_ERROR
            )

    def import_completed(self, result):
        """Callback after import completion"""
        if result:
            self["status"].setText(_("Import completed - Sorting contacts..."))

            # Sort contacts after import
            try:
                self.birthday_manager.sort_contacts_by_name()
            except Exception as e:
                print("[VCardImporter] Error sorting contacts: {0}".format(e))

            # Refresh file list
            self["filelist"].refresh()

    def cancel(self):
        """Cancel and close"""
        self.close()


class VCardFileImporterThread:
    """Non-threaded importer using timer"""

    def __init__(self, birthday_manager, filepath, callback):
        self.birthday_manager = birthday_manager
        self.filepath = filepath
        self.callback = callback
        self.cancelled = False
        self.imported = 0
        self.skipped = 0
        self.errors = 0
        self.current = 0
        self.total_blocks = 0
        self.vcard_blocks = []
        self.current_index = 0
        self.timer = eTimer()
        try:
            self.timer_conn = self.timer.timeout.connect(self.process_next_block)
        except AttributeError:
            self.timer.callback.append(self.process_next_block)

    def start(self):
        """Start import process - legge tutto il file una volta sola"""
        print("[VCardImporterThread] Starting import")

        try:
            # Read the entire file into memory
            with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Split by VCARD blocks
            self.vcard_blocks = split(r'BEGIN:VCARD\s*', content, flags=IGNORECASE)

            # Count total blocks
            self.total_blocks = len([b for b in self.vcard_blocks
                                    if b.strip() and 'END:VCARD' in b.upper()])

            print("[VCardImporterThread] Total blocks: {0}".format(self.total_blocks))

            if self.total_blocks == 0:
                self.callback(1.0, 0, 0, 0, 0, 0, True)
                return False

            # Start processing
            self.timer.start(10, True)
            return True

        except Exception as e:
            print("[VCardImporterThread] Error starting import: {0}".format(e))
            self.callback(1.0, 0, 0, 0, 0, 0, True)
            return False

    def process_next_block(self):
        """Process one contact block"""
        if self.cancelled:
            self.callback(1.0, self.current, self.total_blocks,
                          self.imported, self.skipped, self.errors, True)
            return

        # Skip empty blocks until you find a valid one
        while self.current_index < len(self.vcard_blocks):
            block = self.vcard_blocks[self.current_index]
            self.current_index += 1

            if not block.strip() or 'END:VCARD' not in block.upper():
                continue

            self.current += 1

            try:
                # Process the block
                contact_data = VCardFileImporter.parse_vcard_block(block)

                if not contact_data:
                    self.errors += 1
                elif VCardFileImporter.contact_exists(self.birthday_manager, contact_data):
                    self.skipped += 1
                else:
                    contact_id = self.birthday_manager.save_contact(contact_data)
                    if contact_id:
                        self.imported += 1
                    else:
                        self.errors += 1

                break  # Exit the while loop after processing a block

            except Exception as e:
                print("[VCardImporterThread] Error processing block: {0}".format(e))
                self.errors += 1
                break

        # Update progress
        progress = float(self.current) / self.total_blocks if self.total_blocks > 0 else 0
        self.callback(progress, self.current, self.total_blocks,
                      self.imported, self.skipped, self.errors, False)

        # If there are still blocks, continue
        if not self.cancelled and self.current < self.total_blocks:
            self.timer.start(10, True)
        else:
            # Import done
            self.callback(1.0, self.current, self.total_blocks,
                          self.imported, self.skipped, self.errors, True)


class VCardFileImporter:
    """Main vCard file importer - unified class with static methods"""

    @staticmethod
    def count_contacts(filepath):
        """Count contacts in vCard file"""
        contact_count = 0
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                # Read file in chunks for efficiency
                chunk_size = 1024 * 1024  # 1MB chunks
                buffer = ''

                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break

                    buffer += chunk

                    # Count BEGIN:VCARD occurrences in buffer
                    while 'BEGIN:VCARD' in buffer.upper():
                        contact_count += 1
                        # Find position and remove counted part
                        pos = buffer.upper().find('BEGIN:VCARD')
                        # Move past this BEGIN:VCARD
                        buffer = buffer[pos + len('BEGIN:VCARD'):]

                # Count any remaining in final buffer
                contact_count += buffer.upper().count('BEGIN:VCARD')

            print("[VCardFileImporter] Counted {0} contacts in {1}".format(contact_count, filepath))
            return contact_count

        except Exception as e:
            print("[VCardFileImporter] Error counting contacts: {0}".format(e))
            # Fallback: quick count from file start
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(1000000)  # Read first 1MB
                    return max(content.count('BEGIN:VCARD'),
                               content.count('BEGIN:VCARD\r\n'),
                               content.count('BEGIN:VCARD\n'))
            except:
                return 0

    @staticmethod
    def import_file_sync(birthday_manager, filepath, progress_callback=None):
        """
        Import contacts from vCard file synchronously

        Returns:
            Tuple (imported_count, skipped_count, error_count)
        """
        print("[VCardFileImporter] Starting import from: {0}".format(filepath))

        if not exists(filepath):
            print("[VCardFileImporter] ERROR: File not found")
            return 0, 0, 1

        imported = 0
        skipped = 0
        errors = 0

        try:
            # Count total contacts
            total = VCardFileImporter.count_contacts(filepath)
            print("[VCardFileImporter] Total contacts found: {0}".format(total))

            if total == 0:
                print("[VCardFileImporter] No contacts found in file")
                if progress_callback:
                    progress_callback(1.0, 0, 0, 0, 0, 0)
                return 0, 0, 0

            # Read file content
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Split by VCARD blocks
            vcard_blocks = split(r'BEGIN:VCARD\s*', content, flags=IGNORECASE)
            print("[VCardFileImporter] Found {0} blocks".format(len(vcard_blocks)))

            current = 0
            for block in vcard_blocks:
                if not block.strip() or 'END:VCARD' not in block.upper():
                    continue

                current += 1

                # Update progress
                if progress_callback:
                    progress = float(current) / total if total > 0 else 0
                    if not progress_callback(progress, current, total, imported, skipped, errors):
                        print("[VCardFileImporter] Import cancelled by user")
                        break

                try:
                    # Parse vCard block
                    contact_data = VCardFileImporter.parse_vcard_block(block)

                    if not contact_data:
                        errors += 1
                        continue

                    # Check if contact already exists
                    if VCardFileImporter.contact_exists(birthday_manager, contact_data):
                        skipped += 1
                        continue

                    # Save contact
                    contact_id = birthday_manager.save_contact(contact_data)
                    if contact_id:
                        imported += 1
                    else:
                        errors += 1

                except Exception as e:
                    print("[VCardFileImporter] ERROR importing contact #{0}: {1}".format(current, str(e)))
                    errors += 1

            print("[VCardFileImporter] Import completed. Result: imported={0}, skipped={1}, errors={2}".format(
                imported, skipped, errors))
            return imported, skipped, errors

        except Exception as e:
            print("[VCardFileImporter] ERROR: File import failed: {0}".format(str(e)))
            import traceback
            traceback.print_exc()
            return 0, 0, 1

    @staticmethod
    def parse_vcard_block(block):
        """Parse single vCard block into contact data"""
        contact = {
            'FN': '',           # Formatted Name
            'BDAY': '',         # Birthday
            'TEL': '',          # Telephone
            'EMAIL': '',        # Email
            'ADR': '',          # Address
            'ORG': '',          # Organization
            'TITLE': '',        # Title
            'CATEGORIES': '',   # Categories/Tags
            'NOTE': '',         # Notes
            'URL': '',          # Website
        }

        lines = block.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.upper() == 'END:VCARD':
                break

            # Handle multi-line values
            if line.startswith(' ') or line.startswith('\t'):
                continue

            # Skip lines without colon
            if ':' not in line:
                continue

            try:
                parts = line.split(':', 1)
                if len(parts) < 2:
                    continue

                prop_full = parts[0].strip()
                value = parts[1].strip()
                prop_base = prop_full.split(';')[0].upper()

                if prop_base == 'FN':
                    contact['FN'] = value
                elif prop_base == 'N':
                    # Structured Name: Last;First;Middle;Prefix;Suffix
                    name_parts = value.split(';')
                    if len(name_parts) >= 2:
                        last_name = name_parts[0] if name_parts[0] else ''
                        first_name = name_parts[1] if name_parts[1] else ''
                        if first_name and last_name:
                            contact['FN'] = first_name + " " + last_name
                        elif first_name:
                            contact['FN'] = first_name
                        elif last_name:
                            contact['FN'] = last_name
                elif prop_base == 'TEL':
                    # Clean phone number
                    clean_tel = ''.join(c for c in value if c.isdigit() or c == '+')
                    if clean_tel:
                        if contact['TEL']:
                            contact['TEL'] += " | " + clean_tel
                        else:
                            contact['TEL'] = clean_tel
                elif prop_base == 'EMAIL':
                    if value and '@' in value:
                        if contact['EMAIL']:
                            contact['EMAIL'] += " | " + value
                        else:
                            contact['EMAIL'] = value
                elif prop_base == 'ORG':
                    if value and value != ';':
                        contact['ORG'] = value
                elif prop_base == 'TITLE':
                    if value:
                        contact['TITLE'] = value
                elif prop_base == 'CATEGORIES':
                    if value:
                        cats = value.split(',')
                        clean_cats = [c.strip() for c in cats if c.strip()]
                        if clean_cats:
                            contact['CATEGORIES'] = ', '.join(clean_cats)
                elif prop_base == 'NOTE':
                    if value:
                        contact['NOTE'] = value
                elif prop_base == 'URL':
                    if value and ('http://' in value.lower() or 'https://' in value.lower()):
                        contact['URL'] = value
                elif prop_base == 'BDAY':
                    bday = VCardFileImporter.parse_birthday(value)
                    if bday:
                        contact['BDAY'] = bday

            except Exception:
                continue

        return contact if contact['FN'] else None

    @staticmethod
    def parse_birthday(value):
        """Parse birthday in various formats"""
        if not value:
            return ''

        # Remove time part if present
        value = value.split('T')[0].split(' ')[0]

        # Try different date formats
        formats = [
            '%Y%m%d',        # 19900515
            '%Y-%m-%d',      # 1990-05-15
            '%d-%m-%Y',      # 15-05-1990
            '%d/%m/%Y',      # 15/05/1990
            '%m/%d/%Y',      # 05/15/1990
            '%d.%m.%Y',      # 15.05.1990
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(value, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue

        # If still not parsed, try to extract year-month-day patterns
        year_match = search(r'(\d{4})[/\-\.](\d{1,2})[/\-\.](\d{1,2})', value)
        if year_match:
            try:
                year = int(year_match.group(1))
                month = int(year_match.group(2))
                day = int(year_match.group(3))
                return "{0:04d}-{1:02d}-{2:02d}".format(year, month, day)
            except:
                pass

        return ''

    @staticmethod
    def contact_exists(birthday_manager, contact_data):
        """Check if contact already exists"""
        name = contact_data.get('FN', '').strip()
        bday = contact_data.get('BDAY', '').strip()

        if not name:
            return False

        # Search in existing contacts
        for contact in birthday_manager.contacts:
            existing_name = contact.get('FN', '').strip()
            existing_bday = contact.get('BDAY', '').strip()

            # Match by name (case-insensitive)
            if existing_name.lower() == name.lower():
                # If birthdays match or one is empty, it's a duplicate
                if not bday or not existing_bday or existing_bday == bday:
                    return True

        return False


class ImportProgressScreen(Screen):
    if (getDesktop(0).size().width() >= 1920):
        skin = """
        <screen name="ImportProgressScreen" position="10,10" size="1000,135" title="Importing vCard" flags="wfNoBorder">
            <widget name="title" position="10,10" size="981,40" font="Regular;32" halign="left" valign="center" />
            <widget name="filename" position="10,50" size="700,30" font="Regular;24" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="progress" position="10,80" size="700,20" />
            <widget name="status" position="10,100" size="700,30" font="Regular;24" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="details" position="713,52" size="280,80" font="Regular;24" foregroundColor="#00ffcc33" backgroundColor="background" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="746,40" size="150,10" alphatest="blend" />
            <widget name="key_red" position="746,12" size="150,25" font="Regular;20" halign="center" valign="center" />
        </screen>
        """
    else:
        skin = """
        <screen name="ImportProgressScreen" position="560,10" size="800,300" title="Importing vCard" flags="wfNoBorder">
            <widget name="title" position="10,10" size="780,40" font="Regular;32" halign="center" valign="center" />
            <widget name="filename" position="10,60" size="780,30" font="Regular;24" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="progress" position="10,95" size="780,20" />
            <widget name="status" position="10,120" size="780,30" font="Regular;24" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="details" position="10,155" size="780,72" font="Regular;24" foregroundColor="#00ffcc33" backgroundColor="background" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="35,261" size="150,10" alphatest="blend" />
            <widget name="key_red" position="35,235" size="150,25" font="Regular;20" halign="center" valign="center" />
        </screen>
        """

    def __init__(self, session, birthday_manager, filepath):
        Screen.__init__(self, session)
        self.birthday_manager = birthday_manager
        self.filepath = filepath
        self.import_thread = None
        self.last_update = time.time()
        self["title"] = Label(_("Importing vCard File"))
        self["filename"] = Label(basename(filepath))
        self["progress"] = ProgressBar()
        self["status"] = Label(_("Initializing..."))
        self["details"] = Label("")
        self["key_red"] = Label(_("Cancel"))

        self["actions"] = ActionMap(
            ["ColorActions"],
            {
                "red": self.cancel_import,
            }, -1
        )

        # Start import thread after screen is shown
        self.onShown.append(self.start_import)

    def start_import(self):
        """Start import process"""
        print("[ImportProgress] Starting import process")

        def progress_callback(progress, current, total, imported, skipped, errors, finished):
            """Callback for progress updates"""
            # Update progress bar
            self["progress"].setValue(int(progress * 100))

            # Update status text
            status_parts = []
            if current > 0:
                status_parts.append(_("{0}").format(current))
            if imported > 0:
                status_parts.append(_("I:{0}").format(imported))
            if skipped > 0:
                status_parts.append(_("S:{0}").format(skipped))
            if errors > 0:
                status_parts.append(_("E:{0}").format(errors))

            if status_parts:
                self["status"].setText(" | ".join(status_parts))

            # Update details
            details = []
            if total > 0:
                details.append(_("Progress: {0}%").format(int(progress * 100)))
            if imported > 0:
                details.append(_("Imported: {0}").format(imported))

            if details:
                self["details"].setText("\n".join(details))

            # If finished, show completion message
            if finished:
                self.import_completed(imported, skipped, errors)

        # Create and start importer
        self.importer = VCardFileImporterThread(
            self.birthday_manager,
            self.filepath,
            progress_callback
        )

        if not self.importer.start():
            self.session.open(
                MessageBox,
                _("Failed to start import"),
                MessageBox.TYPE_ERROR
            )
            self.close(False)

    def import_completed(self, imported, skipped, errors):
        """Import completed"""
        print("[ImportProgress] Import completed: imported={0}, skipped={1}, errors={2}".format(
            imported, skipped, errors))

        # Update final status
        self["progress"].setValue(100)
        self["status"].setText(_("Completed"))

        # Show result message after short delay
        timer = eTimer()

        def show_result():
            message = [
                _("Import completed!"),
                _("Imported: {0}").format(imported),
                _("Skipped: {0}").format(skipped),
                _("Errors: {0}").format(errors),
                _("Total: {0}").format(imported + skipped + errors)
            ]

            self.session.openWithCallback(
                lambda x: self.close(True),
                MessageBox,
                "\n".join(message),
                MessageBox.TYPE_INFO,
                timeout=3
            )

        try:
            timer_conn = timer.timeout.connect(show_result)
        except AttributeError:
            timer.callback.append(show_result)
        timer.start(300, True)  # 300ms delay

    def cancel_import(self):
        """Cancel import"""
        if self.import_thread and self.import_thread.is_alive():
            self.import_thread.cancelled = True
            self["status"].setText(_("Cancelling..."))
            self["details"].setText(_("Waiting for thread to stop..."))

            # Wait for thread to finish
            def check_thread():
                if not self.import_thread.is_alive():
                    self.close(False)
                else:
                    # Create timer for next check
                    self.check_timer = eTimer()
                    try:
                        self.check_timer_conn = self.check_timer.timeout.connect(check_thread)
                    except AttributeError:
                        self.check_timer.callback.append(check_thread)
                    self.check_timer.start(500, True)

            # Start the checking timer
            self.check_timer = eTimer()
            try:
                self.check_timer_conn = self.check_timer.timeout.connect(check_thread)
            except AttributeError:
                self.check_timer.callback.append(check_thread)
            self.check_timer.start(500, True)

        else:
            self.close(False)

    def close(self, result=None):
        """Close screen"""
        # Ensure thread is stopped
        if self.import_thread and self.import_thread.is_alive():
            self.import_thread.cancelled = True
            self.import_thread.join(1.0)  # Wait max 1 second

        Screen.close(self, result)


# Utility functions
def quick_import_vcard(birthday_manager, filepath):
    """
    Quick import function for CLI/testing
    """
    importer = VCardFileImporter(birthday_manager)
    return importer.import_file(filepath)


def export_contacts_to_vcard(birthday_manager, output_file):
    """
    Export all contacts to vCard file
    """
    contacts = birthday_manager.contacts

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# vCard export from Calendar Plugin\n")
        f.write("# Generated: {}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        f.write("# Total contacts: {}\n\n".format(len(contacts)))

        for contact in contacts:
            f.write("BEGIN:VCARD\n")
            f.write("VERSION:3.0\n")

            # Write fields
            for key, value in contact.items():
                if key in ['FN', 'BDAY', 'TEL', 'EMAIL', 'ADR',
                           'ORG', 'TITLE', 'CATEGORIES', 'NOTE', 'URL']:
                    if value:
                        f.write("{}:{}\n".format(key, value))

            f.write("END:VCARD\n\n")
