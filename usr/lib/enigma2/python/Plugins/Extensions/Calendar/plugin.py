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
#                                                         #
#  KEY CONTROLS - MAIN CALENDAR:                          #
#   OK          - Open main menu                          #
#                 (New/Edit/Remove/Events/Holidays)       #
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
#  FILE STRUCTURE:                                        #
#  • plugin.py - Main plugin entry point                  #
#  • event_manager.py - Event management core             #
#  • event_dialog.py - Event add/edit interface           #
#  • events_view.py - Events browser                      #
#  • notification_system.py - Notification display        #
#  • holidays.py - Holiday import and management          #
#  • events.json - Event database (JSON format)           #
#  • base/ - Date information storage                     #
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
#  • Virtual keyboard integration                         #
#  • Auto-skin detection (HD/FHD)                         #
#  • Configurable via setup.xml                           #
#  • Uses eServiceReference for audio playback            #
#  • Holiday cache system for fast rendering              #
#  • File-based holiday storage (no database)             #
#                                                         #
#  PERFORMANCE:                                           #
#  • Efficient event checking algorithm                   #
#  • Skipped checks for past non-recurring events         #
#  • Holiday cache: 1 file read per month                 #
#  • Minimal memory usage                                 #
#  • Fast loading of date information                     #
#                                                         #
#  DEBUGGING:                                             #
#  • Enable debug logs: check enigma2.log                 #
#  • Filter: grep EventManager /tmp/enigma2.log           #
#  • Holiday debug: grep Holidays /tmp/enigma2.log        #
#  • Event check interval: 30 seconds                     #
#  • Notification window: event time ± 5 minutes          #
#  • Audio debug: check play_notification_sound() calls   #
#                                                         #
#  CREDITS:                                               #
#  • Original Calendar plugin: Sirius0103                 #
#  • Event system & modifications: Lululla                #
#  • Holiday system & enhancements: Custom implementation #
#  • Notification system: Custom implementation           #
#  • Audio system: Enigma2 eServiceReference integration  #
#  • Testing & feedback: Enigma2 community                #
#                                                         #
#  VERSION HISTORY:                                       #
#  • v1.0 - Basic calendar functionality                  #
#  • v1.1 - Complete event system added                   #
#  • v1.2 - Holiday import and coloring system            #
#  • v1.3 - Rewrite complete code . screen and source..   #
#                                                         #
#  Last Updated: 2025-12-21                               #
#  Status: Stable with event & holiday system             #
###########################################################
"""

import datetime
from time import localtime
from os import remove, makedirs
from os.path import exists, dirname, join, getmtime

from enigma import getDesktop
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Setup import Setup

try:
    from Screens.Setup import setupDom as original_setupDom
except ImportError:
    # Fallback Python 2
    from Screens.Setup import setupdom as original_setupDom

from Screens.VirtualKeyBoard import VirtualKeyBoard

from Components.ActionMap import ActionMap  # , HelpableActionMap
from Components.MenuList import MenuList
from Components.Label import Label
from Components.Sources.StaticText import StaticText
from Components.config import (
    config,
    ConfigSubsection,
    ConfigSelection,
    ConfigYesNo,
)

from Tools.Directories import (
    fileExists,
    resolveFilename,
    SCOPE_PLUGINS,
    fileReadXML
)
from enigma import eTimer
from skin import parseColor
import Screens.Setup

from . import _, plugin_path, PLUGIN_VERSION
from .events_view import EventsView

# Performance Cache
domSetups = {}
setupModTimes = {}


def init_calendar_config():
    """Initialize all calendar configurations"""
    if not hasattr(config.plugins, 'calendar'):
        config.plugins.calendar = ConfigSubsection()

    config.plugins.calendar.menu = ConfigSelection(default="no", choices=[
        ("no", _("no")),
        ("yes", _("yes"))])
    config.plugins.calendar.events_enabled = ConfigYesNo(default=True)
    config.plugins.calendar.events_notifications = ConfigYesNo(default=True)
    config.plugins.calendar.events_show_indicators = ConfigYesNo(default=True)
    config.plugins.calendar.events_color = ConfigSelection(
        choices=[
            ("blue", _("Blue")),
            ("red", _("Red")),
            ("green", _("Green")),
            ("orange", _("Orange")),
            ("yellow", _("Yellow")),
            ("white", _("White")),
        ],
        default="cyan"  # cyan as default
    )
    config.plugins.calendar.events_play_sound = ConfigYesNo(default=True)
    config.plugins.calendar.events_sound_type = ConfigSelection(
        choices=[
            ("short", _("Short beep")),
            ("notify", _("Notification tone")),
            ("alert", _("Alert sound")),
            ("none", _("No sound"))
        ],
        default="notify"
    )
    config.plugins.calendar.holidays_enabled = ConfigYesNo(default=True)
    config.plugins.calendar.holidays_show_indicators = ConfigYesNo(default=True)
    config.plugins.calendar.holidays_color = ConfigSelection(
        choices=[
            ("blue", _("Blue")),
            ("red", _("Red")),
            ("green", _("Green")),
            ("orange", _("Orange")),
            ("yellow", _("Yellow")),
            ("white", _("White")),
        ],
        default="blue"  # blue as default
    )
    config.plugins.calendar.debug_enabled = ConfigYesNo(default=False)


DEBUG = config.plugins.calendar.debug_enabled.value if hasattr(config.plugins, 'calendar') and hasattr(config.plugins.calendar, 'debug_enabled') else False
init_calendar_config()


class MenuDialog(Screen):
    skin = """
    <screen name="MenuDialog" position="center,center" size="600,600" title="Edit Settings" flags="wfNoBorder">
        <widget name="menu" position="10,10" size="580,540" itemHeight="40" font="Regular;32" scrollbarMode="showOnDemand" />
        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_updown.png" position="135,560" size="75,36" alphatest="blend" zPosition="5" />
        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_ok.png" position="400,560" size="74,40" alphatest="on" zPosition="5" />
    </screen>
    """

    def __init__(self, session, menu):
        Screen.__init__(self, session)
        self["menu"] = MenuList(menu)
        self["actions"] = ActionMap(
            ["OkCancelActions"],
            {
                "ok": self.ok,
                "cancel": self.cancel,
            }, -1
        )

    def ok(self):
        selection = self["menu"].getCurrent()
        if selection:
            self.close(selection)

    def cancel(self):
        self.close(None)


class Calendar(Screen):
    if (getDesktop(0).size().width() >= 1920):
        skin = """
        <!-- Calendar -->
        <screen name="Calendar" position="5,5" size="1900,1060" title=" " flags="wfNoBorder">
            <eLabel backgroundColor="#001a2336" cornerRadius="30" position="0,910" size="1905,90" zPosition="0" />
            <eLabel name="" position="-118,-404" size="1920,1080" zPosition="-1" cornerRadius="18" backgroundColor="#00171a1c" foregroundColor="#00171a1c" />
            <widget source="session.VideoPicture" render="Pig" position="1392,622" zPosition="19" size="475,271" backgroundColor="transparent" transparent="0" cornerRadius="14" />

            <!-- SEPARATORE
            <eLabel position="30,915" size="1740,5" backgroundColor="#FF555555" zPosition="1" />
            -->
            <!-- NOMI GIORNI SETTIMANA -->
            <widget name="w0" position="15,60" size="62,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w1" position="81,60" size="62,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w2" position="148,60" size="62,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w3" position="216,60" size="62,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w4" position="283,60" size="62,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w5" position="350,60" size="62,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w6" position="418,60" size="62,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w7" position="485,60" size="64,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />

            <!-- NUMERI SETTIMANA -->
            <widget name="wn0" position="15,128" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn1" position="15,195" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn2" position="15,263" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn3" position="15,330" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn4" position="15,398" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn5" position="15,465" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />

            <!-- GIORNI DEL MESE (42 celle) -->
            <widget name="d0" position="83,128" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d1" position="150,128" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d2" position="218,128" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d3" position="285,128" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d4" position="353,128" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d5" position="420,128" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d6" position="488,128" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />

            <widget name="d7" position="83,195" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d8" position="150,195" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d9" position="218,195" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d10" position="285,195" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d11" position="353,195" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d12" position="420,195" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d13" position="488,195" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />

            <widget name="d14" position="83,263" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d15" position="150,263" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d16" position="218,263" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d17" position="285,263" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d18" position="353,263" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d19" position="420,263" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d20" position="488,263" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />

            <widget name="d21" position="83,330" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d22" position="150,330" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d23" position="218,330" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d24" position="285,330" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d25" position="353,330" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d26" position="420,330" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d27" position="488,330" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />

            <widget name="d28" position="83,398" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d29" position="150,398" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d30" position="218,398" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d31" position="285,398" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d32" position="353,398" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d33" position="420,398" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d34" position="488,398" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />

            <widget name="d35" position="83,465" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d36" position="150,465" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d37" position="218,465" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d38" position="285,465" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d39" position="353,465" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d40" position="420,465" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />
            <widget name="d41" position="488,465" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="background" />

            <!-- TESTI INFORMATIVI -->
            <widget name="monthname" position="15,8" size="533,45" font="Regular; 36" foregroundColor="#00ffcc33" backgroundColor="background" halign="center" transparent="1" />
            <widget name="date" position="555,10" size="1230,40" font="Regular; 30" foregroundColor="#00ffcc33" backgroundColor="background" halign="center" transparent="1" />
            <widget name="datepeople" position="555,60" size="1230,38" font="Regular; 30" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="monthpeople" position="15,540" size="533,368" font="Regular; 30" foregroundColor="#008f8f8f" backgroundColor="background" halign="left" transparent="1" />
            <widget name="sign" position="555,105" size="1230,75" font="Regular; 30" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="holiday" position="555,188" size="1230,75" font="Regular; 30" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="description" position="555,270" size="1230,638" font="Regular; 30" foregroundColor="#008f8f8f" backgroundColor="background" halign="left" valign="top" transparent="1" />
            <widget name="status" position="555,858" size="976,50" font="Regular; 32" foregroundColor="#3333ff" zPosition="5" halign="left" transparent="1" />

            <!-- TASTI FUNZIONE -->
            <widget name="key_red" position="113,928" size="200,30" font="Regular;30" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_green" position="443,928" size="200,30" font="Regular;30" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_yellow" position="773,928" size="200,30" font="Regular;30" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_blue" position="1103,928" size="200,30" font="Regular;30" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />

            <!-- ICONE TASTI -->
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="110,960" size="230,10" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_green.png" position="440,960" size="230,10" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_yellow.png" position="771,960" size="230,10" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_blue.png" position="1099,960" size="230,10" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_leftright.png" position="1353,930" size="75,36" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_updown.png" position="1447,930" size="75,36" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_ok.png" position="1540,930" size="74,40" alphatest="on" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_menu.png" position="1633,930" size="77,36" alphatest="on" zPosition="5" />
        </screen>"""
    else:
        skin = """
        <!-- Calendar -->
        <screen name="Calendar" position="center,center" size="1280,720" title=" " flags="wfNoBorder">
            <eLabel backgroundColor="#001a2336" cornerRadius="20" position="0,630" size="1280,50" zPosition="0" />
            <eLabel name="" position="-80,-270" size="1280,720" zPosition="-1" cornerRadius="12" backgroundColor="#00171a1c" foregroundColor="#00171a1c" />
            <widget source="session.VideoPicture" render="Pig" position="933,431" zPosition="19" size="315,180" backgroundColor="transparent" transparent="0" cornerRadius="10" />

            <!-- NOMI GIORNI SETTIMANA -->
            <widget name="w0" position="10,40" size="42,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w1" position="54,40" size="42,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w2" position="98,40" size="42,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w3" position="143,40" size="42,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w4" position="187,40" size="42,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w5" position="232,40" size="42,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w6" position="276,40" size="42,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w7" position="320,40" size="42,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />

            <!-- NUMERI SETTIMANA -->
            <widget name="wn0" position="10,85" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn1" position="10,130" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn2" position="10,175" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn3" position="10,220" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn4" position="10,265" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn5" position="10,310" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />

            <!-- GIORNI DEL MESE (42 celle) -->
            <widget name="d0" position="55,85" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d1" position="100,85" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d2" position="145,85" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d3" position="190,85" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d4" position="235,85" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d5" position="280,85" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d6" position="325,85" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />

            <widget name="d7" position="55,130" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d8" position="100,130" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d9" position="145,130" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d10" position="190,130" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d11" position="235,130" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d12" position="280,130" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d13" position="325,130" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />

            <widget name="d14" position="55,175" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d15" position="100,175" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d16" position="145,175" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d17" position="190,175" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d18" position="235,175" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d19" position="280,175" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d20" position="325,175" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />

            <widget name="d21" position="55,220" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d22" position="100,220" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d23" position="145,220" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d24" position="190,220" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d25" position="235,220" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d26" position="280,220" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d27" position="325,220" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />

            <widget name="d28" position="55,265" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d29" position="100,265" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d30" position="145,265" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d31" position="190,265" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d32" position="235,265" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d33" position="280,265" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d34" position="325,265" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />

            <widget name="d35" position="55,310" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d36" position="100,310" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d37" position="145,310" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d38" position="190,310" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d39" position="235,310" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d40" position="280,310" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />
            <widget name="d41" position="325,310" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="background" />

            <!-- TESTI INFORMATIVI -->
            <widget name="monthname" position="10,5" size="355,30" font="Regular; 24" foregroundColor="#00ffcc33" backgroundColor="background" halign="center" transparent="1" />
            <widget name="date" position="370,7" size="820,27" font="Regular; 20" foregroundColor="#00ffcc33" backgroundColor="background" halign="center" transparent="1" />
            <widget name="datepeople" position="370,40" size="820,25" font="Regular; 20" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="monthpeople" position="10,360" size="355,245" font="Regular; 20" foregroundColor="#008f8f8f" backgroundColor="background" halign="left" transparent="1" />
            <widget name="sign" position="370,70" size="820,50" font="Regular; 20" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="holiday" position="370,125" size="820,50" font="Regular; 20" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="description" position="370,180" size="820,410" font="Regular; 20" foregroundColor="#008f8f8f" backgroundColor="background" halign="left" valign="top" transparent="1" />
            <widget name="status" position="371,588" size="648,40" font="Regular; 22" foregroundColor="#3333ff" halign="left" zPosition="5" transparent="1" />

            <!-- TASTI FUNZIONE -->
            <widget name="key_red" position="70,640" size="155,20" font="Regular;20" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_green" position="295,640" size="155,20" font="Regular;20" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_yellow" position="515,640" size="155,20" font="Regular;20" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_blue" position="730,640" size="155,20" font="Regular;20" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />

            <!-- ICONE TASTI -->
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="70,660" size="155,7" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_green.png" position="295,660" size="155,7" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_yellow.png" position="515,660" size="155,7" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_blue.png" position="730,660" size="155,7" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_leftright.png" position="900,640" size="50,24" alphatest="blend" zPosition="5" scale="1" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_updown.png" position="962,640" size="50,24" alphatest="blend" zPosition="5" scale="1" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_ok.png" position="1024,640" size="49,27" alphatest="on" zPosition="5" scale="1" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_menu.png" position="1086,640" size="51,24" alphatest="on" zPosition="5" scale="1" />
        </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self.setup_title = _("Calendar Planner")

        self.year = localtime()[0]
        self.month = localtime()[1]
        self.day = localtime()[2]
        self.selected_day = self.day

        if config.plugins.calendar.events_enabled.value:
            from .event_manager import EventManager
            self.event_manager = EventManager(session)
        else:
            self.event_manager = None

        self.language = config.osd.language.value.split("_")[0].strip()
        self.path = plugin_path

        self.selected_bg_color = None
        self.nowday = False
        self.current_field = None

        self.holiday_cache = {}
        self.cells_by_day = {}

        # Create all UI elements
        for x in range(6):
            self['wn' + str(x)] = Label()

        for x in range(42):
            if x < 8:
                weekname = (_('...'),
                            _('Mon'),
                            _('Tue'),
                            _('Wed'),
                            _('Thu'),
                            _('Fri'),
                            _('Sat'),
                            _('Sun'))
                self['w' + str(x)] = Label(weekname[x])
            self['d' + str(x)] = Label()

        self["Title"] = StaticText(_("Calendar Planner v.%s") % PLUGIN_VERSION)
        self["key_red"] = Label(_("Month -"))
        self["key_green"] = Label(_("Month +"))
        self["key_yellow"] = Label(_("Day -"))
        self["key_blue"] = Label(_("Day +"))

        self["date"] = Label(_("Files is Empty..."))
        self["monthname"] = Label(_(".............."))
        self["datepeople"] = Label(_(".............."))
        self["monthpeople"] = Label(_(".............."))
        self["sign"] = Label(_(".............."))
        self["holiday"] = Label(_(".............."))
        self["description"] = Label(_(".............."))
        self["status"] = Label(_("Calendar Planner | Ready"))

        self["actions"] = ActionMap(
            [
                "CalendarActions",
            ],
            {
                "cancel": self.exit,
                "ok": self.key_ok,

                "red": self._prevmonth,
                "redRepeated": self._prevmonth,
                "green": self._nextmonth,
                "greenRepeated": self._nextmonth,
                "yellow": self._prevday,
                "yellowRepeated": self._prevday,
                "blue": self._nextday,
                "blueRepeated": self._nextday,

                "left": self._prevday,
                "right": self._nextday,
                "up": self._prevmonth,
                "down": self._nextmonth,

                "menu": self.config,
                "info": self.about,
                # "epg": self.about,
                "0": self.show_events,
            }, -1
        )
        self.onLayoutFinish.append(self._paint_calendar)

    def menu_callback(self, result):
        if result:
            result[1]()

    def ok(self):
        selection = self["menu"].getCurrent()
        if selection:
            self.close(selection)

    def key_ok(self):
        """Open main menu with conditional event options"""
        menu = [
            (_("New Date"), self.new_date),
            (_("Edit Date"), self.edit_all_fields),
            (_("Remove Date"), self.remove_date),
            (_("Delete File"), self.delete_file),
        ]

        # ADD EVENT OPTIONS ONLY IF ENABLED
        if config.plugins.calendar.events_enabled.value and self.event_manager:
            menu.extend([
                (_("Manage Events"), self.show_events),
                (_("Add Event"), self.add_event),
                (_("Cleanup past events"), self.cleanup_past_events),
            ])

        # ADD HOLIDAYS
        menu.extend([
            (_("Import Holidays"), self.import_holidays),
            (_("Show Today's Holidays"), self.show_today_holidays),
            (_("Show Upcoming Holidays"), self.show_upcoming_holidays),
            (_("Clear Holiday Database"), self.clear_holiday_database),
        ])
        # ADD UPDATER
        menu.extend([
            (_("Check for Updates"), self.check_for_updates),
        ])

        menu.append((_("Exit"), self.close))

        self.session.openWithCallback(self.menu_callback, MenuDialog, menu)

    def check_for_updates(self):
        """Check for plugin updates"""
        from .update_manager import UpdateManager
        from .updater import PluginUpdater
        print("check_for_updates called from main menu")
        try:
            print("Creating UpdateManager instance...")
            updater = PluginUpdater()
            print("PluginUpdater created successfully")

            latest = updater.get_latest_version()
            print("Direct test - Latest version: %s" % latest)

            # UpdateManager
            UpdateManager.check_for_updates(self.session, self["status"])

        except Exception as e:
            print("Direct test error: %s" % e)
            self["status"].setText(_("Update check error"))
            self.session.open(MessageBox,
                              _("Error: %s") % str(e),
                              MessageBox.TYPE_ERROR)

    def clear_fields(self):
        """Clear all fields for new date (but keep date)"""
        if DEBUG:
            print("[Calendar] Clearing all fields (except date)")

        # Keep the current date
        default_date = "{0}-{1:02d}-{2:02d}".format(self.year, self.month, self.day)
        self["date"].setText(default_date)

        # Clear other fields
        self["datepeople"].setText("")
        self["sign"].setText("")
        self["holiday"].setText("")
        self["description"].setText("")
        self["monthpeople"].setText("")

    def load_data(self):
        """Load data from file and display labels with data"""
        file_path = "{0}base/{1}/day/{2}{3:02d}{4:02d}.txt".format(
            self.path,
            self.language,
            self.year,
            self.month,
            self.day
        )

        # ALWAYS show the current date as default
        default_date = "{0}-{1:02d}-{2:02d}".format(self.year, self.month, self.day)

        if exists(file_path):
            try:
                with open(file_path, "r") as f:
                    lines = f.readlines()

                day_data = {}
                month_data = {}
                current_section = None

                for line in lines:
                    line = line.strip()
                    if line == "[day]":
                        current_section = "day"
                    elif line == "[month]":
                        current_section = "month"
                    elif current_section == "day" and ":" in line:
                        key, value = line.split(":", 1)
                        day_data[key.strip()] = value.strip()
                    elif current_section == "month" and ":" in line:
                        key, value = line.split(":", 1)
                        month_data[key.strip()] = value.strip()

                # Date - use value from file if present, otherwise default date
                date_val = day_data.get("date", default_date)
                self["date"].setText(date_val)

                # Date People - add label
                datepeople_val = day_data.get("datepeople", "")
                if datepeople_val:
                    self["datepeople"].setText(_("Date People: ") + datepeople_val)
                else:
                    self["datepeople"].setText("")

                # Sign - add label
                sign_val = day_data.get("sign", "")
                if sign_val:
                    self["sign"].setText(_("Sign: ") + sign_val)
                else:
                    self["sign"].setText("")

                # Holiday - add label
                holiday_val = day_data.get("holiday", "")
                if holiday_val and holiday_val != "None":
                    self["holiday"].setText(_("Holiday: ") + holiday_val)
                else:
                    self["holiday"].setText("")

                # Description - no label (already multi-line)
                description_val = day_data.get("description", "")
                self["description"].setText(description_val)

                # Month People - add label
                monthpeople_val = month_data.get("monthpeople", "")
                if monthpeople_val:
                    self["monthpeople"].setText(_("Month People: ") + monthpeople_val)
                else:
                    self["monthpeople"].setText("")

            except Exception as e:
                print("[Calendar] Error loading data: {0}".format(str(e)))
                # In case of error, show at least the default date
                self["date"].setText(default_date)
                self.clear_other_fields()
        else:
            if DEBUG:
                print("[Calendar] File not found: {0}".format(file_path))
            # If the file does not exist, show the default date
            self["date"].setText(default_date)
            self.clear_other_fields()

        # Add events if enabled
        if self.event_manager:
            self.add_events_to_description()

    def clear_other_fields(self):
        """Clear all fields except date"""
        self["datepeople"].setText("")
        self["sign"].setText("")
        self["holiday"].setText("")
        self["description"].setText("")
        self["monthpeople"].setText("")

    def save_data(self):
        """Save data to unified file"""
        file_path = "{0}base/{1}/day/{2}{3:02d}{4:02d}.txt".format(
            self.path,
            self.language,
            self.year,
            self.month,
            self.day
        )

        directory = dirname(file_path)
        if not exists(directory):
            try:
                makedirs(directory)
                if DEBUG:
                    print("[Calendar] Created directory: {0}".format(directory))
            except Exception as e:
                print("[Calendar] Error creating directory: {0}".format(str(e)))

        try:
            # Get current values
            date_text = self['date'].getText() or ""
            datepeople_text = self['datepeople'].getText() or ""
            sign_text = self['sign'].getText() or ""
            holiday_text = self['holiday'].getText() or ""
            description_text = self['description'].getText() or ""
            monthpeople_text = self['monthpeople'].getText() or ""

            # IMPORTANT: Remove any event display from description before saving
            # Events should only be in events.json, not in the database file
            if _("TODAY'S EVENTS:") in description_text:
                # Split at the events section and keep only the user's description
                parts = description_text.split(_("TODAY'S EVENTS:"))
                description_text = parts[0].rstrip()
                if DEBUG:
                    print("[Calendar] Cleaned events from description before saving")
            if DEBUG:
                print("[Calendar] Saving description: '{0}'".format(description_text[:50] if description_text else "EMPTY"))

            # Format the file content
            day_data = (
                "[day]\n"
                "date: {0}\n"
                "datepeople: {1}\n"
                "sign: {2}\n"
                "holiday: {3}\n"
                "description: {4}\n\n"
                "[month]\n"
                "monthpeople: {5}\n"
            ).format(
                date_text,
                datepeople_text,
                sign_text,
                holiday_text,
                description_text,  # Clean description without events
                monthpeople_text
            )

            # Write to file
            with open(file_path, "w") as f:
                f.write(day_data)

            if DEBUG:
                print("[Calendar] Data saved successfully to: {0}".format(file_path))

            # After saving, if there are events for this date, add them to display
            if self.event_manager:
                # First load the clean data we just saved
                self["description"].setText(description_text)
                # Then add events for display only
                self.add_events_to_description()

        except Exception as e:
            print("[Calendar] Error saving data: {0}".format(str(e)))
            # Optionally show error to user
            self.session.open(
                MessageBox,
                _("Error saving data"),
                MessageBox.TYPE_ERROR
            )

    def open_virtual_keyboard_for_field(self, field, field_name):
        """
        Open the virtual keyboard for a specific field
        """
        current_text = field.getText()

        if DEBUG:
            print("[Calendar] Editing field '{0}', current text: '{1}'".format(
                field_name, current_text[:50] if current_text else "EMPTY"))

        def calendar_callback(input_text):
            if input_text:
                if DEBUG:
                    print("[Calendar] Field '{0}' updated to: '{1}'".format(
                        field_name, input_text[:50]))
                field.setText(input_text)
                self.save_data()

            self.navigate_to_next_field()

        self.session.openWithCallback(
            calendar_callback,
            VirtualKeyBoard,
            title=field_name,
            text=current_text
        )

    def new_date(self):
        """
        Create a NEW date - clear all fields first
        """
        if DEBUG:
            print("[Calendar] Creating NEW date - clearing all fields")
        self.clear_fields()

        default_date = "{0}-{1:02d}-{2:02d}".format(self.year, self.month, self.day)
        self["date"].setText(default_date)

        self.current_field = self["date"]
        self.open_virtual_keyboard_for_field(self["date"], _("Date"))

    def edit_all_fields(self):
        if DEBUG:
            print("[Calendar] === EDIT ALL FIELDS START ===")

        self.load_data()

        # CLEAN the description from events BEFORE editing
        current_desc = self["description"].getText()
        if _("SCHEDULED EVENTS:") in current_desc:
            parts = current_desc.split(_("SCHEDULED EVENTS:"))
            clean_desc = parts[0].rstrip()
            self["description"].setText(clean_desc)
            if DEBUG:
                print("[Calendar] Cleaned description before editing: '{0}'".format(clean_desc[:50]))

        self.edit_fields_sequence = [
            ("date", _("Edit Date")),
            ("datepeople", _("Edit Date People")),
            ("sign", _("Edit Sign")),
            ("holiday", _("Edit Holiday")),
            ("description", _("Edit Description")),
            ("monthpeople", _("Edit Month People"))
        ]

        self.current_edit_index = 0
        self._edit_next_field()

    def _edit_next_field(self):
        if DEBUG:
            print("[Calendar] _edit_next_field() - index: {0}".format(self.current_edit_index))

        if self.current_edit_index >= len(self.edit_fields_sequence):
            if DEBUG:
                print("[Calendar] ERROR: Index out of range!")
            return

        field_name, title = self.edit_fields_sequence[self.current_edit_index]
        current_text = self[field_name].getText()
        if DEBUG:
            print("[Calendar] Opening VirtualKeyBoard for: {0}".format(field_name))
            print("[Calendar] Current text length: {0}".format(len(current_text)))

        if field_name == "description":
            if DEBUG:
                print("[Calendar] === THIS IS DESCRIPTION FIELD ===")
                print("[Calendar] Text preview: '{0}'".format(current_text[:100]))

        self.session.openWithCallback(
            self._save_edited_field,
            VirtualKeyBoard,
            title=title,
            text=current_text
        )

    def _save_edited_field(self, input_text):
        if DEBUG:
            print("[Calendar] _save_edited_field() - index: {0}".format(self.current_edit_index))

        if self.current_edit_index >= len(self.edit_fields_sequence):
            return

        field_name, _ = self.edit_fields_sequence[self.current_edit_index]

        # Sand input is None or empty, keep the current value
        if input_text is None:
            print("[Calendar] No input received, keeping current value")
            # Do nothing, move on to the next field
        else:
            old_text = self[field_name].getText()
            # If the text is DIFFERENT, then update
            if input_text != old_text:
                if DEBUG:
                    print("[Calendar] Updating field '{0}'".format(field_name))
                self[field_name].setText(input_text)
            else:
                print("[Calendar] Text unchanged for '{0}', skipping".format(field_name))

        self.current_edit_index += 1

        if self.current_edit_index < len(self.edit_fields_sequence):
            self._edit_next_field()
        else:
            if DEBUG:
                print("[Calendar] === EDIT SEQUENCE COMPLETE ===")
            self.save_data()

    def remove_date(self):
        """Remove the date and clear all fields"""
        file_path = "{0}base/{1}/day/{2}{3:02d}{4:02d}.txt".format(
            self.path,
            self.language,
            self.year,
            self.month,
            self.day
        )

        if exists(file_path):
            try:
                with open(file_path, "w") as f:
                    f.write("")

                # Clear all relevant UI fields
                self["date"].setText(_("No file in database..."))
                self["datepeople"].setText("")
                self["sign"].setText("")
                self["holiday"].setText("")
                self["description"].setText("")
                self["monthpeople"].setText("")
                if DEBUG:
                    print("Date removed for m{0}d{1}".format(self.month, self.day))
            except Exception as e:
                print("Error removing date: {0}".format(e))
        else:
            self.session.open(MessageBox, _("File not found!"), MessageBox.TYPE_INFO)

    def delete_file(self):
        """Delete the data file for the selected date and update the UI accordingly."""
        file_path = "{0}base/{1}/day/{2}{3:02d}{4:02d}.txt".format(
            self.path,
            self.language,
            self.year,
            self.month,
            self.day
        )

        if exists(file_path):
            try:
                remove(file_path)
                self["date"].setText(_("No file in database..."))
                if DEBUG:
                    print("File deleted: {0}".format(file_path))
            except Exception as e:
                print("Error deleting file: {0}".format(e))
        else:
            self.session.open(MessageBox, _("File not found!"), MessageBox.TYPE_INFO)

    def _paint_calendar(self):
        # Clear original states when the month changes
        if hasattr(self, 'original_cell_states'):
            self.original_cell_states = {}
        if hasattr(self, 'previous_selected_day'):
            self.previous_selected_day = None

        monthname = (_('January'),
                     _('February'),
                     _('March'),
                     _('April'),
                     _('May'),
                     _('June'),
                     _('July'),
                     _('August'),
                     _('September'),
                     _('October'),
                     _('November'),
                     _('December'))

        i = 1
        ir = 0
        d1 = datetime.date(self.year, self.month, 1)
        d2 = d1.weekday()

        if self.month == 12:
            sdt1 = datetime.date(self.year + 1, 1, 1) - datetime.timedelta(1)
        else:
            sdt1 = datetime.date(self.year, self.month + 1, 1) - datetime.timedelta(1)

        self.monthday = int(sdt1.day)
        self.monthname = monthname[self.month - 1]
        self["monthname"].setText(str(self.year) + ' ' + str(self.monthname))

        for x in range(8):
            if x < 8:
                self['w' + str(x)].instance.setBackgroundColor(parseColor('#333333'))
                self['w' + str(x)].instance.setForegroundColor(parseColor('white'))

        for x in range(6):
            self['wn' + str(x)].instance.setBackgroundColor(parseColor('#333333'))
            self['wn' + str(x)].instance.setForegroundColor(parseColor('white'))

        # Informational texts
        self["monthname"].instance.setForegroundColor(parseColor('yellow'))
        self["date"].instance.setForegroundColor(parseColor('yellow'))
        self["datepeople"].instance.setForegroundColor(parseColor('white'))
        self["monthpeople"].instance.setForegroundColor(parseColor('#8F8F8F'))
        self["sign"].instance.setForegroundColor(parseColor('white'))
        self["holiday"].instance.setForegroundColor(parseColor('white'))
        self["description"].instance.setForegroundColor(parseColor('#8F8F8F'))
        self["status"].instance.setForegroundColor(parseColor('yellow'))

        # Keys
        self["key_red"].instance.setForegroundColor(parseColor('white'))
        self["key_green"].instance.setForegroundColor(parseColor('white'))
        self["key_yellow"].instance.setForegroundColor(parseColor('white'))
        self["key_blue"].instance.setForegroundColor(parseColor('white'))

        # Load holidays for the current month into cache
        if config.plugins.calendar.holidays_enabled.value:
            current_month_holidays = self._load_month_holidays(self.year, self.month)
        else:
            current_month_holidays = {}

        for x in range(42):
            self['d' + str(x)].setText('')
            self['d' + str(x)].instance.clearForegroundColor()
            self['d' + str(x)].instance.clearBackgroundColor()

            if (x + 7) % 7 == 0:
                ir += 1
                if ir < 5:
                    self['wn' + str(ir)].setText('')

            if x >= d2 and i <= self.monthday:
                r = datetime.datetime(self.year, self.month, i)
                wn1 = r.isocalendar()[1]
                if ir <= 5:
                    self['wn' + str(ir - 1)].setText('%0.2d' % wn1)

                    # IMPORTANT: save the cell reference for this day
                    self.cells_by_day[i] = 'd' + str(x)

                    self['d' + str(x)].setText(str(i))

                    # Check for holidays FIRST (priority 1)
                    is_holiday = False
                    if config.plugins.calendar.holidays_enabled.value:
                        if i in current_month_holidays:
                            is_holiday = True
                            holiday_color = config.plugins.calendar.holidays_color.value
                            self['d' + str(x)].instance.setForegroundColor(parseColor(holiday_color))
                            if config.plugins.calendar.holidays_show_indicators.value:
                                current_text = self['d' + str(x)].getText()
                                self['d' + str(x)].setText(current_text + " H")

                    # Check for events (priority 2 - only if not a holiday)
                    has_events = False
                    if not is_holiday and self.event_manager and config.plugins.calendar.events_show_indicators.value:
                        date_str = "{0}-{1:02d}-{2:02d}".format(self.year, self.month, i)
                        day_events = self.event_manager.get_events_for_date(date_str)

                        if day_events:
                            has_events = True
                            event_color = config.plugins.calendar.events_color.value
                            self['d' + str(x)].instance.setForegroundColor(parseColor(event_color))
                            current_text = self['d' + str(x)].getText()
                            self['d' + str(x)].setText(current_text + " *")

                    # Weekend colors (priority 3 - only if not holiday and not event)
                    if not is_holiday and not has_events:
                        if datetime.date(self.year, self.month, i).weekday() == 5:
                            self['d' + str(x)].instance.setForegroundColor(parseColor('yellow'))
                        elif datetime.date(self.year, self.month, i).weekday() == 6:
                            self['d' + str(x)].instance.setForegroundColor(parseColor('red'))
                        else:
                            self['d' + str(x)].instance.setForegroundColor(parseColor('white'))

                    # TODAY background (highest priority - always applied)
                    if datetime.date(self.year, self.month, i) == datetime.date.today():
                        self.nowday = True
                        self['d' + str(x)].instance.setBackgroundColor(parseColor('green'))

                    i = i + 1

        # Load content for the current date
        self.load_data()

        # IMPORTANT: apply selection AFTER drawing everything
        self._highlight_selected_day(self.selected_day)

    def show_events(self):
        """Show the events view for the current date - with safety checks"""

        # 1. Master switch check
        if not config.plugins.calendar.events_enabled.value:
            if DEBUG:
                print("[Calendar] Event system disabled, skipping show_events")
            return

        # 2. Check that EventManager exists
        if self.event_manager is None:
            # This should never happen if events_enabled = True
            # But initialize it for safety
            try:
                from .event_manager import EventManager
                self.event_manager = EventManager(self.session)
                if DEBUG:
                    print("[Calendar] EventManager initialized on-demand")
            except Exception as e:
                print("[Calendar] Error initializing EventManager: {0}".format(e))
                return

        # 3. Proceed normally
        current_date = datetime.date(self.year, self.month, self.day)

        def refresh_calendar(result=None):
            """Refresh calendar after event changes"""
            if result:
                print("[Calendar] Event changes detected, refreshing...")
            self._paint_calendar()
            self.load_data()
            if DEBUG:
                print("[Calendar] Calendar refreshed after event changes")

        self.session.openWithCallback(
            refresh_calendar,
            EventsView,
            self.event_manager,
            current_date
        )

    def event_added_callback(self, result):
        """Callback after adding event"""
        if result:
            self._paint_calendar()
            self.load_data()

    def add_event(self):
        """Add new event - with safety check"""
        if not config.plugins.calendar.events_enabled.value or not self.event_manager:
            self.session.open(
                MessageBox,
                _("Event system is disabled. Enable it in settings."),
                MessageBox.TYPE_INFO
            )
            return

        try:
            from .event_dialog import EventDialog
            date_str = "{0}-{1:02d}-{2:02d}".format(
                self.year,
                self.month,
                self.day
            )
            self.session.openWithCallback(
                self.event_added_callback,
                EventDialog,
                self.event_manager,
                date=date_str
            )
        except Exception as e:
            print("[Calendar] Error opening EventDialog: {0}".format(e))
            import traceback
            traceback.print_exc()
            self.session.open(
                MessageBox,
                _("Error opening event dialog"),
                MessageBox.TYPE_ERROR
            )

    def cleanup_past_events(self):
        """Clean up past non-recurring events"""
        if not config.plugins.calendar.events_enabled.value or not self.event_manager:
            self.session.open(
                MessageBox,
                _("Event system is disabled. Enable it in settings."),
                MessageBox.TYPE_INFO
            )
            return

        # Directly call the method on the existing event_manager
        removed = self.event_manager.cleanup_past_events()

        # Show the result
        if removed > 0:
            message = _("Removed {0} past events").format(removed)
            # Refresh the calendar
            self._paint_calendar()
            self.load_data()
        else:
            message = _("No past events to remove")

        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)

    def clear_holiday_cache(self):
        """Clear holiday cache (call after importing new holidays)"""
        self.holiday_cache = {}

    def import_holidays_callback(self, result=None):
        """Callback after importing holidays"""

        def refresh_after_import():
            self.clear_holiday_cache()
            self._paint_calendar()
            self.load_data()
            if DEBUG:
                print("[Calendar] Calendar refreshed after import operation")

        self.refresh_timer = eTimer()
        try:
            self.refresh_timer_conn = self.refresh_timer.timeout.connect(refresh_after_import)
        except AttributeError:
            self.refresh_timer.callback.append(refresh_after_import)
        self.refresh_timer.start(2000, True)

    def import_holidays(self):
        """Import holidays from Holidata.net"""
        try:
            from .holidays import HolidaysImportScreen
            if DEBUG:
                print("DEBUG: Opening HolidaysImportScreen")
            self.session.openWithCallback(
                self.import_holidays_callback,
                HolidaysImportScreen,
                plugin_path=self.path,
                language=self.language
            )

        except Exception as e:
            print("Holidays import error: " + str(e))
            self.session.open(
                MessageBox,
                "Error: " + str(e),
                MessageBox.TYPE_ERROR
            )

    def show_today_holidays(self):
        """Show today's holidays"""
        try:
            from .holidays import show_holidays_today
            show_holidays_today(self.session)
        except Exception as e:
            print("Show holidays error: " + str(e))
            self.session.open(
                MessageBox,
                "Error: " + str(e),
                MessageBox.TYPE_ERROR
            )

    def show_upcoming_holidays(self):
        """Show upcoming holidays"""
        try:
            from .holidays import show_upcoming_holidays as holidays_upcoming
            holidays_upcoming(self.session, days=30)
        except Exception as e:
            print("Show upcoming holidays error: " + str(e))
            self.session.open(
                MessageBox,
                "Error: " + str(e),
                MessageBox.TYPE_ERROR
            )

    def clear_holiday_database(self):
        """Clears all holiday fields from files"""
        try:
            from .holidays import clear_holidays_dialog
            clear_holidays_dialog(self.session)

            def refresh_calendar():
                self.clear_holiday_cache()
                self._paint_calendar()
                self.load_data()
                if DEBUG:
                    print("[Calendar] Calendar refreshed after holiday database clearing")

            self.refresh_timer = eTimer()
            try:
                self.refresh_timer_conn = self.refresh_timer.timeout.connect(refresh_calendar)
            except AttributeError:
                self.refresh_timer.callback.append(refresh_calendar)
            self.refresh_timer.start(2000, True)

        except Exception as e:
            print("Clear holidays error: " + str(e))
            self.session.open(
                MessageBox,
                "Error: " + str(e),
                MessageBox.TYPE_ERROR
            )

    def navigate_to_next_field(self):
        """
        Navigate to the next input field in sequence, opening the virtual keyboard for each.
        Once all fields have been updated, save the data.
        """
        if self.current_field == self["date"]:
            self.open_virtual_keyboard_for_field(self["datepeople"], _("Date People"))
            self.current_field = self["datepeople"]
        elif self.current_field == self["datepeople"]:
            self.open_virtual_keyboard_for_field(self["sign"], _("Sign"))
            self.current_field = self["sign"]
        elif self.current_field == self["sign"]:
            self.open_virtual_keyboard_for_field(self["holiday"], _("Holiday"))
            self.current_field = self["holiday"]
        elif self.current_field == self["holiday"]:
            self.open_virtual_keyboard_for_field(self["description"], _("Description"))
            self.current_field = self["description"]
        elif self.current_field == self["description"]:
            self.open_virtual_keyboard_for_field(self["monthpeople"], _("Month People"))
            self.current_field = self["monthpeople"]
        else:
            if DEBUG:
                print("All fields have been updated.")
            self.save_data()

    def add_events_to_description(self):
        """Add events to description display"""
        try:
            date_str = "{0}-{1:02d}-{2:02d}".format(self.year, self.month, self.day)
            day_events = self.event_manager.get_events_for_date(date_str)

            if day_events:
                # Create visual separator
                separator = "\n" + "-" * 40 + "\n"
                events_text = separator + _("SCHEDULED EVENTS:") + "\n"

                for event in day_events:
                    time_str = event.time[:5] if event.time else "00:00"

                    # Repeat indicators
                    repeat_symbol = ""
                    if event.repeat == "daily":
                        repeat_symbol = " [D]"
                    elif event.repeat == "weekly":
                        repeat_symbol = " [W]"
                    elif event.repeat == "monthly":
                        repeat_symbol = " [M]"
                    elif event.repeat == "yearly":
                        repeat_symbol = " [Y]"

                    status_symbol = " *" if event.enabled else " [OFF]"

                    # ADD LABELS TO DISPLAY
                    labels_display = ""
                    if event.labels:
                        labels_display = " [" + ", ".join(event.labels[:3]) + "]"  # Show only first 3 labels

                    events_text += "- {0} - {1}{2}{3}{4}\n".format(
                        time_str,
                        event.title,
                        repeat_symbol,
                        status_symbol,
                        labels_display
                    )

                    if event.description:
                        desc = event.description
                        if len(desc) > 80:
                            desc = desc[:77] + "..."
                        events_text += "  {0}\n".format(desc)

                events_text += "-" * 40

                # Get current description
                current_desc = self["description"].getText()

                # Remove any existing events display
                if _("SCHEDULED EVENTS:") in current_desc:
                    parts = current_desc.split(_("SCHEDULED EVENTS:"))
                    current_desc = parts[0].rstrip()

                # Add events to display only
                self["description"].setText(current_desc + events_text)
                if DEBUG:
                    print("[Calendar] Events displayed with labels")

        except Exception as e:
            print("[Calendar] Error displaying events: {0}".format(e))

    def _load_month_holidays(self, year, month):
        """Load holidays for a specific month into cache"""
        cache_key = (year, month)

        # Return if already in cache
        if cache_key in self.holiday_cache:
            return self.holiday_cache[cache_key]

        month_holidays = {}
        language = config.osd.language.value.split("_")[0].strip()

        # Iterate through possible days in month (1-31)
        for day in range(1, 32):
            file_path = "{0}base/{1}/day/{2}{3:02d}{4:02d}.txt".format(
                self.path,
                language,
                year,
                month,
                day
            )

            if exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()

                    # Parse holiday field
                    for line in content.split('\n'):
                        line = line.strip()
                        if line.startswith('holiday:'):
                            holiday_value = line.split(':', 1)[1].strip()
                            if holiday_value and holiday_value != "None":
                                month_holidays[day] = holiday_value
                                break  # Found holiday, move to next day
                except Exception as e:
                    print("[Calendar] Error reading holiday file {0}: {1}".format(file_path, str(e)))

        # Store in cache
        self.holiday_cache[cache_key] = month_holidays
        return month_holidays

    def _highlight_selected_day(self, day):
        """Highlight selected day with blue background and white text"""
        # controlla se questo giorno è OGGI (stesso anno, mese e giorno)
        current_time = localtime()
        is_today = (day == current_time[2] and
                    self.year == current_time[0] and
                    self.month == current_time[1])

        # First, restore the original color of the previously selected day (if any and not today)
        if hasattr(self, 'previous_selected_day') and self.previous_selected_day:
            # MODIFICA: controlla se il previous_selected_day era oggi
            was_today = (self.previous_selected_day == current_time[2] and
                         self.year == current_time[0] and
                         self.month == current_time[1])

            if not was_today and hasattr(self, 'original_cell_states') and self.previous_selected_day in self.original_cell_states:
                state = self.original_cell_states[self.previous_selected_day]
                for x in range(42):
                    cell_text = self['d' + str(x)].getText()
                    if cell_text:
                        clean_text = cell_text.replace(' H', '').replace(' *', '').replace('H', '').replace('*', '').strip()
                        if clean_text.isdigit() and int(clean_text) == self.previous_selected_day:
                            # Restore original color
                            self['d' + str(x)].instance.setForegroundColor(state['color'])

                            # Restore original text with marker if needed
                            display_text = str(self.previous_selected_day)
                            if state['is_holiday'] and config.plugins.calendar.holidays_enabled.value and config.plugins.calendar.holidays_show_indicators.value:
                                display_text += " H"
                            elif state['has_events'] and config.plugins.calendar.events_enabled.value and config.plugins.calendar.events_show_indicators.value:
                                display_text += " *"
                            self['d' + str(x)].setText(display_text)

                            # Clear blue background
                            self['d' + str(x)].instance.clearBackgroundColor()
                            break

        # Clear backgrounds of all non-today cells and save original states
        if not hasattr(self, 'original_cell_states'):
            self.original_cell_states = {}

        for x in range(42):
            cell_text = self['d' + str(x)].getText()
            if cell_text and cell_text.replace(' H', '').replace(' *', '').replace('H', '').replace('*', '').strip().isdigit():
                cell_day = int(cell_text.replace(' H', '').replace(' *', '').replace('H', '').replace('*', '').strip())

                # Skip today - it keeps green background
                # usa is_today invece di day != today
                cell_is_today = (cell_day == current_time[2] and
                               self.year == current_time[0] and
                               self.month == current_time[1])

                if not cell_is_today:
                    # Clear any selection background (blue)
                    self['d' + str(x)].instance.clearBackgroundColor()

                    # Save original state for this day if not already saved
                    if cell_day not in self.original_cell_states:
                        is_holiday = ' H' in cell_text or 'H' in cell_text
                        has_events = ' *' in cell_text or '*' in cell_text

                        # Determine original color based on configuration
                        original_color = parseColor('white')  # default

                        # Check holiday color (if holidays enabled and has holiday)
                        if is_holiday and config.plugins.calendar.holidays_enabled.value:
                            original_color = parseColor(config.plugins.calendar.holidays_color.value)
                        # Check event color (if events enabled and has events)
                        elif has_events and config.plugins.calendar.events_enabled.value:
                            original_color = parseColor(config.plugins.calendar.events_color.value)
                        else:
                            # Check weekend colors
                            try:
                                weekday = datetime.date(self.year, self.month, cell_day).weekday()
                                if weekday == 5:  # Saturday
                                    original_color = parseColor('yellow')
                                elif weekday == 6:  # Sunday
                                    original_color = parseColor('red')
                            except:
                                pass

                        self.original_cell_states[cell_day] = {
                            'color': original_color,
                            'is_holiday': is_holiday,
                            'has_events': has_events
                        }

        # Set new selection
        self.selected_day = day

        # Save current as previous for next time
        self.previous_selected_day = day

        # Apply blue background and white text to selected day
        if not is_today:  # usa is_today invece di day != today
            for x in range(42):
                cell_text = self['d' + str(x)].getText()
                if cell_text:
                    clean_text = cell_text.replace(' H', '').replace(' *', '').replace('H', '').replace('*', '').strip()
                    if clean_text.isdigit() and int(clean_text) == day:
                        # Save original state if not already saved
                        if day not in self.original_cell_states:
                            is_holiday = ' H' in cell_text or 'H' in cell_text
                            has_events = ' *' in cell_text or '*' in cell_text

                            # Determine original color based on configuration
                            original_color = parseColor('white')  # default

                            # Check holiday color (if holidays enabled and has holiday)
                            if is_holiday and config.plugins.calendar.holidays_enabled.value:
                                original_color = parseColor(config.plugins.calendar.holidays_color.value)
                            # Check event color (if events enabled and has events)
                            elif has_events and config.plugins.calendar.events_enabled.value:
                                original_color = parseColor(config.plugins.calendar.events_color.value)
                            else:
                                # Check weekend colors
                                try:
                                    weekday = datetime.date(self.year, self.month, day).weekday()
                                    if weekday == 5:  # Saturday
                                        original_color = parseColor('yellow')
                                    elif weekday == 6:  # Sunday
                                        original_color = parseColor('red')
                                except:
                                    pass

                            self.original_cell_states[day] = {
                                'color': original_color,
                                'is_holiday': is_holiday,
                                'has_events': has_events
                            }

                        # Apply blue background and white text
                        self['d' + str(x)].instance.setBackgroundColor(parseColor('blue'))
                        self['d' + str(x)].instance.setForegroundColor(parseColor('white'))

                        # Remove markers when selected (clean display) - only show number
                        self['d' + str(x)].setText(str(day))
                        break
        else:
            # If selecting today, ensure text is visible on green background
            for x in range(42):
                cell_text = self['d' + str(x)].getText()
                if cell_text:
                    clean_text = cell_text.replace(' H', '').replace(' *', '').replace('H', '').replace('*', '').strip()
                    if clean_text.isdigit() and int(clean_text) == day:
                        # Today has green background, use white text
                        self['d' + str(x)].instance.setForegroundColor(parseColor('white'))

                        # Also save original state for today if not already saved
                        if day not in self.original_cell_states:
                            is_holiday = ' H' in cell_text or 'H' in cell_text
                            has_events = ' *' in cell_text or '*' in cell_text

                            # For today, we use white text regardless (for contrast on green)
                            original_color = parseColor('white')

                            self.original_cell_states[day] = {
                                'color': original_color,
                                'is_holiday': is_holiday,
                                'has_events': has_events
                            }
                        break

    def _nextday(self):
        try:
            current_date = datetime.date(self.year, self.month, self.selected_day)
            next_date = current_date + datetime.timedelta(days=1)
            self.year = next_date.year
            self.month = next_date.month
            self.day = next_date.day
            self.selected_day = self.day
        except ValueError:
            if self.month == 12:
                self.year += 1
                self.month = 1
                self.day = 1
                self.selected_day = 1
            else:
                self.month += 1
                self.day = 1
                self.selected_day = 1

        self._paint_calendar()

    def _prevday(self):
        try:
            current_date = datetime.date(self.year, self.month, self.selected_day)
            prev_date = current_date - datetime.timedelta(days=1)
            self.year = prev_date.year
            self.month = prev_date.month
            self.day = prev_date.day
            self.selected_day = self.day
        except ValueError:
            if self.month == 1:
                self.year -= 1
                self.month = 12
                self.day = 31
                self.selected_day = 31
            else:
                self.month -= 1
                last_day = (datetime.date(self.year, self.month + 1, 1) - datetime.timedelta(days=1)).day
                self.day = last_day
                self.selected_day = last_day

        self._paint_calendar()

    def _nextmonth(self):
        if self.month == 12:
            self.month = 1
            self.year = self.year + 1
        else:
            self.month = self.month + 1

        # Check if the selected day exists in the new month
        try:
            # Try to create a date with the selected day
            datetime.date(self.year, self.month, self.selected_day)
            # If no error is raised, the day exists in the new month
            self.day = self.selected_day
        except ValueError:
            # If the day does not exist (e.g. February 31), use the last day of the month
            last_day = (datetime.date(self.year, self.month + 1, 1) - datetime.timedelta(days=1)).day
            self.day = last_day
            self.selected_day = last_day

        self._paint_calendar()

    def _prevmonth(self):
        if self.month == 1:
            self.month = 12
            self.year = self.year - 1
        else:
            self.month = self.month - 1

        # Check if the selected day exists in the new month
        try:
            # Try to create a date with the selected day
            datetime.date(self.year, self.month, self.selected_day)
            # If no error is raised, the day exists in the new month
            self.day = self.selected_day
        except ValueError:
            # If the day does not exist (e.g. April 31), use the last day of the month
            last_day = (datetime.date(self.year, self.month + 1, 1) - datetime.timedelta(days=1)).day
            self.day = last_day
            self.selected_day = last_day

        self._paint_calendar()

    def config(self):
        self.session.open(settingCalendar)

    def about(self):
        info_text = (
            "Calendar Planner v.%s\n"
            "Developer: on base plugin from Sirius0103 Rewrite Code by Lululla\n"
            "Homepage: www.corvoboys.org\n\n"
            "Homepage: www.linuxsat-support.com\n\n"
            "Homepage: www.gisclub.tv\n\n"
        ) % PLUGIN_VERSION
        self.session.open(MessageBox, info_text, MessageBox.TYPE_INFO)

    def cancel(self):
        self.close(None)

    def exit(self):
        self.close()


