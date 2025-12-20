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
#  • Asterisk (*) indicator for days with events          #
#  • Week numbers display                                 #
#  • Smooth month navigation                              #
#                                                         #
#  CONFIGURATION:                                         #
#  • Event system enable/disable                          #
#  • Notification settings (duration, advance time)       #
#  • Audio notification type (short/notify/alert/none)    #
#  • Enable/disable sound playback                        #
#  • Event color selection                                #
#  • Show event indicators toggle                         #
#  • Menu integration option                              #
#                                                         #
#  KEY CONTROLS - MAIN CALENDAR:                          #
#   OK          - Open main menu (New/Edit/Remove/Events) #
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
#   OK          - Edit current field                      #
    RED         - Cancel                                  #
    GREEN       - Save event                              #
    YELLOW      - Delete event (edit mode only)           #
    UP/DOWN     - Navigate between fields                 #
    LEFT/RIGHT  - Change selection options                #
#                                                         #
#  KEY CONTROLS - EVENTS VIEW:                            #
#   OK          - Edit selected event                     #
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
#  • Uses eServiceReference for audio playback            #
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
#  • Audio debug: check play_notification_sound() calls   #
#                                                         #
#  CREDITS:                                               #
#  • Original Calendar plugin: Sirius0103                 #
#  • Event system & modifications: Lululla                #
#  • Notification system: Custom implementation           #
#  • Audio system: Enigma2 eServiceReference integration  #
#  • Testing & feedback: Enigma2 community                #
#                                                         #
#  VERSION HISTORY:                                       #
#  • v1.0 - Basic calendar functionality                  #
#  • v1.1 - Complete event system added                   #
#                                                         #
#  Last Updated: 2025-12-20                               #
#  Status: Stable with event & audio system               #
###########################################################
"""

import datetime
from time import localtime
from enigma import getDesktop
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Setup import Setup
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.ActionMap import ActionMap  # , HelpableActionMap
from Components.MenuList import MenuList
from Components.ScrollLabel import ScrollLabel
from Components.Sources.StaticText import StaticText
from Components.Label import Label
from os.path import exists, dirname
from os import remove, makedirs
from skin import parseColor
from Components.config import config, ConfigSubsection, ConfigSelection, ConfigYesNo


from . import _, plugin_path
from .events_view import EventsView

currversion = '1.1'


def init_calendar_config():
    """Initialize all calendar configurations"""
    if not hasattr(config.plugins, 'calendar'):
        config.plugins.calendar = ConfigSubsection()

    config.plugins.calendar.menu = ConfigSelection(default="no", choices=[
        ("no", _("no")),
        ("yes", _("yes"))])
    config.plugins.calendar.events_enabled = ConfigYesNo(default=True)
    config.plugins.calendar.events_notifications = ConfigYesNo(default=True)
    config.plugins.calendar.highlight = ConfigYesNo(default=True)
    config.plugins.calendar.events_show_indicators = ConfigYesNo(default=True)
    config.plugins.calendar.events_color = ConfigSelection(
        choices=[
            ("#FF0000FF", "Blue"),      # Opaque blue
            ("#FF00FFFF", "Cyan"),      # Opaque cyan
            ("#FF800080", "Purple"),    # Opaque purple
            ("#FFFF0000", "Red"),       # Opaque red
            ("#FFFF00FF", "Magenta"),   # Opaque magenta
            ("#FFFFA500", "Orange"),    # Opaque orange
            ("#FFFFFF00", "Yellow"),    # Opaque yellow
            ("#FFFFFFFF", "White"),     # Opaque white
        ],
        default="#FF00FFFF"  # Opaque cyan as default
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


init_calendar_config()


class MenuDialog(Screen):
    skin = """
    <screen name="MenuDialog" position="center,center" size="600,400" title="Edit Settings">
        <widget name="menu" position="10,10" size="580,380" itemHeight="40" font="Regular;28" scrollbarMode="showOnDemand" />
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
        <screen name="Calendar" position="60,52" size="1800,975" title=" " flags="wfNoBorder">
            <eLabel position="30,915" size="1740,5" backgroundColor="#00555555" zPosition="1" />

            <widget name="w0" position="15,60" size="62,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w1" position="81,60" size="62,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w2" position="148,60" size="62,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w3" position="216,60" size="62,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w4" position="283,60" size="62,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w5" position="351,60" size="62,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w6" position="418,60" size="62,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w7" position="486,60" size="62,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />

            <widget name="wn0" position="15,128" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn1" position="15,195" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn2" position="15,263" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn3" position="15,330" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn4" position="15,398" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn5" position="15,465" size="60,60" font="Regular;30" halign="center" valign="center" backgroundColor="#00808080" />

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

            <widget name="monthname" position="15,8" size="533,45" font="Regular; 36" foregroundColor="#00ffcc33" backgroundColor="background" halign="center" transparent="1" />
            <widget name="date" position="555,10" size="1230,40" font="Regular; 30" foregroundColor="#00ffcc33" backgroundColor="background" halign="center" transparent="1" />
            <widget name="datepeople" position="555,60" size="1230,38" font="Regular; 30" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="monthpeople" position="15,540" size="533,368" font="Regular; 30" foregroundColor="#008f8f8f" backgroundColor="background" halign="left" transparent="1" />
            <widget name="sign" position="555,105" size="1230,75" font="Regular; 30" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="holiday" position="555,188" size="1230,75" font="Regular; 30" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="description" position="555,270" size="1230,638" font="Regular; 30" foregroundColor="#008f8f8f" backgroundColor="background" halign="left" transparent="1" />

            <widget name="key_red" position="113,928" size="200,30" font="Regular;30" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_green" position="443,928" size="200,30" font="Regular;30" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_yellow" position="773,928" size="200,30" font="Regular;30" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_blue" position="1103,928" size="200,30" font="Regular;30" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />

            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="110,960" size="230,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_green.png" position="440,960" size="230,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_yellow.png" position="771,960" size="230,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_blue.png" position="1099,960" size="230,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_leftright.png" position="1323,930" size="75,36" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_updown.png" position="1417,930" size="75,36" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_ok.png" position="1505,930" size="74,40" alphatest="on" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_menu.png" position="1598,930" size="77,36" alphatest="on" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_epg.png" position="1695,930" size="76,37" alphatest="on" />
        </screen>"""
    else:
        skin = """
        <!-- Calendar -->
       <screen name="Calendar" position="360,215" size="1200,650" title=" " flags="wfNoBorder">
            <eLabel position="20,605" size="1160,3" backgroundColor="#00555555" zPosition="1" />

            <widget name="w0" position="10,40" size="42,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w1" position="55,40" size="42,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w2" position="100,40" size="42,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w3" position="145,40" size="42,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w4" position="190,40" size="42,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w5" position="235,40" size="42,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w6" position="280,40" size="42,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="w7" position="325,40" size="42,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />

            <widget name="wn0" position="10,85" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn1" position="10,130" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn2" position="10,175" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn3" position="10,220" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn4" position="10,265" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />
            <widget name="wn5" position="10,310" size="40,40" font="Regular;20" halign="center" valign="center" backgroundColor="#00808080" />

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

            <widget name="monthname" position="10,5" size="355,30" font="Regular; 24" foregroundColor="#00ffcc33" backgroundColor="background" halign="center" transparent="1" />
            <widget name="date" position="370,5" size="820,30" font="Regular; 20" foregroundColor="#00ffcc33" backgroundColor="background" halign="center" transparent="1" />
            <widget name="datepeople" position="370,40" size="820,25" font="Regular; 20" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="monthpeople" position="10,360" size="355,245" font="Regular; 20" foregroundColor="#008f8f8f" backgroundColor="background" halign="left" transparent="1" />
            <widget name="sign" position="370,70" size="820,50" font="Regular; 20" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="holiday" position="370,125" size="820,50" font="Regular; 20" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="description" position="370,180" size="820,425" font="Regular; 20" foregroundColor="#008f8f8f" backgroundColor="background" halign="left" transparent="1" />

            <widget name="key_red" position="37,615" size="150,25" font="Regular;24" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_green" position="231,615" size="180,25" font="Regular;24" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_yellow" position="451,616" size="150,25" font="Regular;24" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_blue" position="661,615" size="150,25" font="Regular;24" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="37,640" size="150,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_green.png" position="230,640" size="180,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_yellow.png" position="452,640" size="150,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_blue.png" position="660,640" size="150,10" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_leftright.png" position="823,612" size="75,36" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_updown.png" position="899,612" size="75,36" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_ok.png" position="974,612" size="71,38" alphatest="blend" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_menu.png" position="1048,612" size="74,35" alphatest="on" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_epg.png" position="1124,612" size="74,35" alphatest="on" />
        </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self.setup_title = _("Calendar Planner")

        self.year = localtime()[0]
        self.month = localtime()[1]
        self.day = localtime()[2]

        if config.plugins.calendar.events_enabled.value:
            from .event_manager import EventManager
            self.event_manager = EventManager(session)
        else:
            self.event_manager = None

        self.language = config.osd.language.value.split("_")[0].strip()
        self.path = plugin_path

        self.selected_day = self.day
        self.nowday = False
        self.current_field = None

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

        self["Title"] = StaticText(_("Calendar Planner v.%s") % currversion)
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
        self["description"] = ScrollLabel(_(".............."))

        self["actions"] = ActionMap(
            [
                "CalendarActions",
                "OkCancelActions",
                "ColorActions",
                "DirectionActions",
                "MenuActions",
                "EPGSelectActions"
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
                "epg": self.about,
                "0": self.show_events,
            }, -1
        )
        self.onLayoutFinish.append(self._paint_calendar)

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

        # ⬇️ ADD EVENT OPTIONS ONLY IF ENABLED
        if config.plugins.calendar.events_enabled.value and self.event_manager:
            menu.extend([
                (_("Manage Events"), self.show_events),
                (_("Add Event"), self.add_event),
                (_("Cleanup past events"), self.cleanup_past_events),
            ])

        menu.append((_("Exit"), self.close))

        self.session.openWithCallback(self.menu_callback, MenuDialog, menu)

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

    def event_added_callback(self, result):
        """Callback after adding event"""
        if result:
            self._paint_calendar()
            self.load_data()

    def manage_events(self):
        """Manage events"""
        if self.event_manager:
            from .events_view import EventsView
            current_date = datetime.date(self.year, self.month, self.day)
            self.session.open(EventsView, self.event_manager, current_date)

    def menu_callback(self, result):
        if result:
            result[1]()

    def show_events(self):
        """Show the events view for the current date - with safety checks"""

        # 1. Master switch check
        if not config.plugins.calendar.events_enabled.value:
            print("[Calendar] Event system disabled, skipping show_events")
            return

        # 2. Check that EventManager exists
        if self.event_manager is None:
            # This should never happen if events_enabled = True
            # But initialize it for safety
            try:
                from .event_manager import EventManager
                self.event_manager = EventManager(self.session)
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
            print("[Calendar] Calendar refreshed after event changes")

        self.session.openWithCallback(
            refresh_calendar,
            EventsView,
            self.event_manager,
            current_date
        )

    def open_virtual_keyboard_for_field(self, field, field_name):
        """
        Open the virtual keyboard for a specific field, allowing user input.
        After input is entered and saved, automatically navigate to the next field.
        """
        current_text = field.getText()

        def calendar_callback(input_text):
            if input_text:
                field.setText(input_text)
                self.save_data()

            self.navigate_to_next_field()

        self.session.openWithCallback(
            calendar_callback,
            VirtualKeyBoard,
            title=field_name,
            text=current_text
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

        # Call EventManager cleanup method directly
        removed = self.event_manager.cleanup_past_events()

        # Show result
        if removed > 0:
            message = _("Removed {0} past events").format(removed)
            # Reload calendar
            self._paint_calendar()
        else:
            message = _("No past events to remove")

        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)

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
            print("All fields have been updated.")
            self.save_data()

    def new_date(self):
        """
        Open the virtual keyboard to input a new date, focusing on the 'date' field.
        """
        self.current_field = self["date"]
        self.open_virtual_keyboard_for_field(self["date"], _("Date"))

    def save_data(self):
        """Save data in the unified file"""
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
            except Exception as e:
                print("Error creating directory: {0}".format(e))

        try:
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
                self['date'].getText(),
                self['datepeople'].getText(),
                self['sign'].getText(),
                self['holiday'].getText(),
                self['description'].getText(),
                self['monthpeople'].getText()
            )

            with open(file_path, "w") as f:
                f.write(day_data)

        except Exception as e:
            print("Error saving data: {0}".format(e))

    def edit_all_fields(self):
        """
        Start the process to edit all fields one by one by loading existing data first,
        then sequentially opening the virtual keyboard for each field.
        """
        self.load_data()

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
        """
        Open the virtual keyboard to edit the next field in the sequence.
        If all fields have been edited, save all data to the file.
        """
        if self.current_edit_index < len(self.edit_fields_sequence):
            field_name, title = self.edit_fields_sequence[self.current_edit_index]
            current_text = self[field_name].getText()
            self.session.openWithCallback(
                self._save_edited_field,
                VirtualKeyBoard,
                title=title,
                text=current_text
            )
        else:
            self.save_data()  # Save all fields to file at the end
            print("All fields edited and saved.")

    def _save_edited_field(self, input_text):
        """
        Save the edited input text to the current field and proceed to edit the next field.
        """
        if input_text is not None:
            field_name, _ = self.edit_fields_sequence[self.current_edit_index]
            self[field_name].setText(input_text)
        self.current_edit_index += 1
        self._edit_next_field()

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
                print("File deleted: {0}".format(file_path))
            except Exception as e:
                print("Error deleting file: {0}".format(e))
        else:
            self.session.open(MessageBox, _("File not found!"), MessageBox.TYPE_INFO)

    def load_data(self):
        """Load data from the file and populate the corresponding fields in the UI."""
        file_path = "{0}base/{1}/day/{2}{3:02d}{4:02d}.txt".format(
            self.path,
            self.language,
            self.year,
            self.month,
            self.day
        )

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

                self["date"].setText(day_data.get("date", ""))
                self["datepeople"].setText(day_data.get("datepeople", ""))
                self["sign"].setText(day_data.get("sign", ""))
                self["holiday"].setText(day_data.get("holiday", ""))
                self["description"].setText(day_data.get("description", ""))
                self["monthpeople"].setText(month_data.get("monthpeople", ""))

            except Exception as e:
                print("Error loading data: {0}".format(e))
                self.clear_fields()
        else:
            self.clear_fields()

        if self.event_manager:
            self.add_events_to_description()

    def clear_fields(self):
        """Clear all fields"""
        self["date"].setText(_("No file in database..."))
        self["datepeople"].setText("")
        self["sign"].setText("")
        self["holiday"].setText("")
        self["description"].setText("")
        self["monthpeople"].setText("")

    def add_events_to_description(self):
        """Add events to the description"""
        try:
            date_str = "{0}-{1:02d}-{2:02d}".format(self.year, self.month, self.day)
            day_events = self.event_manager.get_events_for_date(date_str)

            if day_events:
                events_text = "\n\n" + _("TODAY'S EVENTS:") + "\n"
                for event in day_events:
                    time_str = event.time[:5] if event.time else "00:00"
                    repeat_symbol = ""
                    if event.repeat == "daily":
                        repeat_symbol = " [D]"
                    elif event.repeat == "weekly":
                        repeat_symbol = " [W]"
                    elif event.repeat == "monthly":
                        repeat_symbol = " [M]"
                    elif event.repeat == "yearly":
                        repeat_symbol = " [Y]"

                    status_symbol = " *" if event.enabled else " [X]"
                    events_text += "• {0} - {1}{2}{3}\n".format(
                        time_str,
                        event.title,
                        repeat_symbol,
                        status_symbol
                    )

                    if event.description:
                        desc = event.description
                        if len(desc) > 80:
                            desc = desc[:77] + "..."
                        events_text += "  {0}\n".format(desc)

                current_desc = self["description"].getText()
                if current_desc == _("No file in database..."):
                    self["description"].setText(events_text.strip())
                else:
                    self["description"].setText(current_desc + events_text)

        except Exception as e:
            print("Error adding events to description: {0}".format(e))

    def _paint_calendar(self):
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
                    self['d' + str(x)].setText(str(i))
                    self['d' + str(x)].instance.setForegroundColor(parseColor('white'))

                # Check if there are events (only if enabled in config)
                if self.event_manager and config.plugins.calendar.events_show_indicators.value:
                    date_str = "{0}-{1:02d}-{2:02d}".format(self.year, self.month, i)
                    day_events = self.event_manager.get_events_for_date(date_str)

                    if day_events:
                        # Use color from configuration
                        event_color = config.plugins.calendar.events_color.value
                        self['d' + str(x)].instance.setForegroundColor(parseColor(event_color))
                        # Add asterisk
                        current_text = self['d' + str(x)].getText()
                        self['d' + str(x)].setText(current_text + " *")

                # Special colors (overridden if events exist)
                if datetime.date(self.year, self.month, i) == datetime.date.today():
                    self.nowday = True
                    self['d' + str(x)].instance.setBackgroundColor(parseColor('green'))

                if datetime.date(self.year, self.month, i).weekday() == 5:
                    self['d' + str(x)].instance.setForegroundColor(parseColor('yellow'))

                if datetime.date(self.year, self.month, i).weekday() == 6:
                    self['d' + str(x)].instance.setForegroundColor(parseColor('red'))

                i = i + 1

        # Load content for the current date
        self.load_data()
        self._highlight_selected_day(self.selected_day)

    def _highlight_selected_day(self, day):
        """Highlight selected day with different background color"""
        today = localtime()[2]
        for x in range(42):
            # If this is the selected day, highlight it
            if self['d' + str(x)].getText() == str(day) and day != today:
                self['d' + str(x)].instance.setBackgroundColor(parseColor('blue'))
                self['d' + str(x)].instance.setForegroundColor(parseColor('white'))

    def onDaySelected(self, day):
        """Method to update selected day manually (when user selects a day)"""
        self.selected_day = day
        self._paint_calendar()

    def _nextday(self):
        try:
            # Create a date object for the current day
            current_date = datetime.date(self.year, self.month, self.day)
            # Calculate next day
            next_date = current_date + datetime.timedelta(days=1)
            self.year = next_date.year
            self.month = next_date.month
            self.day = next_date.day
        except ValueError:
            # Handle invalid date (e.g., day out of range)
            if self.month == 12:
                self.year += 1
                self.month = 1
                self.day = 1
            else:
                self.month += 1
                self.day = 1
        # self._highlight_selected_day(self.selected_day)
        self.selected_day = self.day
        self._paint_calendar()

    def _prevday(self):
        try:
            # Create a date object for the current day
            current_date = datetime.date(self.year, self.month, self.day)
            # Calculate previous day
            prev_date = current_date - datetime.timedelta(days=1)
            self.year = prev_date.year
            self.month = prev_date.month
            self.day = prev_date.day
        except ValueError:
            # Handle invalid date (e.g., day out of range)
            if self.month == 1:
                self.year -= 1
                self.month = 12
                # Last day of December
                self.day = 31
            else:
                self.month -= 1
                # Get last day of previous month
                last_day = (datetime.date(self.year, self.month + 1, 1) - datetime.timedelta(days=1)).day
                self.day = last_day

        # self._highlight_selected_day(self.selected_day)
        self.selected_day = self.day
        self._paint_calendar()

    def _nextmonth(self):
        if self.month == 12:
            self.month = 1
            self.year = self.year + 1
        else:
            self.month = self.month + 1
        self.day = 1
        self._paint_calendar()

    def _prevmonth(self):
        if self.month == 1:
            self.month = 12
            self.year = self.year - 1
        else:
            self.month = self.month - 1
            self.year = self.year
        self.day = 1
        self._paint_calendar()

    def config(self):
        self.session.open(settingCalendar)

    def about(self):
        info_text = (
            "Calendar Planner v.%s\n"
            "Developer: on base plugin from Sirius0103 mod by Lululla\n"
            "Homepage: www.gisclub.tv\n\n"
        ) % currversion
        self.session.open(MessageBox, info_text, MessageBox.TYPE_INFO)

    def cancel(self):
        self.close(None)

    def exit(self):
        self.close()


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
