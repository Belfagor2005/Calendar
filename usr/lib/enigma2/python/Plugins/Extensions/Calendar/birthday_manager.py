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
from os import makedirs, listdir, remove
from datetime import datetime
from os.path import exists, join


class BirthdayManager:
    """Manages contacts and birthdays in vCard-like format"""

    def __init__(self, plugin_path):
        self.plugin_path = plugin_path
        self.contacts_path = join(plugin_path, "base", "contacts")
        self.contacts = []
        self._ensure_directories()
        self.load_all_contacts()

    def _ensure_directories(self):
        """Create necessary directories"""
        if not exists(self.contacts_path):
            makedirs(self.contacts_path)

    def sort_contacts_by_name(self):
        """Sort contacts alphabetically by FN (Formatted Name)"""
        self.contacts.sort(key=lambda x: x.get('FN', '').lower())

    def sort_contacts_by_birthday(self):
        """Sort contacts by birthday (month/day)"""
        def get_birthday_sort_key(contact):
            bday = contact.get('BDAY', '')
            if bday:
                try:
                    # Extract month and day for sorting
                    from datetime import datetime
                    bday_date = datetime.strptime(bday, "%Y-%m-%d")
                    return (bday_date.month, bday_date.day, contact.get('FN', '').lower())
                except:
                    return (13, 32, contact.get('FN', '').lower())  # Invalid dates at end
            else:
                return (13, 32, contact.get('FN', '').lower())  # No birthday at end

        self.contacts.sort(key=get_birthday_sort_key)

    def sort_contacts_by_category(self):
        """Sort contacts by category"""
        self.contacts.sort(key=lambda x: x.get('CATEGORIES', '').lower())

    def search_and_sort(self, search_term, sort_by='name'):
        """
        Search and sort contacts

        Args:
            search_term: Text to search for
            sort_by: 'name', 'birthday', or 'category'

        Returns:
            Sorted list of matching contacts
        """
        results = self.search_contacts(search_term)

        if sort_by == 'name':
            results.sort(key=lambda x: x.get('FN', '').lower())
        elif sort_by == 'birthday':
            results.sort(key=lambda x: (
                x.get('BDAY', '9999-99-99'),  # No birthday last
                x.get('FN', '').lower()
            ))
        elif sort_by == 'category':
            results.sort(key=lambda x: x.get('CATEGORIES', '').lower())

        return results

    def get_contact_count(self):
        """Return number of contacts"""
        return len(self.contacts)

    def get_contacts_with_birthdays(self):
        """Get contacts that have birthday information"""
        results = []
        for contact in self.contacts:
            if contact.get('BDAY'):
                results.append(contact)
        return results

    def get_contacts_by_category(self, category):
        """Get contacts by category/tag"""
        results = []
        category_lower = category.lower()

        for contact in self.contacts:
            categories = contact.get('CATEGORIES', '').lower()
            if category_lower in categories:
                results.append(contact)

        return results

    def get_contacts_by_birthday_month(self, month):
        """Get contacts with birthdays in specific month"""
        results = []
        for contact in self.contacts:
            bday = contact.get('BDAY', '')
            if bday:
                try:
                    bday_date = datetime.strptime(bday, "%Y-%m-%d")
                    if bday_date.month == month:
                        results.append(contact)
                except:
                    continue
        return results

    def get_contacts_for_date(self, date_str):
        """Get contacts with birthdays on specific date"""
        try:
            # Parse date string (format: YYYY-MM-DD)
            target_date = datetime.strptime(date_str, "%Y-%m-%d")

            results = []
            for contact in self.contacts:
                bday = contact.get('BDAY', '')
                if not bday:
                    continue

                try:
                    # Check if birthday matches (ignore year)
                    bday_date = datetime.strptime(bday, "%Y-%m-%d")
                    if bday_date.month == target_date.month and bday_date.day == target_date.day:
                        results.append(contact)
                except ValueError:
                    # Invalid date format
                    continue

            return results
        except Exception as e:
            print("[BirthdayManager] Error getting contacts for date: {}".format(e))
            return []

    def load_all_contacts(self):
        """Load all contacts from directory - SORTED by name"""
        self.contacts = []

        if not exists(self.contacts_path):
            return

        for filename in listdir(self.contacts_path):
            if filename.endswith(".txt"):
                contact_id = filename[:-4]
                contact = self.load_contact(contact_id)
                if contact:
                    self.contacts.append(contact)

        # SORT contacts alphabetically when loading
        self.sort_contacts_by_name()

        print("[BirthdayManager] Loaded {0} contacts (sorted)".format(len(self.contacts)))

    def load_contact(self, contact_id):
        """Load single contact from file"""
        filepath = join(self.contacts_path, contact_id + ".txt")

        if not exists(filepath):
            return None

        contact = {
            'id': contact_id,
            'FN': '',           # Formatted Name
            'BDAY': '',         # Birthday (YYYY-MM-DD)
            'TEL': '',          # Telephone
            'EMAIL': '',        # Email
            'ADR': '',          # Address
            'ORG': '',          # Organization
            'TITLE': '',        # Title/Job
            'CATEGORIES': '',   # Tags (Family,Work,Friend)
            'NOTE': '',         # Notes
            'URL': '',          # Website
            'created': ''
        }

        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()

            current_section = None
            for line in lines:
                line = line.strip()
                if line == "[contact]":
                    current_section = "contact"
                elif current_section == "contact" and ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    if key in contact:
                        contact[key] = value.strip()

            return contact

        except Exception as e:
            print("[BirthdayManager] Error loading contact {0}: {1}".format(contact_id, str(e)))
            return None

    def save_contact(self, contact_data):
        """Save contact to file"""
        if 'id' in contact_data:
            contact_id = contact_data['id']
        else:
            # Generate new ID
            contact_id = str(int(time.time() * 1000))
            contact_data['id'] = contact_id

        filepath = join(self.contacts_path, contact_id + ".txt")

        try:
            # Format contact file
            content = "[contact]\n"
            for key in ['FN', 'BDAY', 'TEL', 'EMAIL', 'ADR',
                        'ORG', 'TITLE', 'CATEGORIES', 'NOTE', 'URL']:
                value = contact_data.get(key, '')
                if value:
                    content += "{0}: {1}\n".format(key, value)

            # Add creation date if new contact
            if 'created' not in contact_data or not contact_data['created']:
                contact_data['created'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            content += "CREATED: {0}\n".format(contact_data.get('created', ''))

            # Save to file
            with open(filepath, 'w') as f:
                f.write(content)

            # Reload contacts
            self.load_all_contacts()
            return contact_id

        except Exception as e:
            print("[BirthdayManager] Error saving contact: {0}".format(str(e)))
            return None

    def delete_contact(self, contact_id):
        """Delete contact"""
        filepath = join(self.contacts_path, contact_id + ".txt")

        if exists(filepath):
            try:
                remove(filepath)
                self.load_all_contacts()
                return True
            except Exception as e:
                print("[BirthdayManager] Error deleting contact: {0}".format(str(e)))

        return False

    def search_contacts(self, search_term):
        """Search contacts by name, phone, email, or note"""
        results = []
        search_term = search_term.lower()

        for contact in self.contacts:
            # Search in various fields
            search_fields = ['FN', 'TEL', 'EMAIL', 'NOTE', 'CATEGORIES', 'ORG', 'TITLE']

            for field in search_fields:
                field_value = contact.get(field, '').lower()
                if search_term in field_value:
                    results.append(contact)
                    break

        return results