def customSetupDom(setup=None, plugin=None):
    """Version that supports setup.it.xml, setup.de.xml, etc."""
    # Determine language
    try:
        lang = config.osd.language.value.split('_')[0]
    except:
        lang = "en"

    # Locate plugin directory
    if plugin:
        plugin_dir = resolveFilename(SCOPE_PLUGINS, plugin)
    else:
        from Tools.Directories import SCOPE_SKIN
        plugin_dir = resolveFilename(SCOPE_SKIN, "")

    # List of XML files to try
    xml_files = [
        "setup." + lang + ".xml",  # setup.it.xml
        "setup.xml"                # default
    ]

    setupFile = None
    for xml_file in xml_files:
        if plugin_dir:
            test_path = join(plugin_dir, xml_file)
            if fileExists(test_path):
                setupFile = test_path
                print("[Calendar] ✓ Using localized setup:", xml_file)
                break

    # If not found, fall back to the original
    if not setupFile:
        return original_setupDom(setup, plugin)

    # Local cache
    if not hasattr(customSetupDom, 'domSetups'):
        customSetupDom.domSetups = {}
        customSetupDom.setupModTimes = {}

    try:
        modTime = getmtime(setupFile)
    except OSError:
        return original_setupDom(setup, plugin)

    # Check cache
    if (setupFile in customSetupDom.domSetups and
            setupFile in customSetupDom.setupModTimes and
            customSetupDom.setupModTimes[setupFile] == modTime):
        return customSetupDom.domSetups[setupFile]

    # Read file
    fileDom = fileReadXML(setupFile)
    if fileDom:
        customSetupDom.domSetups[setupFile] = fileDom
        customSetupDom.setupModTimes[setupFile] = modTime
        return fileDom

    return original_setupDom(setup, plugin)


Screens.Setup.setupDom = customSetupDom
Screens.Setup.setupdom = customSetupDom


class settingCalendar(Setup):
    def __init__(self, session, parent=None):
        Setup.__init__(self, session, setup="settingCalendar", plugin="Extensions/Calendar")
        self.parent = parent

    def keySave(self):
        Setup.keySave(self)


def mainMenu(menuid):
    if menuid != "information":
        return []
    return [(_("Calendar"), menuCalendar, "Calendar", None)]


def menuCalendar(session, **kwargs):
    session.open(Calendar)


def main(session, **kwargs):
    session.open(Calendar)


def Plugins(**kwargs):
    result = []

    result.append(PluginDescriptor(
        name=_("Calendar"),
        description=_("Calendar with events and notifications"),
        where=[PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU],
        icon="plugin.png",
        fnc=main
    ))

    if config.plugins.calendar.menu.value == 'yes':
        result.append(PluginDescriptor(
            name=_("Calendar"),
            where=PluginDescriptor.WHERE_MENU,
            fnc=mainMenu
        ))

    return result
