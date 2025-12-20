![](https://komarev.com/ghpvc/?username=Belfagor2005&label=Repository%20Views&color=blueviolet)
[![Version](https://img.shields.io/badge/Version-1.1-blue.svg)](https://github.com/Belfagor2005/Calendar)
[![Enigma2](https://img.shields.io/badge/Enigma2-Plugin-ff6600.svg)](https://www.enigma2.net)
[![Python](https://img.shields.io/badge/Python-2.7%2B%203.X%2B-blue.svg)](https://www.python.org)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![GitHub stars](https://img.shields.io/github/stars/Belfagor2005/Calendar?style=social)](https://github.com/Belfagor2005/Calendar/stargazers)


# Calendar Plugin for Enigma2

A comprehensive calendar plugin for Enigma2-based receivers with event management, notification, and audio alert system.

## ✨ Features

### Core Calendar Features
- **Monthly Calendar Display**: Visual calendar with color-coded days (weekends, today, events)
- **Date Information**: Load and display date-specific data from structured text files
- **Data Management**: Edit multiple fields via virtual keyboard with intuitive field navigation
- **File Operations**: Create, edit, remove, or delete date data files with custom naming (YYYYMMDD.txt)
- **Multi-language Support**: Data organized by language folders for localization

### Event Management System
- **Smart Event Notifications**: Get notified before events start (configurable from 0 to 60 minutes before)
- **Recurring Events**: Support for daily, weekly, monthly, and yearly recurring events
- **Visual Indicators**: Days with events are highlighted in different colors on the calendar
- **Event Browser**: View all events for a specific date or upcoming events (7-day view)
- **Event Settings**: Configurable notification duration, colors, and display options
- **Automatic Monitoring**: Background event checking every 30 seconds
- **Past Event Cleanup**: Automatic skipping of old non-recurring events to improve performance

### Audio Notification System
- **Built-in Sound Alerts**: Three distinct sound types for different priorities
- **Priority-based Selection**:
  - **Alert Sound**: For events currently in progress (`notify_before=0`)
  - **Notify Sound**: For imminent events (≤5 minutes before)
  - **Short Beep**: For regular notifications
- **Dual Format Support**: Plays both WAV and MP3 audio files
- **Auto-stop Feature**: Automatic audio cleanup after playback completion
- **Service Restoration**: Intelligently restores previous TV/radio service after audio playback
- **Configurable Sound**: Choose sound type or disable audio completely in settings

## 📦 Installation

1. Copy the entire `Calendar` plugin folder to your Enigma2 plugins directory:
   ```
   /usr/lib/enigma2/python/Plugins/Extensions/Calendar/
   ```

2. Ensure all required files are present:
   - `plugin.py` - Main plugin file
   - `event_manager.py` - Event management core
   - `event_dialog.py` - Event add/edit interface
   - `events_view.py` - Events browser
   - `notification_system.py` - Notification display system
   - `sounds/` - Audio files directory (new!)
   - `buttons/` - Button images directory
   - `base/` - Data storage directory structure

3. Audio files setup (optional but recommended):
   - Place `alert.wav`, `notify.wav`, `beep.wav` in `sounds/` directory
   - Or use MP3 versions: `alert.mp3`, `notify.mp3`, `beep.mp3`
   - Files are included in the repository

4. Restart your receiver or reload plugins
5. Access the plugin from the Extensions menu

## 🚀 Usage

### Basic Calendar Navigation
- Open the plugin from the menu
- Use arrow keys to navigate between months and days
- Press **OK** to open the main menu with options:
  - **New Date**: Create or add a new date entry
  - **Edit Date**: Edit existing date data fields
  - **Remove Date**: Clear data from the selected date's file
  - **Delete File**: Delete the file associated with the selected date
  - **Manage Events**: Access event management
  - **Add Event**: Create a new event for selected date
  - **Cleanup Past Events**: Remove old non-recurring events
  - **Exit**: Close the plugin

### Event Management
- Press **0** (zero key) from main calendar to access event management
- **Add Event**: Create new events with date, time, and notification settings
- **Edit Event**: Modify existing events
- **Delete Event**: Remove unwanted events
- **Event Types**: 
  - One-time events (no repeat)
  - Daily recurring events
  - Weekly recurring events (same weekday)
  - Monthly recurring events (same day of month)
  - Yearly recurring events (same date annually)

### Audio Notifications
- **Automatic Playback**: Sounds play automatically when events trigger
- **Visual Overlay**: 5-second visual notification appears simultaneously
- **Priority Handling**: Different sounds based on event urgency
- **Non-intrusive**: Auto-stops after playback, restores previous service

## 📁 File Structure

```
Calendar/
├── plugin.py
├── event_manager.py
├── event_dialog.py
├── events_view.py
├── notification_system.py
├── sounds/                 # Audio notification files
│   ├── beep.wav           # Short beep (low priority)
│   ├── beep.mp3           # MP3 version
│   ├── notify.wav         # Normal notification tone
│   ├── notify.mp3         # MP3 version
│   ├── alert.wav          # Alert sound (high priority)
│   └── alert.mp3          # MP3 version
├── buttons/
├── base/
├── setup.xml
└── events.json
```

### Data File Format
Date information files are stored in:
```
base/[language]/day/YYYYMMDD.txt
```

Format example:
```ini
[day]
date: 2025-06-10
datepeople: John Doe
sign: Gemini
holiday: None
description: Special day description.

[month]
monthpeople: Important people of the month
```

### Event Database
Events are stored in JSON format in `events.json`:
```json
[
  {
    "id": 1766153767369,
    "title": "Meeting",
    "description": "Team meeting",
    "date": "2025-12-19",
    "time": "14:30",
    "repeat": "none",
    "notify_before": 15,
    "enabled": true,
    "created": "2024-12-19 14:25:47"
  }
]
```

## ⚙️ Configuration

The plugin includes configuration options accessible through:
- **Menu → Setup** from within the plugin

### Available Settings:
- **Show in Main Menu**: Enable/disable plugin in information menu
- **Event System**: Enable/disable event management
- **Notifications**: Toggle event notifications
- **Notification Duration**: Set how long notifications appear (3-15 seconds)
- **Default Notification Time**: Minutes before event to notify (0-60)
- **Event Color**: Color for days with events on calendar
- **Show Event Indicators**: Toggle visual indicators on calendar
- **Audio Settings**:
  - **Play Sound**: Enable/disable audio notifications
  - **Sound Type**: Choose between Short beep, Notification tone, Alert sound, or None
  - **Auto-start Event Monitor**: Start event monitoring on plugin launch

## 🔧 Technical Details

### Event Notification Logic
- Background monitoring every 30 seconds
- Notifications shown within configurable time window
- Each event notified only once per occurrence
- Automatic skipping of past non-recurring events
- Priority-based audio selection

### Audio System Architecture
- **Enigma2 Native Playback**: Uses `eServiceReference` for reliable audio playback
- **Service Management**: Intelligently handles TV/radio service interruption
- **Format Support**: Automatic detection of WAV/MP3 files
- **Error Handling**: Graceful fallback if audio files missing
- **Performance**: Minimal CPU usage during playback

### Key Components
1. **EventManager**: Central event handling with JSON storage and audio playback
2. **EventDialog**: User interface for event creation/editing
3. **EventsView**: Browser for viewing and managing events
4. **NotificationSystem**: Display system for visual alerts
5. **AudioEngine**: Integrated sound playback using Enigma2 services

### Dependencies
- Python standard libraries: `datetime`, `json`, `os`
- Enigma2 components: `eTimer`, `ActionMap`, `Screen`, `eServiceReference`
- Custom notification system for visual alerts
- Audio files (included in repository)

## 🐛 Troubleshooting

### Common Issues
1. **No audio notifications**:
   - Check audio files exist in `sounds/` directory
   - Verify "Play Sound" is enabled in settings
   - Ensure audio format is WAV or MP3
   - Check file permissions: `chmod 644 sounds/*`

2. **Audio interrupts TV/radio permanently**:
   - Normal behavior: audio stops automatically after 3 seconds
   - Previous service should restore automatically
   - Check for errors in `/tmp/enigma2.log`

3. **No notifications appearing**:
   - Check event system is enabled in settings
   - Verify notification duration is set correctly
   - Ensure event time has passed the scheduled time

4. **Events not saving**:
   - Check write permissions in plugin directory
   - Verify `events.json` file exists and is writable

5. **Calendar not displaying**:
   - Ensure all skin files are present
   - Check for Python errors in debug log

### Debug Mode
Enable debug messages by checking the plugin logs:
```
# Event system debug
tail -f /tmp/enigma2.log | grep EventManager

# Audio system debug
tail -f /tmp/enigma2.log | grep "Playing\|No sound file\|Audio"

# General plugin debug
tail -f /tmp/enigma2.log | grep Calendar
```

## 📝 Changelog

### v1.0
- Initial release with basic calendar functionality

### v1.1
- **Added**: Complete event management system
- **Added**: Smart notifications with configurable timing
- **Added**: Recurring event support (daily, weekly, monthly, yearly)
- **Added**: Visual indicators for days with events
- **Added**: Event browser and management interface
- **Added**: Configuration options for event system
- **Improved**: Navigation and user interface
- **Fixed**: Various bug fixes and performance improvements
- **Added**: Complete audio notification system with priority-based sounds
- **Added**: Support for WAV and MP3 audio formats
- **Added**: Automatic audio playback for event notifications
- **Added**: Service restoration after audio playback
- **Added**: Past event skipping for improved performance
- **Added**: Cleanup past events feature
- **Added**: Color configuration with hexadecimal color codes
- **Enhanced**: Event checking algorithm efficiency
- **Improved**: Error handling and debugging information
- **Fixed**: Skin warnings and widget count mismatches
- **Fixed**: Recursion errors in event management

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows existing style and structure
- New features include appropriate configuration options
- All changes are tested on Enigma2 receivers
- Audio files follow naming convention: `beep`, `notify`, `alert` with `.wav` or `.mp3` extension

## 📄 License

This plugin is open-source software. See the LICENSE file for details.

## 🙏 Credits

- **Original Developer**: Sirius0103
- **Modifications & Event System**: Lululla
- **Audio Notification System**: Integrated by Lululla
- **Homepage**: www.gisclub.tv

---

*Note: This plugin requires an Enigma2-based receiver (OpenPLi, OpenATV, etc.)*
*Audio notifications work best with receivers that support audio playback via eServiceReference*
```
