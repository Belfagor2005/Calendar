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
from Screens.Screen import Screen
from skin import parseColor
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.ActionMap import ActionMap
from Components.Label import Label
from Screens.MessageBox import MessageBox
from enigma import getDesktop

from . import _
from .event_manager import create_event_from_data


class EventDialog(Screen):
    """Dialog to add or edit an event"""

    if (getDesktop(0).size().width() >= 1920):
        skin = """
        <screen name="EventDialog" position="center,center" size="1000,700" title="Event Management" flags="wfNoBorder">
            <widget name="title_label" position="20,20" size="960,40" font="Regular;32" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="title_value" position="20,70" size="960,50" font="Regular;28" backgroundColor="#00808080" />

            <widget name="date_label" position="20,140" size="300,40" font="Regular;32" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="date_value" position="20,190" size="300,50" font="Regular;28" backgroundColor="#00808080" />

            <widget name="time_label" position="340,140" size="300,40" font="Regular;32" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="time_value" position="340,190" size="300,50" font="Regular;28" backgroundColor="#00808080" />

            <widget name="repeat_label" position="660,140" size="300,40" font="Regular;32" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="repeat_value" position="660,190" size="300,50" font="Regular;28" backgroundColor="#00808080" />

            <widget name="notify_label" position="20,260" size="300,40" font="Regular;32" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="notify_value" position="20,310" size="300,50" font="Regular;28" backgroundColor="#00808080" />

            <widget name="enabled_label" position="340,260" size="300,40" font="Regular;32" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="enabled_value" position="340,310" size="300,50" font="Regular;28" backgroundColor="#00808080" />

            <widget name="description_label" position="20,380" size="960,40" font="Regular;32" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="description_value" position="20,430" size="960,200" font="Regular;28" backgroundColor="#00808080" />

            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="50,690" size="230,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_green.png" position="401,693" size="230,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_yellow.png" position="751,691" size="230,10" alphatest="blend" />
            <widget name="key_red" position="51,650" size="230,40" font="Regular;28" halign="center" />
            <widget name="key_green" position="400,650" size="230,40" font="Regular;28" halign="center" />
            <widget name="key_yellow" position="750,650" size="230,40" font="Regular;28" halign="center" />
        </screen>"""
    else:
        skin = """
        <screen name="EventDialog" position="center,center" size="800,600" title="Event Management" flags="wfNoBorder">
            <widget name="title_label" position="20,20" size="760,30" font="Regular;24" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="title_value" position="20,55" size="760,35" font="Regular;20" backgroundColor="#00808080" />

            <widget name="date_label" position="20,110" size="240,30" font="Regular;24" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="date_value" position="20,145" size="240,35" font="Regular;20" backgroundColor="#00808080" />

            <widget name="time_label" position="280,110" size="240,30" font="Regular;24" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="time_value" position="280,145" size="240,35" font="Regular;20" backgroundColor="#00808080" />

            <widget name="repeat_label" position="540,110" size="240,30" font="Regular;24" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="repeat_value" position="540,145" size="240,35" font="Regular;20" backgroundColor="#00808080" />

            <widget name="notify_label" position="20,200" size="240,30" font="Regular;24" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="notify_value" position="20,235" size="240,35" font="Regular;20" backgroundColor="#00808080" />

            <widget name="enabled_label" position="280,200" size="240,30" font="Regular;24" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="enabled_value" position="280,235" size="240,35" font="Regular;20" backgroundColor="#00808080" />

            <widget name="description_label" position="20,290" size="760,30" font="Regular;24" foregroundColor="#00ffcc33" backgroundColor="background" />
            <widget name="description_value" position="20,325" size="760,200" font="Regular;20" backgroundColor="#00808080" />

            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="45,586" size="200,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_green.png" position="308,587" size="200,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_yellow.png" position="568,587" size="200,10" alphatest="blend" />
            <widget name="key_red" position="50,550" size="200,35" font="Regular;24" halign="center" />
            <widget name="key_green" position="310,550" size="200,35" font="Regular;24" halign="center" />
            <widget name="key_yellow" position="570,550" size="200,35" font="Regular;24" halign="center" />
        </screen>"""

    def action_mapped(self, action):
        """Handle action mapping dynamically"""
        if action == "yellow" and not self.is_edit:
            return  # Ignore yellow button unless in edit mode

        if action == "yellow":
            self.delete()
        elif action == "green":
            self.save()
        elif action == "red":
            self.cancel()
        elif action == "ok":
            self.edit_field()
        elif action == "up":
            self.prev_field()
        elif action == "down":
            self.next_field()
        elif action == "left":
            self.prev_option()
        elif action == "right":
            self.next_option()

    def __init__(self, session, event_manager, date=None, event=None):
        Screen.__init__(self, session)
        self.event_manager = event_manager
        self.event = event
        self.is_edit = event is not None

        # Configuration
        self.repeat_options = [
            ("none", "Do not repeat"),
            ("daily", "Daily"),
            ("weekly", "Weekly"),
            ("monthly", "Monthly"),
            ("yearly", "Yearly")
        ]

        self.notify_options = [
            (0, "At event time"),
            (5, "5 minutes before"),
            (10, "10 minutes before"),
            (15, "15 minutes before"),
            (30, "30 minutes before"),
            (60, "1 hour before")
        ]

        # Initialize widgets
        self["title_label"] = Label(_("Title:"))
        self["title_value"] = Label(_("Event") if not (event and event.title) else "")  # Default
        self["date_label"] = Label(_("Date:"))
        self["date_value"] = Label(date or "")
        self["time_label"] = Label(_("Time:"))
        self["time_value"] = Label("00:00")
        self["repeat_label"] = Label(_("Repeat:"))
        self["repeat_value"] = Label("Do not repeat")
        self["notify_label"] = Label(_("Notify:"))
        self["notify_value"] = Label("5 minutes before")
        self["enabled_label"] = Label(_("Active:"))
        self["enabled_value"] = Label("Yes")
        self["description_label"] = Label(_("Description:"))
        self["description_value"] = Label(_("Description") if not (event and event.description) else "")

        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label(_("Save"))
        self["key_yellow"] = Label(_("Delete") if self.is_edit else "")

        self.fields = [
            ("title", _("Title"), self["title_value"]),
            ("date", _("Date"), self["date_value"]),
            ("time", _("Time"), self["time_value"]),
            ("repeat", _("Repeat"), self["repeat_value"]),
            ("notify", _("Notify"), self["notify_value"]),
            ("enabled", _("Active"), self["enabled_value"]),
            ("description", _("Description"), self["description_value"])
        ]

        self.current_field_index = 0
        self.enabled = True

        if self.event:
            self.load_event_data()
        else:
            self.set_default_values()

        self["actions"] = ActionMap(
            [
                "CalendarActions",
            ],
            {
                "cancel": self.cancel,
                "ok": self.edit_field,
                "red": self.cancel,
                "green": self.save,
                "yellow": self.action_mapped,
                "up": self.prev_field,
                "down": self.next_field,
                "left": self.prev_option,
                "right": self.next_option,
            }, -1
        )

        if self.is_edit:
            self["actions"].actions.update({"yellow": self.delete})
        self.onLayoutFinish.append(self.force_first_field_highlight)

    def force_first_field_highlight(self):
        """Evidenzia il primo campo all'apertura del dialog"""
        self.current_field_index = 0
        self.update_highlight()

    def load_event_data(self):
        """Load event data into fields"""
        if not self.event:
            return

        # Title – if empty, use default
        title = self.event.title.strip() if self.event.title else _("Event")
        self["title_value"].setText(title)

        self["date_value"].setText(self.event.date)
        self["time_value"].setText(self.event.time)

        # Find repeat text
        repeat_text = dict(self.repeat_options).get(self.event.repeat, "Do not repeat")
        self["repeat_value"].setText(repeat_text)

        # Find notify text
        notify_text = (
            "{0} minutes before".format(self.event.notify_before)
            if self.event.notify_before > 0
            else "At event time"
        )
        self["notify_value"].setText(notify_text)

        self["enabled_value"].setText("Yes" if self.event.enabled else "No")

        # Description – if empty, use default
        description = self.event.description.strip() if self.event.description else _("Description")
        self["description_value"].setText(description)

        self.enabled = self.event.enabled

    def set_default_values(self):
        """Set default values for new events"""
        if not self.event:
            if not self["title_value"].getText():
                self["title_value"].setText(_("Event"))
            if not self["description_value"].getText():
                self["description_value"].setText(_("Description"))

    def edit_field(self):
        """Edit current field with placeholder handling"""
        if self.current_field_index >= len(self.fields):
            return

        field_name, field_label, widget = self.fields[self.current_field_index]

        if field_name in ["repeat", "notify", "enabled"]:
            # These fields use selection, not the virtual keyboard
            return

        current_text = widget.getText()

        # If it is a placeholder, pass an empty string to the keyboard
        if current_text in [_("Event"), _("Description")]:
            current_text = ""

        def callback(new_text):
            if new_text is not None:
                # If the new string is empty, restore the placeholder
                if not new_text.strip():
                    if field_name == "title":
                        new_text = _("Event")
                    elif field_name == "description":
                        new_text = _("Description")
                widget.setText(new_text)

                # Immediately update the highlight
                self.update_highlight()

        self.session.openWithCallback(
            callback,
            VirtualKeyBoard,
            title=_("Enter ") + field_label,
            text=current_text
        )

    def prev_field(self):
        """Move to previous field"""
        self.current_field_index = (self.current_field_index - 1) % len(self.fields)
        self.update_highlight()
        print("[EventDialog] Moved to field: {0}".format(self.fields[self.current_field_index][0]))

    def next_field(self):
        """Move to next field"""
        self.current_field_index = (self.current_field_index + 1) % len(self.fields)
        self.update_highlight()
        print("[EventDialog] Moved to field: {0}".format(self.fields[self.current_field_index][0]))

    def update_highlight(self):
        """Update current field highlight with better visibility"""
        current_field_name = self.fields[self.current_field_index][0]
        print("[EventDialog] Highlighting field: {0}".format(current_field_name))
        for i, (field_name, field_label, widget) in enumerate(self.fields):
            if i == self.current_field_index:
                # Current field – intense highlight
                widget.instance.setBorderWidth(3)
                widget.instance.setBorderColor(parseColor("#00FF00"))

                # Ensure the text is visible even if it is the default
                current_text = widget.getText()
                if not current_text or current_text in [_("Event"), _("Description")]:
                    # If it is a placeholder, use a slightly different color
                    widget.instance.setForegroundColor(parseColor("#AAAAAA"))
                else:
                    widget.instance.setForegroundColor(parseColor("#FFFFFF"))

                # Background highlight
                widget.instance.setBackgroundColor(parseColor("#1A3C1A"))
            else:
                # Unselected fields
                widget.instance.setBorderWidth(1)
                widget.instance.setBorderColor(parseColor("#404040"))

                # Restore normal colors
                widget.instance.setForegroundColor(parseColor("#FFFFFF"))
                widget.instance.setBackgroundColor(parseColor("#00808080"))

    def prev_option(self):
        """Previous option for selection fields"""
        field_name, _, widget = self.fields[self.current_field_index]

        if field_name == "repeat":
            current = widget.getText()
            options = [opt[1] for opt in self.repeat_options]
            try:
                idx = options.index(current)
                new_idx = (idx - 1) % len(options)
                widget.setText(options[new_idx])
            except ValueError:
                widget.setText(options[0])

        elif field_name == "notify":
            current = widget.getText()
            options = [
                "{0} minutes before".format(opt[0]) if opt[0] > 0 else "At event time"
                for opt in self.notify_options
            ]

            try:
                idx = options.index(current)
                new_idx = (idx - 1) % len(options)
                widget.setText(options[new_idx])
            except ValueError:
                widget.setText("15 minutes before")

        elif field_name == "enabled":
            current = widget.getText()
            new_text = "No" if current == "Yes" else "Yes"
            widget.setText(new_text)
            self.enabled = (new_text == "Yes")

    def next_option(self):
        """Next option for selection fields"""
        field_name, _, widget = self.fields[self.current_field_index]

        if field_name == "repeat":
            current = widget.getText()
            options = [opt[1] for opt in self.repeat_options]
            try:
                idx = options.index(current)
                new_idx = (idx + 1) % len(options)
                widget.setText(options[new_idx])
            except ValueError:
                widget.setText(options[0])

        elif field_name == "notify":
            current = widget.getText()
            options = [
                "{0} minutes before".format(opt[0]) if opt[0] > 0 else "At event time"
                for opt in self.notify_options
            ]
            try:
                idx = options.index(current)
                new_idx = (idx + 1) % len(options)
                widget.setText(options[new_idx])
            except ValueError:
                widget.setText("15 minutes before")

        elif field_name == "enabled":
            current = widget.getText()
            new_text = "Yes" if current == "No" else "No"
            widget.setText(new_text)
            self.enabled = (new_text == "Yes")

    def get_repeat_value(self):
        """Get repeat value from text"""
        text = self["repeat_value"].getText()
        reverse_map = {v: k for k, v in self.repeat_options}
        return reverse_map.get(text, "none")

    def get_notify_value(self):
        """Get notify value from text"""
        text = self["notify_value"].getText()
        if text == "At event time":
            return 0

        try:
            return int(text.split()[0])
        except:
            return 5

    def save(self):
        """Save event with placeholder handling"""
        title = self["title_value"].getText().strip()
        date = self["date_value"].getText().strip()
        event_time = self["time_value"].getText().strip()

        # If the title is placeholder, treat as empty
        if title == _("Event"):
            title = ""

        if not title or not date:
            self.session.open(
                MessageBox,
                _("Title and date are required!"),
                MessageBox.TYPE_ERROR
            )
            return

        # Placeholder handling for description
        description = self["description_value"].getText().strip()
        if description == _("Description"):
            description = ""

        # Create event data
        event_data = {
            'title': title,
            'description': description,
            'date': date,
            'event_time': event_time,
            'repeat': self.get_repeat_value(),
            'notify_before': self.get_notify_value(),
            'enabled': self.enabled
        }

        if self.is_edit:
            # Update existing event
            success = self.event_manager.update_event(self.event.id, **event_data)
            if success:
                self.close(True)
        else:
            # Create new event - labels will be auto-extracted in Event.__init__
            new_event = create_event_from_data(**event_data)
            self.event_manager.add_event(new_event)
            self.close(True)

    def delete(self):
        """Delete event"""
        if self.event:
            self.event_manager.delete_event(self.event.id)
            self.close(True)

    def cancel(self):
        """Cancel"""
        self.close(False)
