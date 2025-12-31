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
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Components.Language import language
from os.path import exists
from os import environ
import gettext

PLUGIN_NAME = "Calendar"
PLUGIN_VERSION = "1.7"
PLUGIN_PATH = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format(PLUGIN_NAME))
PLUGIN_ICON = resolveFilename(SCOPE_PLUGINS, "Extensions/Calendar/plugin.png")
USER_AGENT = "Calendar-Enigma2-Updater/%s" % PLUGIN_VERSION
PluginLanguageDomain = 'Calendar'
PluginLanguagePath = "Extensions/Calendar/locale"
isDreambox = exists("/usr/bin/apt-get")


def localeInit():
    if isDreambox:
        lang = language.getLanguage()[:2]
        environ["LANGUAGE"] = lang
    if PLUGIN_NAME and PluginLanguagePath:
        gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))


if isDreambox:
    def _(txt):
        return gettext.dgettext(PluginLanguageDomain, txt) if txt else ""
else:
    def _(txt):
        translated = gettext.dgettext(PluginLanguageDomain, txt)
        if translated:
            return translated
        else:
            print(("[%s] fallback to default translation for %s" % (PluginLanguageDomain, txt)))
            return gettext.gettext(txt)

localeInit()
language.addCallback(localeInit)
