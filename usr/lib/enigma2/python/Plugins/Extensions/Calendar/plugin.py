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
import datetime
from time import localtime
from os import remove, makedirs
from os.path import exists, dirname, join

from enigma import getDesktop
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Setup import Setup
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Components.ActionMap import ActionMap  # , HelpableActionMap
from Components.Label import Label
from Components.Sources.StaticText import StaticText
from Components.config import (
    config,
    ConfigSubsection,
    ConfigSelection,
    ConfigYesNo,
)
from enigma import eTimer
from skin import parseColor

from . import _, PLUGIN_PATH, PLUGIN_VERSION, PLUGIN_ICON
from .events_view import EventsView
from .event_manager import EventManager
from .birthday_manager import BirthdayManager
from .contacts_view import ContactsView
from .birthday_dialog import BirthdayDialog
from .database_converter import DatabaseConverter, auto_convert_database
from .formatters import format_field_display, MenuDialog


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

    # DATABASE FORMAT CONFIGURATION
    config.plugins.calendar.database_format = ConfigSelection(
        choices=[
            ("legacy", _("Legacy format (text files)")),
            ("vcard", _("vCard format (standard)"))
        ],
        default="legacy"
    )
    config.plugins.calendar.auto_convert = ConfigYesNo(default=True)


DEBUG = config.plugins.calendar.debug_enabled.value if hasattr(config.plugins, 'calendar') and hasattr(config.plugins.calendar, 'debug_enabled') else False
init_calendar_config()


