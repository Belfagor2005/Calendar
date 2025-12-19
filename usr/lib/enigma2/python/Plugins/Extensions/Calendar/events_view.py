#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
###########################################################
#                                                         #
#  Calendar Plugin for Enigma2                            #
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
#                                                         #
#  EVENT SYSTEM:                                          #
#  • Smart notifications (0-60 minutes before event)      #
#  • Background monitoring every 30 seconds               #
#  • Visual indicators on calendar for days with events   #
#  • Event persistence in JSON format                     #
#  • Configurable notification duration (3-15 seconds)    #
#  • Automatic cleanup of past event notifications        #
#                                                         #
#  DATE MANAGEMENT:                                       #
#  • Create, edit, remove date information                #
#  • Virtual keyboard for field editing                   #
#  • Automatic field navigation during editing            #
#  • File structure: base/[language]/day/YYYYMMDD.txt     #
#  • Sections: [day] for date info, [month] for people    #
#                                                         #
#  CALENDAR DISPLAY:                                      #
#  • Color coding: Today=green, Saturday=yellow, Sunday=red #
#  • Event days highlighted in blue/cyan (configurable)   #
#  • Asterisk (*) indicator for days with events          #
#  • Week numbers display                                 #
#  • Smooth month navigation                              #
#                                                         #
#  CONFIGURATION:                                         #
#  • Event system enable/disable                          #
#  • Notification settings (duration, advance time)       #
#  • Event color selection                                #
#  • Show event indicators toggle                         #
#  • Menu integration option                              #
#                                                         #
#  KEY CONTROLS - MAIN CALENDAR:                          #
#    OK          - Open main menu (New/Edit/Remove/Events)#
    RED         - Previous month                          #
    GREEN       - Next month                              #
    YELLOW      - Previous day                            #
    BLUE        - Next day                                #
    0 (ZERO)    - Open event management                   #
    LEFT/RIGHT  - Previous/Next day                       #
    UP/DOWN     - Previous/Next month                     #
    MENU        - Configuration                           #
    INFO/EPG    - About dialog                            #
#                                                         #
#  KEY CONTROLS - EVENT DIALOG:                           #
#    OK          - Edit current field                     #
    RED         - Cancel                                  #
    GREEN       - Save event                              #
    YELLOW      - Delete event (edit mode only)           #
    UP/DOWN     - Navigate between fields                 #
    LEFT/RIGHT  - Change selection options                #
#                                                         #
#  KEY CONTROLS - EVENTS VIEW:                            #
#    OK          - Edit selected event                    #
    RED         - Add new event                           #
    GREEN       - Edit selected event                     #
    YELLOW      - Delete selected event                   #
    BLUE        - Back to calendar                        #
    UP/DOWN     - Navigate event list                     #
