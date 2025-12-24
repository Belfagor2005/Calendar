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
from Screens.MessageBox import MessageBox

from .updater import PluginUpdater
from . import _


class UpdateManager:
    """Centralized update manager using existing PluginUpdater"""

    @staticmethod
    def check_for_updates(session, status_label=None):
        """Check for updates - unified function for both plugin and settings"""
        print("UpdateManager.check_for_updates called")

        if status_label:
            status_label.setText(_("Checking for updates..."))

        try:
            updater = PluginUpdater()
            print("PluginUpdater created successfully")

            def update_callback(result):
                print("update_callback received result: %s" % result)

                if result is None:
                    if status_label:
                        status_label.setText(_("Update check failed"))
                    session.open(MessageBox,
                                 _("Could not check for updates. Check internet connection."),
                                 MessageBox.TYPE_ERROR)

                elif result:
                    if status_label:
                        status_label.setText(_("Update available!"))
                    UpdateManager.ask_to_update(session, status_label, updater)

                else:
                    if status_label:
                        status_label.setText(_("Plugin is up to date"))
                    session.open(MessageBox,
                                 _("You have the latest version of Calendar."),
                                 MessageBox.TYPE_INFO)

            print("Calling updater.check_update()")
            updater.check_update(update_callback)

        except Exception as e:
            print("Error in check_for_updates: %s" % str(e))
            if status_label:
                status_label.setText(_("Update check error"))
            session.open(MessageBox,
                         _("Could not check for updates: %s") % str(e),
                         MessageBox.TYPE_ERROR)

    @staticmethod
    def ask_to_update(session, status_label=None, updater=None):
        """Ask user if they want to update"""
        if updater is None:
            updater = PluginUpdater()

        def update_confirmed(result):
            print("User update confirmation: %s" % result)
            if result:
                UpdateManager.perform_update(session, status_label, updater)
            elif status_label:
                status_label.setText(_("Update cancelled"))

        message = _("A new version is available!\n\nUpdate now?\n\n(Recommended to backup first)")
        session.openWithCallback(update_confirmed,
                                 MessageBox,
                                 message,
                                 MessageBox.TYPE_YESNO)

    @staticmethod
    def perform_update(session, status_label=None, updater=None):
        """Perform the update"""
        if updater is None:
            updater = PluginUpdater()

        def update_progress(success, message):
            print("Update progress: success=%s, message=%s" % (success, message))
            if success:
                if status_label:
                    status_label.setText(_("Update successful!"))

                restart_msg = _("%s\n\nRestart Enigma2 now for changes to take effect.") % message
                session.openWithCallback(
                    lambda result: UpdateManager.restart_enigma2(session, result),
                    MessageBox,
                    restart_msg,
                    MessageBox.TYPE_YESNO
                )
            else:
                if status_label:
                    status_label.setText(_("Update failed"))
                session.open(MessageBox,
                             message,
                             MessageBox.TYPE_ERROR)

        if status_label:
            status_label.setText(_("Updating plugin... Please wait"))

        print("Starting download_update()")
        updater.download_update(update_progress)

    @staticmethod
    def restart_enigma2(session, result):
        """Restart Enigma2 if user confirms"""
        print("Restart Enigma2 confirmation: %s" % result)
        if result:
            try:
                from enigma import quitMainloop
                quitMainloop(3)  # 3 = Restart Enigma2
                print("Enigma2 restart initiated")
            except Exception as e:
                print("Failed to restart Enigma2: %s" % e)
                session.open(MessageBox,
                             _("Please restart Enigma2 manually."),
                             MessageBox.TYPE_INFO)
