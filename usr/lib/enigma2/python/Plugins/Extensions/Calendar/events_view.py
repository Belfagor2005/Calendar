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
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Label import Label
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from enigma import getDesktop

from . import _


class EventsView(Screen):
    """View to display and manage events"""

    if (getDesktop(0).size().width() >= 1920):
        skin = """
        <screen name="EventsView" position="center,center" size="1200,800" title="Events View" flags="wfNoBorder">
            <widget name="date_label" position="20,20" size="1160,50" font="Regular;36" halign="center" valign="center" />
            <widget name="events_list" position="20,90" size="1160,500" itemHeight="50" font="Regular;30" scrollbarMode="showNever" />
            <widget name="event_details" position="20,594" size="1160,121" font="Regular;24" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="50,768" size="230,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_green.png" position="364,769" size="230,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_yellow.png" position="666,770" size="230,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_blue.png" position="944,770" size="230,10" alphatest="blend" />
            <widget name="key_red" position="50,725" size="230,40" font="Regular;28" halign="center" valign="center" />
            <widget name="key_green" position="365,725" size="230,40" font="Regular;28" halign="center" valign="center" />
            <widget name="key_yellow" position="665,725" size="230,40" font="Regular;28" halign="center" valign="center" />
            <widget name="key_blue" position="944,725" size="230,40" font="Regular;28" halign="center" valign="center" />
        </screen>"""
    else:
        skin = """
        <screen name="EventsView" position="center,center" size="800,600" title="Events View" flags="wfNoBorder">
            <widget name="date_label" position="20,20" size="760,35" font="Regular;24" halign="center" valign="center" />
            <widget name="events_list" position="20,70" size="760,350" itemHeight="35" font="Regular;20" scrollbarMode="showNever" />
            <widget name="event_details" position="20,425" size="760,110" font="Regular;18" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="35,571" size="150,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_green.png" position="213,572" size="150,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_yellow.png" position="398,572" size="150,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_blue.png" position="591,572" size="150,10" alphatest="blend" />
            <widget name="key_red" position="35,545" size="150,25" font="Regular;20" halign="center" valign="center" />
            <widget name="key_green" position="215,545" size="150,25" font="Regular;20" halign="center" valign="center" />
            <widget name="key_yellow" position="400,545" size="150,25" font="Regular;20" halign="center" valign="center" />
            <widget name="key_blue" position="595,545" size="150,25" font="Regular;20" halign="center" valign="center" />
        </screen>"""

    def __init__(self, session, event_manager, date=None):
        Screen.__init__(self, session)
        self.event_manager = event_manager
        self.date = date
        self.current_events = []

        self["date_label"] = Label("")
        self["events_list"] = MenuList([])
        self["event_details"] = Label("")

        self["key_red"] = Label(_("Add"))
        self["key_green"] = Label(_("Edit"))
        self["key_yellow"] = Label(_("Remove"))
        self["key_blue"] = Label(_("Back"))

        self["actions"] = ActionMap(
            [
                "CalendarActions",
            ],
            {
                "cancel": self.close,
                "ok": self.edit_event,
                "red": self.add_event,
                "green": self.edit_event,
                "yellow": self.delete_event,
                "blue": self.close,
                "up": self.up,
                "down": self.down,
            }, -1
        )

        self.onLayoutFinish.append(self.load_events)

    def load_events(self):
        """Load events for the current date"""
        if self.date:
            date_str = "{0}-{1:02d}-{2:02d}".format(
                self.date.year,
                self.date.month,
                self.date.day
            )
            self["date_label"].setText("Events for {0}".format(date_str))
            self.current_events = self.event_manager.get_events_for_date(date_str)
        else:
            self["date_label"].setText("Upcoming events (7 days)")
            upcoming = self.event_manager.get_upcoming_events(7)
            self.current_events = [event for _, event in upcoming]

        # Prepare list for display
        event_list = []
        for event in self.current_events:
            time_str = event.time if event.time else "00:00"
            repeat_str = {
                "none": "",
                "daily": " [D]",
                "weekly": " [W]",
                "monthly": " [M]",
                "yearly": " [Y]"
            }.get(event.repeat, "")

            status = "✓" if event.enabled else "✗"
            event_list.append("{0} {1} - {2}{3}".format(status, time_str, event.title, repeat_str))

        self["events_list"].setList(event_list)

        # Update details
        self.update_details()

    def update_details(self):
        """Update details of the selected event"""
        index = self["events_list"].getSelectedIndex()

        if 0 <= index < len(self.current_events):
            event = self.current_events[index]
            details = []

            if event.description:
                details.append(event.description[:100])

            if event.notify_before > 0:
                details.append("Notify: {0} min before".format(event.notify_before))

            if event.repeat != "none":
                repeat_text = {
                    "daily": "Daily",
                    "weekly": "Weekly",
                    "monthly": "Monthly",
                    "yearly": "Yearly"
                }.get(event.repeat, "")
                details.append("Repeat: {0}".format(repeat_text))

            self["event_details"].setText(" | ".join(details))
        else:
            self["event_details"].setText("")

    def up(self):
        """Move selection up"""
        self["events_list"].up()
        self.update_details()

    def down(self):
        """Move selection down"""
        self["events_list"].down()
        self.update_details()

    def add_event(self):
        """Add new event"""
        if self.date:
            from .event_dialog import EventDialog
            self.session.openWithCallback(
                self.event_added_callback,
                EventDialog,
                self.event_manager,
                date="{0}-{1:02d}-{2:02d}".format(self.date.year, self.date.month, self.date.day)
            )

    def edit_event(self):
        """Edit selected event"""
        index = self["events_list"].getSelectedIndex()
        if 0 <= index < len(self.current_events):
            from .event_dialog import EventDialog
            self.session.openWithCallback(
                self.event_updated_callback,
                EventDialog,
                self.event_manager,
                event=self.current_events[index]
            )

    def delete_event(self):
        """Delete selected event"""
        index = self["events_list"].getSelectedIndex()
        if 0 <= index < len(self.current_events):
            event = self.current_events[index]

            self.session.openWithCallback(
                lambda result: self.confirm_delete(event.id, result),
                MessageBox,
                "Delete event '{0}'?".format(event.title),
                MessageBox.TYPE_YESNO
            )

    def confirm_delete(self, event_id, result=None):
        """Confirm event deletion"""
        if result:
            self.event_manager.delete_event(event_id)
            self.load_events()
            self.close(True)

    def event_added_callback(self, result=None):
        """Callback after adding event"""
        if result:
            self.load_events()
            self.close(True)

    def event_updated_callback(self, result=None):
        """Callback after editing event"""
        if result:
            self.load_events()
            self.close(True)

    def close(self, result=None):
        """Close the screen"""
        Screen.close(self, result)
