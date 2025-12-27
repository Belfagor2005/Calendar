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
• Phone and email formatters for Calendar Planner
• Maintains consistent formatting across import, display, and storage

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
from datetime import datetime
from enigma import eTimer, getDesktop
from re import split, IGNORECASE, search, sub
from os.path import basename, exists, getsize, join, getmtime
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Components.Label import Label
from Components.FileList import FileList
from Components.ActionMap import ActionMap
from Components.ProgressBar import ProgressBar

from . import _
from .formatters import parse_vcard_phone, parse_vcard_email, clean_field_storage


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
    def normalize_contact_data(contact_data):
        """Normalize contact data for comparison"""
        normalized = {}

        # Name: lowercase, strip extra spaces
        name = contact_data.get('FN', '').strip()
        normalized['FN'] = ' '.join(name.split()).lower() if name else ''

        # Birthday: standardize format
        bday = contact_data.get('BDAY', '').strip()
        normalized['BDAY'] = VCardFileImporter.parse_birthday(bday) if bday else ''

        # Phone: keep only digits and +
        phone = contact_data.get('TEL', '').strip()
        if phone:
            # Take only first phone if multiple
            phones = phone.split('|')
            first_phone = phones[0].strip() if phones else ''
            normalized['TEL'] = ''.join(c for c in first_phone if c.isdigit() or c == '+')
        else:
            normalized['TEL'] = ''

        # Email: lowercase
        email = contact_data.get('EMAIL', '').strip()
        if email:
            # Take only first email if multiple
            emails = email.split('|')
            first_email = emails[0].strip() if emails else ''
            normalized['EMAIL'] = first_email.lower()
        else:
            normalized['EMAIL'] = ''

        return normalized

    @staticmethod
    def contact_exists(birthday_manager, contact_data):
        """Check if contact already exists - OPTIMIZED VERSION"""
        # Normalize new contact
        new_norm = VCardFileImporter.normalize_contact_data(contact_data)

        if not new_norm['FN']:
            return False

        # Pre-calculate normalized existing contacts ONCE
        if not hasattr(birthday_manager, '_normalized_contacts_cache'):
            birthday_manager._normalized_contacts_cache = []
            for contact in birthday_manager.contacts:
                birthday_manager._normalized_contacts_cache.append(
                    VCardFileImporter.normalize_contact_data(contact)
                )

        # Search in cache
        for existing_norm in birthday_manager._normalized_contacts_cache:
            if new_norm['FN'] == existing_norm['FN']:
                # Names match, check other fields
                if new_norm['BDAY'] and existing_norm['BDAY'] and \
                   new_norm['BDAY'] == existing_norm['BDAY']:
                    return True

                if new_norm['TEL'] and existing_norm['TEL'] and \
                   new_norm['TEL'] == existing_norm['TEL']:
                    return True

                if new_norm['EMAIL'] and existing_norm['EMAIL'] and \
                   new_norm['EMAIL'] == existing_norm['EMAIL']:
                    return True

                # If names match but no other info, assume duplicate
                if not new_norm['BDAY'] and not new_norm['TEL'] and not new_norm['EMAIL']:
                    return True

        return False

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
        """Import contacts from vCard file synchronously"""
        print("[VCardFileImporter] Starting import from: {0}".format(filepath))

        if not exists(filepath):
            print("[VCardFileImporter] ERROR: File not found")
            return 0, 0, 1

        imported = 0
        updated = 0  # NEW: track updates
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
                    if not progress_callback(progress, current, total, imported, updated, skipped, errors):
                        print("[VCardFileImporter] Import cancelled by user")
                        break

                try:
                    # Parse vCard block
                    contact_data = VCardFileImporter.parse_vcard_block(block)

                    if not contact_data:
                        errors += 1
                        continue

                    # NEW LOGIC: Try to update existing contact first
                    updated_id = VCardFileImporter.update_existing_contact(birthday_manager, contact_data)

                    if updated_id:
                        updated += 1
                        print("[VCardFileImporter] Updated contact: {0}".format(
                            contact_data.get('FN', 'Unknown')))
                        continue

                    # Check if exact duplicate (should update instead of skip)
                    if VCardFileImporter.contact_exists(birthday_manager, contact_data):
                        skipped += 1
                        print("[VCardFileImporter] Skipped duplicate: {0}".format(
                            contact_data.get('FN', 'Unknown')))
                        continue

                    # Save new contact
                    contact_id = birthday_manager.save_contact(contact_data)
                    if contact_id:
                        imported += 1
                        print("[VCardFileImporter] Imported new contact: {0}".format(
                            contact_data.get('FN', 'Unknown')))
                    else:
                        errors += 1

                except Exception as e:
                    print("[VCardFileImporter] ERROR importing contact #{0}: {1}".format(current, str(e)))
                    errors += 1

            print("[VCardFileImporter] Import completed. Result: imported={0}, updated={1}, skipped={2}, errors={3}".format(
                imported, updated, skipped, errors))
            return imported, updated, skipped, errors

        except Exception as e:
            print("[VCardFileImporter] ERROR: File import failed: {0}".format(str(e)))
            import traceback
            traceback.print_exc()
            return 0, 0, 0, 1

    @staticmethod
    def parse_vcard_block(block):
        """Parse a single vCard block into contact data – FIX spacing issue"""
        contact = {
            'FN': '',           # Formatted Name
            'BDAY': '',         # Birthday
            'TEL': '',          # Telephone – will be cleaned
            'EMAIL': '',        # Email
            'ADR': '',          # Address
            'ORG': '',          # Organization
            'TITLE': '',        # Title
            'CATEGORIES': '',   # Categories / Tags
            'NOTE': '',         # Notes
            'URL': '',          # Website
        }

        lines = block.split('\n')
        phones = []      # Store multiple phone numbers
        emails = []      # Store multiple email addresses

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.upper() == 'END:VCARD':
                break

            # Skip continuation lines
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
                    # Structured Name
                    name_parts = value.split(';')
                    if len(name_parts) >= 2:
                        last_name = name_parts[0] if name_parts[0] else ''
                        first_name = name_parts[1] if name_parts[1] else ''
                        if not contact['FN']:
                            if first_name and last_name:
                                contact['FN'] = first_name + " " + last_name
                            elif first_name:
                                contact['FN'] = first_name
                            elif last_name:
                                contact['FN'] = last_name

                elif prop_base == 'TEL':
                    # Use specialized vCard parser
                    clean_tel = parse_vcard_phone(value)
                    if clean_tel:
                        phones.append(clean_tel)

                elif prop_base == 'EMAIL':
                    if value and '@' in value:
                        clean_email = parse_vcard_email(value)
                        emails.append(clean_email)

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

            except Exception as e:
                print("[VCardImporter] Error parsing line: {0} - {1}".format(
                    line[:50] if line else "empty", str(e)))
                continue

        # Format numbers using "|" as separator (NO spaces) for storage
        if phones:
            contact['TEL'] = '|'.join(phones)

        if emails:
            contact['EMAIL'] = '|'.join(emails)

        # Apply Google Contacts–specific fixes
        contact = VCardFileImporter.fix_google_contacts(contact)

        return contact if contact['FN'] else None

    @staticmethod
    def fix_google_contacts(contact):
        """Apply fixes for Google Contacts specific issues"""
        if not contact:
            return contact

        # 1. Fix NOTE field - remove "File As:" references
        if 'NOTE' in contact and contact['NOTE']:
            note = contact['NOTE']

            # Remove "File As\:" or "File As:" patterns
            note = sub(r'File As[\\:]?\s*', '', note)

            # Remove trailing/leading whitespace
            note = note.strip()

            # If note is now empty or just contains the name, clear it
            if not note or note == contact.get('FN', ''):
                contact['NOTE'] = ''
            else:
                contact['NOTE'] = note

        # 2. Fix ORGANIZATION field
        if 'ORG' in contact and contact['ORG']:
            org = contact['ORG'].strip()
            # Remove single semicolons or commas
            if org in [';', ',', ';;', ',,', ';,', ',;']:
                contact['ORG'] = ''
            else:
                contact['ORG'] = org

        # 3. Clean up CATEGORIES field
        if 'CATEGORIES' in contact and contact['CATEGORIES']:
            categories = contact['CATEGORIES'].strip()
            # Remove empty categories
            cats = [c.strip() for c in categories.split(',') if c.strip()]
            if cats:
                contact['CATEGORIES'] = ', '.join(cats)
            else:
                contact['CATEGORIES'] = ''

        # 4. Clean up NAME field
        if 'FN' in contact and contact['FN']:
            name = contact['FN'].strip()
            # Remove extra spaces
            name = ' '.join(name.split())
            contact['FN'] = name

        # 5. Clean up BIRTHDAY field
        if 'BDAY' in contact and contact['BDAY']:
            bday = contact['BDAY'].strip()
            # Ensure proper format
            try:
                datetime.strptime(bday, "%Y-%m-%d")
                contact['BDAY'] = bday
            except ValueError:
                # Try to fix if not in correct format
                fixed = VCardFileImporter.parse_birthday(bday)
                if fixed:
                    contact['BDAY'] = fixed
                else:
                    contact['BDAY'] = ''

        # 6. Clean emails
        if 'TEL' in contact and contact['TEL']:
            contact['TEL'] = clean_field_storage(contact['TEL'])

        # 7. Clean emails
        if 'EMAIL' in contact and contact['EMAIL']:
            contact['EMAIL'] = clean_field_storage(contact['EMAIL'])

        return contact

    @staticmethod
    def parse_birthday(value):
        """Parse birthday in various formats - ENHANCED for Google Contacts"""
        if not value:
            return ''

        # Remove time part if present (Google doesn't use time in BDAY)
        value = value.split('T')[0].split(' ')[0].strip()

        # Try Google's preferred format first: YYYYMMDD
        try:
            # Check if it's 8 digits (YYYYMMDD)
            if len(value) == 8 and value.isdigit():
                year = int(value[0:4])
                month = int(value[4:6])
                day = int(value[6:8])

                # Validate date
                if 1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31:
                    return "{0:04d}-{1:02d}-{2:02d}".format(year, month, day)
        except:
            pass

        # Try other common formats
        formats = [
            '%Y%m%d',        # 19900515 (Google)
            '%Y-%m-%d',      # 1990-05-15 (standard)
            '%d-%m-%Y',      # 15-05-1990 (european)
            '%d/%m/%Y',      # 15/05/1990
            '%m/%d/%Y',      # 05/15/1990 (US)
            '%d.%m.%Y',      # 15.05.1990
            '%Y/%m/%d',      # 1990/05/15
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(value, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue

        # Try regex extraction
        # Pattern for YYYYMMDD without separators
        match = search(r'(\d{4})(\d{2})(\d{2})', value)
        if match:
            try:
                year = int(match.group(1))
                month = int(match.group(2))
                day = int(match.group(3))
                if 1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31:
                    return "{0:04d}-{1:02d}-{2:02d}".format(year, month, day)
            except:
                pass

        # Pattern with separators
        patterns = [
            r'(\d{4})[/\-\.](\d{1,2})[/\-\.](\d{1,2})',  # YYYY-MM-DD
            r'(\d{1,2})[/\-\.](\d{1,2})[/\-\.](\d{4})',  # DD-MM-YYYY
        ]

        for pattern in patterns:
            match = search(pattern, value)
            if match:
                try:
                    groups = match.groups()
                    if len(groups) == 3:
                        # Try to determine format by year position
                        if len(groups[0]) == 4:  # YYYY-MM-DD
                            year = int(groups[0])
                            month = int(groups[1])
                            day = int(groups[2])
                        else:  # DD-MM-YYYY
                            day = int(groups[0])
                            month = int(groups[1])
                            year = int(groups[2])

                        if 1900 <= year <= 2100 and 1 <= month <= 12 and 1 <= day <= 31:
                            return "{0:04d}-{1:02d}-{2:02d}".format(year, month, day)
                except:
                    continue

        return ''  # Could not parse

    @staticmethod
    def is_same_person(contact1, contact2):
        """Determine if two contacts are the same person"""
        name1 = contact1.get('FN', '').strip().lower()
        name2 = contact2.get('FN', '').strip().lower()

        if not name1 or not name2:
            return False

        # 1. Exact name match
        if name1 == name2:
            # Check for strong identifiers
            bday1 = contact1.get('BDAY', '').strip()
            bday2 = contact2.get('BDAY', '').strip()
            phone1 = contact1.get('TEL', '').strip()
            phone2 = contact2.get('TEL', '').strip()
            email1 = contact1.get('EMAIL', '').strip()
            email2 = contact2.get('EMAIL', '').strip()

            # Strong match: same birthday
            if bday1 and bday2 and bday1 == bday2:
                return True

            # Strong match: same phone
            if phone1 and phone2 and phone1 == phone2:
                return True

            # Strong match: same email
            if email1 and email2 and email1 == email2:
                return True

            # Weak match: no conflicting info
            if (not bday1 or not bday2) and (not phone1 or not phone2) and (not email1 or not email2):
                # Names match but no other info to distinguish
                return True

        # 2. Similar name (e.g., "John Doe" vs "John A. Doe")
        # Could add fuzzy matching here if needed

        return False

    @staticmethod
    def update_existing_contact(birthday_manager, contact_data):
        """Update existing contact instead of skipping"""
        name = contact_data.get('FN', '').strip()

        if not name:
            return None

        for i, contact in enumerate(birthday_manager.contacts):
            # Use is_same_person for better matching
            if VCardFileImporter.is_same_person(contact, contact_data):
                # UPDATE LOGIC: Fill empty fields, don't overwrite existing data
                updated = False

                existing_bday = contact.get('BDAY', '').strip()
                new_bday = contact_data.get('BDAY', '').strip()
                existing_phone = contact.get('TEL', '').strip()
                new_phone = contact_data.get('TEL', '').strip()
                existing_email = contact.get('EMAIL', '').strip()
                new_email = contact_data.get('EMAIL', '').strip()

                # Update only empty fields
                if not existing_bday and new_bday:
                    contact['BDAY'] = new_bday
                    updated = True

                if not existing_phone and new_phone:
                    contact['TEL'] = new_phone
                    updated = True
                elif existing_phone and new_phone and existing_phone != new_phone:
                    # Add additional phone
                    phones = existing_phone.split('|')
                    if new_phone not in [p.strip() for p in phones]:
                        contact['TEL'] = existing_phone + " | " + new_phone
                        updated = True

                if not existing_email and new_email:
                    contact['EMAIL'] = new_email
                    updated = True
                elif existing_email and new_email and existing_email != new_email:
                    # Add additional email
                    emails = existing_email.split('|')
                    if new_email not in [e.strip() for e in emails]:
                        contact['EMAIL'] = existing_email + " | " + new_email
                        updated = True

                # Update other fields if empty
                for field in ['ADR', 'ORG', 'TITLE', 'CATEGORIES', 'NOTE', 'URL']:
                    existing = contact.get(field, '').strip()
                    new_val = contact_data.get(field, '').strip()
                    if not existing and new_val:
                        contact[field] = new_val
                        updated = True

                if updated:
                    # Save the updated contact
                    birthday_manager.save_contact(contact)
                    return contact['id']  # Return contact ID

        return None


class ImportProgressScreen(Screen):
    if (getDesktop(0).size().width() >= 1920):
        skin = """
        <screen name="ImportProgressScreen" position="10,10" size="1000,135" title="Importing vCard" flags="wfNoBorder">
            <widget name="title" position="10,10" size="981,40" font="Regular;32" halign="left" valign="center" />
            <widget name="filename" position="10,50" size="700,50" font="Regular;24" halign="center" valign="center" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="progress" position="10,100" size="700,30" />
            <widget name="status" position="712,100" size="284,30" font="Regular;24" halign="center" valign="center" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="details" position="713,50" size="280,50" font="Regular;24" halign="center" valign="center" foregroundColor="#00ffcc33" backgroundColor="background" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="771,35" size="150,10" alphatest="blend" />
            <widget name="key_red" position="771,7" size="150,25" font="Regular;20" halign="center" valign="center" />
        </screen>
        """
    else:
        skin = """
        <screen name="ImportProgressScreen" position="10,10" size="800,300" title="Importing vCard" flags="wfNoBorder">
            <widget name="title" position="10,10" size="780,40" font="Regular;32" halign="center" valign="center" />
            <widget name="filename" position="10,60" size="780,30" font="Regular;24" halign="center" valign="center" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="progress" position="10,95" size="780,20" />
            <widget name="status" position="10,120" size="780,30" font="Regular;24" halign="center" valign="center" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="details" position="10,155" size="780,72" font="Regular;24" halign="center" valign="center" foregroundColor="#00ffcc33" backgroundColor="background" />
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
            ["CalendarActions"],
            {
                "red": self.cancel_import,
                "cancel": self.on_exit_pressed,
            }, -1
        )

        # Start import thread after screen is shown
        self.onShown.append(self.start_import)

    def on_exit_pressed(self):
        """Exit button management"""
        if self["key_red"].getText() == _("Close"):
            self.close(True)
        else:
            self.close(False)

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

            if finished:
                self["key_red"].setText(_("Close"))
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

        # Clear normalization cache
        if hasattr(self.birthday_manager, '_normalized_contacts_cache'):
            del self.birthday_manager._normalized_contacts_cache

        # Update final status
        self["progress"].setValue(100)
        self["status"].setText(_("Completed"))

        # CHANGE RED BUTTON TO "CLOSE"
        self["key_red"].setText(_("Close"))

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
        """Cancel import - ora diventa Close alla fine"""
        # Se l'import è completato, chiudi semplicemente
        if self["key_red"].getText() == _("Close"):
            self.close(True)
            return

        # Altrimenti, è ancora in corso, quindi cancella
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
            self.import_thread.join(1.0)

        Screen.close(self, result)


# Utility functions
def quick_import_vcard(birthday_manager, filepath):
    """
    Quick import function for CLI/testing
    """
    importer = VCardFileImporter(birthday_manager)
    return importer.import_file(filepath)


def export_contacts_to_vcf(birthday_manager, output_path="/tmp/calendar.vcf", sort_by='name'):
    """Export contacts with sorting options - USES SAME TAGS AS IMPORT"""
    try:
        contacts = birthday_manager.contacts

        if not contacts:
            print("[VCardExport] No contacts found")
            return 0

        # Apply sorting
        if sort_by == 'name':
            # Sort alphabetically by name
            contacts = sorted(contacts, key=lambda x: x.get('FN', '').lower())
        elif sort_by == 'birthday':
            # Sort by birthday month/day
            def birthday_key(contact):
                bday = contact.get('BDAY', '')
                if bday:
                    try:
                        bday_date = datetime.strptime(bday, "%Y-%m-%d")
                        # Sort by month and day
                        return (bday_date.month, bday_date.day, contact.get('FN', '').lower())
                    except:
                        return (13, 32, contact.get('FN', '').lower())
                return (13, 32, contact.get('FN', '').lower())
            contacts = sorted(contacts, key=birthday_key)
        elif sort_by == 'category':
            # Sort by category
            contacts = sorted(contacts, key=lambda x: x.get('CATEGORIES', '').lower())

        print("[VCardExport] Exporting {0} contacts ({1}) to {2}".format(
            len(contacts), sort_by, output_path))

        count = 0
        with open(output_path, 'w', encoding='utf-8') as f:
            for contact in contacts:
                # Skip contacts without name
                name = contact.get('FN', '').strip()
                if not name:
                    continue

                f.write("BEGIN:VCARD\n")
                f.write("VERSION:3.0\n")

                # *** ALL THE SAME TAGS AS IMPORT ***
                # 1. FN - Formatted Name (REQUIRED)
                f.write("FN:{0}\n".format(name))

                # 2. N - Structured Name (for Google compatibility)
                # Create structured name from FN
                name_parts = name.split(' ', 1)
                if len(name_parts) == 2:
                    # Assume "FirstName LastName"
                    f.write("N:{1};{0};;;\n".format(name_parts[0], name_parts[1]))
                else:
                    # Single name
                    f.write("N:{0};;;;\n".format(name))

                # 3. BDAY - Birthday (same format as import: YYYY-MM-DD)
                bday = contact.get('BDAY', '').strip()
                if bday:
                    f.write("BDAY:{0}\n".format(bday))

                # 4. TEL - Telephone (use | separator like import)
                tel = contact.get('TEL', '').strip()
                if tel:
                    # IMPORTANT: keep | separator format
                    f.write("TEL:{0}\n".format(tel))

                # 5. EMAIL - Email (use | separator like import)
                email = contact.get('EMAIL', '').strip()
                if email:
                    f.write("EMAIL:{0}\n".format(email))

                # 6. ADR - Address
                adr = contact.get('ADR', '').strip()
                if adr:
                    f.write("ADR:{0}\n".format(adr))

                # 7. ORG - Organization
                org = contact.get('ORG', '').strip()
                if org:
                    f.write("ORG:{0}\n".format(org))

                # 8. TITLE - Job Title / Position
                title = contact.get('TITLE', '').strip()
                if title:
                    f.write("TITLE:{0}\n".format(title))

                # 9. CATEGORIES - Categories / Tags
                categories = contact.get('CATEGORIES', '').strip()
                if categories:
                    f.write("CATEGORIES:{0}\n".format(categories))

                # 10. NOTE - Notes
                note = contact.get('NOTE', '').strip()
                if note:
                    # Replace newlines with \n for vCard compatibility
                    note = note.replace('\n', '\\n')
                    f.write("NOTE:{0}\n".format(note))

                # 11. URL - Website
                url = contact.get('URL', '').strip()
                if url:
                    f.write("URL:{0}\n".format(url))

                f.write("END:VCARD\n\n")
                count += 1

        print("[VCardExport] Successfully exported {0} contacts".format(count))
        return count

    except Exception as e:
        print("[VCardExport] Error: {0}".format(str(e)))
        import traceback
        traceback.print_exc()
        return 0


def export_vcard_file(self):
    """Export all contacts to vCard file in /tmp"""
    try:
        from .vcf_importer import export_contacts_to_vcf

        # DEBUG: Check how many contacts we have
        print("[Calendar DEBUG] Contacts in manager: {0}".format(len(self.birthday_manager.contacts)))

        # Ask for confirmation first
        def confirm_callback(result):
            if result:
                export_path = "/tmp/calendar.vcf"

                # Show progress
                self["status"].setText(_("Exporting contacts..."))

                # DEBUG before export
                print("[Calendar DEBUG] About to export to: {0}".format(export_path))

                # Export
                count = export_contacts_to_vcf(self.birthday_manager, export_path)

                print("[Calendar DEBUG] Export result count: {0}".format(count))

                if count > 0:
                    message = _("Contacts exported successfully!\n\nFile: {0}\nContacts: {1}").format(
                        export_path, count)
                    self.session.open(
                        MessageBox,
                        message,
                        MessageBox.TYPE_INFO
                    )
                else:
                    # Show more detailed error
                    if len(self.birthday_manager.contacts) > 0:
                        message = _("Export failed, but {0} contacts were found.\n\nCheck permissions in /tmp/").format(
                            len(self.birthday_manager.contacts))
                    else:
                        message = _("No contacts to export.\n\nAdd contacts first via Contacts menu.")

                    self.session.open(
                        MessageBox,
                        message,
                        MessageBox.TYPE_INFO
                    )

        # Check if there are any contacts first
        if len(self.birthday_manager.contacts) == 0:
            self.session.open(
                MessageBox,
                _("No contacts to export.\n\nAdd contacts first via Contacts menu."),
                MessageBox.TYPE_INFO
            )
            return

        self.session.openWithCallback(
            confirm_callback,
            MessageBox,
            _("Export all contacts to vCard file?\n\nFile will be saved in /tmp/calendar.vcf\n\nContacts: {0}").format(
                len(self.birthday_manager.contacts)),
            MessageBox.TYPE_YESNO
        )

    except Exception as e:
        print("[Calendar] Error exporting vCard: {0}".format(str(e)))
        import traceback
        traceback.print_exc()
        self.session.open(
            MessageBox,
            _("Error exporting vCard: {0}").format(str(e)),
            MessageBox.TYPE_ERROR
        )


def export_contacts_to_vcard(birthday_manager, output_file):
    """
    Export all contacts to vCard file
    """
    contacts = birthday_manager.contacts

    with open(output_file, 'w', encoding='utf-8') as f:
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
