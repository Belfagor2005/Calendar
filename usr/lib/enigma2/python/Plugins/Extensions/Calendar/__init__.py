#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
###########################################################
#  Calendar Planner for Enigma2 v1.7                      #
#  Created by: Lululla (based on Sirius0103)              #
###########################################################
Last Updated: 2025-12-27
Status: Stable with complete vCard & ICS support
Credits: Sirius0103 (original), Lululla (modifications)
Homepage: www.corvoboys.org www.linuxsat-support.com
###########################################################
"""
from __future__ import print_function

from os import environ
from os.path import exists
import gettext

from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Components.Language import language


PLUGIN_NAME = "Calendar"
PLUGIN_VERSION = "1.8.1"
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
