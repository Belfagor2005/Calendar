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
from Screens.MessageBox import MessageBox
from enigma import quitMainloop

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
                quitMainloop(3)  # 3 = Restart Enigma2
                print("Enigma2 restart initiated")
            except Exception as e:
                print("Failed to restart Enigma2: %s" % e)
                session.open(MessageBox,
                             _("Please restart Enigma2 manually."),
                             MessageBox.TYPE_INFO)
