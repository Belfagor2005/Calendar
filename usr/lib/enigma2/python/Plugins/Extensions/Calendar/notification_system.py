#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
###########################################################
#                                                         #
#  Notifier Plugin for Enigma2                            #
#  Created by: Lululla                                    #
#                                                         #
#  EVENT SYSTEM:                                          #
#  • Configurable notification duration (3-15 seconds)    #
#                                                         #
#  FILE STRUCTURE:                                        #
#  • notification_system.py - Notification display        #
#                                                         #
#  CREDITS:                                               #
#  • Notification system: Custom implementation           #
#  • Testing & feedback: Enigma2 community                #
#                                                         #
#  VERSION HISTORY:                                       #
#  • v1.0 - Basic functionality                           #
#                                                         #
#  Last Updated: 2025-12-19                               #
#  Status: Stable with event system                       #
###########################################################
"""

from Screens.Screen import Screen
from Components.Label import Label
from enigma import eTimer


class SimpleNotifyWidget(Screen):
    """Simple notification widget for Enigma2 plugins"""

    skin = """
    <screen name="SimpleNotifyWidget" position="10,30" zPosition="10" size="1280,150" title=" " backgroundColor="#201F1F1F" flags="wfNoBorder">
        <widget name="notification_text" font="Regular;28" position="5,5" zPosition="2" valign="center" halign="center" size="1270,140" foregroundColor="#00FF00" backgroundColor="#201F1F1F" transparent="1" />
    </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.skin = SimpleNotifyWidget.skin
        self["notification_text"] = Label("")
        self.onLayoutFinish.append(self._setupUI)

    def _setupUI(self):
        """Setup UI after layout completion"""
        self.instance.setAnimationMode(0)  # Disable animations

    def updateMessage(self, text):
        """Update notification text"""
        self["notification_text"].setText(text)


class NotificationManager:
    """Central notification manager for plugins"""

    def __init__(self):
        self.notification_window = None
        self.hide_timer = eTimer()
        self.hide_timer.callback.append(self._hideNotification)
        self.is_initialized = False

    def initialize(self, session):
        """Initialize manager with session"""
        if not self.is_initialized:
            self.notification_window = session.instantiateDialog(SimpleNotifyWidget)
            self.is_initialized = True

    def _hideNotification(self):
        """Hide notification (timer callback)"""
        if self.notification_window:
            self.notification_window.hide()

    def showMessage(self, message, duration=10000):
        """
        Show temporary notification

        Args:
            message (str): Text to display
            duration (int): Duration in milliseconds (default: 3000 = 3 seconds)
        """
        if not self.is_initialized:
            print("[NotificationManager] Not initialized! Call initialize() first.")
            return

        if self.notification_window:
            # Stop any previous timer
            self.hide_timer.stop()

            # Update and show message
            self.notification_window.updateMessage(message)
            self.notification_window.show()

            # Start auto-hide timer
            self.hide_timer.start(duration, True)

    def show(self, message, seconds=5):
        """Simplified version with duration in seconds"""
        self.showMessage(message, seconds * 1000)

    def hide(self):
        """Hide notification immediately"""
        self.hide_timer.stop()
        self._hideNotification()


# Global notification manager instance
_notification_manager = NotificationManager()


# Public API functions
def init_notification_system(session):
    """
    Initialize notification system (call this once in your plugin)

    Args:
        session: Enigma2 session object
    """
    _notification_manager.initialize(session)


def show_notification(message, duration=10000):
    """
    Show a notification message

    Args:
        message (str): Text to display
        duration (int): Display duration in milliseconds (default: 3000)

    Example:
        show_notification("Processing completed!")
        show_notification("Download finished", 5000)
    """
    _notification_manager.showMessage(message, duration)


def quick_notify(message, seconds=10):
    """
    Quick notification with duration in seconds

    Args:
        message (str): Text to display
        seconds (int): Display duration in seconds (default: 3)

    Example:
        quick_notify("Task completed")
        quick_notify("Operation failed", 5)
    """
    _notification_manager.show(message, seconds)


def hide_current_notification():
    """Hide the current notification immediately"""
    _notification_manager.hide()


# =============================================================================
# USAGE EXAMPLES - How to use in your plugins
# =============================================================================

"""
from .notification_system import init_notification_system, quick_notify, show_notification

# 1. INITIALIZATION (in your main plugin class)
class MyPlugin(Screen):
    def __init__(self, session):
        Screen.__init__(self, session)
        # Initialize notification system once
        init_notification_system(session)

# 2. BASIC USAGE
# Show 3-second notification
show_notification("Processing completed!")

# Show 5-second notification
show_notification("Download finished", 5000)

# Simplified version (seconds instead of milliseconds)
quick_notify("File saved successfully")

# Longer notification
quick_notify("Backup completed successfully", 5)

# Hide manually if needed
hide_current_notification()

# 3. AFTER OPERATIONS
def on_download_finished(self, success, filename):
    if success:
        quick_notify("Downloaded: {0}".format(filename))
    else:
        quick_notify("Download failed!", 5)

def on_processing_done(self, result):
    quick_notify("Processed {0} files".format(result.file_count))

# 4. ERROR NOTIFICATIONS
def handle_error(self, error_message):
    quick_notify("Error: {0}".format(error_message), 5)

"""