#                                                         #
#  FILE STRUCTURE:                                        #
#  • plugin.py - Main plugin entry point                  #
#  • event_manager.py - Event management core             #
#  • event_dialog.py - Event add/edit interface           #
#  • events_view.py - Events browser                      #
#  • notification_system.py - Notification display        #
#  • events.json - Event database (JSON format)           #
#  • base/ - Date information storage                     #
#  • buttons/ - Button images for UI                      #
#                                                         #
#  EVENT STORAGE FORMAT (events.json):                    #
#  [{                                                     #
#    "id": 1766153767369,                                 #
#    "title": "Meeting",                                  #
#    "description": "Team meeting",                       #
#    "date": "2025-12-19",                                #
#    "time": "14:30",                                     #
#    "repeat": "none",                                    #
#    "notify_before": 15,                                 #
#    "enabled": true,                                     #
#    "created": "2024-12-19 14:25:47"                     #
#  }]                                                     #
#                                                         #
#  DATE FILE FORMAT (YYYYMMDD.txt):                       #
#  [day]                                                  #
#  date: 2025-06-10                                       #
#  datepeople: John Doe                                   #
#  sign: Gemini                                           #
#  holiday: None                                          #
#  description: Special day description.                  #
#                                                         #
#  [month]                                                #
#  monthpeople: Important people of the month             #
#                                                         #
#  TECHNICAL DETAILS:                                     #
#  • Python 2.7+ compatible                               #
#  • Uses eTimer for background monitoring                #
#  • JSON storage for events                              #
#  • Virtual keyboard integration                         #
#  • Auto-skin detection (HD/FHD)                         #
#  • Configurable via setup.xml                           #
#                                                         #
#  PERFORMANCE:                                           #
#  • Efficient event checking algorithm                   #
#  • Skipped checks for past non-recurring events         #
#  • Minimal memory usage                                 #
#  • Fast loading of date information                     #
#                                                         #
#  DEBUGGING:                                             #
#  • Enable debug logs: check enigma2.log                 #
#  • Filter: grep EventManager /tmp/enigma2.log           #
#  • Event check interval: 30 seconds                     #
#  • Notification window: event time ± 5 minutes          #
#                                                         #
#  CREDITS:                                               #
#  • Original Calendar plugin: Sirius0103                 #
#  • Event system & modifications: Lululla                #
#  • Notification system: Custom implementation           #
#  • Testing & feedback: Enigma2 community                #
#                                                         #
#  VERSION HISTORY:                                       #
#  • v1.0 - Basic calendar functionality                  #
#  • v1.1 - Complete event system added                   #
#           (Current version)                             #
#                                                         #
#  Last Updated: 2025-12-19                               #
#  Status: Stable with event system                       #
###########################################################
"""

from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.Label import Label
from Screens.MessageBox import MessageBox
from enigma import getDesktop
from . import _


class EventsView(Screen):
    """View to display and manage events"""

    if (getDesktop(0).size().width() >= 1920):
        skin = """
        <screen name="EventsView" position="center,center" size="1200,800" title="EventsView" flags="wfNoBorder">
            <widget name="date_label" position="20,20" size="1160,50" font="Regular;36" />
            <widget name="events_list" position="20,90" size="1160,550" itemHeight="50" font="Regular;30" scrollbarMode="showNever" />
            <widget name="event_details" position="20,645" size="1160,70" font="Regular;24" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="50,768" size="230,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_green.png" position="364,769" size="230,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_yellow.png" position="666,770" size="230,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_blue.png" position="944,770" size="230,10" alphatest="blend" />
            <widget name="key_red" position="50,725" size="230,40" font="Regular;28" />
            <widget name="key_green" position="365,725" size="230,40" font="Regular;28" />
            <widget name="key_yellow" position="665,725" size="230,40" font="Regular;28" />
            <widget name="key_blue" position="944,725" size="230,40" font="Regular;28" />
        </screen>"""
    else:
        skin = """
        <screen name="EventsView" position="560,240" size="800,600" title="EventsView" flags="wfNoBorder">
            <widget name="date_label" position="20,20" size="760,35" font="Regular;24" />
            <widget name="events_list" position="20,70" size="760,420" itemHeight="35" font="Regular;20" scrollbarMode="showNever" />
            <widget name="event_details" position="20,495" size="760,40" font="Regular;18" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="35,571" size="150,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_green.png" position="213,572" size="150,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_yellow.png" position="398,572" size="150,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_blue.png" position="591,572" size="150,10" alphatest="blend" />
            <widget name="key_red" position="35,545" size="150,25" font="Regular;20" />
            <widget name="key_green" position="215,545" size="150,25" font="Regular;20" />
            <widget name="key_yellow" position="400,545" size="150,25" font="Regular;20" />
            <widget name="key_blue" position="595,545" size="150,25" font="Regular;20" />
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
                "EventsViewActions",
                "ColorActions",
                "OkCancelActions"
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
                lambda result: self.confirm_delete(result, event.id),
                MessageBox,
                "Delete event '{0}'?".format(event.title),
                MessageBox.TYPE_YESNO
            )

    def confirm_delete(self, result, event_id):
        """Confirm event deletion"""
        if result:
            self.event_manager.delete_event(event_id)
            self.load_events()
            self.close(True)

    def event_added_callback(self, result):
        """Callback after adding event"""
        if result:
            self.load_events()
            self.close(True)

    def event_updated_callback(self, result):
        """Callback after editing event"""
        if result:
            self.load_events()
            self.close(True)
