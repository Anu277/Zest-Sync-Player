# Zest Sync Player - Complete Documentation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows/)

**AI-Powered Video Player with Automatic Subtitle Generation & Translation**

## 🚀 Available Versions

- **Zest Sync Player** - CPU-optimized version for all devices
- **Zest Sync G** - GPU-accelerated version for CUDA-compatible devices (5-10x faster)

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [System Requirements](#system-requirements)
4. [Installation](#installation)
5. [User Guide](#user-guide)
6. [Developer Guide](#developer-guide)
7. [Technical Architecture](#technical-architecture)
8. [API Reference](#api-reference)
9. [Troubleshooting](#troubleshooting)
10. [Performance](#performance)
11. [Privacy & Security](#privacy--security)
12. [Contributing](#contributing)
13. [Changelog](#changelog)
14. [License](#license)

---

## Overview

Zest Sync Player is a revolutionary AI-powered video player that automatically generates and translates subtitles for any video file. Built with cutting-edge machine learning technology, it provides a seamless experience for content creators, international viewers, and accessibility requirements.

### Key Highlights
- **Local Processing**: No internet required after initial setup
- **90+ Languages**: Transcription support for global content
- **14 Translation Languages**: Real-time subtitle translation
- **Dual Accuracy Modes**: Balance between speed and precision
- **Modern GUI**: Professional dark interface with full controls
- **Zero Dependencies**: Complete standalone application

---

## Features

### 🎬 Video Playback
- **Supported Formats**: MP4, MKV, AVI with MPV engine
- **Full Controls**: Play/pause, speed adjustment, volume control
- **Timeline Scrubbing**: Precise seeking with visual feedback
- **Fullscreen Mode**: Immersive viewing experience
- **Keyboard Shortcuts**: Professional hotkey support

### 🤖 AI Subtitle Generation
- **faster-whisper Technology**: State-of-the-art speech recognition
- **Dual Accuracy Modes**: 
  - Fast Mode: ~1.4 minutes for 10-minute video
  - Slow Mode: ~10 minutes for 25-minute video (higher accuracy)
- **Real-time Progress**: Live estimated time display
- **Automatic SRT Saving**: Files saved next to video automatically

### 🌍 Multi-Language Support
- **90+ Transcription Languages**: Including English, Spanish, French, German, Italian, Japanese, Russian, Arabic, Chinese, Hindi, Dutch, Swedish, Ukrainian, Urdu
- **14 Translation Languages**: Real-time subtitle translation
- **Language Detection**: Automatic source language identification
- **Model Management**: Automatic downloading and caching

### 📱 User Interface
- **Modern Dark Theme**: Professional Netflix-style interface
- **Interactive Tutorial**: First-time user guidance system
- **Drag & Drop**: Easy file import with visual feedback
- **Queue Management**: Playlist support with auto-play
- **Settings Persistence**: Remembers user preferences

### ⚙️ Advanced Features
- **System Info Detection**: Automatic hardware profiling
- **Multi-threading**: Background processing prevents UI freezing
- **Complete Uninstall**: Removes all cache, settings, and integration
- **Performance Logging**: Detailed debug information
- **Memory Optimization**: Efficient resource management

---

## System Requirements

### Zest Sync Player (CPU Version)
#### Minimum Requirements
- **Operating System**: Windows 10 (64-bit) or Windows 11
- **RAM**: 4GB minimum
- **Storage**: 2GB free space + language models
- **Processor**: Intel i3 or AMD equivalent
- **Internet**: Required for initial model downloads only

#### Recommended Requirements
- **RAM**: 8GB or more for optimal performance
- **Storage**: SSD for faster processing
- **Processor**: Intel i5 or AMD Ryzen 5 (4+ cores)

### Zest Sync G (GPU Version)
#### Minimum Requirements
- **Operating System**: Windows 10 (64-bit) or Windows 11
- **GPU**: CUDA-compatible NVIDIA GPU (GTX 1050+)
- **CUDA**: CUDA 12.8 ([download from NVIDIA](https://developer.nvidia.com/cuda-12-8-0-download-archive))
- **VRAM**: 4GB minimum for optimal performance
- **RAM**: 8GB minimum
- **Storage**: 2GB free space + language models
- **Processor**: Intel i5 or AMD Ryzen 5 (4+ cores)
- **Internet**: Required for initial model downloads only

#### Recommended Requirements
- **VRAM**: 6GB+ for handling larger models
- **RAM**: 16GB for optimal performance
- **Storage**: NVMe SSD for fastest processing
- **GPU**: RTX series for maximum acceleration

### Language Model Sizes
| Language | Code | Model Size |
|----------|------|------------|
| English | en | 300MB |
| Spanish | es | 1.16GB |
| French | fr | 1.10GB |
| German | de | 1.6GB |
| Italian | it | 958MB |
| Japanese | jap | 820MB |
| Russian | ru | 1.38GB |
| Arabic | ar | 1.38GB |
| Chinese | zh | 620MB |
| Hindi | hi | 587MB |
| Dutch | nl | 1.43GB |
| Swedish | sv | 1.31GB |
| Ukrainian | uk | 585MB |
| Urdu | ur | 870MB |

---

## Installation

### For End Users

#### Method 1: Installer (Recommended)
1. **Choose Version**:
   - Download `ZestSyncPlayer-CPU-Setup.exe` for standard CPU version
   - Download `ZestSyncG-GPU-Setup.exe` for GPU-accelerated version
2. Run the installer as Administrator
3. Follow the installation wizard
4. Launch from Start Menu or Desktop shortcut

> **Note**: Both versions install to the same directory. Installing one will replace the other.

#### Method 2: Portable Version
1. Download the portable ZIP from releases
2. Extract to desired location
3. Run `Zest Sync Player.exe`

### For Developers

#### Prerequisites
```bash
# Install Python 3.10+
# Download from python.org

# Install Git
# Download from git-scm.com
```

#### Clone and Setup
```bash
git clone https://github.com/anu277/zest-sync-player.git
cd zest-sync-player
pip install -r requirements.txt
```

#### Required Files (Not in Repository)
Due to GitHub file size limits, manually add:

**FFmpeg** (Download from [ffmpeg.org](https://ffmpeg.org/download.html)):
```
ffmpeg/
├── bin/
│   ├── ffmpeg.exe
│   ├── ffplay.exe
│   └── ffprobe.exe
├── ffmpeg.exe
└── ffprobe.exe
```

**Faster-Whisper Models** (Download from [Hugging Face](https://huggingface.co/guillaumekln/)):
```
Whisper/
├── base/          # Fast mode model
│   ├── config.json
│   ├── model.bin
│   ├── tokenizer.json
│   └── vocabulary.txt
└── small/         # Slow mode model
    ├── config.json
    ├── model.bin
    ├── tokenizer.json
    └── vocabulary.txt
```

**Additional Files**:
- `libmpv-2.dll` (MPV library)
- `mpv.exe` (MPV player)
- `icon.ico` (Application icon)
- `assets/intro.mp4` (Intro video)
- `assets/manual/` (Tutorial images: 1.jpg, 3.jpg, 4.jpg, 5.png)

#### Run Development Version
```bash
python main.py
```

---

## User Guide

### First Launch Experience

#### 1. Intro Video
- Beautiful welcome video showcases the application
- Sets the tone for professional experience
- Automatically transitions to tutorial

#### 2. Interactive Tutorial
- **Step 1**: Import video files using the '+' button
- **Step 2**: Select source language from dropdown
- **Step 3**: Choose accuracy mode and click Generate
- **Step 4**: Watch with automatically loaded subtitles
- Visual guides with actual screenshots
- Skip option for experienced users

#### 3. Language Setup
- First-time language selection
- Automatic model downloading with progress
- One-time setup per language

### Basic Usage

#### Importing Videos
1. **Method 1**: Click the '+' button in the interface
2. **Method 2**: Drag and drop video files onto the window
3. **Method 3**: Use File menu > Open Video
4. **Supported Formats**: MP4, MKV, AVI

#### Generating Subtitles
1. Select video from queue
2. Choose source language from dropdown (90+ options)
3. Select accuracy mode:
   - **Fast Mode**: Quick processing, good accuracy
   - **Slow Mode**: Longer processing, maximum accuracy
4. Click "Generate Subtitles"
5. Monitor real-time progress with estimated completion time
6. Subtitles automatically load when complete

#### Translation
1. Generate original subtitles first
2. Click "Translate" button
3. Select target language (14 options available)
4. Wait for translation processing
5. Translated subtitles replace original automatically

#### Playback Controls
- **Play/Pause**: Spacebar or K key
- **Seek**: J (backward 10s), L (forward 10s)
- **Volume**: U (down), I (up), or mouse wheel over video
- **Fullscreen**: F key or double-click video
- **Speed**: Use speed slider or +/- keys
- **Timeline**: Click or drag on progress bar

### Advanced Features

#### Queue Management
- **Add Multiple Videos**: Drag multiple files at once
- **Reorder**: Drag videos in queue to reorder
- **Remove**: Right-click video > Remove
- **Auto-play**: Automatically plays next video in queue
- **Clear Queue**: File menu > Clear Queue

#### Settings & Preferences
- **Accuracy Mode**: Persistent selection (Fast/Slow)
- **Font Size**: Adjustable subtitle text size
- **Language Preferences**: Remember last used languages
- **Auto-save**: Settings saved automatically

#### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| K | Play/Pause |
| J | Skip backward 10 seconds |
| L | Skip forward 10 seconds |
| U | Volume down |
| I | Volume up |
| F | Toggle fullscreen |
| + | Increase playback speed |
| - | Decrease playback speed |
| Mouse Wheel | Volume control (over video) |

---

## Developer Guide

### Project Structure
```
zest-sync-player/
├── main.py                 # Main application entry point
├── tutorial_window.py      # Tutorial system implementation
├── requirements.txt        # Python dependencies
├── main_onedir.spec       # PyInstaller configuration
├── ZestSyncInstaller.iss  # Inno Setup installer script
├── assets/
│   ├── intro.mp4          # Welcome video
│   └── manual/            # Tutorial images
├── ffmpeg/                # FFmpeg binaries
├── Whisper/               # AI models
└── docs/                  # Documentation
```

### Core Components

#### Main Application (main.py)
```python
class VideoPlayer(QMainWindow):
    """Main application window with video playback and subtitle generation"""
    
    def __init__(self):
        # Initialize UI components
        # Setup MPV player
        # Configure AI models
        
    def generate_subtitles(self):
        # Extract audio using FFmpeg
        # Process with faster-whisper
        # Generate SRT file
        
    def translate_subtitles(self):
        # Load existing SRT
        # Process with Helsinki-NLP
        # Save translated SRT
```

#### Tutorial System (tutorial_window.py)
```python
class TutorialWindow(QDialog):
    """Interactive tutorial with image carousel"""
    
    def __init__(self):
        # Setup 4-step tutorial
        # Load manual images
        # Configure navigation
        
    def show_step(self, step):
        # Display tutorial step
        # Update navigation buttons
        # Handle completion
```

### Key Technologies

#### PyQt6 Framework
- **QMainWindow**: Main application window
- **QMediaPlayer**: Video playback (replaced with MPV)
- **QThread**: Background processing
- **QProgressBar**: Real-time progress display
- **QComboBox**: Language selection
- **QSlider**: Volume and speed controls

#### MPV Integration
```python
import mpv

class MPVWidget(QWidget):
    def __init__(self):
        self.mpv = mpv.MPV(
            wid=str(int(self.winId())),
            vo='gpu,direct3d',
            hwdec='auto'
        )
```

#### AI Processing
```python
from faster_whisper import WhisperModel

# Initialize model
model = WhisperModel("base", device="cpu", compute_type="int8")

# Transcribe audio
segments, info = model.transcribe("audio.wav", language="en")
```

#### Translation
```python
from easynmt import EasyNMT

# Initialize translation model
model = EasyNMT('opus-mt')

# Translate text
translated = model.translate(text, target_lang='es')
```

### Building Executable

#### PyInstaller Configuration
```python
# main_onedir.spec
a = Analysis(
    ['main.py'],
    binaries=[
        ('libmpv-2.dll', '.'),
        ('mpv.exe', '.'),
        ('ffmpeg/ffmpeg.exe', 'ffmpeg'),
    ],
    datas=[
        ('assets/intro.mp4', 'assets'),
        ('Whisper', 'whisper'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'faster_whisper',
        'easynmt',
    ]
)
```

#### Build Commands
```bash
# Create executable
pyinstaller main_onedir.spec

# Create installer
iscc ZestSyncInstaller.iss
```

### Testing

#### Unit Tests
```python
import unittest
from main import VideoPlayer

class TestVideoPlayer(unittest.TestCase):
    def test_subtitle_generation(self):
        # Test subtitle generation functionality
        pass
        
    def test_translation(self):
        # Test translation functionality
        pass
```

#### Integration Tests
```python
def test_full_workflow():
    # Test complete user workflow
    # Import video -> Generate -> Translate -> Play
    pass
```

---

## Technical Architecture

### System Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PyQt6 GUI     │    │  MPV Player     │    │  AI Processing  │
│                 │    │                 │    │                 │
│ • Main Window   │◄──►│ • Video Render  │    │ • faster-whisper│
│ • Tutorial      │    │ • Audio Output  │    │ • Helsinki-NLP  │
│ • Settings      │    │ • Subtitle Sync │    │ • Model Cache   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                        ┌─────────────────┐
                        │  FFmpeg Engine  │
                        │                 │
                        │ • Audio Extract │
                        │ • Format Convert│
                        │ • Media Info    │
                        └─────────────────┘
```

### Data Flow
1. **Video Import**: User selects video file
2. **Audio Extraction**: FFmpeg extracts audio track
3. **AI Processing**: faster-whisper transcribes speech
4. **SRT Generation**: Formatted subtitle file created
5. **Translation** (Optional): Helsinki-NLP translates text
6. **Playback**: MPV loads video with synchronized subtitles

### Threading Model
```python
# Main Thread: UI and user interaction
# Worker Thread 1: Audio extraction (FFmpeg)
# Worker Thread 2: AI transcription (faster-whisper)
# Worker Thread 3: Translation (Helsinki-NLP)
# Timer Thread: Progress updates and UI refresh
```

### Memory Management
- **Model Caching**: AI models loaded once, reused
- **Audio Buffering**: Temporary audio files cleaned automatically
- **Progress Tracking**: Minimal memory footprint for real-time updates
- **Resource Cleanup**: Proper disposal of threads and temporary files

---

## API Reference

### Main Classes

#### VideoPlayer
```python
class VideoPlayer(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        """Initialize the video player application"""
        
    def import_video(self, file_path: str) -> bool:
        """Import a video file into the queue"""
        
    def generate_subtitles(self, language: str, accuracy: str) -> None:
        """Generate subtitles for current video"""
        
    def translate_subtitles(self, target_lang: str) -> None:
        """Translate existing subtitles"""
        
    def play_video(self) -> None:
        """Start video playback"""
        
    def pause_video(self) -> None:
        """Pause video playback"""
```

#### TutorialWindow
```python
class TutorialWindow(QDialog):
    """Interactive tutorial system"""
    
    def __init__(self, parent=None):
        """Initialize tutorial window"""
        
    def show_step(self, step: int) -> None:
        """Display specific tutorial step"""
        
    def next_step(self) -> None:
        """Navigate to next tutorial step"""
        
    def previous_step(self) -> None:
        """Navigate to previous tutorial step"""
```

### Configuration

#### Settings Management
```python
# Settings file: ~/.zestsyncsetting.json
{
    "accuracy_mode": "fast",
    "font_size": 14,
    "last_language": "en",
    "tutorial_completed": true,
    "window_geometry": "800x600+100+100"
}
```

#### Language Codes
```python
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish', 
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'ja': 'Japanese',
    'ru': 'Russian',
    'ar': 'Arabic',
    'zh': 'Chinese',
    'hi': 'Hindi',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'uk': 'Ukrainian',
    'ur': 'Urdu'
}
```

---

## Troubleshooting

### Common Issues

#### Slow Subtitle Generation
**Symptoms**: Processing takes longer than expected
**Causes**: 
- CPU-intensive AI processing
- Large video files
- Background applications consuming resources
**Solutions**:
- Use Fast mode instead of Slow mode
- Close unnecessary applications
- Ensure video is stored on SSD
- Check available RAM (minimum 4GB)

#### Model Download Fails
**Symptoms**: Error during language model download
**Causes**:
- Network connectivity issues
- Windows symlink restrictions
- Insufficient disk space
**Solutions**:
- Check internet connection stability
- Run application as Administrator
- Free up disk space (models can be 1GB+)
- Retry download after network issues resolve

#### Video Won't Play
**Symptoms**: Black screen or error when opening video
**Causes**:
- Unsupported video format
- Corrupted video file
- Missing codecs
**Solutions**:
- Convert video to MP4 with H.264 codec
- Try different video file to isolate issue
- Install K-Lite Codec Pack
- Check video file integrity

#### Application Won't Start
**Symptoms**: Application crashes on launch or won't open
**Causes**:
- Missing dependencies
- Antivirus software blocking
- Corrupted installation
**Solutions**:
- Add application to antivirus exclusions
- Run as Administrator
- Reinstall application
- Check Windows Event Viewer for error details

#### CUDA Not Detected
**Symptoms**: No GPU acceleration available
**Causes**:
- Missing CUDA 12.8 installation
- Outdated GPU drivers
- Incompatible GPU
**Solutions**:
- Download and install [CUDA 12.8 from NVIDIA](https://developer.nvidia.com/cuda-12-8-0-download-archive)
- Update NVIDIA drivers
- Verify GPU CUDA compatibility
- Use CPU processing as fallback

#### Settings Not Saving
**Symptoms**: Preferences reset on application restart
**Causes**:
- File permission issues
- Corrupted settings file
- Antivirus blocking file writes
**Solutions**:
- Run as Administrator
- Delete `.zestsyncsetting.json` to reset
- Add settings folder to antivirus exclusions
- Check user profile permissions

### Debug Information

#### Log Files
- **Location**: `%USERPROFILE%\.zestsync_logs\`
- **Retention**: 24 hours automatic cleanup
- **Content**: Detailed processing information, error traces

#### System Information
```python
# Automatically collected on startup
{
    "os": "Windows 10",
    "cpu": "Intel i5-10300H",
    "ram": "16GB",
    "gpu": "NVIDIA GTX 1650",
    "python": "3.10.8",
    "cuda": "Available"
}
```

#### Performance Monitoring
- Real-time memory usage tracking
- Processing time measurements
- Model loading performance
- Thread utilization statistics

---

## Performance

### Benchmarks

#### Processing Times

**CPU Version (Intel i5-10300H, 4C/8T)**
| Video Length | Fast Mode | Slow Mode | Translation |
|--------------|-----------|-----------|-------------|
| 5 minutes | 42 seconds | 2.5 minutes | 30-90 seconds |
| 10 minutes | 1.4 minutes | 5 minutes | 1-2 minutes |
| 25 minutes | 3.5 minutes | 10 minutes | 2.5-4 minutes |
| 60 minutes | 8.5 minutes | 24 minutes | 6-10 minutes |

**GPU Version (GTX 1650, 4GB VRAM)**
| Video Length | Fast Mode | Slow Mode | Translation |
|--------------|-----------|-----------|-------------|
| 2.35 minutes | 18 seconds | 42 seconds | 15-30 seconds |
| 10 minutes | 77 seconds | 3 minutes | 45-90 seconds |
| 24 minutes | 3 minutes | 6.5 minutes | 2-3 minutes |
| 60 minutes | 7.5 minutes | 16 minutes | 5-7 minutes |

#### Memory Usage

**CPU Version**
- **Idle**: ~150MB
- **Video Playback**: ~300MB
- **Subtitle Generation**: ~600MB peak
- **Translation**: ~400MB additional

**GPU Version**
- **Idle**: ~200MB
- **Video Playback**: ~350MB
- **Subtitle Generation**: ~800MB RAM + 2.3GB VRAM peak
- **Translation**: ~450MB additional

#### Model Loading Times
| Model Size | First Load | Cached Load |
|------------|------------|-------------|
| 300MB (English) | 15-30 seconds | 2-5 seconds |
| 1GB+ (Other languages) | 45-90 seconds | 5-10 seconds |

### Optimization Tips

#### For Better Performance
1. **Use SSD Storage**: 2-3x faster audio extraction
2. **Close Background Apps**: More CPU/RAM for processing
3. **Fast Mode**: 7x faster than Slow mode
4. **Smaller Videos**: Process in segments if very long
5. **Adequate RAM**: 8GB+ recommended for large files

#### Hardware Recommendations
- **CPU**: 4+ cores, 3GHz+ for optimal performance
- **RAM**: 8GB minimum, 16GB for large videos
- **Storage**: SSD for temporary file operations
- **GPU**: CUDA-compatible for future acceleration

---

## Privacy & Security

### Data Protection

#### Local Processing
- **No Cloud Upload**: All processing happens on your device
- **No Data Collection**: No telemetry or usage statistics
- **No Account Required**: Completely offline operation
- **No Network Access**: Only for initial model downloads

#### File Handling
- **Temporary Files**: Automatically cleaned after processing
- **Original Videos**: Never modified or moved
- **Subtitle Files**: Saved locally next to video files
- **Settings**: Stored in user profile only

#### Model Downloads
- **Source**: Hugging Face (reputable AI model repository)
- **Verification**: Model integrity checked during download
- **Caching**: Models stored locally for offline use
- **Updates**: Manual only, no automatic updates

### Security Features

#### Application Security
- **Code Signing**: Executable signed for authenticity
- **Virus Scanning**: Regular scans of releases
- **Open Source**: Full source code available for audit
- **No Admin Rights**: Runs with standard user permissions

#### Network Security
- **HTTPS Only**: All downloads use encrypted connections
- **No Telemetry**: No data sent to external servers
- **Firewall Friendly**: No incoming connections required
- **Proxy Support**: Works through corporate proxies

---

## Contributing

### Development Setup

#### Prerequisites
- Python 3.10 or higher
- Git for version control
- Windows 10/11 for testing
- 8GB+ RAM for development

#### Getting Started
```bash
# Fork the repository on GitHub
git clone https://github.com/yourusername/zest-sync-player.git
cd zest-sync-player

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python main.py
```

### Code Style

#### Python Standards
- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type annotations where possible
- **Docstrings**: Document all classes and functions
- **Comments**: Explain complex logic and algorithms

#### Example Code Style
```python
from typing import Optional, List
from PyQt6.QtWidgets import QMainWindow

class VideoPlayer(QMainWindow):
    """Main video player application window.
    
    Handles video playback, subtitle generation, and user interface.
    Integrates MPV player with AI-powered subtitle processing.
    """
    
    def __init__(self) -> None:
        """Initialize the video player with default settings."""
        super().__init__()
        self._setup_ui()
        self._initialize_models()
    
    def generate_subtitles(self, 
                          video_path: str, 
                          language: str = "en",
                          accuracy: str = "fast") -> Optional[str]:
        """Generate subtitles for the specified video.
        
        Args:
            video_path: Path to the video file
            language: Source language code (e.g., 'en', 'es')
            accuracy: Processing mode ('fast' or 'slow')
            
        Returns:
            Path to generated SRT file, or None if failed
        """
        # Implementation here
        pass
```

### Testing

#### Unit Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_subtitle_generation.py

# Run with coverage
python -m pytest --cov=main tests/
```

#### Integration Tests
```bash
# Test full workflow
python tests/integration/test_full_workflow.py

# Test UI components
python tests/integration/test_ui.py
```

### Pull Request Process

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** Pull Request with detailed description

#### PR Requirements
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New features include tests
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)

---

## Changelog

### [2.0.0] - 2025-09-19

#### Added
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

#### Features
- Support for MP4, MKV, AVI video formats with MPV engine
- Local AI processing (no data upload required)
- Automatic subtitle saving as .srt files next to videos
- Performance optimizations for CPU-intensive processing
- Persistent settings for accuracy modes and font sizes
- Auto-play and queue management
- Visual tutorial walkthrough with manual images

#### Technical
- Built with PyQt6 for modern GUI framework
- Integrated FFmpeg for optimized media processing
- MPV engine for high-quality video playback
- faster-whisper for efficient speech recognition
- Helsinki-NLP models for translation
- Multi-threading to prevent UI freezing
- Automatic model downloading from Hugging Face

#### Performance
- Fast mode: ~1.4 minutes per 10-minute video
- Slow mode: ~10 minutes per 25-minute video (higher accuracy)
- Translation: ~1.2-4 minutes depending on language
- RAM usage: ~600MB during processing

#### Fixed
- Generate button timing issues during translation
- Estimated time calculations for accuracy modes
- UI updates between generation completion and SRT loading
- Progress display synchronization

#### Known Issues
- Subtitle generation is CPU-intensive (use Fast mode for speed)
- Model downloads require internet connection

### [3.0.0] - Planned Features

#### 🚀 Upcoming
- **🎮 CUDA GPU Acceleration**: Hardware-accelerated transcription for 5-10x faster processing
- **⚡ Batch Processing**: Divide long videos into 10-minute segments for parallel processing
- **🔄 Real-time SRT Loading**: Progressive subtitle display every 5 seconds as batches complete
- **📊 Advanced Progress**: Per-batch progress tracking with estimated completion times
- **🎯 Smart Segmentation**: Intelligent audio splitting at silence points for better accuracy
- **💾 Resume Support**: Continue processing from last completed batch after interruption

#### Technical Improvements
- PyTorch CUDA integration for GPU-accelerated Whisper models
- Multi-threaded batch processing with queue management
- Progressive SRT file writing and MPV subtitle reloading
- Memory optimization for handling multiple audio segments
- Automatic hardware detection (CPU vs GPU processing modes)

### [1.0.0] - Initial Release

#### Features
- VLC Media Player integration with ZSLoader extension
- Automatic subtitle generation using OpenAI Whisper
- Background processing with Windows startup script
- Automatic .srt file generation when opening videos in VLC
- Windows notification system integration
- Subtitle track switching with 'V' key in VLC

#### Setup Requirements
- VLC Media Player installation required
- Manual startup script (start_zestsync.vbs) placement
- Administrator setup.bat execution
- ZSLoader extension activation in VLC
- Optional Python 3.8+ with dependencies (moviepy, psutil, openai-whisper, winotify)

#### Technical
- Background EXE process integration
- VLC extension-based architecture
- Windows Startup folder integration
- Command-line dependency management

---

## License

### MIT License

Copyright (c) 2024 Zest Sync Player

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### Third-Party Licenses

#### Dependencies
- **PyQt6**: GPL v3 / Commercial License
- **faster-whisper**: MIT License
- **FFmpeg**: LGPL v2.1+ / GPL v2+
- **MPV**: GPL v2+
- **Helsinki-NLP Models**: Apache 2.0 / MIT (varies by model)

#### Acknowledgments
- **OpenAI Whisper**: Original speech recognition research
- **Hugging Face**: Model hosting and distribution
- **University of Helsinki**: Translation model development
- **FFmpeg Project**: Media processing capabilities
- **MPV Project**: Video playback engine

---

## Support & Contact

### Getting Help

#### Documentation
- **README**: Quick start guide and basic usage
- **This Document**: Comprehensive documentation
- **GitHub Wiki**: Community-contributed guides
- **Code Comments**: Inline documentation for developers

#### Community Support
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community help
- **Stack Overflow**: Technical programming questions (tag: zest-sync-player)

#### Professional Support
For commercial use or professional support:
- Email: [anub0709@gmail.com](mailto:anub0709@gmail.com)
- Response time: 24-48 hours
- Available for custom development and integration

### Reporting Issues

#### Bug Reports
When reporting bugs, please include:
1. **System Information**: OS version, RAM, CPU
2. **Application Version**: Found in Help > About
3. **Steps to Reproduce**: Detailed reproduction steps
4. **Expected Behavior**: What should happen
5. **Actual Behavior**: What actually happens
6. **Log Files**: From `%USERPROFILE%\.zestsync_logs\`
7. **Screenshots**: If UI-related issue

#### Feature Requests
For new features:
1. **Use Case**: Why is this feature needed?
2. **Proposed Solution**: How should it work?
3. **Alternatives**: Other ways to achieve the goal
4. **Priority**: How important is this feature?

---

**Zest Sync Player v2.1** | Available in CPU and GPU versions | Built for Windows 10/11 | Self-contained AI-powered video player with comprehensive documentation

*Last updated: September 2025*