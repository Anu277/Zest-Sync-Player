# Zest Sync Player

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows/)

**AI-Powered Video Player with Automatic Subtitle Generation & Translation**

## 🚀 Available Versions

- **Zest Sync Player** - CPU-optimized version for all devices
- **Zest Sync G** - GPU-accelerated version for CUDA-compatible devices (5-10x faster)

![Zest Sync Player Demo](https://raw.githubusercontent.com/Anu277/Zest-Sync-Player/refs/heads/main/icon.ico)

## 🎯 Features

- **🎬 Video Playback**: Supports MP4, MKV, AVI formats with MPV engine
- **🤖 AI Subtitles**: Automatic speech-to-text using faster-whisper
- **🌍 Multi-Language**: Translate subtitles to 14 languages (90+ transcription languages)
- **⚡ Dual Accuracy**: Fast/Slow modes for optimal speed vs quality
- **📱 Responsive UI**: Modern dark interface with adaptive sizing and smooth animations
- **🎛️ Full Controls**: Speed, volume, fullscreen, timeline scrubbing
- **📂 Queue Management**: Playlist support with drag-drop, auto-play, and visual queue indicators
- **⚙️ Smart Settings**: Scrollable settings panel with font customization and stroke options
- **🎨 Subtitle Customization**: Font color selection (7 colors) and text stroke toggle for better readability
- **🔄 System Info**: Automatic hardware detection and performance logging
- **🎓 Interactive Tutorial**: First-time user guide with visual walkthrough
- **📊 Real-time Progress**: Live estimated time display during subtitle generation
- **🔒 Complete Uninstall**: Removes all cache, settings, and system integration

## 🚀 Quick Start

### For Users
1. **Choose Version**:
   - **Zest Sync Player**: Standard CPU version (works on all devices)
   - **Zest Sync G**: GPU version (requires CUDA-compatible NVIDIA GPU)
2. **Download** the installer from [GitHub Releases](https://github.com/anu277/zest-sync-player/releases/latest)
3. **Install** and run the application
4. **Tutorial**: Interactive guide shows you how to use the player (first-time users)
5. **First Launch**: Select languages to download (one-time setup)
6. **Import Video**: Click the **'+'** button to add media files
7. **Generate Subtitles**: Select language and click "Generate"

### For Developers

> **⚠️ Important**: Due to GitHub file size limits, you'll need to manually add these required files:
> 
> **FFmpeg** (Download from [ffmpeg.org](https://ffmpeg.org/download.html)):
> ```
> ffmpeg/
> ├── bin/
> │   ├── ffmpeg.exe
> │   ├── ffplay.exe
> │   └── ffprobe.exe
> ├── ffmpeg.exe
> └── ffprobe.exe
> ```
> 
> **Faster-Whisper Models** (Download from [Hugging Face](https://huggingface.co/guillaumekln/)):
> ```
> Whisper/
> ├── base/          # Fast mode model
> │   ├── config.json
> │   ├── model.bin
> │   ├── tokenizer.json
> │   └── vocabulary.txt
> └── small/         # Slow mode model
>     ├── config.json
>     ├── model.bin
>     ├── tokenizer.json
>     └── vocabulary.txt
> ```
> 
> **Additional Files**:
> - `libmpv-2.dll` (MPV library)
> - `mpv.exe` (MPV player)
> - `icon.ico` (Application icon)
> - `assets/intro.mp4` (Intro video)
> - `assets/manual/` (Tutorial images: 1.jpg, 3.jpg, 4.jpg, 5.png)

```bash
git clone https://github.com/anu277/zest-sync-player.git
cd zest-sync-player
pip install -r requirements.txt
python main.py
```

## 🌐 Supported Languages

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

## ⌨️ Keyboard Shortcuts

- **K**: Play/Pause
- **J/L**: Skip backward/forward (10s)
- **U/I**: Volume down/up
- **F**: Toggle fullscreen
- **Mouse Wheel**: Volume control (over video)

## 📋 System Requirements

### Zest Sync Player (CPU Version)
- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space + language models
- **Internet**: Required for initial model downloads

### Zest Sync G (GPU Version)
- **OS**: Windows 10/11 (64-bit)
- **GPU**: CUDA-compatible NVIDIA GPU (GTX 1050+)
- **CUDA**: CUDA 12.8 ([download from NVIDIA](https://developer.nvidia.com/cuda-12-8-0-download-archive))
- **VRAM**: 4GB minimum for optimal performance
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 2GB free space + language models
- **Internet**: Required for initial model downloads

## 🔧 How It Works

1. **Audio Extraction**: FFmpeg extracts audio from video with optimized settings
2. **Speech Recognition**: faster-whisper transcribes with dual accuracy modes
3. **Translation**: Helsinki-NLP models with automatic model downloading
4. **Multi-threading**: Background processing prevents UI freezing
5. **Subtitle Display**: Real-time overlay with customizable fonts, colors, stroke effects, and transparency

## 📁 File Locations

- **Installation**: `C:\Program Files\Zest Sync Player\`
- **Logs**: `%USERPROFILE%\.zestsync_logs\`
- **Models**: `%LOCALAPPDATA%\Zest Sync\cache\models\hub\`
- **Settings**: `%USERPROFILE%\.zestsyncsetting.json`
- **Subtitles**: Saved next to video files as `.srt`

> **Note**: Both CPU and GPU versions use the same installation path. Installing one version will replace the other.

## 🛠️ Troubleshooting

### Slow Subtitle Generation
- **Cause**: CPU-intensive AI processing
- **Solution**: Use Fast mode, close other applications, ensure SSD storage

### Model Download Fails
- **Cause**: Network connectivity or Windows symlink issues
- **Solution**: Check internet connection, run as administrator, retry download

### Video Won't Play
- **Cause**: Unsupported format or missing codecs
- **Solution**: Convert to MP4/H.264 format, install K-Lite Codec Pack

### Application Won't Start
- **Cause**: Missing dependencies or antivirus blocking
- **Solution**: Add to antivirus exclusions, run as administrator, check logs

### CUDA Not Detected (Zest Sync G)
- **Cause**: Missing CUDA 12.8 or incompatible GPU
- **Solution**: Download [CUDA 12.8 from NVIDIA](https://developer.nvidia.com/cuda-12-8-0-download-archive), update NVIDIA drivers, or use CPU version

### Settings Not Saving
- **Cause**: File permissions or corrupted settings file
- **Solution**: Run as administrator, delete `.zestsyncsetting.json` to reset

## 🎨 UI Enhancements

**New Interface Features**:
- **Responsive Design**: UI elements automatically scale based on screen size
- **Scrollable Settings**: Settings panel with vertical scrolling for better organization
- **Visual Queue Indicators**: Playing media items highlighted with red-orange theme color
- **Font Customization**: 7 color options (Black, Blue, Green, Orange, Red, White, Yellow)
- **Text Stroke Toggle**: Optional subtitle outline for improved readability
- **Adaptive Sizing**: Controls and buttons scale appropriately for different screen resolutions

## 📊 Performance Notes

### Zest Sync Player (CPU Version)
**Estimated Generation Times** (based on i5-10300H, 4C/8T):
- **English Fast Mode**: ~1.4 minutes per 10-minute video
- **English Slow Mode**: ~10 minutes per 25-minute video (higher accuracy)
- **Translation**: ~1.2-4 minutes depending on target language
- **RAM Usage**: ~600MB during processing

### Zest Sync G (GPU Version)
**Estimated Generation Times** (based on GTX 1650, 4GB VRAM):
- **English Fast Mode**: ~18 seconds per 2.35-minute video (5-7x faster)
- **English Slow Mode**: ~100 seconds per 24-minute video (6-8x faster)
- **Translation**: ~30-90 seconds depending on target language
- **VRAM Usage**: ~2.3GB peak, 1.6GB persistent

*Performance varies by GPU model, VRAM, CPU speed, and available RAM.*

## 🔒 Privacy & Data

- **Local Processing**: All AI processing happens on your device
- **No Data Upload**: Videos and subtitles never leave your computer
- **Model Downloads**: Only language models are downloaded from Hugging Face
- **Logs**: Local debug logs only (auto-deleted after 24 hours)
- **Clean Uninstall**: Complete removal of all data, cache, and system integration

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/anu277/zest-sync-player/issues)
- **Logs**: Check `%USERPROFILE%\.zestsync_logs\`
- **Discussions**: [GitHub Discussions](https://github.com/anu277/zest-sync-player/discussions)
- **Uninstall**: Use Windows "Add or Remove Programs" (removes all data and cache)

## 📚 Documentation

For detailed technical documentation, see [DOCUMENTATION.md](DOCUMENTATION.md).

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- **Whisper AI**: OpenAI (Speech Recognition)
- **Helsinki-NLP**: University of Helsinki (Translation Models)
- **PyQt6**: GUI Framework
- **FFmpeg**: Media Processing
- **MPV**: Video Playback Engine

---

**Version 2.1** | Built for Windows 10/11 | Available in CPU and GPU-accelerated versions | Self-contained AI-powered video player with responsive UI, enhanced subtitle customization, and dual accuracy modes