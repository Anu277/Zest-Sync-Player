# Zest Sync Player

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows/)

**AI-Powered Video Player with Automatic Subtitle Generation & Translation**

![Zest Sync Player Demo](https://raw.githubusercontent.com/anu277/zest-sync-player/icon.ico)

## 🎯 Features

- **🎬 Video Playback**: Supports MP4, MKV, AVI formats
- **🤖 AI Subtitles**: Automatic speech-to-text using Whisper AI
- **🌍 Multi-Language**: Translate subtitles to 14+ languages
- **⚡ Real-time**: Generate subtitles while watching
- **📱 Modern UI**: Dark interface
- **🎛️ Full Controls**: Speed, volume, fullscreen, timeline
- **📂 Queue Management**: Playlist support with auto-play

## 🚀 Quick Start

### For Users
1. **Download** the installer from [GitHub Releases](https://github.com/anu277/zest-sync-player/releases/latest)
2. **Install** and run the application
3. **First Launch**: Select languages to download (one-time setup)
4. **Import Video**: Click the **'+'** button to add media files
5. **Generate Subtitles**: Select language and click "Generate"

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
> **Faster-Whisper Base Model** (Download from [Hugging Face](https://huggingface.co/guillaumekln/faster-whisper-base)):
> ```
> Whisper/
> ├── config.json
> ├── main
> ├── model.bin
> ├── tokenizer.json
> └── vocabulary.txt
> ```

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

- **Space**: Play/Pause
- **←/→**: Skip backward/forward (10s)
- **↑/↓**: Volume up/down
- **F**: Toggle fullscreen
- **Mouse Wheel**: Volume control (over video)

## 📋 System Requirements

- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space + language models
- **Internet**: Required for initial model downloads

## 🔧 How It Works

1. **Audio Extraction**: FFmpeg extracts audio from video
2. **Speech Recognition**: Whisper AI transcribes to English
3. **Translation**: Helsinki-NLP models translate to target language
4. **Subtitle Display**: Real-time subtitle overlay

## 📁 File Locations

- **Installation**: `C:\Program Files\Zest Sync Player\`
- **Logs**: `%USERPROFILE%\.zestsync_logs\`
- **Models**: `C:\Program Files\Zest Sync Player\_internal\models\hub\`
- **Subtitles**: Saved next to video files as `.srt`

## 🛠️ Troubleshooting

### Slow Subtitle Generation
- **Cause**: CPU-intensive AI processing
- **Solution**: Close other applications, use SSD storage

### Model Download Fails
- **Cause**: Network connectivity issues
- **Solution**: Check internet connection, retry download

### Video Won't Play
- **Cause**: Unsupported format or codec
- **Solution**: Convert to MP4/H.264 format

### Application Won't Start
- **Cause**: Missing dependencies or antivirus blocking
- **Solution**: Add to antivirus exclusions, run as administrator

### First Launch Crash (Known Issue)
- **Cause**: Initial setup and model initialization
- **Solution**: Simply reopen the application (max 2 times) - this resolves automatically

## 📊 Performance Notes

**Estimated Generation Times** (based on i5-10300H, 4C/8T):
- **English Transcription**: ~1.4 minutes per 10-minute video
- **Translation**: ~1.2-4 minutes depending on target language
- **RAM Usage**: ~600MB during processing

*Performance varies by CPU speed, cores/threads, and available RAM.*

## 🔒 Privacy & Data

- **Local Processing**: All AI processing happens on your device
- **No Data Upload**: Videos and subtitles never leave your computer
- **Model Downloads**: Only language models are downloaded from Hugging Face
- **Logs**: Local debug logs only (auto-deleted after 24 hours)

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/anu277/zest-sync-player/issues)
- **Logs**: Check `%USERPROFILE%\.zestsync_logs\`
- **Discussions**: [GitHub Discussions](https://github.com/anu277/zest-sync-player/discussions)
- **Uninstall**: Use Windows "Add or Remove Programs"

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

**Version 2.0** | Built for Windows 10/11 | Self-contained AI-powered video player