class Calendar(Screen):
    if (getDesktop(0).size().width() >= 1920):
        skin = """
        <!-- Calendar -->
        <screen name="Calendar" position="center,center" size="1900,1060" title=" " flags="wfNoBorder" zPosition="0">
            <eLabel backgroundColor="#001a2336" cornerRadius="30" position="10,980" size="1880,90" zPosition="0" />
            <eLabel name="" position="0,0" size="1920,1080" zPosition="-1" cornerRadius="20" backgroundColor="#00171a1c" foregroundColor="#00171a1c" />
            <widget source="session.VideoPicture" render="Pig" position="1402,687" zPosition="19" size="475,271" backgroundColor="transparent" transparent="0" cornerRadius="20" />

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
            <widget name="date" position="555,10" size="1330,45" font="Regular; 34" foregroundColor="#00ffcc33" backgroundColor="background" halign="center" transparent="1" />
            <widget name="datepeople" position="555,60" size="1330,45" font="Regular; 30" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="monthpeople" position="15,540" size="533,427" font="Regular; 30" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="sign" position="555,110" size="1330,75" font="Regular; 30" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="holiday" position="555,188" size="1330,75" font="Regular; 30" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="description" position="555,270" size="1330,696" font="Regular; 30" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" valign="top" transparent="1" />
            <widget name="status" position="1351,971" size="537,45" font="Regular; 32" foregroundColor="#1edb76" zPosition="5" halign="center" transparent="1" />

            <!-- TASTI FUNZIONE -->
            <widget name="key_red" position="110,995" size="230,35" font="Regular;30" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_green" position="440,995" size="230,35" font="Regular;30" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_yellow" position="773,995" size="230,35" font="Regular;30" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_blue" position="1100,995" size="230,35" font="Regular;30" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />

            <!-- ICONE TASTI -->
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="110,1030" size="230,10" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_green.png" position="440,1030" size="230,10" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_yellow.png" position="771,1030" size="230,10" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_blue.png" position="1100,1030" size="230,10" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_leftright.png" position="1453,1020" size="75,36" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_updown.png" position="1547,1020" size="75,36" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_ok.png" position="1640,1020" size="74,40" alphatest="on" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_menu.png" position="1728,1020" size="77,36" alphatest="on" zPosition="5" />
        </screen>"""
    else:
        skin = """
        <!-- Calendar -->
        <screen name="Calendar" position="center,center" size="1280,720" title=" " flags="wfNoBorder">
            <eLabel backgroundColor="#001a2336" cornerRadius="20" position="10,655" size="1260,60" zPosition="0" />
            <eLabel name="" position="-80,-270" size="1280,720" zPosition="-1" cornerRadius="12" backgroundColor="#00171a1c" foregroundColor="#00171a1c" />
            <widget source="session.VideoPicture" render="Pig" position="943,466" zPosition="19" size="315,180" backgroundColor="transparent" transparent="0" cornerRadius="10" />

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
            <widget name="date" position="370,5" size="895,30" font="Regular; 24" foregroundColor="#00ffcc33" backgroundColor="background" halign="center" transparent="1" />
            <widget name="datepeople" position="370,35" size="895,40" font="Regular; 20" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="monthpeople" position="10,360" size="355,290" font="Regular; 20" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="sign" position="370,75" size="895,50" font="Regular; 20" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="holiday" position="370,125" size="895,50" font="Regular; 20" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" transparent="1" />
            <widget name="description" position="370,175" size="895,475" font="Regular; 20" foregroundColor="#00f4f4f4" backgroundColor="background" halign="left" valign="top" transparent="1" />
            <widget name="status" position="894,656" size="378,25" font="Regular; 20" foregroundColor="#1edb76" halign="center" zPosition="5" transparent="1" />

            <!-- TASTI FUNZIONE -->
            <widget name="key_red" position="70,675" size="155,20" font="Regular;20" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_green" position="295,675" size="155,20" font="Regular;20" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_yellow" position="515,675" size="155,20" font="Regular;20" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />
            <widget name="key_blue" position="730,675" size="155,20" font="Regular;20" halign="center" valign="center" backgroundColor="#20000000" zPosition="5" transparent="1" />

            <!-- ICONE TASTI -->
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_red.png" position="70,695" size="155,7" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_green.png" position="295,695" size="155,7" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_yellow.png" position="515,695" size="155,7" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_blue.png" position="730,695" size="155,7" alphatest="blend" zPosition="5" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_leftright.png" position="985,685" size="50,24" alphatest="blend" zPosition="5" scale="1" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_updown.png" position="1037,685" size="50,24" alphatest="blend" zPosition="5" scale="1" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_ok.png" position="1089,685" size="50,24" alphatest="on" zPosition="5" scale="1" />
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/Calendar/buttons/key_menu.png" position="1141,685" size="50,24" alphatest="on" zPosition="5" scale="1" />
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
            self.event_manager = EventManager(session)
        else:
            self.event_manager = None

        self.language = config.osd.language.value.split("_")[0].strip()

        self.birthday_manager = BirthdayManager()
        print("[Calendar] BirthdayManager initialized, contacts: {0}".format(
            len(self.birthday_manager.contacts)))

        # Force reload to be sure
        self.birthday_manager.load_all_contacts()
        print("[Calendar] Contacts after reload: {0}".format(
            len(self.birthday_manager.contacts)))

        self.database_format = config.plugins.calendar.database_format.value

        self.selected_bg_color = None
        self.nowday = False
        self.current_field = None

        self.holiday_cache = {}
        self.cells_by_day = {}

        if config.plugins.calendar.auto_convert.value:
            self.auto_convert_database()

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
                "0": self.show_events,
            }, -1
        )
        self.onLayoutFinish.append(self._paint_calendar)

    def menu_callback(self, result=None):
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

            (_("Manage Contacts"), self.show_contacts),
            (_("Add Contact"), self.add_contact),
            (_("Import vCard File"), self.import_vcard_file),
            (_("Export vCard File"), self.export_vcard_file),
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

        # ADD DATABASE CONVERSION OPTIONS
        menu.extend([
            (_("Database Converter"), self.database_converter),  # NUOVO!
        ])
        if self.database_format == "legacy":
            menu.append((_("Convert to vCard format"), self.convert_to_vcard))
        else:
            menu.append((_("Convert to legacy format"), self.convert_to_legacy))

        # ADD UPDATER
        menu.extend([
            (_("Check for Updates"), self.check_for_updates),
        ])

        self.session.openWithCallback(self.menu_callback, MenuDialog, menu)

    def check_for_updates(self):
        """Check for plugin updates"""
        print("check_for_updates called from main menu")
        try:
            print("Creating UpdateManager instance...")
            from .updater import PluginUpdater
            updater = PluginUpdater()
            print("PluginUpdater created successfully")
            latest = updater.get_latest_version()
            print("Direct test - Latest version: %s" % latest)
            from .update_manager import UpdateManager
            UpdateManager.check_for_updates(self.session, self["status"])
            self.update_cache_status()
        except Exception as e:
            print("Direct test error: %s" % e)
            self["status"].setText(_("Update check error"))

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
        """Load data from file - UNIFIED PARSER that reads any format"""
        if self.database_format == "vcard":
            file_path = "{0}base/vcard/{1}/{2}{3:02d}{4:02d}.txt".format(
                PLUGIN_PATH,
                self.language,
                self.year,
                self.month,
                self.day
            )
        else:
            file_path = "{0}base/{1}/day/{2}{3:02d}{4:02d}.txt".format(
                PLUGIN_PATH,
                self.language,
                self.year,
                self.month,
                self.day
            )

        default_date = "{0}-{1:02d}-{2:02d}".format(self.year, self.month, self.day)

        if exists(file_path):
            try:
                with open(file_path, "r") as f:
                    lines = f.readlines()

                # Parse file content with unified parser
                data = self._parse_file_content(lines, self.database_format)

                # Display data with correct mapping
                self._display_parsed_data(data, default_date)

            except Exception as e:
                print("[Calendar] Error loading data: {0}".format(str(e)))
                # In case of error, show at least the default date
                self._load_default_data(default_date)
                self.clear_other_fields()
        else:
            if DEBUG:
                print("[Calendar] File not found: {0}".format(file_path))
            self._load_default_data(default_date)
            self.clear_other_fields()

        self.add_contacts_to_display()

        # Add events if enabled
        if self.event_manager:
            self.add_events_to_description()

        # Add events if enabled
        if self.event_manager:
            self.add_events_to_description()

    def _parse_file_content(self, lines, format_type):
        """
        Unified parser that reads any format and returns standardized data

        Mapping CORRECTED:
        Legacy → vCard
        date: → DATE:
        datepeople: → FN:
        sign: → CATEGORIES:
        holiday: → holiday: (STAYS SAME - don't change!)
        description: → NOTE:
        monthpeople: → CONTACTS:
        """
        data = {}
        current_section = None

        for line in lines:
            line = line.strip()

            # Detect sections
            if line == "[day]" or line == "[contact]":
                current_section = "main"
            elif line == "[month]":
                current_section = "month"
            elif line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1]

            # Parse key-value pairs
            elif current_section and ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                # Store with original key
                data[key] = value

        return data

    def _display_parsed_data(self, data, default_date):
        """Display parsed data with correct labels"""
        # Determine which fields to use based on format
        if self.database_format == "vcard":
            # vCard format mapping
            date_val = data.get("DATE:", data.get("BDAY:", default_date))
            datepeople_val = data.get("FN:", "")
            sign_val = data.get("CATEGORIES:", "")
            holiday_val = data.get("holiday:", data.get("NOTE:", ""))  # holiday: stays first priority
            description_val = data.get("NOTE:", data.get("DESCRIPTION:", ""))
            monthpeople_val = data.get("CONTACTS:", data.get("ORG:", ""))
        else:
            # Legacy format
            date_val = data.get("date", default_date)
            datepeople_val = data.get("datepeople", "")
            sign_val = data.get("sign", "")
            holiday_val = data.get("holiday", "")
            description_val = data.get("description", "")
            monthpeople_val = data.get("monthpeople", "")

        # Display values with labels
        self["date"].setText(date_val)

        if datepeople_val:
            self["datepeople"].setText(_("Date People: ") + datepeople_val)
        else:
            self["datepeople"].setText("")

        if sign_val:
            self["sign"].setText(_("Sign: ") + sign_val)
        else:
            self["sign"].setText("")

        if holiday_val and holiday_val != "None":
            self["holiday"].setText(_("Holiday: ") + holiday_val)
        else:
            self["holiday"].setText("")

        self["description"].setText(description_val)

        if monthpeople_val:
            self["monthpeople"].setText(_("Month People: ") + monthpeople_val)
        else:
            self["monthpeople"].setText("")

    def _load_default_data(self, default_date):
        """Load default data when file doesn't exist"""
        self["date"].setText(default_date)
        self["datepeople"].setText("")
        self["sign"].setText("")
        self["holiday"].setText("")
        self["description"].setText("")
        self["monthpeople"].setText("")

    def convert_to_vcard(self):
        """Convert all existing data to vCard format"""

        def conversion_callback(result):
            if result:
                config.plugins.calendar.database_format.value = "vcard"
                config.plugins.calendar.database_format.save()
                self.database_format = "vcard"
                self._paint_calendar()
                self.load_data()
                self.session.open(
                    MessageBox,
                    _("Database converted to vCard format"),
                    MessageBox.TYPE_INFO
                )

        self.session.openWithCallback(
            conversion_callback,
            MessageBox,
            _("Convert all existing data to vCard format?"),
            MessageBox.TYPE_YESNO
        )

    def convert_to_legacy(self):
        """Convert back to legacy format"""
        config.plugins.calendar.database_format.value = "legacy"
        config.plugins.calendar.database_format.save()
        self.database_format = "legacy"
        self._paint_calendar()
        self.load_data()
        self.session.open(
            MessageBox,
            _("Using legacy database format"),
            MessageBox.TYPE_INFO
        )

    def clear_other_fields(self):
        """Clear all fields except date"""
        self["datepeople"].setText("")
        self["sign"].setText("")
        self["holiday"].setText("")
        self["description"].setText("")
        self["monthpeople"].setText("")

    def save_data(self):
        """Save data to file - supports both formats"""
        if self.database_format == "vcard":
            self._save_vcard_data()
        else:
            self._save_legacy_data()

    def _save_legacy_data(self):
        """Save data to unified file in legacy format"""
        file_path = "{0}base/{1}/day/{2}{3:02d}{4:02d}.txt".format(
            PLUGIN_PATH,
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
            # Get current values and remove labels
            date_text = self._clean_field_text(self['date'].getText())
            datepeople_text = self._clean_field_text(self['datepeople'].getText(), "Date People: ")
            sign_text = self._clean_field_text(self['sign'].getText(), "Sign: ")
            holiday_text = self._clean_field_text(self['holiday'].getText(), "Holiday: ")
            description_text = self._clean_field_text(self['description'].getText())
            monthpeople_text = self._clean_field_text(self['monthpeople'].getText(), "Month People: ")

            # Clean events from description before saving
            if _("SCHEDULED EVENTS:") in description_text:
                parts = description_text.split(_("SCHEDULED EVENTS:"))
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
                print("[Calendar] Legacy data saved successfully to: {0}".format(file_path))

            # After saving, if there are events for this date, add them to display
            # if self.event_manager:
                # # First load the clean data we just saved
                # self["description"].setText(description_text)
                # # Then add events for display only
                # self.add_events_to_description()

        except Exception as e:
            print("[Calendar] Error saving legacy data: {0}".format(str(e)))
            self.session.open(
                MessageBox,
                _("Error saving data"),
                MessageBox.TYPE_ERROR
            )

    def _save_vcard_data(self):
        """Save in vCard format"""
        file_path = "{0}base/vcard/{1}/{2}{3:02d}{4:02d}.txt".format(
            PLUGIN_PATH,
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
                print("[Calendar] Error creating directory: {0}".format(str(e)))

        try:
            # Get current values and remove labels
            date_text = self._clean_field_text(self['date'].getText())
            datepeople_text = self._clean_field_text(self['datepeople'].getText(), "Date People: ")
            sign_text = self._clean_field_text(self['sign'].getText(), "Sign: ")
            holiday_text = self._clean_field_text(self['holiday'].getText(), "Holiday: ")
            description_text = self._clean_field_text(self['description'].getText())
            monthpeople_text = self._clean_field_text(self['monthpeople'].getText(), "Month People: ")

            # Clean events from description before saving
            if _("SCHEDULED EVENTS:") in description_text:
                parts = description_text.split(_("SCHEDULED EVENTS:"))
                description_text = parts[0].rstrip()

            # Format as vCard-like file
            # MAPPING CORRECTED:
            # date: → DATE:
            # datepeople: → FN:
            # sign: → CATEGORIES:
            # holiday: → holiday: (STAYS SAME!)
            # description: → NOTE:
            # monthpeople: → CONTACTS:

            contact_data = (
                "[contact]\n"
                "DATE: {0}\n"
                "FN: {1}\n"
                "CATEGORIES: {2}\n"
                "holiday: {3}\n"
                "NOTE: {4}\n"
                "CONTACTS: {5}\n"
            ).format(
                date_text,
                datepeople_text,
                sign_text,
                holiday_text,
                description_text,
                monthpeople_text
            )

            with open(file_path, "w") as f:
                f.write(contact_data)

            print("[Calendar] vCard data saved to: {0}".format(file_path))

        except Exception as e:
            print("[Calendar] Error saving vCard data: {0}".format(str(e)))

    def _clean_field_text(self, text, prefix=""):
        """Remove label prefix from field text"""
        if not text:
            return ""

        if prefix and text.startswith(prefix):
            return text[len(prefix):].strip()

        return text.strip()

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

    def show_contacts(self):
        """Show contacts list - WITH PROPER REFRESH"""

        def contacts_closed_callback(changes_made):
            print("[Calendar] ContactsView closed, changes_made:", changes_made)

            if changes_made:
                print("[Calendar] Refreshing calendar after contacts changes")
                self.birthday_manager.load_all_contacts()

                if hasattr(self, 'original_cell_states'):
                    self.original_cell_states = {}

                self._paint_calendar()
                self.load_data()

                print("[Calendar] Calendar fully refreshed")
            else:
                print("[Calendar] No changes in contacts")

        self.session.openWithCallback(
            contacts_closed_callback,
            ContactsView,
            self.birthday_manager
        )

    def add_contact(self):
        """Add new contact"""
        self.session.openWithCallback(
            self.contact_updated_callback,
            BirthdayDialog,
            self.birthday_manager
        )

    def add_contacts_to_display(self):
        """Add contact information to display"""
        try:
            date_str = "{0}-{1:02d}-{2:02d}".format(self.year, self.month, self.day)
            day_contacts = self.birthday_manager.get_contacts_for_date(date_str)

            if day_contacts:
                contacts_text = _("CONTACTS WITH BIRTHDAYS TODAY:\n\n")

                for contact in day_contacts:
                    name = contact.get('FN', 'Unknown')
                    age = self._calculate_age(contact.get('BDAY', ''))
                    phone = contact.get('TEL', '')
                    email = contact.get('EMAIL', '')

                    contact_line = "• {0}".format(name)
                    if age:
                        contact_line += " ({0})".format(age)

                    if phone:
                        phone_display = format_field_display(phone)
                        contact_line += "\n  Tel: {0}".format(phone_display)

                    if email:
                        email_display = format_field_display(email)
                        contact_line += "\n  Email: {0}".format(email_display)

                    contacts_text += contact_line + "\n\n"

                current_desc = self["description"].getText()

                if _("CONTACTS WITH BIRTHDAYS TODAY:") in current_desc:
                    parts = current_desc.split(_("CONTACTS WITH BIRTHDAYS TODAY:"))
                    current_desc = parts[0].rstrip()

                separator = "\n" + "-" * 40 + "\n"
                self["description"].setText(current_desc + separator + contacts_text.rstrip())

        except Exception as e:
            print("[Calendar] Error displaying contacts: {0}".format(e))

    def auto_convert_database(self):
        """Auto-convert database based on configuration"""
        try:
            print("[Calendar] Checking for auto-conversion...")
            print("[Calendar] Current format: {0}".format(self.database_format))
            print("[Calendar] Auto-convert enabled: {0}".format(
                config.plugins.calendar.auto_convert.value))

            converted = auto_convert_database(
                self.language,
                self.database_format
            )

            if converted:
                print("[Calendar] Database auto-converted successfully")
                # Ricarica i dati dopo la conversione
                self._paint_calendar()
                self.load_data()

                # Mostra messaggio all'utente
                self.session.open(
                    MessageBox,
                    _("Database has been automatically converted to {0} format.").format(
                        self.database_format),
                    MessageBox.TYPE_INFO,
                    timeout=5
                )
            else:
                print("[Calendar] No conversion needed")

        except Exception as e:
            print("[Calendar] Auto-convert error: {0}".format(str(e)))
            # Non mostrare errore all'utente, è solo un'opzione automatica

    def _calculate_age(self, bday_str):
        """Calculate age from birthday string"""
        if not bday_str:
            return ""

        try:
            from datetime import datetime
            birth_date = datetime.strptime(bday_str, "%Y-%m-%d")
            today = datetime.now()

            age = today.year - birth_date.year
            # Adjust if birthday hasn't occurred this year
            if (today.month, today.day) < (birth_date.month, birth_date.day):
                age -= 1

            return str(age)
        except:
            return ""

    def import_vcard_file(self):
        """Import contacts from a vCard file"""
        print("[Calendar] DEBUG: Starting vCard import function")

        try:
            from .vcf_importer import VCardImporter
            print("[Calendar] DEBUG: VCardImporter imported successfully")

            print("[Calendar] DEBUG: Opening VCardImporter screen")
            self.session.open(
                VCardImporter,
                self.birthday_manager
            )

        except ImportError as e:
            print("[Calendar] ERROR: Import failed: {}".format(e))
            import traceback
            traceback.print_exc()

            self.session.open(
                MessageBox,
                _("vCard import feature not available: {0}").format(str(e)),
                MessageBox.TYPE_INFO
            )
        except Exception as e:
            print("[Calendar] ERROR: Unexpected error: {}".format(e))
            import traceback
            traceback.print_exc()

    def export_vcard_file(self):
        """Export all contacts to vCard file in /tmp"""
        try:
            # Prima controlla se ci sono contatti
            if len(self.birthday_manager.contacts) == 0:
                self.session.open(
                    MessageBox,
                    _("No contacts to export.\n\nAdd contacts first via Contacts menu."),
                    MessageBox.TYPE_INFO
                )
                return

            # Menu per scegliere l'ordinamento
            menu = [
                (_("Sort by name (alphabetical)"), lambda: self.do_export('name')),
                (_("Sort by birthday (month/day)"), lambda: self.do_export('birthday')),
                (_("Sort by category"), lambda: self.do_export('category')),
                (_("No sorting (original order)"), lambda: self.do_export('none')),
            ]

            self.session.openWithCallback(
                lambda choice: choice[1]() if choice else None,
                MenuDialog,
                menu
            )

        except Exception as e:
            print("[Calendar] Error in export_vcard_file: {0}".format(str(e)))
            self.session.open(
                MessageBox,
                _("Error: {0}").format(str(e)),
                MessageBox.TYPE_ERROR
            )

    def do_export(self, sort_method='name'):
        """Perform export with specified sort method"""
        try:
            from .vcf_importer import export_contacts_to_vcf
            export_path = "/tmp/calendar.vcf"
            self["status"].setText(_("Exporting contacts..."))
            count = export_contacts_to_vcf(self.birthday_manager, export_path, sort_method)

            if count > 0:
                sort_text = {
                    'name': _("sorted by name"),
                    'birthday': _("sorted by birthday"),
                    'category': _("sorted by category"),
                    'none': _("not sorted")
                }

                message = _("Contacts exported successfully!\n\nFile: {0}\nContacts: {1}\n({2})").format(
                    export_path, count, sort_text.get(sort_method, ''))
                self.session.open(
                    MessageBox,
                    message,
                    MessageBox.TYPE_INFO
                )
            else:
                self.session.open(
                    MessageBox,
                    _("Export failed or no contacts to export"),
                    MessageBox.TYPE_INFO
                )

            # Reset status
            self["status"].setText(_("Calendar Planner | Ready"))

        except Exception as e:
            print("[Calendar] Error in do_export: {0}".format(str(e)))
            self.session.open(
                MessageBox,
                _("Export error: {0}").format(str(e)),
                MessageBox.TYPE_ERROR
            )

    def database_converter(self):
        """Open database converter dialog"""
        try:
            print("[Calendar DEBUG] Plugin path: {0}".format(PLUGIN_PATH))
            print("[Calendar DEBUG] Language: {0}".format(self.language))

            legacy_path = join(PLUGIN_PATH, "base", self.language, "day")
            vcard_path = join(PLUGIN_PATH, "base", "vcard", self.language)

            print("[Calendar DEBUG] Legacy path exists: {0} -> {1}".format(
                legacy_path, exists(legacy_path)))
            print("[Calendar DEBUG] vCard path exists: {0} -> {1}".format(
                vcard_path, exists(vcard_path)))

            self.session.open(
                DatabaseConverter,
                self.language
            )
        except Exception as e:
            print("[Calendar] Error opening database converter: {0}".format(str(e)))
            import traceback
            traceback.print_exc()
            self.session.open(
                MessageBox,
                _("Database converter error: {0}").format(str(e)),
                MessageBox.TYPE_ERROR
            )

    def contact_updated_callback(self, result=None):
        """Callback after contact operations"""
        print("[Calendar DEBUG] Contact callback called with result: {0}".format(result))

        self.birthday_manager.load_all_contacts()
        self._paint_calendar()
        self.load_data()

        if result:
            print("[Calendar] Contact operation successful")
        else:
            print("[Calendar] Contact operation cancelled or no changes")

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
        if self.database_format == "vcard":
            file_path = "{0}base/vcard/{1}/{2}{3:02d}{4:02d}.txt".format(
                PLUGIN_PATH,
                self.language,
                self.year,
                self.month,
                self.day
            )
        else:
            file_path = "{0}base/{1}/day/{2}{3:02d}{4:02d}.txt".format(
                PLUGIN_PATH,
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
        """Delete the data file for the selected date"""
        if self.database_format == "vcard":
            file_path = "{0}base/vcard/{1}/{2}{3:02d}{4:02d}.txt".format(
                PLUGIN_PATH,
                self.language,
                self.year,
                self.month,
                self.day
            )
        else:
            file_path = "{0}base/{1}/day/{2}{3:02d}{4:02d}.txt".format(
                PLUGIN_PATH,
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

    def event_added_callback(self, result=None):
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
            # Use correct path based on format
            if self.database_format == "vcard":
                file_path = "{0}base/vcard/{1}/{2}{3:02d}{4:02d}.txt".format(
                    PLUGIN_PATH,
                    language,
                    year,
                    month,
                    day
                )
            else:
                file_path = "{0}base/{1}/day/{2}{3:02d}{4:02d}.txt".format(
                    PLUGIN_PATH,
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
        """Open configuration"""
        def config_closed_callback(result=None):
            self.holiday_cache = {}
            self._paint_calendar()
            self.load_data()

        self.session.openWithCallback(config_closed_callback, settingCalendar)

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


class settingCalendar(Setup):
    def __init__(self, session, parent=None):
        Setup.__init__(self, session, setup="settingCalendar", plugin="Extensions/Calendar")
        self.parent = parent

    def keySave(self):
        Setup.keySave(self)

        if self.parent:
            old_format = self.parent.database_format
            new_format = config.plugins.calendar.database_format.value
            if old_format != new_format:
                print("[settingCalendar] Database format changed: {0} -> {1}".format(
                    old_format, new_format))

                if config.plugins.calendar.auto_convert.value:
                    print("[settingCalendar] Auto-converting database...")
                    self.parent.auto_convert_database()
        self.close()


# class settingCalendar(Setup):
    # def __init__(self, session, parent=None):
        # Setup.__init__(self, session, setup="settingCalendar", plugin="Extensions/Calendar")
        # self.parent = parent

    # def keySave(self):
        # Setup.keySave(self)


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
        icon=PLUGIN_ICON,
        fnc=main
    ))

    if config.plugins.calendar.menu.value == 'yes':
        result.append(PluginDescriptor(
            name=_("Calendar"),
            where=PluginDescriptor.WHERE_MENU,
            fnc=mainMenu
        ))

    return result
