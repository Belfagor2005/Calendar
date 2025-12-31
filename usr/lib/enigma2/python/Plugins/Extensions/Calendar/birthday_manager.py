#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
###########################################################
#  Calendar Planner for Enigma2 v1.7                      #
#  Created by: Lululla (based on Sirius0103)              #
###########################################################

MAIN FEATURES:
• Calendar with color-coded days (events/holidays/today)
• Event system with smart notifications & audio alerts
• Holiday import for 30+ countries with auto-coloring
• vCard import/export with contact management
• ICS/Google Calendar import with event management
• Database format converter (Legacy ↔ vCard ↔ ICS)
• Phone and email formatters for Calendar Planner
• Maintains consistent formatting across import, display, and storage

NEW IN v1.7:
ICS EVENT MANAGEMENT - Browse, edit, delete imported events
ICS EVENTS BROWSER - Similar to contacts browser with CH+/CH- navigation
ICS EVENT EDITOR - Full-screen dialog like contact editor
ICS FILE ARCHIVE - Store imported .ics files in /base/ics
DUPLICATE DETECTION - Smart cache for fast duplicate checking
ENHANCED SEARCH - Search in events titles, descriptions, dates

KEY CONTROLS - MAIN:
OK    - Main menu (Events/Holidays/Contacts/Import/Export/Converter)
RED   - Previous month
GREEN - Next month
YELLOW- Previous day
BLUE  - Next day
0     - Event management
MENU  - Configuration

KEY CONTROLS - ICS BROWSER:
OK    - Edit selected event
RED   - Add new event
GREEN - Edit event
YELLOW- Delete event (single/all)
BLUE  - Change sorting (date/title/category)
CH+   - Next event
CH-   - Previous event
TEXT  - Search events

ICS MANAGEMENT:
• Import Google Calendar .ics files
• Browse imported ICS files in archive
• View and edit individual ICS events
• Delete events (single or all)
• Search events by title/description/date
• Filter events by category/labels
• Archive original .ics files for re-import

DATABASE FORMATS:
• Legacy format (text files)
• vCard format (standard contacts)
• ICS format (Google Calendar compatible)

CONFIGURATION:
• Database format (Legacy/vCard/ICS)
• Auto-convert option
• Export sorting preference
• Event/holiday colors & indicators
• Audio notification settings

TECHNICAL:
• Python 2.7+ compatible
• Multi-threaded vCard/ICS import
• Smart cache system for duplicates
• File-based storage with backup
• Configurable via setup.xml

VERSION HISTORY:
v1.0 - Basic calendar
v1.1 - Event system
v1.2 - Holiday import
v1.3 - Code rewrite
v1.4 - Bug fixes
v1.5 - vCard import
v1.6 - vCard export & converter
v1.7 - ICS event management & browser

Last Updated: 2025-12-27
Status: Stable with complete vCard & ICS support
Credits: Sirius0103 (original), Lululla (modifications)
Homepage: www.corvoboys.org www.linuxsat-support.com
###########################################################
"""
from __future__ import print_function
import time
from os import makedirs, listdir, remove
from datetime import datetime
from os.path import exists, join
from . import PLUGIN_PATH

DATA_PATH = join(PLUGIN_PATH, "base")


class BirthdayManager:
    """Manages contacts and birthdays in vCard-like format"""

    def __init__(self):
        self.contacts_path = join(DATA_PATH, "contacts")
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
                        if 'TEL' in contact and contact['TEL']:
                            tel = contact['TEL']
                            if '|' in tel and ' | ' not in tel:
                                contact['TEL'] = tel.replace('|', ' | ')
                        results.append(contact)
                except ValueError:
                    # Invalid date format
                    continue

            return results
        except Exception as e:
            print("[BirthdayManager] Error getting contacts for date: {0}".format(e))
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
        """Load single contact from file - CLEAN phone numbers"""
        filepath = join(self.contacts_path, contact_id + ".txt")

        if not exists(filepath):
            return None

        contact = {
            'id': contact_id,
            'FN': '',           # Formatted Name
            'BDAY': '',         # Birthday (YYYY-MM-DD)
            'TEL': '',          # Telephone - will be cleaned
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
                        if key == 'TEL' and value:
                            value = value.strip()
                            value = value.replace(' | ', '|').replace(' |', '|').replace('| ', '|')
                            value = ' '.join(value.split())
                            value = value.replace(' ', '')
                        elif key == 'EMAIL' and value:
                            value = value.strip()
                            value = value.replace(' | ', '|').replace(' |', '|').replace('| ', '|')
                            value = ' '.join(value.split())
                            value = value.replace(' ', '')

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
