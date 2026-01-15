![](https://komarev.com/ghpvc/?username=Belfagor2005&label=Repository%20Views&color=blueviolet)
[![Version](https://img.shields.io/badge/Version-1.9-blue.svg)](https://github.com/Belfagor2005/Calendar)
[![Enigma2](https://img.shields.io/badge/Enigma2-Plugin-ff6600.svg)](https://www.enigma2.net)
[![Python](https://img.shields.io/badge/Python-2.7%2B%203.X%2B-blue.svg)](https://www.python.org)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![GitHub stars](https://img.shields.io/github/stars/Belfagor2005/Calendar?style=social)](https://github.com/Belfagor2005/Calendar/stargazers)

# Calendar Planner for Enigma2

A comprehensive calendar plugin for Enigma2-based receivers with event management, holiday import system, notifications, audio alerts, **ICS import support**, and contact management.

## ✨ Features

### Core Calendar Features
- **Monthly Calendar Display**: Visual calendar with color-coded days (weekends, today, events, holidays)
- **Date Information**: Load and display date-specific data from structured text files
- **Data Management**: Edit multiple fields via virtual keyboard with intuitive field navigation
- **File Operations**: Create, edit, remove, or delete date data files with custom naming (YYYYMMDD.txt)
- **Multi-language Support**: Data organized by language folders for localization
- **Smooth navigation**: with keyboard shortcuts
- **Autostart System**: Implemented auto-start system at decoder boot
- **Monitor Timer**: Efficient timer for continuous monitoring
- **Autostart Event**: Lazy event loading on startup

### Event Management System
- **Smart Event Notifications**: Get notified before events start (configurable from 0 to 60 minutes before)
- **Recurring Events**: Support for daily, weekly, monthly, and yearly recurring events
- **Visual Indicators**: Days with events are highlighted in different colors on the calendar
- **Event Browser**: View all events for a specific date or upcoming events (7-day view)
- **Event Settings**: Configurable notification duration, colors, and display options
- **Automatic Monitoring**: Background event checking every 30 seconds
- **Past Event Cleanup**: Automatic skipping of old non-recurring events to improve performance
- **Intelligent Event Time Conversion**: Auto-converts existing events when default time changes
- **Universal Navigation**: CH+/CH- wrap-around navigation in all event screens

### vCard Contact Management System
- **vCard Import/Export**: Import thousands of contacts from .vcf files with progress tracking
- **Contact Management**: Full contact database with birthday tracking and age calculation
- **Contact Browser**: Browse, search, and sort contacts by name, birthday, or category
- **Contact sorting**: (name, birthday, category)
- **Birthday Tracking**: Automatically track birthdays and show on calendar
- **Duplicate Detection**: Smart detection during import to avoid duplicate contacts
- **Multi-threaded Import**: Import large vCard files without GUI freeze
- **Contact Sorting**: Sort contacts by name, birthday, or category
- **Search Function**: Search contacts by name, phone, email, notes
- **Database Format**: Stores contacts in vCard-like format for compatibility
- **Database format converter**: (Legacy ↔ vCard)
- **Duplicate detection**: during import
- **vCard export**: to `/tmp/calendar.vcf`
- **Universal Navigation**: CH+/CH- wrap-around navigation in contact screens

### ICS Calendar Import System
- **ICS Event Management**: Browse, edit, delete imported events from .ics files
- **ICS Events Browser**: Similar to contacts browser with CH+/CH- navigation
- **ICS Event Editor**: Full-screen dialog like contact editor
- **ICS File Archive**: Store imported .ics files in `/base/ics` directory
- **Duplicate Detection**: Smart cache for fast duplicate checking of imported events
- **Enhanced Search**: Search in events titles, descriptions, dates
- **Universal Navigation**: CH+/CH- wrap-around navigation in ICS screens

### Holiday Import & Management System
- **Automatic Coloring**: Holiday days are automatically colored on the calendar
- **Country Support**: Italy, Germany, France, UK, USA, Spain, and many more
- **International Holiday Database**: Import holidays from Holidata.net for 30+ countries
- **Language Support**: Localized holiday names for each country
- **Smart Cache**: Fast loading with month-based caching system
- **Today's Holidays**: View holidays for the current day
- **Upcoming Holidays**: Display holidays for the next 30 days
- **Visual Indicators**: "H" marker shown on holiday days (configurable)

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

### Universal Navigation System
- **Wrap-around Navigation**: CH+/CH- navigation works in ALL screens (EventsView, EventDialog, ContactsView, ICSEventsView, ICSEventDialog, BirthdayDialog)
- **Real-time Position Display**: Shows current position like "Edit Event (3/15)" or "Contacts: 5/20"
- **Jump to Today**: BLUE button jumps to today's event from anywhere in the system
- **Return to Start**: MENU button returns to the start position where navigation began
- **Auto-save Navigation**: Changes automatically saved when navigating with CH+/CH-
- **Page Navigation**: PAGE UP/DOWN to skip 5 items at a time in long lists
- **Search Function**: TEXT button opens search dialog in all views
- **Sorting Options**: BLUE button changes sorting (dates/title/category) where applicable
- **Navigation Through Entire Database**: Not just today's events, but the ENTIRE event database

## 🎮 Key Controls

### Main Calendar
- **OK**: Main menu (Events/Holidays/Contacts/Import/Export/Converter)
- **RED**: Previous month
- **GREEN**: Next month
- **YELLOW**: Previous day
- **BLUE**: Next day
- **0**: Event management
- **LEFT/RIGHT**: Previous/Next day
- **UP/DOWN**: Previous/Next month
- **MENU**: Configuration
- **INFO/EPG**: About dialog

### Universal Navigation Controls
- **CH+**: Next item (wrap-around)
- **CH-**: Previous item (wrap-around)
- **UP/DOWN**: Standard navigation (wrap-around)
- **PAGE UP/DOWN**: Jump 5 items
- **BLUE**: Jump to TODAY'S item
- **MENU**: Return to START position
- **TEXT**: Open search dialog
- **OK**: Edit selected item
- **GREEN**: Save and close
- **RED**: Cancel
- **YELLOW**: Delete (when editing)

### Event Dialog
- **OK**: Edit current field
- **RED**: Cancel
- **GREEN**: Save event
- **YELLOW**: Delete event (edit mode only)
- **UP/DOWN**: Navigate between fields
- **LEFT/RIGHT**: Change selection options

### Events View
- **OK**: Edit selected event
- **RED**: Add new event
- **GREEN**: Edit selected event
- **YELLOW**: Delete selected event
- **BLUE**: Back to calendar
- **UP/DOWN**: Navigate event list

### ICS Browser Specific
- **OK**: Edit selected event
- **RED**: Add new event
- **GREEN**: Edit event
- **YELLOW**: Delete event (single/all)
- **BLUE**: Change sorting (date/title/category)
- **CH+**: Next event
- **CH-**: Previous event
- **TEXT**: Search events

### Contacts View
- **OK**: Edit selected contact
- **RED**: Add new contact
- **GREEN**: Edit selected contact
- **YELLOW**: Delete selected contact
- **BLUE**: Toggle sort mode (Name/Birthday/Category)
- **UP/DOWN**: Navigate contact list

### vCard Import/Export
- **OK**: Select file
- **RED**: Cancel / Close
- **GREEN**: Import selected file / Start export
- **YELLOW**: View file info (size, contacts)
- **BLUE**: Refresh file list / Toggle sort


### Database Converter
- **OK**: Show statistics
- **RED**: Cancel
- **GREEN**: Convert to vCard format
- **BLUE**: Convert to legacy format

### Birthday Dialog (Contact Editor)
- **OK**: Edit current highlighted field
- **RED**: Cancel
- **GREEN**: Save contact
- **YELLOW**: Next field
- **BLUE**: Delete contact / Clear all fields
- **UP/DOWN**: Navigate between fields
- **Field Highlighting**: Current field highlighted with color background

## 📦 Installation

1. Instalaltion Mode: Telnet/Wget:

```bash
wget -q --no-check-certificate https://raw.githubusercontent.com/Belfagor2005/Calendar/main/installer.sh -O - | /bin/bash
```

2. Ensure all required files are present:
   - `plugin.py` - Main plugin file
   - `event_manager.py` - Event management core
   - `event_dialog.py` - Event add/edit interface
   - `events_view.py` - Events browser
   - `notification_system.py` - Notification display system
   - `holidays.py` - Holiday import and management
   - `vcard_importer.py` - vCard import system
   - `birthday_manager.py` - Contact management
   - `contacts_view.py` - Contacts browser
   - `birthday_dialog.py` - Contact add/edit dialog
   - `database_converter.py` - Database format converter
   - `sounds/` - Audio files directory
   - `buttons/` - Button images directory
   - `base/` - Data storage directory structure
   - `base/contacts/` - Contact storage directory

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
  - **Import Holidays**: Import holidays from Holidata.net
  - **Show Today's Holidays**: Display holidays for current day
  - **Show Upcoming Holidays**: View holidays for next 30 days
  - **Manage Contacts**: Access contact management
  - **Import vCard**: Import contacts from vCard files
  - **Database Converter**: Convert between contact database formats
  - **Cleanup Past Events**: Remove old non-recurring events
  - **Exit**: Close the plugin

### Universal Navigation System
- **CH+/CH-**: Navigate through items in any screen (wrap-around)
- **BLUE**: Jump directly to today's event from anywhere
- **MENU**: Return to the starting position where you began navigation
- **PAGE UP/DOWN**: Skip 5 items at a time in long lists
- **TEXT**: Open search dialog to find specific items
- **Real-time Position**: Always see your current position (e.g., "Event 3/15")

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
- **Navigation**: Use CH+/CH- to navigate through all events in the database

### Contact Management
- **Contacts Menu**: Access from main menu to manage contacts
- **Add Contact**: Manually add new contacts with birthdays
- **Edit Contact**: Modify existing contact information
- **Delete Contact**: Remove unwanted contacts
- **Sort Contacts**: Sort by name, birthday, or category
- **Search Contacts**: Search by name, phone, email, notes
- **Birthday Tracking**: Contacts with birthdays automatically shown on calendar
- **vCard Import**: Import thousands of contacts from .vcf files
- **Navigation**: Use CH+/CH- to navigate through all contacts

### ICS Event Management
- **Import ICS**: Import events from Google Calendar .ics files
- **Browse ICS Files**: View imported ICS files in archive
- **Edit ICS Events**: Modify individual ICS events
- **Delete Events**: Remove single or all ICS events
- **Search**: Search events by title, description, date
- **Filter**: Filter events by category/labels
- **Navigation**: Use CH+/CH- to navigate through all ICS events

### Event Time Conversion System
- **Automatic Conversion**: When you change the default event time in settings, existing events are automatically converted
- **Time Tracking**: System tracks the last configured default time
- **Smart Conversion**: Converts events from both old fixed default (14:00) and last configured time
- **Calendar Refresh**: Calendar automatically repaints with converted event times

### vCard Import Process
1. Select **Import vCard** from main menu
2. Navigate to your .vcf or .vcard file
3. View file information (size, contact count)
4. Start import with progress tracking
5. Duplicate contacts are automatically skipped
6. Contacts are automatically sorted by name

### Holiday Management
- **Import Holidays**: Select a country to import holidays for current year
- **Import All**: Import holidays for all available countries at once
- **Today's View**: See all holidays happening today
- **Upcoming View**: Preview holidays for the next month
- **Automatic Integration**: Holidays are saved to existing date files
- **Color Coding**: Holiday days are automatically colored on calendar

### Database Format Converter
- **Convert to vCard**: Convert legacy contact format to standard vCard
- **Convert to Legacy**: Convert vCard format back to legacy format
- **Automatic Backup**: Creates backup before conversion
- **Progress Tracking**: Shows conversion progress
- **Data Preservation**: All contact data preserved during conversion

### Audio Notifications
- **Automatic Playback**: Sounds play automatically when events trigger
- **Visual Overlay**: 5-second visual notification appears simultaneously
- **Priority Handling**: Different sounds based on event urgency
- **Non-intrusive**: Auto-stops after playback, restores previous service

## 📁 File Structure

```
★ Calendar/
├── plugin.py                      # Main plugin entry point
├── autostart.py                   # Start autostart events in backgrount
├── config_manager.py              # Setup plugin Options
├── event_manager.py               # Event management core
├── event_dialog.py                # Event add/edit interface
├── events_view.py                 # Events browser
├── notification_system.py         # Notification display system
├── holidays.py                    # Holiday import and management
├── vcard_importer.py              # vCard import system
├── vcf_importer.py                # vCard file importer
├── birthday_manager.py            # Contact management core
├── contacts_view.py               # Contacts browser
├── birthday_dialog.py             # Contact add/edit dialog
├── formatters.py                  # Plugin utils
├── ics_browser.py                 # Browser ICS Files
├── ics_events_view.py             # ICS Events browser
├── ics_event_dialog.py            # ICS Event editor
├── ics_importer.py                # ICS import system
├── ics_manager.py                 # ICS management core
├── database_converter.py          # Database format converter
├── duplicate_checker.py           # Wrapper for check duplicate format converter
├── update_manager.py              # Update management
├── updater.py                     # Plugin updater
├── sounds/                        # Audio notification files
│   ├── beep.wav                   # Short beep (low priority)
│   ├── beep.mp3                   # MP3 version
│   ├── notify.wav                 # Normal notification tone
│   ├── notify.mp3                 # MP3 version
│   ├── alert.wav                  # Alert sound (high priority)
│   └── alert.mp3                  # MP3 version
├── buttons/                       # UI button images
├── base/                          # Data storage & events.json
│   ├── events.json                # Event database (JSON format)
│   ├── contacts/                  # Contact storage
│   ├── holidays/                  # holidays storage
│   ├── vcards/                    # vcards storage
│   └── ics/                       # ICS file archive
├── keymap.xml                     # Plugin keymap configuration
└── setup.xml                      # Plugin setup configuration                    
```

### Data File Formats

#### Date Information Files
Stored in: `base/[language]/day/YYYYMMDD.txt`
```ini
[day]
date: 2025-12-25
datepeople:
sign: Capricorn
holiday: Christmas Day
description: Christmas celebration with family.

[month]
monthpeople:
```

#### Contact Storage Format
Each contact stored as `[contact_id].txt` in `base/contacts/`:
```ini
[contact]
FN: John Doe
BDAY: 1990-05-15
TEL: +391234567890
EMAIL: john@example.com
CATEGORIES: Family, Friends
NOTE: Birthday reminder
CREATED: 2024-12-25 10:30:00
```

#### Event Database
Events stored in JSON format in `events.json`:
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

### Holiday Integration
Holidays are imported and stored directly in date files:
- **Source**: Holidata.net (JSON Lines format)
- **Integration**: Updates `holiday:` field in existing date files
- **Multiple Holidays**: Can store multiple holidays separated by commas
- **Preservation**: Keeps existing data when adding new holidays

## ⚙️ Configuration

The plugin includes configuration options accessible through:
- **Menu → Setup** from within the plugin

### Available Settings:
- **Show in Main Menu**: Enable/disable plugin in information menu
- **Event System**: Enable/disable event management
- **Notifications**: Toggle event notifications
- **Notification Duration**: Set how long notifications appear (3-15 seconds)
- **Default Notification Time**: Minutes before event to notify (0-60)
- **Default Event Time**: Default time for new events with auto-conversion
- **Event Color**: Color for days with events on calendar
- **Show Event Indicators**: Toggle visual indicators on calendar
- **Holiday System**: Enable/disable holiday coloring
- **Show Holiday Indicators**: Toggle "H" marker on holiday days
- **Holiday Color**: Color for holiday days on calendar
- **Contact Database Format**: Choose between Legacy or vCard format
- **Audio Settings**:
  - **Play Sound**: Enable/disable audio notifications
  - **Sound Type**: Choose between Short beep, Notification tone, Alert sound, or None
  - **Auto-start Event Monitor**: Start event monitoring on plugin launch

## 🔧 Technical Details

#### vCard Import/Export
- **Multi-threaded Architecture**: Imports large vCard files without blocking GUI
- **Progress Tracking**: Real-time progress bar with contact count
- **Duplicate Detection**: Smart duplicate checking during import
- **Error Handling**: Graceful handling of malformed vCard entries
- **Performance**: Efficient memory usage for large files
- **Fields Supported**: Name, Birthday, Phone, Email, Address, Organization, Categories, Notes, URL
- **Field Parsing**: Support for standard vCard fields with charset detection
- **vCard Export**: Export contacts to `/tmp/calendar.vcf`
- **Database Converter**: UI for format conversion
- **Auto-conversion**: Automatic format conversion option
- **Contact Sorting**: Sort by name, birthday, or category in export
- **Import**: Supports standard .vcf/.vcard files
- **Export**: Contacts can be exported to vCard format
- **Format Compatibility**: Works with vCard 2.1 and 3.0

### Contact Management
- **Birthday Calculation**: Automatic age calculation from birth dates
- **Sorting Algorithms**: Efficient sorting by name, birthday, category
- **Search Functionality**: Fast text search across multiple fields
- **File-based Storage**: Each contact stored in separate .txt file
- **Automatic Backups**: Before database format conversion

### Event Management
- **Background monitoring**: Every 30 seconds
- **Intelligent Time Conversion**: Auto-converts events when default time changes
- **Time Tracking**: Tracks last configured default time (LAST_USED_DEFAULT_TIME)
- **Universal Navigation**: Wrap-around CH+/CH- navigation across all event screens
- **Position Tracking**: Real-time position display in all interfaces
- **Auto-save Navigation**: Automatic save when navigating between items

### Notification Logic
- Notifications shown within configurable time window
- Each event notified only once per occurrence
- Automatic skipping of past non-recurring events
- Priority-based audio selection

### Holiday System Architecture
- **File-based Storage**: Holidays stored in existing date files
- **Smart Caching**: Month-based cache for fast rendering
- **International Support**: 30+ countries with localized names
- **Performance**: Reads files once per month, not per day
- **Integration**: Seamless integration with existing date data

### Audio System Architecture
- **Enigma2 Native Playback**: Uses `eServiceReference` for reliable audio playback
- **Service Management**: Intelligently handles TV/radio service interruption
- **Format Support**: Automatic detection of WAV/MP3 files
- **Error Handling**: Graceful fallback if audio files missing
- **Performance**: Minimal CPU usage during playback

### Key Components
1. **EventManager**: Central event handling with JSON storage and audio playback
2. **BirthdayManager**: Contact management with vCard import/export
3. **VCardImporter**: vCard file parser and importer with progress tracking
4. **HolidaysManager**: Holiday import, caching, and display management
5. **EventDialog**: User interface for event creation/editing with universal navigation
6. **BirthdayDialog**: Contact add/edit interface with field highlighting
7. **ContactsView**: Contact browser with sorting, search, and universal navigation
8. **DatabaseConverter**: Format conversion between Legacy and vCard
9. **EventsView**: Browser for viewing and managing events with universal navigation
10. **HolidaysImportScreen**: Interface for importing holidays by country
11. **NotificationSystem**: Display system for visual alerts
12. **AudioEngine**: Integrated sound playback using Enigma2 services

### Dependencies
- Python standard libraries: `datetime`, `json`, `os`, `urllib2`, `threading`
- Enigma2 components: `eTimer`, `ActionMap`, `Screen`, `eServiceReference`
- Custom notification system for visual alerts
- Audio files (included in repository)

## 🐛 Troubleshooting
### Common Issues
1. **vCard Import Issues**:
   - Check file format is .vcf or .vcard
   - Ensure file contains valid vCard data
   - Check file permissions: `chmod 644 filename.vcf`
   - Large files may take time to process

2. **No audio notifications**:
   - Check audio files exist in `sounds/` directory
   - Verify "Play Sound" is enabled in settings
   - Ensure audio format is WAV or MP3
   - Check file permissions: `chmod 644 sounds/*`

3. **Contacts not showing**:
   - Verify contacts exist in `base/contacts/` directory
   - Check file permissions on contacts folder
   - Ensure birthday format is YYYY-MM-DD
   - Restart plugin to reload contacts

4. **Holidays not showing/coloring**:
   - Verify holiday system is enabled in settings
   - Check internet connection for holiday import
   - Ensure `holidays.py` file exists and is executable
   - Import holidays for your country first

5. **Audio interrupts TV/radio permanently**:
   - Normal behavior: audio stops automatically after 3 seconds
   - Previous service should restore automatically
   - Check for errors in `/tmp/enigma2.log`

6. **Database conversion errors**:
   - Automatic backup created before conversion
   - Check disk space availability
   - Verify contact files are not corrupted
   - Manual backup available in plugin directory

7. **No notifications appearing**:
   - Check event system is enabled in settings
   - Verify notification duration is set correctly
   - Ensure event time has passed the scheduled time

8. **Events/Holidays not saving**:
   - Check write permissions in plugin directory
   - Verify `events.json` file exists and is writable
   - Ensure `base/` directory has write permissions

9. **Calendar not displaying**:
   - Ensure all skin files are present
   - Check for Python errors in debug log

10. **Navigation not working**:
    - Verify CH+/CH- buttons are configured in your remote
    - Check that universal navigation is enabled in all dialog classes
    - Ensure position tracking variables are initialized

### Debug Mode
Enable debug messages by checking the plugin logs:
```
# Event system debug
tail -f /tmp/enigma2.log | grep EventManager

# vCard import debug
tail -f /tmp/enigma2.log | grep VCardImporter

# Contact management debug
tail -f /tmp/enigma2.log | grep BirthdayManager

# Holiday system debug
tail -f /tmp/enigma2.log | grep Holidays

# Audio system debug
tail -f /tmp/enigma2.log | grep "Playing\|No sound file\|Audio"

# Navigation debug
tail -f /tmp/enigma2.log | grep "CH+\|CH-\|Navigation\|Position"

# General plugin debug
tail -f /tmp/enigma2.log | grep Calendar
```

## 📝 Changelog

### v1.0
- Initial release with basic calendar functionality

### v1.1
- Added complete event management system
- Added smart notifications with configurable timing
- Added recurring event support (daily, weekly, monthly, yearly)
- Added visual indicators for days with events
- Added event browser and management interface

### v1.2
- Added complete audio notification system with priority-based sounds
- Added support for WAV and MP3 audio formats
- Added automatic audio playback for event notifications
- Added service restoration after audio playback
- Added past event skipping for improved performance

### v1.3
- Added international holiday import system from Holidata.net
- Added automatic holiday coloring on calendar
- Added "H" indicator for holiday days
- Added country selection for holiday import (30+ countries)
- Added smart cache system for fast holiday loading
- Added today's and upcoming holidays display

### v1.4
- Improved calendar rendering with holiday/event priority system
- Enhanced day selection with blue background over holidays/events
- Fixed skin warnings and widget count mismatches
- Improved error handling and debugging information
- Enhanced navigation and user interface

### v1.5 
- **vCard import/export system for contacts**
- Complete contact management with birthday tracking
- Contact browser with sorting by name, birthday, category
- Multi-threaded vCard import with progress tracking
- Database format converter (Legacy ↔ vCard)
- Search function for contacts
- Duplicate detection during vCard import
- Birthday dialog with field highlighting
- Contact storage in vCard-like format
- Memory management for large contact imports
- Enhanced user interface for contact management
- Automatic backups before database conversion

### v1.6
- **vCard Export**: Export contacts to `/tmp/calendar.vcf`
- **Database Converter**: UI for format conversion
- **Auto-conversion**: Automatic format conversion option
- **Contact Sorting**: Sort by name, birthday, or category in export
- **Progress Tracking**: Visual feedback for all operations
- **Performance**: Faster contact deduplication with cache
- **UI**: Better progress bars and completion messages
- **Config**: New database format settings

### v1.7
- **ICS Event Management**: Browse, edit, delete imported events
- **ICS Events Browser**: Similar to contacts browser with navigation
- **ICS Event Editor**: Full-screen dialog like contact editor
- **ICS File Archive**: Store imported .ics files in `/base/ics`
- **Duplicate Detection**: Smart cache for fast duplicate checking
- **Enhanced Search**: Search in events titles, descriptions, dates

### v1.8
- **Universal Navigation System**: CH+/CH- wrap-around navigation in ALL screens
- **Intelligent Event Time Conversion**: Auto-converts events when default time changes
- **Real-time Position Display**: Shows current position in all interfaces
- **Jump to Today**: BLUE button jumps to today's event from anywhere
- **Auto-save Navigation**: Changes saved when navigating with CH+/CH-
- **Page Navigation**: PAGE UP/DOWN to skip 5 items
- **Unified Interface**: Same navigation across all dialogs and browsers

### v1.9
- **Autostart System**: Implemented auto-start system at decoder boot

## 🤝 Contributing
Contributions are welcome! Please ensure:
- Code follows existing style and structure
- New features include appropriate configuration options
- All changes are tested on Enigma2 receivers
- Audio files follow naming convention: `beep`, `notify`, `alert` with `.wav` or `.mp3` extension
- Holiday data follows JSON Lines format compatible with Holidata.net
- vCard import supports standard vCard 2.1/3.0 format
- Navigation system maintains wrap-around functionality across all screens

## 📄 License

This plugin is open-source software. See the LICENSE file for details.

## 🙏 Credits

- **Original Developer**: Sirius0103
- **Modifications & Event System**: Lululla
- **vCard System & Contact Management**: Lululla
- **Audio Notification System**: Integrated by Lululla
- **Holiday Import System**: Integrated by Lululla
- **ICS Import & Universal Navigation**: Lululla
- **Homepage**: www.linuxsat-support.com - www.corvoboys.org - www.gisclub.tv

---

*Note: This plugin requires an Enigma2-based receiver (OpenPLi, OpenATV, etc.)*
*Audio notifications work best with receivers that support audio playback via eServiceReference*
*Holiday import requires internet connection to access Holidata.net*
*vCard import requires .vcf or .vcard files in standard vCard format*
*Contact management requires sufficient disk space for contact storage*
*Universal navigation requires CH+/CH- buttons on your remote control*
```
