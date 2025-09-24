# Changelog

All notable changes to Zest Sync Player will be documented in this file.

## [2.1.0] - 2025-09-19

### Added
- 📱 Responsive UI design that automatically scales based on screen size
- ⚙️ Scrollable settings panel with vertical scrolling for better organization
- 🎨 Font color selection dropdown with 7 color options (Black, Blue, Green, Orange, Red, White, Yellow)
- 🖋️ Text stroke toggle switch for improved subtitle readability
- 🎯 Visual queue indicators - playing media items highlighted with red-orange theme color (#e50409)
- 🔧 Adaptive sizing for controls and buttons based on screen resolution
- ✨ Enhanced media list widget styling with custom scrollbars
- 🎨 White set as default subtitle color for better visibility

### Changed
- 🖼️ Reverted custom window controls back to default Windows title bar
- 🎨 Updated media queue item colors to use red-orange theme instead of green
- 📐 Improved responsive sizing calculations for different screen resolutions
- 🎛️ Enhanced subtitle customization with color and stroke management

### Technical Improvements
- Better color management system for subtitle customization
- Improved UI scaling algorithms for responsive design
- Enhanced settings panel layout with proper scrolling
- Optimized media list styling and visual feedback

## [2.0.0] - 2025-09-15

### Added
- 🎓 Interactive tutorial system for first-time users
- 🤖 AI-powered automatic subtitle generation using faster-whisper
- 🌍 Multi-language translation support (14+ languages)
- ⚡ Dual accuracy modes (Fast/Slow) for optimal speed vs quality
- 📱 Modern dark UI interface with smooth animations
- 📂 Queue management with drag-drop playlist support
- 🎛️ Full video controls (speed, volume, fullscreen, timeline scrubbing)
- ⌨️ Keyboard shortcuts for better user experience
- 📊 Real-time progress with estimated time display
- 🔄 System info with automatic hardware detection
- 🔒 Complete uninstall with cache and settings cleanup

### Features
- Support for MP4, MKV, AVI video formats with MPV engine
- Local AI processing (no data upload required)
- Automatic subtitle saving as .srt files next to videos
- Performance optimizations for CPU-intensive processing
- Persistent settings for accuracy modes and font sizes
- Auto-play and queue management
- Visual tutorial walkthrough with manual images

### Technical
- Built with PyQt6 for modern GUI framework
- Integrated FFmpeg for optimized media processing
- MPV engine for high-quality video playback
- faster-whisper for efficient speech recognition
- Helsinki-NLP models for translation
- Multi-threading to prevent UI freezing
- Automatic model downloading from Hugging Face

### Performance
- Fast mode: ~1.4 minutes per 10-minute video
- Slow mode: ~10 minutes per 25-minute video (higher accuracy)
- Translation: ~1.2-4 minutes depending on language
- RAM usage: ~600MB during processing

### Fixed
- Generate button timing issues during translation
- Estimated time calculations for accuracy modes
- UI updates between generation completion and SRT loading
- Progress display synchronization

### Known Issues
- Subtitle generation is CPU-intensive (use Fast mode for speed)
- Model downloads require internet connection

## [1.0.0] - Initial Release

### Features
- VLC Media Player integration with ZSLoader extension
- Automatic subtitle generation using OpenAI Whisper
- Background processing with Windows startup script
- Automatic .srt file generation when opening videos in VLC
- Windows notification system integration
- Subtitle track switching with 'V' key in VLC

### Setup Requirements
- VLC Media Player installation required
- Manual startup script (start_zestsync.vbs) placement
- Administrator setup.bat execution
- ZSLoader extension activation in VLC
- Optional Python 3.8+ with dependencies (moviepy, psutil, openai-whisper, winotify)

### Technical
- Background EXE process integration
- VLC extension-based architecture
- Windows Startup folder integration
- Command-line dependency management 