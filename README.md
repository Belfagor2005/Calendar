![](https://komarev.com/ghpvc/?username=Belfagor2005&label=Repository%20Views&color=blueviolet)
[![Version](https://img.shields.io/badge/Version-1.1-blue.svg)](https://github.com/Belfagor2005/Calendar)
[![Enigma2](https://img.shields.io/badge/Enigma2-Plugin-ff6600.svg)](https://www.enigma2.net)
[![Python](https://img.shields.io/badge/Python-2.7%2B%203.X%2B-blue.svg)](https://www.python.org)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![GitHub stars](https://img.shields.io/github/stars/Belfagor2005/Calendar?style=social)](https://github.com/Belfagor2005/Calendar/stargazers)


# Calendar Plugin for Enigma2

A comprehensive calendar plugin for Enigma2-based receivers with event management and notification system.

## ✨ Features

### Core Calendar Features
- **Monthly Calendar Display**: Visual calendar with color-coded days (weekends, today, events)
- **Date Information**: Load and display date-specific data from structured text files
- **Data Management**: Edit multiple fields via virtual keyboard with intuitive field navigation
- **File Operations**: Create, edit, remove, or delete date data files with custom naming (YYYYMMDD.txt)
- **Multi-language Support**: Data organized by language folders for localization

### Event Management System (New!)
- **Smart Event Notifications**: Get notified before events start (configurable from 0 to 60 minutes before)
- **Recurring Events**: Support for daily, weekly, monthly, and yearly recurring events
- **Visual Indicators**: Days with events are highlighted in different colors on the calendar
- **Event Browser**: View all events for a specific date or upcoming events (7-day view)
- **Event Settings**: Configurable notification duration, colors, and display options
- **Automatic Monitoring**: Background event checking every 30 seconds

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
   - `buttons/` - Button images directory
   - `base/` - Data storage directory structure

3. Restart your receiver or reload plugins
4. Access the plugin from the Extensions menu

## 🚀 Usage

### Basic Calendar Navigation
- Open the plugin from the menu
- Use arrow keys to navigate between months and days
- Press **OK** to open the main menu with options:
  - **New Date**: Create or add a new date entry
  - **Edit Date**: Edit existing date data fields
  - **Remove Date**: Clear data from the selected date's file
  - **Delete File**: Delete the file associated with the selected date
  - **Manage Events**: Access event management (new feature)
  - **Event Settings**: Configure event-related options
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

### Color Coding on Calendar
- **Green**: Current day
- **Yellow**: Saturdays
- **Red**: Sundays
- **Blue/Cyan**: Days with events (configurable color)
- *** (asterisk)**: Indicator for days with events

## 📁 File Structure

```
Calendar/
├── plugin.py
├── event_manager.py
├── event_dialog.py
├── events_view.py
├── notification_system.py
├── sounds/
│   ├── beep.wav
│   ├── beep.mp3
│   ├── notify.wav
│   ├── notify.mp3
│   ├── alert.wav
│   └── alert.mp3
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
- **Auto-start Event Monitor**: Start event monitoring on plugin launch

## 🔧 Technical Details

### Event Notification Logic
- Background monitoring every 30 seconds
- Notifications shown within configurable time window
- Each event notified only once per occurrence
- Automatic cleanup of past event notifications

### Key Components
1. **EventManager**: Central event handling with JSON storage
2. **EventDialog**: User interface for event creation/editing
3. **EventsView**: Browser for viewing and managing events
4. **NotificationSystem**: Display system for event alerts

### Dependencies
- Python standard libraries: `datetime`, `json`, `os`
- Enigma2 components: `eTimer`, `ActionMap`, `Screen`
- Custom notification system for visual alerts

## 🐛 Troubleshooting

### Common Issues
1. **No notifications appearing**:
   - Check event system is enabled in settings
   - Verify notification duration is set correctly
   - Ensure event time has passed the scheduled time

2. **Events not saving**:
   - Check write permissions in plugin directory
   - Verify `events.json` file exists and is writable

3. **Calendar not displaying**:
   - Ensure all skin files are present
   - Check for Python errors in debug log

### Debug Mode
Enable debug messages by checking the plugin logs:
```
tail -f /tmp/enigma2.log | grep EventManager
```

## 📝 Changelog

### v1.0
- Initial release with basic calendar functionality

### v1.1 (Current)
- **Added**: Complete event management system
- **Added**: Smart notifications with configurable timing
- **Added**: Recurring event support (daily, weekly, monthly, yearly)
- **Added**: Visual indicators for days with events
- **Added**: Event browser and management interface
- **Added**: Configuration options for event system
- **Improved**: Navigation and user interface
- **Fixed**: Various bug fixes and performance improvements

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows existing style and structure
- New features include appropriate configuration options
- All changes are tested on Enigma2 receivers

## 📄 License

This plugin is open-source software. See the LICENSE file for details.

## 🙏 Credits

- **Original Developer**: Sirius0103
- **Modifications & Event System**: Lululla
- **Homepage**: www.gisclub.tv

---

*Note: This plugin requires an Enigma2-based receiver (OpenPLi, OpenATV, etc.)*
```
