import sys
import os
import time
import subprocess
import tempfile
import logging
from datetime import timedelta, datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

# Setup logging with auto-cleanup
def setup_logging():
    log_dir = os.path.join(os.path.expanduser("~"), ".zestsync_logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Clean old logs (>24 hours)
    now = datetime.now()
    for log_file in os.listdir(log_dir):
        if log_file.endswith('.log'):
            log_path = os.path.join(log_dir, log_file)
            if os.path.getmtime(log_path) < (now - timedelta(hours=24)).timestamp():
                try:
                    os.remove(log_path)
                except:
                    pass
    
    # Setup current log
    log_file = os.path.join(log_dir, f"zestsync_{now.strftime('%Y%m%d_%H%M%S')}.log")
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return log_file

log_file_path = setup_logging()
logging.info(f"Zest Sync Player started. Log file: {log_file_path}")

# Make sure these are installed:
# pip install mpv-python PyQt6 PyQt6-Qtawesome faster-whisper onnxruntime easyNMT nltk
# You also need to run this once to download the nltk data:
# python -c "import nltk; nltk.download('punkt_tab')"

# --- START OF CRITICAL PATH CONFIGURATION ---
try:
    # Get the base path (works for both script and EXE)
    if getattr(sys, 'frozen', False):
        # Running as EXE
        base_path = sys._MEIPASS
    else:
        # Running as script
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Add paths for EXE compatibility - use absolute paths
    current_dir = os.path.abspath(base_path)
    ffmpeg_dir = os.path.abspath(os.path.join(base_path, "ffmpeg"))
    
    # Ensure current directory is first in PATH for MPV DLL loading
    os.environ["PATH"] = current_dir + os.pathsep + os.environ["PATH"]
    
    # Add other paths
    paths_to_add = [
        ffmpeg_dir,
        os.path.abspath(os.path.dirname(sys.executable))
    ]
    
    for path in paths_to_add:
        if path not in os.environ["PATH"]:
            os.environ["PATH"] = path + os.pathsep + os.environ["PATH"]
    
    # Import and configure ONNX runtime (optional)
    try:
        import onnxruntime
        onnx_path = os.path.dirname(onnxruntime.__file__)
        if onnx_path not in os.environ["PATH"]:
            os.environ["PATH"] = onnx_path + os.pathsep + os.environ["PATH"]
    except Exception as onnx_error:
        logging.warning(f"ONNX runtime not available: {onnx_error}")
        print(f"ONNX runtime not available: {onnx_error}")
        
except Exception as e:
    logging.error(f"Failed to set environment path: {e}")
    print(f"Failed to set environment path: {e}")
# --- END OF CRITICAL PATH CONFIGURATION ---

# Import MPV after PATH configuration
try:
    import mpv
except Exception as e:
    logging.error(f"Failed to import MPV: {e}")
    print(f"Failed to import MPV: {e}")
    print(f"Current PATH: {os.environ.get('PATH', 'Not set')}")
    raise

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QProgressBar,
    QSizePolicy,
    QSlider,
    QGridLayout,
    QMenu,
    QGraphicsOpacityEffect,
    QFileDialog,
    QListWidget,
    QAbstractItemView,
    QListWidgetItem,
    QDialog,
    QCheckBox,
    QScrollArea,
    QFrame,
)
from PyQt6.QtCore import Qt, QSize, QTimer, QEvent, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QRectF, QPointF, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QFont, QColor, QIcon, QWheelEvent, QPainter, QBrush, QPen, QKeyEvent, QAction
import qtawesome as qta
# Lazy imports for heavy libraries - imported only when needed
# from faster_whisper import WhisperModel  # Import when needed
# from easynmt import EasyNMT  # Import when needed

# Defer heavy imports to speed up startup
def lazy_import_huggingface():
    try:
        from huggingface_hub import snapshot_download
        return snapshot_download
    except ImportError as e:
        logging.error(f"Failed to import huggingface_hub: {e}")
        return None

# Language Download Dialog
class LanguageDownloadDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Language Model Setup")
        self.setFixedSize(730, 600)
        self.setModal(True)
        self.selected_languages = []
        self.language_sizes = {
            "English": "300MB",
            "Spanish": "1.16GB",
            "French": "1.10GB", 
            "German": "1.6GB",
            "Italian": "958MB",
            "Japanese": "820MB",
            "Russian": "1.38GB",
            "Arabic": "1.38GB",
            "Chinese": "620MB",
            "Hindi": "587MB",
            "Dutch": "1.43GB",
            "Swedish": "1.31GB",
            "Ukrainian": "585MB",
            "Urdu": "870MB"
        }
        self.checkboxes = {}
        self.setup_ui()
        
    def setup_ui(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #f0f0f0;
                font-family: Roboto;
            }
            QLabel {
                color: #f0f0f0;
            }
            QCheckBox {
                color: #f0f0f0;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #555;
                border-radius: 3px;
                background-color: #2a2a2a;
            }
            QCheckBox::indicator:checked {
                background-color: #e50914;
                border-color: #e50914;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #f61a27;
            }
            QPushButton {
                background-color: #e50914;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f61a27;
            }
            QPushButton:pressed {
                background-color: #c00814;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #999;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header_label = QLabel("Welcome to Zest Sync Player!")
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #e50914; margin-bottom: 10px; background-color:transparent")
        layout.addWidget(header_label)
        
        # Description
        desc_label = QLabel("Select the languages you want to download for subtitle generation. You can always download more languages later from the settings.")
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("font-size: 14px; color: #ccc; margin-bottom: 20px; background-color:transparent")
        layout.addWidget(desc_label)
        
        # Scroll area for languages
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #555;
                border-radius: 8px;
                background-color: #2a2a2a;
            }
            QScrollBar:vertical {
                background-color: #333;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #e50914;
                border-radius: 6px;
                min-height: 20px;
            }
        """)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(8)
        scroll_layout.setContentsMargins(15, 15, 15, 15)
        
        # Add English first (pre-selected)
        english_cb = QCheckBox(f"English ({self.language_sizes['English']})")
        english_cb.setChecked(True)
        english_cb.setEnabled(False)  # English is required
        english_cb.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.checkboxes["English"] = english_cb
        scroll_layout.addWidget(english_cb)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("color: #555; margin: 10px 0;")
        scroll_layout.addWidget(separator)
        
        # Add other languages
        other_languages = [lang for lang in self.language_sizes.keys() if lang != "English"]
        other_languages.sort()
        
        for language in other_languages:
            size = self.language_sizes[language]
            cb = QCheckBox(f"{language} ({size})")
            cb.setStyleSheet("font-size: 14px;")
            self.checkboxes[language] = cb
            scroll_layout.addWidget(cb)
        
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        # Selection info
        self.info_label = QLabel("Selected: English (300MB)")
        self.info_label.setStyleSheet("font-size: 12px; color: #aaa; margin-top: 10px; background-color:transparent")
        layout.addWidget(self.info_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(self.select_all)
        select_all_btn.setStyleSheet("background-color: #555; min-width: 100px;")
        
        select_none_btn = QPushButton("Select None")
        select_none_btn.clicked.connect(self.select_none)
        select_none_btn.setStyleSheet("background-color: #555; min-width: 100px;")
        
        self.download_btn = QPushButton("Download Selected")
        self.download_btn.clicked.connect(self.accept)
        self.download_btn.setStyleSheet("min-width: 150px;")
        
        skip_btn = QPushButton("Skip for Now")
        skip_btn.clicked.connect(self.reject)
        skip_btn.setStyleSheet("background-color: #666; min-width: 120px;")
        
        button_layout.addWidget(select_all_btn)
        button_layout.addWidget(select_none_btn)
        button_layout.addStretch()
        button_layout.addWidget(skip_btn)
        button_layout.addWidget(self.download_btn)
        
        layout.addLayout(button_layout)
        
        # Connect checkboxes to update info
        for cb in self.checkboxes.values():
            cb.toggled.connect(self.update_selection_info)
        
        self.update_selection_info()
    
    def select_all(self):
        for cb in self.checkboxes.values():
            if cb.isEnabled():
                cb.setChecked(True)
    
    def select_none(self):
        for lang, cb in self.checkboxes.items():
            if lang != "English" and cb.isEnabled():
                cb.setChecked(False)
    
    def update_selection_info(self):
        selected = []
        total_size_mb = 0
        
        for lang, cb in self.checkboxes.items():
            if cb.isChecked():
                selected.append(lang)
                size_str = self.language_sizes[lang]
                if "GB" in size_str:
                    size_mb = float(size_str.replace("GB", "")) * 1024
                else:
                    size_mb = float(size_str.replace("MB", ""))
                total_size_mb += size_mb
        
        if total_size_mb >= 1024:
            total_size_str = f"{total_size_mb/1024:.1f}GB"
        else:
            total_size_str = f"{int(total_size_mb)}MB"
        
        self.info_label.setText(f"Selected: {len(selected)} languages ({total_size_str})")
        self.selected_languages = selected
        
        # Enable/disable download button
        self.download_btn.setEnabled(len(selected) > 0)

# Custom toggle switch widget for a modern look
class SwitchButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setChecked(True)
        self.setFixedSize(50, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        bg_color = QColor("#e50914") if self.isChecked() else QColor("#555555")
        handle_color = QColor("#f0f0f0")
        
        rect = QRectF(0, 0, self.width(), self.height())
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 14, 14)
        
        handle_pos = self.width() - 24 if self.isChecked() else 4
        handle_rect = QRectF(handle_pos, 4, 20, 20)
        painter.setBrush(QBrush(handle_color))
        painter.drawEllipse(handle_rect)

class ZestSyncPlayer(QMainWindow):
    # This signal will safely carry subtitle text from the mpv thread to the main GUI thread
    subtitle_updated = pyqtSignal(str)
    # NEW SIGNAL for background process status
    status_message = pyqtSignal(str)
    # Signal for model downloads
    model_download_finished = pyqtSignal(str, str)
    model_download_started = pyqtSignal(str)

    # Place this method and its helper method at the top of your ZestSyncPlayer class,
# before the `__init__` method.

    # Place these methods at the top of your ZestSyncPlayer class,
# before the `__init__` method.

    def _calculate_estimated_time(self, video_duration_seconds, lang_code="en"):
        if video_duration_seconds <= 0:
            return 0
        
        # Base transcription time: 50s for 10.40 min (624 seconds)
        base_ratio = 85 / (10.14 * 60)
        
        # Translation time factors based on 641-second test file
        translation_factors = {
            "en": 85,    # Base transcription time
            "nl": 77,    # Dutch
            "fr": 72,    # French
            "de": 80,    # German
            "it": 120,   # Italian
            "jap": 110,  # Japanese
            "ru": 108,   # Russian
            "es": 100,   # Spanish
            "sv": 106,   # Swedish
            "ur": 62,    # Urdu
            "hi": 74,    # Hindi
            "zh": 240,   # Chinese
            "ar": 195,   # Arabic
            "uk": 40     # Ukrainian
        }
        
        factor_seconds = translation_factors.get(lang_code, 85)
        ratio = factor_seconds / 614  # 641 seconds test file
        estimated_time = video_duration_seconds * ratio
        return estimated_time
    
    def _load_manual_srt(self):
        if self.current_media_index == -1: return
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Subtitle File", "", "Subtitle Files (*.srt)")
        if file_path:
            try:
                self.mpv_player.sub_add(file_path)
                self._show_toast("Subtitle file loaded successfully")
            except Exception as e:
                logging.error(f"Error loading manual subtitle file: {e}")
                print(f"Error loading manual subtitle file: {e}")
                self._show_toast("Error loading subtitle file")

    def _delete_selected_media(self):
        for item in self.media_list_widget.selectedItems():
            self._delete_item(item)

    def _delete_all_media(self):
        self.media_list_widget.clear()
        self.media_queue.clear()
        self.mpv_player.command('stop')
        self.video_label.setVisible(True)
        self.status_bar_label.setText("Now Playing: None | Ready")
        self.is_playing = False
        self.play_pause_btn.setIcon(qta.icon("fa5s.play", color="#f0f0f0"))
    
    def _toggle_subtitles(self, checked):
        self.subtitles_enabled = checked
        self.subtitle_label.setVisible(checked and bool(self.subtitle_label.text()))
        self.mpv_player.sub_visibility = checked
        
    def _show_media_context_menu(self, pos):
        item = self.media_list_widget.itemAt(pos)
        if not item:
            return
            
        context_menu = QMenu(self)
        delete_action = QAction(qta.icon("fa5s.trash-alt", color="#f0f0f0"), "Delete", self)
        delete_action.triggered.connect(lambda: self._delete_item(item))
        context_menu.addAction(delete_action)
        context_menu.exec(self.media_list_widget.mapToGlobal(pos))
        
    def _delete_item(self, item):
        row = self.media_list_widget.row(item)
        self.media_list_widget.takeItem(row)
        if 0 <= row < len(self.media_queue):
            self.media_queue.pop(row)
            
    def _on_animation_finished(self):
        if self.opacity_effect.opacity() == 0.0:
            self.bottom_controls_container.setVisible(False)
        
    def _skip_forward(self):
        if self.current_media_index != -1:
            self.mpv_player.seek(10, reference='relative')

    def _skip_backward(self):
        if self.current_media_index != -1:
            self.mpv_player.seek(-10, reference='relative')
                
    def _play_selected_media(self, item):
        file_path = item.data(Qt.ItemDataRole.UserRole)
        self.current_media_index = self.media_list_widget.row(item)
        self._play_media(file_path)

    def _play_media(self, file_path):
        self.video_label.setVisible(False)
        self.mpv_player.play(file_path)
        self.mpv_player.pause = False
        self.is_playing = True
        self.status_bar_label.setText(f"Now Playing: {os.path.basename(file_path)}")
        self.play_pause_btn.setIcon(qta.icon("fa5s.pause", color="#f0f0f0"))
        self.position_timer.start()

        # Force English selection when media loads
        for i in range(self.language_selector_combo.count()):
            if self.language_selector_combo.itemText(i) == "English":
                self.language_selector_combo.setCurrentIndex(i)
                break
        self._on_language_changed("English")
        # Place this method at the top of your ZestSyncPlayer class,
        # before the `__init__` method.
    def _change_volume(self, delta):
        new_volume = max(0, min(100, self.current_volume + delta))
        self._on_volume_changed(new_volume)
        self.volume_slider.setValue(new_volume)

    def _on_volume_changed(self, value):
        self.current_volume = value
        self.mpv_player.volume = value
        self.volume_indicator.setText(f"Volume: {value}%")
        self._update_volume_icon()
        self._show_volume_indicator()

    def _update_volume_icon(self):
        if self.is_muted or self.current_volume == 0:
            icon = "fa5s.volume-mute"
        elif self.current_volume < 50:
            icon = "fa5s.volume-down"
        else:
            icon = "fa5s.volume-up"
        self.volume_btn.setIcon(QIcon(qta.icon(icon, color="#f0f0f0").pixmap(16, 16)))
        
    def _toggle_mute(self):
        self.is_muted = not self.is_muted
        self.mpv_player.mute = self.is_muted
        self._update_volume_icon()
        self._show_volume_indicator()
            
    def _show_volume_indicator(self):
        self.volume_indicator.setText("Muted" if self.is_muted else f"Volume: {self.current_volume}%")
        self.volume_indicator.setVisible(True)
        self.volume_indicator_timer.start()

    def _handle_volume_wheel(self, e: QWheelEvent):
        self._change_volume(5 if e.angleDelta().y() > 0 else -5)
        
    def _toggle_play_pause(self):
        if self.current_media_index == -1: return
        try:
            self.mpv_player.pause = not self.mpv_player.pause
            self.is_playing = not self.is_playing
            icon = "fa5s.play" if not self.is_playing else "fa5s.pause"
            self.play_pause_btn.setIcon(qta.icon(icon, color="#f0f0f0"))
            if self.is_playing: self.position_timer.start()
            else: self.position_timer.stop()
        except:
            pass  # Ignore mpv errors when no media loaded

    def _play_next_in_queue(self):
        if self.current_media_index + 1 < self.media_list_widget.count():
            self.current_media_index += 1
            item = self.media_list_widget.item(self.current_media_index)
            self.media_list_widget.setCurrentItem(item)
            self._play_selected_media(item)
        else:
            self.is_playing = False
            self.play_pause_btn.setIcon(qta.icon("fa5s.play", color="#f0f0f0"))

    def _play_previous_in_queue(self):
        if self.current_media_index > 0:
            self.current_media_index -= 1
            item = self.media_list_widget.item(self.current_media_index)
            self.media_list_widget.setCurrentItem(item)
            self._play_selected_media(item)

    def _set_position(self, value):
        if self.current_media_index != -1:
            try:
                self.mpv_player.time_pos = value
            except:
                pass  # Ignore mpv errors when no media loaded
    
    def _timeline_click(self, event):
        if self.current_media_index != -1 and self.media_duration > 0:
            click_pos = event.position().x()
            slider_width = self.timeline_slider.width()
            new_position = int((click_pos / slider_width) * self.media_duration)
            self.timeline_slider.setValue(new_position)
            self._set_position(new_position)
        # Call original mousePressEvent to preserve drag functionality
        QSlider.mousePressEvent(self.timeline_slider, event)
    
    def _timeline_hover(self, event):
        if self.current_media_index != -1 and self.media_duration > 0:
            hover_pos = event.position().x()
            slider_width = self.timeline_slider.width()
            hover_time = int((hover_pos / slider_width) * self.media_duration)
            hover_time_str = self._format_time(hover_time)
            self.timeline_slider.setToolTip(hover_time_str)

    def _create_icon_button(self, icon, size=35, icon_size=16):
        btn = QPushButton(); btn.setFixedSize(size, size); btn.setIcon(QIcon(qta.icon(icon, color="#f0f0f0").pixmap(icon_size, icon_size))); btn.setIconSize(QSize(icon_size, icon_size)); btn.setStyleSheet("QPushButton { background-color: transparent; border: none; border-radius: 5px; } QPushButton:hover { background-color: #333333; }"); return btn

    def _populate_controls_bar(self):
        rewind_btn = self._create_icon_button("fa5s.fast-backward"); rewind_btn.clicked.connect(self._play_previous_in_queue)
        skip_backward_btn = self._create_icon_button("fa5s.undo"); skip_backward_btn.clicked.connect(self._skip_backward)
        self.play_pause_btn = self._create_icon_button("fa5s.play", size=45, icon_size=20); self.play_pause_btn.clicked.connect(self._toggle_play_pause)
        skip_forward_btn = self._create_icon_button("fa5s.redo"); skip_forward_btn.clicked.connect(self._skip_forward)
        forward_btn = self._create_icon_button("fa5s.fast-forward"); forward_btn.clicked.connect(self._play_next_in_queue)
        
        volume_layout = QHBoxLayout(); volume_layout.setSpacing(5)
        self.volume_btn = self._create_icon_button("fa5s.volume-up")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal); self.volume_slider.setRange(0, 100); self.volume_slider.setValue(self.current_volume)
        self.volume_slider.setStyleSheet("QSlider::groove:horizontal { border: 1px solid #333; height: 5px; background: #333333; border-radius: 2px; } QSlider::sub-page:horizontal { background: #e50914; border-radius: 2px; } QSlider::handle:horizontal { background: #e50914; border: 1px solid #e50914; width: 12px; height: 12px; margin: -4px 0; border-radius: 6px; }")
        self.volume_btn.clicked.connect(self._toggle_mute); self.volume_slider.valueChanged.connect(self._on_volume_changed);
        volume_layout.addWidget(self.volume_btn); volume_layout.addWidget(self.volume_slider)
        
        speed_button = QPushButton("1x"); speed_button.setMinimumHeight(35)
        speed_button.setStyleSheet("QPushButton { background-color: transparent; color: #f0f0f0; border: none; font-weight: bold; min-width: 40px; } QPushButton::menu-indicator { width: 0px; } QPushButton:hover { color: #e50914; }")
        speed_menu = QMenu(); speed_menu.setStyleSheet("QMenu { background-color: #1e1e1e; color: #f0f0f0; border: 1px solid #333333; border-radius: 8px; padding: 5px; font-size: 15px; min-width: 50px; } QMenu::item { background-color: transparent; padding: 8px 20px ; border-radius: 6px; } QMenu::item:selected { background-color: #333333; color: #e50914; }")
        
        for speed in ["0.5x", "1x", "1.5x", "2x", "2.5x"]:
            action = speed_menu.addAction(speed)
            action.triggered.connect(lambda checked, s=speed: self._set_speed(s, speed_button))
            
        def show_speed_menu():
            pos = speed_button.mapToGlobal(QPointF(0, 0).toPoint())
            menu_height = speed_menu.sizeHint().height()
            speed_menu.move(pos.x(), pos.y() - menu_height)
            speed_menu.show()
        speed_button.clicked.connect(show_speed_menu)

        self.fullscreen_btn = self._create_icon_button("fa5s.expand")
        self.fullscreen_btn.clicked.connect(self._toggle_fullscreen)

        self.controls_bar_layout.addWidget(rewind_btn); self.controls_bar_layout.addWidget(skip_backward_btn)
        self.controls_bar_layout.addWidget(self.play_pause_btn); self.controls_bar_layout.addWidget(skip_forward_btn)
        self.controls_bar_layout.addWidget(forward_btn); self.controls_bar_layout.addStretch()
        self.controls_bar_layout.addWidget(speed_button); self.controls_bar_layout.addLayout(volume_layout)
        self.controls_bar_layout.addWidget(self.fullscreen_btn)
        
    def _show_controls(self): 
        self.controls_animation_group.stop()
        self.bottom_controls_container.setVisible(True)
        self.fade_animation.setDuration(400); self.fade_animation.setStartValue(self.opacity_effect.opacity()); self.fade_animation.setEndValue(1.0)
        self.slide_animation.setDuration(300); self.slide_animation.setStartValue(self.bottom_controls_container.height()); self.slide_animation.setEndValue(90)
        self.slide_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.controls_animation_group.start()

    def _hide_controls(self): 
        self.controls_animation_group.stop()
        self.fade_animation.setDuration(300); self.fade_animation.setStartValue(self.opacity_effect.opacity()); self.fade_animation.setEndValue(0.0)
        self.slide_animation.setDuration(400); self.slide_animation.setStartValue(self.bottom_controls_container.height()); self.slide_animation.setEndValue(0)
        self.slide_animation.setEasingCurve(QEasingCurve.Type.InCubic)
        self.controls_animation_group.start()
    
    def _update_position(self):
        if self.is_playing and self.media_duration > 0 and self.media_position >= self.media_duration -1:
            self.position_timer.stop(); self._play_next_in_queue()
         
    def _open_sidebar(self):
        if self.is_sidebar_open:
            return
        self.is_sidebar_open = True
        self.sidebar_animation_group.stop()
        self.sidebar_min_width_anim.setStartValue(0)
        self.sidebar_min_width_anim.setEndValue(300)
        self.sidebar_max_width_anim.setStartValue(0)
        self.sidebar_max_width_anim.setEndValue(300)
        self.sidebar_animation_group.start()
        self.sidebar_toggle_btn.setIcon(qta.icon("fa5s.chevron-right", color="#f0f0f0"))
        self.sidebar_idle_timer.start()

    def _close_sidebar(self):
        if not self.is_sidebar_open:
            return
        self.is_sidebar_open = False
        self.sidebar_animation_group.stop()
        self.sidebar_min_width_anim.setStartValue(300)
        self.sidebar_min_width_anim.setEndValue(0)
        self.sidebar_max_width_anim.setStartValue(300)
        self.sidebar_max_width_anim.setEndValue(0)
        self.sidebar_animation_group.start()
        self.sidebar_toggle_btn.setIcon(qta.icon("fa5s.chevron-left", color="#f0f0f0"))
        self.sidebar_idle_timer.stop()

    def _set_model_cache_path(self):
        """
        Sets the cache directory for translation models.
        If running as a PyInstaller bundle, it points to the bundled 'models' directory.
        Otherwise, it uses the default Hugging Face cache.
        """
        # if getattr(sys, 'frozen', False):
        #     # Running as EXE
        #     cache_dir = os.path.join(sys._MEIPASS, 'models')
        # else:
        #     # Running as script
        #     cache_dir = os.path.join(os.path.expanduser('~'), '.cache', 'huggingface', 'hub')
        
        if getattr(sys, 'frozen', False):
            # Running as EXE - use user directory instead of Program Files
            cache_dir = os.path.join(os.path.expanduser('~'), '.cache', 'zestsync', 'models')
        else:
            # Running as script
            cache_dir = os.path.join(os.path.expanduser('~'), '.cache', 'huggingface', 'hub')
        
        os.environ['HF_HOME'] = cache_dir
        logging.info(f"Using model cache directory: {cache_dir}")
        print(f"Using model cache directory: {cache_dir}")

    def __init__(self):
        super().__init__()
        self._set_model_cache_path()
        if getattr(sys, 'frozen', False):
            # Running as EXE - use bundled resource
            icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
        else:
            # Running as script
            icon_path = 'icon.ico'
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle("Zest Sync")
        self.setMinimumSize(1280, 768)
        
        # Show window first, then check first run
        self.showMaximized()
        
        # Check if this is first run (after window is shown)
        self.first_run_file = os.path.join(os.path.expanduser("~"), ".zestsync_first_run")
        if not os.path.exists(self.first_run_file):
            QTimer.singleShot(500, self.show_language_download_dialog)  # Delay dialog
        
        # Initialize last used path for imports
        self.settings_file = os.path.join(os.path.expanduser("~"), ".zestsync_settings")
        self.last_import_path = self._load_last_import_path()


        # --- STATE MANAGEMENT ---
        self.is_playing = False
        self.is_sidebar_open = True
        self.current_volume = 75
        self.is_muted = False
        self.volume_before_mute = 75
        self.subtitles_enabled = True 
        self.media_queue = [] 
        self.current_media_index = -1 
        self.media_position = 0
        self.media_duration = 0
        self.is_fullscreen = False
        self.subtitle_font_size = 24
        self.last_mouse_pos = QPointF()

        # NEW: Background thread executors
        self.subtitle_executor = ThreadPoolExecutor(max_workers=1)
        self.download_executor = ThreadPoolExecutor(max_workers=1)
        self.generation_future = None
        self.generation_progress_timer = QTimer(self)
        self.generation_progress_timer.setInterval(500) # Update every 500ms
        self.generation_start_time = 0
        self.estimated_total_time = 0
        self.download_lock = Lock()
        self.download_status = {} # Stores the download state of each model
        self.languages_list = self._get_language_map()
        
        self.model_download_started.connect(self._handle_model_download_started)
        self.model_download_finished.connect(self._handle_model_download_finished)
        
        # Initialize EasyNMT model as a member variable. It will be lazy loaded.
        self.easy_nmt_model = None
        
        # Timer to update UI during downloads
        self.ui_update_timer = QTimer(self)
        self.ui_update_timer.timeout.connect(self._update_language_list_ui)
        self.ui_update_timer.setInterval(2000)  # Update every 2 seconds

        # --- TIMERS ---
        self.mouse_idle_timer = QTimer(self)
        self.mouse_idle_timer.setSingleShot(True)
        self.mouse_idle_timer.timeout.connect(self._hide_controls)
        self.mouse_idle_timer.setInterval(3000)

 
        
        self.position_timer = QTimer(self)
        self.position_timer.setInterval(1000)
        self.position_timer.timeout.connect(self._update_position)
        
        # --- Core UI Setup ---
        self.setStyleSheet(
            "background-color: #121212; color: #f0f0f0; font-family: Roboto;"
        )

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- Video Panel Section ---
        self.video_panel = QWidget()
        self.video_panel_layout = QVBoxLayout(self.video_panel)
        self.video_panel_layout.setContentsMargins(0, 0, 0, 0)
        self.video_panel_layout.setSpacing(0)

        self.video_container = QWidget()
        self.video_container.setStyleSheet("background-color: black;")
        self.video_container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.video_container.setMouseTracking(True)
        self.video_container.setCursor(Qt.CursorShape.PointingHandCursor)
        self.video_container.installEventFilter(self)
        
        # --- CRITICAL FIX: MPV Player MUST be initialized BEFORE any buttons that call it.
        # This resolves the `AttributeError: 'ZestSyncPlayer' object has no attribute 'mpv_player'`
        self.mpv_player = mpv.MPV(
            wid=str(int(self.video_container.winId())),
            hr_seek='yes', ytdl=True
        )
        self.mpv_player.sub_font_size = self.subtitle_font_size
        # Remove black stroke/outline from subtitles
        self.mpv_player.sub_border_size = 0
        self.mpv_player.sub_shadow_offset = 0
        self.mpv_player.observe_property('time-pos', self._on_time_update)
        self.mpv_player.observe_property('duration', self._on_duration_update)
        self.mpv_player.observe_property('sub-text', self._on_subtitle_update)

        self.video_layout = QGridLayout(self.video_container)
        self.video_layout.setContentsMargins(0, 0, 0, 0)
        self.video_layout.setSpacing(0)
        
        self.video_label = QLabel("Import media using the '+' button in the sidebar")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("color: #aaaaaa; font-size: 24px;")
        
        self.status_bar_label = QLabel("Now Playing: None | Ready")
        self.status_bar_label.setStyleSheet(
            "color: rgba(255,255,255,0.6); background-color: rgba(0, 0, 0, 0.5); padding: 10px; font-size: 11px;"
        )

        self.toast_label = QLabel("Subtitles Ready! ✅")
        self.toast_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.toast_label.setStyleSheet(
            "background-color: #1e1e1e; color: #f0f0f0; border-radius: 5px; padding: 10px; border: 1px solid #333333;"
        )
        self.toast_label.setVisible(False)

        self.volume_indicator = QLabel("Volume: 75%")
        self.volume_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.volume_indicator.setStyleSheet(
            "background-color: rgba(30, 30, 30, 0.8); color: #f0f0f0; border-radius: 8px; padding: 15px 25px; font-size: 16px; font-weight: bold;"
        )
        self.volume_indicator.setVisible(False)

        self.volume_indicator_timer = QTimer(self)
        self.volume_indicator_timer.setSingleShot(True)
        self.volume_indicator_timer.timeout.connect(lambda: self.volume_indicator.setVisible(False))
        self.volume_indicator_timer.setInterval(1500)

        self.video_layout.addWidget(self.video_label, 0, 0, 3, 3)

        self.controls_bar = QWidget()
        self.controls_bar.setStyleSheet("background-color: transparent;")
        self.controls_bar_layout = QHBoxLayout(self.controls_bar)
        self.controls_bar_layout.setSpacing(10)
        self.controls_bar_layout.setContentsMargins(20, 5, 20, 10)
        
        self._populate_controls_bar()

        self.bottom_controls_container = QWidget()
        self.bottom_controls_container.setStyleSheet("background-color: #181818;")
        self.bottom_controls_container.setMinimumHeight(90)
        self.bottom_controls_container.setMaximumHeight(90)
        self.bottom_controls_container.setVisible(False)
        self.bottom_controls_container.installEventFilter(self)

        self.controls_animation_group = QParallelAnimationGroup(self)
        self.opacity_effect = QGraphicsOpacityEffect(self.bottom_controls_container)
        self.bottom_controls_container.setGraphicsEffect(self.opacity_effect)
        
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.slide_animation = QPropertyAnimation(self.bottom_controls_container, b"maximumHeight")

        self.controls_animation_group.addAnimation(self.fade_animation)
        self.controls_animation_group.addAnimation(self.slide_animation)
        self.controls_animation_group.finished.connect(self._on_animation_finished)

        bottom_container_layout = QVBoxLayout(self.bottom_controls_container)
        bottom_container_layout.setContentsMargins(0, 5, 0, 0)
        bottom_container_layout.setSpacing(5)

        self.timeline_container = QWidget()
        timeline_layout = QHBoxLayout(self.timeline_container)
        timeline_layout.setContentsMargins(10, 0, 10, 0)
        timeline_layout.setSpacing(10)

        self.current_time_label = QLabel("00:00")
        self.timeline_slider = QSlider(Qt.Orientation.Horizontal)
        self.timeline_slider.setStyleSheet("QSlider::groove:horizontal { border: 1px solid #444; height: 5px; background: #444; border-radius: 2px; } QSlider::sub-page:horizontal { background: #e50914; border-radius: 2px; } QSlider::handle:horizontal { background: #e50914; border: 1px solid #e50914; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; }")
        self.timeline_slider.sliderMoved.connect(self._set_position)
        self.timeline_slider.sliderPressed.connect(self.position_timer.stop)
        self.timeline_slider.sliderReleased.connect(self.position_timer.start)
        self.timeline_slider.mousePressEvent = self._timeline_click
        self.timeline_slider.setMouseTracking(True)
        self.timeline_slider.mouseMoveEvent = self._timeline_hover

        self.total_duration_label = QLabel("00:00")
        
        timeline_layout.addWidget(self.current_time_label)
        timeline_layout.addWidget(self.timeline_slider)
        timeline_layout.addWidget(self.total_duration_label)

        bottom_container_layout.addWidget(self.timeline_container)
        bottom_container_layout.addWidget(self.controls_bar, 0, Qt.AlignmentFlag.AlignHCenter)

        self.overlay_container = QWidget()
        self.overlay_container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.overlay_container.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        overlay_layout = QVBoxLayout(self.overlay_container)
        overlay_layout.setContentsMargins(10, 10, 10, 20)
        overlay_layout.setSpacing(10)
        overlay_layout.addStretch(1)

        self.subtitle_label = QLabel("")
        self.subtitle_label.setStyleSheet(
            f"font-size: {self.subtitle_font_size}px; "
            "background-color: rgba(0, 0, 0, 0.5); color: white; padding: 5px 10px; border-radius: 5px;"
        )
        overlay_layout.addWidget(self.subtitle_label, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        overlay_layout.addSpacing(20)

        self.video_layout.addWidget(self.overlay_container, 0, 0, 3, 3)
        self.video_layout.addWidget(self.status_bar_label, 0, 0, 1, 3, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.video_layout.addWidget(self.toast_label, 2, 2, 1, 1, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        self.video_layout.addWidget(self.volume_indicator, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.overlay_container.raise_()
        
        self.video_panel_layout.addWidget(self.video_container)
        self.video_panel_layout.addWidget(self.bottom_controls_container)
        self.main_layout.addWidget(self.video_panel, 1)

        # --- NEW SIDEBAR ANIMATION LOGIC ---
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(300)
        self.sidebar.setStyleSheet("background-color: #1e1e1e;")
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self._populate_sidebar()

        self.sidebar_handle = QWidget()
        self.sidebar_handle.setFixedWidth(25)
        self.sidebar_handle.setStyleSheet("""background-color: #121212; """)
        self.sidebar_handle.setCursor(Qt.CursorShape.PointingHandCursor)
        handle_layout = QVBoxLayout(self.sidebar_handle)
        handle_layout.setContentsMargins(0, 10, 0, 0)
        
        handle_layout.addStretch()

        self.sidebar_toggle_btn = self._create_icon_button("fa5s.chevron-right", size=25, icon_size=20)
        self.sidebar_toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #121212; 
                border: none;
                padding: 5px;
                border-radius:3px;
                
            }
            QPushButton:hover {
                background-color: black;
            }
        """)
        self.sidebar_toggle_btn.clicked.connect(self._toggle_sidebar)
        handle_layout.addWidget(self.sidebar_toggle_btn)
        self.sidebar_toggle_btn.installEventFilter(self)
        
        self._setup_button_animations()
        
        handle_layout.addStretch()

        self.sidebar.installEventFilter(self)
        self.sidebar_handle.installEventFilter(self)



        self.main_layout.addWidget(self.sidebar_handle)
        self.main_layout.addWidget(self.sidebar)
        # --- END OF NEW LOGIC ---
        
        # Connect signals after UI is ready
        QTimer.singleShot(50, self._connect_signals)
    
    def _connect_signals(self):
        """Connect signals after UI initialization"""
        self.subtitle_updated.connect(self._update_subtitle_label)
        self.status_message.connect(self._update_status_bar)

        # Delay initial model status check
        QTimer.singleShot(200, self._update_language_list_ui)
    
    def show_language_download_dialog(self):
        """Show the language download dialog on first run"""
        dialog = LanguageDownloadDialog(self)
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            # User clicked "Download Selected"
            selected_languages = dialog.selected_languages
            QTimer.singleShot(1000, lambda: self.start_initial_downloads(selected_languages))
        
        # Mark first run as complete
        try:
            with open(self.first_run_file, 'w') as f:
                f.write("first_run_complete")
        except Exception as e:
            logging.error(f"Could not create first run file: {e}")
            print(f"Could not create first run file: {e}")
    
    def start_initial_downloads(self, languages):
        """Start downloading selected languages in background"""
        if not languages:
            return
            
        # Show toast notification
        lang_count = len([l for l in languages if l != "English"])
        if lang_count > 0:
            print(f"Starting download of {lang_count} language models...")
        
        # Start downloads for non-English languages
        for language in languages:
            if language != "English":  # English doesn't need download
                lang_code = self._get_language_code(language)
                print(f"Starting download for {language} ({lang_code})")
                future = self.download_executor.submit(self._download_model_in_background, lang_code)


    def _setup_button_animations(self):
        # Animation for when the mouse enters the button
        self.btn_grow_anim = QPropertyAnimation(self.sidebar_toggle_btn, b"size")
        self.btn_grow_anim.setDuration(150) # Duration in milliseconds for the animation
        self.btn_grow_anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Animation for when the mouse leaves the button
        self.btn_shrink_anim = QPropertyAnimation(self.sidebar_toggle_btn, b"size")
        self.btn_shrink_anim.setDuration(150)
        self.btn_shrink_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def _is_video_area_child(self, obj):
        """Check if the object is a child of the video area"""
        parent = obj
        while parent:
            if parent == self.video_container:
                return True
            parent = parent.parent()
        return False
    
    def _is_mouse_over_sidebar_children(self):
        """Check if mouse is over sidebar or any of its child widgets/dialogs"""
        app = QApplication.instance()
        widget_under_mouse = app.widgetAt(app.primaryScreen().availableGeometry().topLeft() + app.primaryScreen().availableGeometry().center())
        if not widget_under_mouse:
            return False
        
        # Check if widget is part of sidebar hierarchy
        parent = widget_under_mouse
        while parent:
            if parent == self.sidebar or parent == self.sidebar_handle:
                return True
            # Check for file dialogs and combo box popups
            if isinstance(parent, (QFileDialog, QMenu)):
                return True
            parent = parent.parent()
        return False
    
    def _set_speed(self, speed_text, button):
        """Set playback speed"""
        speed_value = float(speed_text.replace('x', ''))
        self.mpv_player.speed = speed_value
        button.setText(speed_text)

    def _format_time(self, seconds):
        """Format seconds into HH:MM:SS format"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def _format_time_srt(self, seconds):
        """Format seconds into SRT timestamp format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

    def _on_time_update(self, name, value):
        if value is not None and not self.timeline_slider.isSliderDown():
            self.media_position = int(value)
            self.timeline_slider.setValue(int(value))
            self.current_time_label.setText(self._format_time(int(value)))

    def _on_duration_update(self, name, value):
        if value is not None:
            self.media_duration = int(value)
            self.timeline_slider.setRange(0, int(value))
            self.total_duration_label.setText(self._format_time(int(value)))

    @pyqtSlot(str)
    def _update_subtitle_label(self, text):
        """This method is a slot that safely updates the subtitle label from the main GUI thread."""
        if text and self.subtitles_enabled:
            self.subtitle_label.setText(text)
            self.subtitle_label.setVisible(True)
        else:
            self.subtitle_label.setVisible(False)
            
    def _on_subtitle_update(self, name, value):
        """
        This method is called from the mpv background thread.
        It must NOT interact with the GUI directly.
        Instead, it emits a signal to be handled by the main thread.
        """
        try:
            if hasattr(self, 'subtitle_updated'):
                text = value if value is not None else ""
                self.subtitle_updated.emit(text)
        except RuntimeError:
            # Object has been deleted, ignore
            pass

    def _create_setting_box(self, title):
        box = QWidget()
        box.setStyleSheet("""
            QWidget {
                background-color: #2a2a2a;
                border-radius: 8px;
            }
        """)
        box_layout = QVBoxLayout(box)
        box_layout.setContentsMargins(12, 12, 12, 12)
        box_layout.setSpacing(10)

        if title:
            title_label = QLabel(title)
            title_label.setFont(QFont("Roboto", 10, QFont.Weight.Bold))
            title_label.setStyleSheet("background-color: transparent; border: none;")
            box_layout.addWidget(title_label)
        
        return box, box_layout

    def _get_language_map(self):
        return {
            "English": "en", "Spanish": "es", "French": "fr", "German": "de",
            "Italian": "it", "Japanese": "jap", "Russian": "ru",
            "Arabic": "ar", "Chinese": "zh", "Hindi": "hi",
            "Dutch": "nl", "Swedish": "sv", "Ukrainian": "uk", "Urdu": "ur"
        }

    def _get_easy_nmt_cache_path(self, lang_code):
        cache_base = os.path.join(Path.home(), ".cache", "torch", "easynmt_v2")
        return os.path.join(cache_base, "opus-mt")

    def _check_model_status(self):
        status = {}
        model_sizes = {
            "en": "300MB", "es": "1.16GB", "fr": "1.10GB", "de": "1.6GB",
            "it": "958MB", "jap": "820MB", "ru": "1.38GB",
            "ar": "1.38GB", "zh": "620MB", "hi": "587MB",
            "nl": "1.43GB", "sv": "1.31GB", "uk": "585MB", "ur": "870MB"
        }
        
        # Check Hugging Face cache for individual models
        # hf_cache = os.path.join(Path.home(), ".cache", "huggingface", "hub")
        hf_cache = os.path.join(os.environ.get('HF_HOME', os.path.join(Path.home(), '.cache', 'huggingface')), 'hub')


        for lang, code in self.languages_list.items():
            is_downloading = self.download_status.get(lang, {}).get("status") == "downloading"
            
            # Check if model exists in Hugging Face cache
            model_name = f"models--Helsinki-NLP--opus-mt-en-{code}"
            model_path = os.path.join(hf_cache, model_name)
            is_downloaded = os.path.exists(model_path) and os.path.isdir(model_path)
            
            # English doesn't need a translation model
            if lang == "English":
                is_downloaded = True

            if is_downloading:
                status[lang] = {"code": code, "status": "downloading", "size": model_sizes.get(code, "Unknown")}
            elif is_downloaded:
                status[lang] = {"code": code, "status": "downloaded"}
            else:
                status[lang] = {"code": code, "status": "not_downloaded", "size": model_sizes.get(code, "Unknown")}
                
        return status

    def _update_language_list_ui(self):
        try:
            self.language_selector_combo.currentTextChanged.disconnect(self._on_language_changed)
        except TypeError:
            pass # Signal was not connected yet
        
        current_language = self.language_selector_combo.currentText()
        self.language_selector_combo.clear()

        self.download_status = self._check_model_status()
        
        downloaded = sorted([k for k, v in self.download_status.items() if v["status"] == "downloaded"])
        downloading = sorted([k for k, v in self.download_status.items() if v.get("status") == "downloading"])
        not_downloaded = sorted([k for k, v in self.download_status.items() if v["status"] == "not_downloaded"])

        for lang in downloaded:
            self.language_selector_combo.addItem(qta.icon("fa5s.check-circle", color="green"), lang)
        
        if downloaded and (downloading or not_downloaded):
            self.language_selector_combo.insertSeparator(len(downloaded))
            
        for lang in downloading:
            size = self.download_status[lang]["size"]
            self.language_selector_combo.addItem(qta.icon("fa5s.spinner", color="blue"), f"{lang} ({size})")
        
        if downloading and not_downloaded:
            self.language_selector_combo.insertSeparator(len(downloaded) + len(downloading) + 1)
            
        for lang in not_downloaded:
            size = self.download_status[lang]["size"]
            self.language_selector_combo.addItem(qta.icon("fa5s.download", color="red"), f"{lang} ({size})")
        
        self.language_selector_combo.currentTextChanged.connect(self._on_language_changed)
        
        # Set English as default, otherwise preserve selection
        clean_current = current_language.split(' (')[0] if ' (' in current_language else current_language
        english_found = False
        
        # First try to find English
        for i in range(self.language_selector_combo.count()):
            item_text = self.language_selector_combo.itemText(i)
            clean_item = item_text.split(' (')[0] if ' (' in item_text else item_text
            if clean_item == "English":
                self.language_selector_combo.setCurrentIndex(i)
                english_found = True
                break
        
        # If English not found or we have a valid current selection, try to preserve it
        if not english_found or clean_current:
            for i in range(self.language_selector_combo.count()):
                item_text = self.language_selector_combo.itemText(i)
                clean_item = item_text.split(' (')[0] if ' (' in item_text else item_text
                if clean_item == clean_current:
                    self.language_selector_combo.setCurrentIndex(i)
                    break

    @pyqtSlot(str)
    def _handle_model_download_started(self, lang_code):
        lang_name = self._get_language_name(lang_code)
        model_sizes = {
            "en": "300MB", "es": "1.16GB", "fr": "1.10GB", "de": "1.6GB",
            "it": "958MB", "jap": "820MB", "ru": "1.38GB",
            "ar": "1.38GB", "zh": "620MB", "hi": "587MB",
            "nl": "1.43GB", "sv": "1.31GB", "uk": "585MB", "ur": "870MB"
        }
        size = model_sizes.get(lang_code, "Unknown")
        with self.download_lock:
            self.download_status[lang_name] = {"code": lang_code, "status": "downloading", "size": size}
        print(f"DEBUG: Updated download status for {lang_name}: downloading")
        self._update_language_list_ui()
        self.ui_update_timer.start()  # Start periodic UI updates
        self._show_toast(f"Downloading {lang_name} model ({size})...")

    @pyqtSlot(str, str)
    def _handle_model_download_finished(self, lang_code, result):
        lang_name = self._get_language_name(lang_code)
        with self.download_lock:
            if result == "success":
                self.download_status[lang_name] = {"code": lang_code, "status": "downloaded"}
            else:
                if lang_name in self.download_status:
                    del self.download_status[lang_name]
        print(f"DEBUG: Updated download status for {lang_name}: {result}")
        
        # Check if all downloads are complete
        downloading_count = sum(1 for status in self.download_status.values() if status.get("status") == "downloading")
        if downloading_count == 0:
            self.ui_update_timer.stop()  # Stop periodic UI updates only when all downloads complete
        
        self._update_language_list_ui()
        if result == "success":
            self._show_toast(f"✅ {lang_name} model downloaded successfully!")
            # Auto-start subtitle generation if this language is currently selected
            current_language = self.language_selector_combo.currentText().split(' (')[0]
            if current_language == lang_name and self.current_media_index != -1:
                QTimer.singleShot(1000, self._start_subtitle_generation)
        else:
            self._show_toast(f"❌ Download failed for {lang_name}. You can retry later.")

    def _download_model_in_background(self, lang_code):
        import sys
        print(f"THREAD LOG: Download method called for {lang_code}")
        logging.info(f"Starting download for language: {lang_code}")
        sys.stdout.flush()
        try:
            # Test network connectivity first
            import urllib.request
            try:
                urllib.request.urlopen('https://huggingface.co', timeout=10)
                print(f"THREAD LOG: Network connectivity confirmed")
                logging.info("Network connectivity confirmed")
            except Exception as net_error:
                print(f"THREAD LOG: ❌ Network connectivity failed: {net_error}")
                logging.error(f"Network connectivity failed: {net_error}")
                raise Exception(f"No internet connection: {net_error}")
            
            print(f"THREAD LOG: Setting environment variables...")
            sys.stdout.flush()
            import os
            os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
            
            print(f"THREAD LOG: Emitting download started signal...")
            sys.stdout.flush()
            self.model_download_started.emit(lang_code)
            print(f"THREAD LOG: Starting model download for {lang_code}...")
            sys.stdout.flush()
            
            # Use huggingface_hub to download the specific model
            snapshot_download = lazy_import_huggingface()
            if not snapshot_download:
                raise Exception("huggingface_hub not available")
            model_id = f"Helsinki-NLP/opus-mt-en-{lang_code}"
            logging.info(f"Attempting to download model: {model_id}")
            
            try:
                path = snapshot_download(repo_id=model_id)
                print(f"THREAD LOG: ✅ Model downloaded to: {path}")
            except Exception as download_error:
                print(f"THREAD LOG: Download error (checking cache): {download_error}")
                # Check if model exists in cache anyway
                cache_path = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub", f"models--Helsinki-NLP--opus-mt-en-{lang_code}")
                if os.path.exists(cache_path):
                    print(f"THREAD LOG: ✅ Model found in cache: {cache_path}")
                else:
                    raise download_error
            
            # Skip EasyNMT initialization during download to prevent crashes
            print(f"THREAD LOG: ✅ Model download completed successfully")
            logging.info(f"Model download completed for {lang_code}")
            
            self.model_download_finished.emit(lang_code, "success")
        except Exception as e:
            print(f"THREAD LOG: ❌ ERROR downloading model for Language[Code:]{lang_code}: {e}")
            logging.error(f"Download failed for {lang_code}: {e}")
            sys.stdout.flush()
            try:
                import traceback
                print(f"THREAD LOG: Full traceback: {traceback.format_exc()}")
                logging.error(f"Full traceback: {traceback.format_exc()}")
            except:
                pass
            sys.stdout.flush()
            self.model_download_finished.emit(lang_code, "failure")

    def _populate_sidebar(self):
        while self.sidebar_layout.count():
            item = self.sidebar_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.sidebar_layout.setContentsMargins(15, 20, 15, 20)
        self.sidebar_layout.setSpacing(15)

        top_container = QWidget()
        top_layout = QVBoxLayout(top_container)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(10)
        
        queue_header_layout = QHBoxLayout()
        queue_header_label = QLabel("Media Queue")
        queue_header_label.setFont(QFont("Roboto", 12, QFont.Weight.Bold))
        queue_header_layout.addWidget(queue_header_label)
        queue_header_layout.addStretch()
        self.import_media_btn = self._create_icon_button("fa5s.plus", size=28, icon_size=12)
        self.import_media_btn.setStyleSheet("""
            QPushButton {
                background-color: #e50914; /* Main background color */
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #f61a27; /* Lighter color on hover */
            }
            QPushButton:pressed {
                background-color: #c00814; /* Darker color when pressed */
            }
        """)
        self.import_media_btn.setToolTip("Import Media Files or Folder")
        self.import_media_btn.clicked.connect(self._import_media)
        self.import_media_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        queue_header_layout.addWidget(self.import_media_btn)

        self.media_list_widget = QListWidget()
        self.media_list_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.media_list_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.media_list_widget.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.media_list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.media_list_widget.customContextMenuRequested.connect(self._show_media_context_menu)
        self.media_list_widget.setStyleSheet("""
            QListWidget { border: 1px solid #474747; border-radius: 10px; padding: 10px; }
            QListWidget::item { padding: 3px; border-radius: 3px; }
            QListWidget::item:hover { background-color: #333; cursor: pointer; }
            QListWidget::item:selected { background-color: #e50914; color: white; }
        """)
        self.media_list_widget.setCursor(Qt.CursorShape.OpenHandCursor)
        self.media_list_widget.itemDoubleClicked.connect(self._play_selected_media)
        
        top_layout.addLayout(queue_header_layout)
        top_layout.addWidget(self.media_list_widget)

        queue_controls_layout = QHBoxLayout()
        delete_selected_btn = QPushButton(" Delete Selected")
        delete_selected_btn.setIcon(qta.icon("fa5s.trash-alt", color="#f0f0f0"))
        delete_selected_btn.clicked.connect(self._delete_selected_media)
        delete_all_btn = QPushButton(" Delete All")
        delete_all_btn.setIcon(qta.icon("fa5s.trash", color="#f0f0f0"))
        delete_all_btn.clicked.connect(self._delete_all_media)
        
        for btn in [delete_selected_btn, delete_all_btn]:
             btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
             btn.setStyleSheet("QPushButton { text-align: center; padding: 5px; background-color: #2a2a2a; border: 1px solid #474747; border-radius: 5px; } QPushButton:hover { border-color: #e50914; }")
        
        queue_controls_layout.addWidget(delete_selected_btn)
        queue_controls_layout.addWidget(delete_all_btn)
        top_layout.addLayout(queue_controls_layout)
        
        bottom_container = QWidget()
        bottom_layout = QVBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(15)

        settings_header_label = QLabel("Settings")
        settings_header_label.setFont(QFont("Roboto", 12, QFont.Weight.Bold))
        settings_header_label.setStyleSheet("margin-top: 10px;")

        display_box, display_layout = self._create_setting_box("Subtitles Display")
        
        display_content_layout = QHBoxLayout(); display_content_layout.setContentsMargins(0,0,0,0)
        display_label = QLabel("Display Subtitles"); display_label.setStyleSheet("background-color: transparent; border: none;")
        self.subtitle_switch = SwitchButton(); self.subtitle_switch.toggled.connect(self._toggle_subtitles)
        display_content_layout.addWidget(display_label); display_content_layout.addStretch(); display_content_layout.addWidget(self.subtitle_switch)
        display_layout.addLayout(display_content_layout)

        font_size_layout = QHBoxLayout()
        font_size_label = QLabel("Font Size")
        font_size_label.setStyleSheet("background: transparent; border: none;")
        self.font_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.font_size_slider.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.font_size_slider.setStyleSheet("QSlider::groove:horizontal { border: 1px solid #333; height: 5px; background: #333333; border-radius: 2px; } QSlider::sub-page:horizontal { background: #e50914; border-radius: 2px; } QSlider::handle:horizontal { background: #e50914; border: 1px solid #e50914; width: 12px; height: 12px; margin: -4px 0; border-radius: 6px; }")
        self.font_size_slider.setRange(14, 72)
        self.font_size_slider.setValue(self.subtitle_font_size)
        self.font_size_slider.valueChanged.connect(self._set_subtitle_font_size)
        font_size_layout.addWidget(font_size_label)
        font_size_layout.addWidget(self.font_size_slider)
        display_layout.addLayout(font_size_layout)
        
        generation_box, generation_layout = self._create_setting_box("Subtitle Generation")
        
        self.language_selector_combo = QComboBox()
        self.language_selector_combo.setMinimumHeight(35)
        self.language_selector_combo.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.language_selector_combo.currentTextChanged.connect(self._on_language_changed)
        script_dir = os.path.dirname(os.path.abspath(__file__)); chevron_icon_path = os.path.join(script_dir, 'chevron-down.png').replace('\\', '/')
        if not os.path.exists(chevron_icon_path): qta.icon('fa5s.chevron-down', color='#f0f0f0').pixmap(QSize(16, 16)).save(chevron_icon_path)
        self.language_selector_combo.setStyleSheet(f"QComboBox {{ background-color: #1e1e1e; color: #f0f0f0; border: 1px solid #474747; border-radius: 10px; padding-left: 10px; padding-right: 10px; }} QComboBox:hover {{ border-color: #e50914; }} QComboBox::drop-down {{ subcontrol-origin: padding; subcontrol-position: top right; width: 25px; border-left-width: 1px; border-left-color: #474747; border-left-style: solid; border-top-right-radius: 10px; border-bottom-right-radius: 10px; }} QComboBox::down-arrow {{ image: url({chevron_icon_path}); width: 12px; height: 12px; }} QComboBox QAbstractItemView {{ background-color: #1e1e1e; color: #f0f0f0; border: 1px solid #474747; border-radius: 10px; selection-background-color: #333333; padding: 5px; }} QComboBox QAbstractItemView::item {{ height: 30px; border-radius: 5px; }} QComboBox QAbstractItemView::item:hover {{ background-color: #333333; color: #e50914; }}")
        
        self.generate_button = QPushButton("Generate")
        self.generate_button.setMinimumHeight(35)
        self.generate_button.setFont(QFont("Roboto", 9, QFont.Weight.Bold))
        self.generate_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.generate_button.setStyleSheet("QPushButton { background-color: #e50914; color: white; border: none; border-radius: 8px; } QPushButton:hover { background-color: #f61a27; } QPushButton:pressed { background-color: #c00814; }")
        self.generate_button.clicked.connect(self._start_subtitle_generation)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate progress for animation
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("QProgressBar { border: 1px solid #333333; border-radius: 8px; background-color: #1e1e1e; height: 16px;} QProgressBar::chunk { background-color: #e50914; border-radius: 7px; }")
        self.progress_bar.setVisible(False)
        
        self.progress_text = QLabel("Generating Subtitles: ...")
        self.progress_text.setStyleSheet("background-color: transparent; border: none; font-size: 9pt; color: #aaa;")
        self.progress_text.setVisible(False)
        
        generation_layout.addWidget(self.language_selector_combo)
        generation_layout.addWidget(self.generate_button)
        generation_layout.addWidget(self.progress_bar)
        generation_layout.addWidget(self.progress_text)
        
        manual_box, manual_layout = self._create_setting_box("Manual Override")
        self.load_srt_button = QPushButton("  Load .SRT File")
        self.load_srt_button.setIcon(qta.icon("fa5s.folder-open", color="#f0f0f0"))
        self.load_srt_button.clicked.connect(self._load_manual_srt)
        self.load_srt_button.setMinimumHeight(35)
        self.load_srt_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.load_srt_button.setStyleSheet("QPushButton { text-align: left; padding-left: 10px; background-color: #1e1e1e; color: #f0f0f0; border: 1px solid #474747; border-radius: 10px; } QPushButton:hover { border-color: #e50914; }")
        manual_layout.addWidget(self.load_srt_button)
        
        # credits_container = QWidget(); credits_container.setStyleSheet("border-top: 1px solid #404040; padding-top: 10px; ")
        # credits_layout = QVBoxLayout(credits_container); credits_layout.setContentsMargins(0,0,0,0); credits_layout.setSpacing(0)
        # credit_label = QLabel("Built with purpose by Anurag 💝"); credit_label.setFont(QFont("Roboto", 9)); credit_label.setStyleSheet("border: none; padding: 0; color: #999;")
        # github_link = QLabel("<a href='https://github.com/anu277' style='color: #f0f0f0; text-decoration: none;'>GitHub Profile</a>"); github_link.setFont(QFont("Roboto", 9, QFont.Weight.Bold)); github_link.setOpenExternalLinks(True); github_link.setStyleSheet("border: none; padding: 0;")
        # help_link = QLabel("<a href='https://github.com/anu277' style='color: #f0f0f0; text-decoration: none;'>Help & Support</a>"); help_link.setFont(QFont("Roboto", 9, QFont.Weight.Bold)); help_link.setOpenExternalLinks(True); help_link.setStyleSheet("border: none; padding: 0;")
        # credits_layout.addWidget(credit_label, 0, Qt.AlignmentFlag.AlignCenter); credits_layout.addWidget(github_link, 0, Qt.AlignmentFlag.AlignCenter); credits_layout.addWidget(help_link, 0, Qt.AlignmentFlag.AlignCenter)

        # # Performance disclaimer
        # disclaimer_container = QWidget(); disclaimer_container.setStyleSheet("border-top: 1px solid #404040; padding-top: 10px;")
        # disclaimer_layout = QVBoxLayout(disclaimer_container); disclaimer_layout.setContentsMargins(0,0,0,0); disclaimer_layout.setSpacing(0)
        # disclaimer_label = QLabel("⚠️ Estimated times based on i5-10300H (4C/8T, 10th Gen) with ~600MB RAM usage.\nPerformance may vary by CPU speed, cores/threads, and RAM.")
        # disclaimer_label.setFont(QFont("Roboto", 8)); disclaimer_label.setStyleSheet("border: none; padding: 0; color: #888; text-align: center;")
        # disclaimer_label.setAlignment(Qt.AlignmentFlag.AlignCenter); disclaimer_label.setWordWrap(True)
        # disclaimer_layout.addWidget(disclaimer_label, 0, Qt.AlignmentFlag.AlignCenter)
        
        # Combined Credits and Disclaimer Section
        bottom_info_container = QWidget()
        bottom_info_layout = QVBoxLayout(bottom_info_container)
        bottom_info_layout.setContentsMargins(0, 10, 0, 0)
        bottom_info_layout.setSpacing(20) # More vertical space for a clean separation

        # Credits Sub-section
        credits_layout = QVBoxLayout()
        credits_layout.setContentsMargins(0,0,0,0)
        credits_layout.setSpacing(5) # Tighter spacing for links
        credits_label = QLabel("Built with purpose by Anurag 💝")
        credits_label.setFont(QFont("Roboto", 9, QFont.Weight.Bold))
        credits_label.setStyleSheet("""
            QLabel {
                border-top: 1px dotted #888888;
                padding-top: 10px;
                color: #e50914;
            }
        """)
        credits_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        github_link = QLabel("<a href='https://github.com/anu277' style='color: #f0f0f0; text-decoration: underline;'>GitHub Profile</a>");
        github_link.setFont(QFont("Roboto", 9));
        github_link.setOpenExternalLinks(True);
        github_link.setStyleSheet("border: none; padding: 0;");
        github_link.setAlignment(Qt.AlignmentFlag.AlignCenter);

        credits_layout.addWidget(credits_label)
        credits_layout.addWidget(github_link)
        
        # Disclaimer Sub-section
        disclaimer_layout = QVBoxLayout()
        disclaimer_layout.setContentsMargins(0,0,0,0)
        disclaimer_layout.setSpacing(5)
        disclaimer_header = QLabel("Performance Note")
        disclaimer_header.setFont(QFont("Roboto", 9, QFont.Weight.Bold))
        disclaimer_header.setStyleSheet("""
            QLabel {
                border-top: 1px dotted #888888;
                padding-top: 10px;
                color: #f0f0f0;
            }
        """)
        disclaimer_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        disclaimer_text = QLabel("⚠️ Estimated times based on i5-10300H (4C/8T, 10th Gen) with ~600MB RAM usage. Performance may vary by CPU speed, cores/threads, and RAM.")
        disclaimer_text.setFont(QFont("Roboto", 8))
        disclaimer_text.setStyleSheet("border: none; padding: 0; color: #888; text-align: center;")
        disclaimer_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        disclaimer_text.setWordWrap(True)

        disclaimer_layout.addWidget(disclaimer_header)
        disclaimer_layout.addWidget(disclaimer_text)

        bottom_info_layout.addLayout(disclaimer_layout)
        bottom_info_layout.addLayout(credits_layout)
        
        bottom_layout.addWidget(settings_header_label)
        bottom_layout.addWidget(display_box)
        bottom_layout.addWidget(generation_box)
        bottom_layout.addWidget(manual_box)
        bottom_layout.addStretch()
        bottom_layout.addWidget(bottom_info_container)
        bottom_layout.addWidget(bottom_info_container)
        
        self.sidebar_layout.addWidget(top_container, 1)
        self.sidebar_layout.addWidget(bottom_container)
    

    def _import_media(self):
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background-color: #1e1e1e; color: #f0f0f0; border: 1px solid #333; } QMenu::item:selected { background-color: #333; }")
        files_action = menu.addAction("Import Files")
        folder_action = menu.addAction("Import Folder")
        action = menu.exec(self.import_media_btn.mapToGlobal(QPointF(0, self.import_media_btn.height()).toPoint()))
        if action == files_action: self._import_files()
        elif action == folder_action: self._import_folder()
    
    def _load_last_import_path(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    return f.read().strip()
        except:
            pass
        return os.path.expanduser("~/Videos")
    
    def _save_last_import_path(self, path):
        try:
            with open(self.settings_file, 'w') as f:
                f.write(path)
        except:
            pass
    
    def _import_files(self): 
        files, _ = QFileDialog.getOpenFileNames(self, "Import Media", self.last_import_path, "Media Files (*.mp4 *.mkv *.avi)")
        if files: 
            self.last_import_path = os.path.dirname(files[0])
            self._save_last_import_path(self.last_import_path)
            self._add_media_files(files)
            
    def _import_folder(self): 
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", self.last_import_path)
        if folder: 
            self.last_import_path = folder
            self._save_last_import_path(self.last_import_path)
            self._scan_folder_for_videos(folder)

    def _scan_folder_for_videos(self, path):
        ext = ('.mp4', '.avi', '.mkv'); files = [os.path.join(r, f) for r, _, fs in os.walk(path) for f in fs if f.lower().endswith(ext)]; files.sort(); self._add_media_files(files)

    def _add_media_files(self, file_paths):
        new_files = False
        for path in file_paths:
            if path not in self.media_queue:
                self.media_queue.append(path); item = QListWidgetItem(os.path.basename(path))
                item.setData(Qt.ItemDataRole.UserRole, path); item.setToolTip(path)
                self.media_list_widget.addItem(item); new_files = True
        if new_files and self.current_media_index == -1 and self.media_list_widget.count() > 0:
            first_item = self.media_list_widget.item(0)
            self.media_list_widget.setCurrentItem(first_item); self._play_selected_media(first_item)
    
    def _play_next_in_queue(self):
        if self.current_media_index + 1 < self.media_list_widget.count():
            self.current_media_index += 1
            item = self.media_list_widget.item(self.current_media_index)
            self.media_list_widget.setCurrentItem(item); self._play_selected_media(item)
        else:
            self.is_playing = False
            self.play_pause_btn.setIcon(qta.icon("fa5s.play", color="#f0f0f0"))

    def _play_previous_in_queue(self):
        if self.current_media_index > 0:
            self.current_media_index -= 1
            item = self.media_list_widget.item(self.current_media_index)
            self.media_list_widget.setCurrentItem(item); self._play_selected_media(item)
            
    def _toggle_sidebar(self):
        if self.is_sidebar_open:
            self.is_sidebar_open = False
            self.sidebar.setVisible(False)
            self.sidebar_toggle_btn.setIcon(qta.icon("fa5s.chevron-left", color="#f0f0f0"))
        else:
            self.is_sidebar_open = True
            self.sidebar.setVisible(True)
            self.sidebar_toggle_btn.setIcon(qta.icon("fa5s.chevron-right", color="#f0f0f0"))
    
    def eventFilter(self, obj, event):
        if not hasattr(self, 'sidebar'):
            return super().eventFilter(obj, event)

        if obj is self.video_container:
            if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
                if self.current_media_index != -1:
                    self._toggle_play_pause()
                return True
            if event.type() == QEvent.Type.MouseButtonDblClick and event.button() == Qt.MouseButton.LeftButton:
                self._toggle_fullscreen()
                return True
            if event.type() == QEvent.Type.MouseMove:
                current_pos = event.position()
                distance = (current_pos - self.last_mouse_pos).manhattanLength()
                if distance > 5:
                    self._show_controls()
                    self.mouse_idle_timer.start()
                self.last_mouse_pos = current_pos
                return False
            if event.type() == QEvent.Type.Enter:
                self.last_mouse_pos = event.position()
                self._show_controls()
                self.mouse_idle_timer.start()
                return False
        
        if obj is self.bottom_controls_container:
            if event.type() == QEvent.Type.Enter:
                self.mouse_idle_timer.stop()
                return False
            elif event.type() == QEvent.Type.Leave:
                self.mouse_idle_timer.start()
                return False

        if event.type() == QEvent.Type.Wheel and self._is_video_area_child(obj):
            self._handle_volume_wheel(event)
            return True

        if obj is self.sidebar_handle:
            if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
                self._toggle_sidebar()
                return True
            
        if obj is self.sidebar_toggle_btn:
            if event.type() == QEvent.Type.Enter:
                self.btn_shrink_anim.stop()
                self.btn_grow_anim.setStartValue(self.sidebar_toggle_btn.size())
                self.btn_grow_anim.setEndValue(QSize(30, 30))
                self.btn_grow_anim.start()
                return True
            elif event.type() == QEvent.Type.Leave:
                self.btn_grow_anim.stop()
                self.btn_shrink_anim.setStartValue(self.sidebar_toggle_btn.size())
                self.btn_shrink_anim.setEndValue(QSize(25, 25))
                self.btn_shrink_anim.start()
                return True

        return super().eventFilter(obj, event)
    
    def _create_icon_button(self, icon, size=35, icon_size=16):
        btn = QPushButton(); btn.setFixedSize(size, size); btn.setIcon(QIcon(qta.icon(icon, color="#f0f0f0").pixmap(icon_size, icon_size))); btn.setIconSize(QSize(icon_size, icon_size)); btn.setStyleSheet("QPushButton { background-color: transparent; border: none; border-radius: 5px; } QPushButton:hover { background-color: #333333; }"); return btn
    
    def _toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.showFullScreen(); self.fullscreen_btn.setIcon(qta.icon("fa5s.compress", color="#f0f0f0"))
        else:
            self.showNormal(); self.fullscreen_btn.setIcon(qta.icon("fa5s.expand", color="#f0f0f0"))

    def _set_subtitle_font_size(self, size):
        self.subtitle_font_size = size
        self.mpv_player.sub_font_size = size
        self.subtitle_label.setStyleSheet(
            f"font-size: {size}px; background-color: rgba(0, 0, 0, 0.5); color: white; padding: 5px 10px; border-radius: 5px;"
        )

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key == Qt.Key.Key_Space: self._toggle_play_pause()
        elif key == Qt.Key.Key_Right: self._skip_forward()
        elif key == Qt.Key.Key_Left: self._skip_backward()
        elif key == Qt.Key.Key_Up: self._change_volume(5)
        elif key == Qt.Key.Key_Down: self._change_volume(-5)
        elif key == Qt.Key.Key_F: self._toggle_fullscreen()
        elif key in [Qt.Key.Key_Tab, Qt.Key.Key_Backtab]: return
        else: super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """Clean up resources when window closes"""
        try:
            if hasattr(self, 'mpv_player'):
                self.mpv_player.terminate()
            if hasattr(self, 'subtitle_executor'):
                self.subtitle_executor.shutdown(wait=False)
            if hasattr(self, 'download_executor'):
                self.download_executor.shutdown(wait=False)
        except:
            pass
        event.accept()

    def _on_language_changed(self, language):
        self.language_selector_combo.clearFocus()
        
        # Extract clean language name (remove size suffix like "(300MB)")
        clean_language = language.split(' (')[0] if ' (' in language else language
        
        if self.current_media_index == -1:
            self.generate_button.setVisible(False)
            self.progress_bar.setVisible(False)
            self.progress_text.setVisible(False)
            return

        current_file_path = self.media_queue[self.current_media_index]
        english_srt_path = self._get_subtitle_path(current_file_path, "en")
        lang_code = self._get_language_code(clean_language)
        subtitle_path = self._get_subtitle_path(current_file_path, lang_code)
        
        # Check if English base subtitle exists
        english_exists = os.path.exists(english_srt_path)
        
        # If not English and no English base, force English selection
        if clean_language != "English" and not english_exists:
            # Calculate estimated time for English transcription
            video_duration = self.media_duration
            estimated_time = self._calculate_estimated_time(video_duration, "en")
            estimated_minutes = int(estimated_time / 60)
            estimated_seconds = int(estimated_time % 60)
            
            # Show waiting message
            self.generate_button.setVisible(False)
            self.progress_bar.setVisible(False)
            self.progress_text.setVisible(True)
            self.progress_text.setText(f"Need English base subtitle first. Est. time: {estimated_minutes}m {estimated_seconds}s")
            
            # Force English selection
            for i in range(self.language_selector_combo.count()):
                if self.language_selector_combo.itemText(i) == "English":
                    self.language_selector_combo.setCurrentIndex(i)
                    break
            return
        
        # Check if the model is downloaded for the selected language
        model_status = self.download_status.get(clean_language, {"status": "not_downloaded"})

        if os.path.exists(subtitle_path):
            self.generate_button.setVisible(False)
            self.progress_bar.setVisible(False)
            self.progress_text.setVisible(False)
            try:
                self.mpv_player.sub_add(subtitle_path)
                self._show_toast(f"Subtitle file for {clean_language} already exists. Loaded successfully.")
            except Exception as e:
                logging.error(f"Error loading subtitle file: {e}")
                print(f"Error loading subtitle file: {e}")
                self._show_toast(f"Error loading subtitle file for {clean_language}")
        else:
            # For English, hide generate button and auto-start
            if clean_language == "English":
                self.generate_button.setVisible(False)
                if not english_exists:
                    # Show progress during transcription
                    self.progress_bar.setVisible(True)
                    self.progress_text.setVisible(True)
                    video_duration = self.media_duration
                    estimated_time = self._calculate_estimated_time(video_duration, "en")
                    estimated_minutes = int(estimated_time / 60)
                    estimated_seconds = int(estimated_time % 60)
                    self.progress_text.setText(f"Generating English subtitles... Est: {estimated_minutes}m {estimated_seconds}s")
                    self._start_subtitle_generation()
                else:
                    self.progress_bar.setVisible(False)
                    self.progress_text.setVisible(False)
            else:
                self.generate_button.setVisible(True)
                self.progress_bar.setVisible(False)
                self.progress_text.setVisible(False)
                
                if model_status["status"] == "downloaded":
                    self.generate_button.setText("Generate")
                    self.generate_button.setEnabled(True)
                elif model_status["status"] == "downloading":
                    self.generate_button.setText("Downloading...")
                    self.generate_button.setEnabled(False)
                else:
                    size = model_status.get('size', 'Unknown')
                    self.generate_button.setText(f"Download ({size})")
                    self.generate_button.setEnabled(True)


    def _start_subtitle_generation(self):
        if self.current_media_index == -1: 
            self._show_toast("No media loaded.")
            return

        current_language = self.language_selector_combo.currentText()
        # Extract clean language name (remove size suffix like "(300MB)")
        clean_language = current_language.split(' (')[0] if ' (' in current_language else current_language
        lang_code = self._get_language_code(clean_language)
        
        if self.download_status.get(clean_language, {}).get("status") == "not_downloaded" and clean_language != "English":
            # Start download instead of generation
            print(f"DEBUG: Starting download for {clean_language} (code: {lang_code})")
            sys.stdout.flush()
            future = self.download_executor.submit(self._download_model_in_background, lang_code)
            print(f"DEBUG: Thread submitted, future: {future}")
            sys.stdout.flush()
            self.generate_button.setText("Downloading...")
            self.generate_button.setEnabled(False)
            return

        if self.generation_future and self.generation_future.running():
            self._show_toast("Subtitle generation is already in progress.")
            return
        
        current_file_path = self.media_queue[self.current_media_index]
        english_srt_path = self._get_subtitle_path(current_file_path, "en")
        output_path = self._get_subtitle_path(current_file_path, lang_code)

        task_type = ""
        if not os.path.exists(english_srt_path):
            task_type = "transcribe"
            self._show_toast("English subtitles not found. Generating English base file...")
        elif clean_language != "English":
            task_type = "translate"
            self._show_toast(f"Generating {clean_language} subtitles by translation...")
        else:
            self._show_toast("English subtitles already exist. Skipping generation.")
            self.generate_button.setVisible(False)
            return
            
        self.generate_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_text.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Disable language dropdown during any subtitle generation
        self.language_selector_combo.setEnabled(False)
        
        if task_type == "transcribe":
            self.progress_bar.setRange(0, 0)  # Animated progress bar
        else:
            self.progress_bar.setRange(0, 100)  # Normal progress bar

        # Get video duration, use fallback if not available yet
        video_duration_seconds = self.media_duration
        if video_duration_seconds <= 0:
            try:
                video_duration_seconds = self.mpv_player.duration or 600  # 10 min fallback
            except:
                video_duration_seconds = 600  # 10 min fallback
        
        self.estimated_total_time = self._calculate_estimated_time(video_duration_seconds, lang_code)
        
        print(f"DEBUG: Video duration: {video_duration_seconds}s, Lang: {lang_code}, Estimated time: {self.estimated_total_time}s")
        
        estimated_time_str = str(timedelta(seconds=int(self.estimated_total_time)))
        self.progress_text.setText(f"Estimated time: {estimated_time_str}")
        self.generation_start_time = time.time()

        if task_type == "transcribe":
            self.generation_future = self.subtitle_executor.submit(
                self._generate_subtitles_from_audio,
                current_file_path,
                "en",
                english_srt_path,
            )
        elif task_type == "translate":
            self.generation_future = self.subtitle_executor.submit(
                self._translate_subtitles_from_english,
                english_srt_path,
                lang_code,
                output_path,
            )
        
        # Show initial progress message in subtitle area
        estimated_minutes = int(self.estimated_total_time / 60)
        estimated_seconds = int(self.estimated_total_time % 60)
        if task_type == "transcribe":
            self.subtitle_label.setText(f"GENERATING SUBTITLES.... ({estimated_minutes}m {estimated_seconds}s estimated)")
        else:
            self.subtitle_label.setText(f"TRANSLATING SUBTITLES.... ({estimated_minutes}m {estimated_seconds}s estimated)")
        self.subtitle_label.setVisible(True)
        
        self.generation_progress_timer.timeout.connect(
            lambda: self._update_progress_bar(self.generation_future, output_path)
        )
        self.generation_progress_timer.start()

    def _update_progress_bar(self, future, output_path):
        if future.done():
            self.generation_progress_timer.stop()
            self.progress_bar.setValue(100)
            self.subtitle_label.setVisible(False)  # Hide progress message
            self._finalize_generation(future, output_path)
        else:
            elapsed_time = time.time() - self.generation_start_time
            if self.estimated_total_time > 0:
                progress_percentage = min(99, int((elapsed_time / self.estimated_total_time) * 100))
                self.progress_bar.setValue(progress_percentage)
                remaining_time = max(0, self.estimated_total_time - elapsed_time)
                remaining_time_str = str(timedelta(seconds=int(remaining_time)))
                self.progress_text.setText(f"Estimated time: {remaining_time_str}")
                # Show progress in subtitle area
                total_time_str = str(timedelta(seconds=int(self.estimated_total_time)))
                current_language = self.language_selector_combo.currentText().split(' (')[0]
                if current_language == "English":
                    self.subtitle_label.setText(f"GENERATING SUBTITLES.... {progress_percentage}% ({remaining_time_str} / {total_time_str})")
                else:
                    self.subtitle_label.setText(f"TRANSLATING SUBTITLES.... {progress_percentage}% ({remaining_time_str} / {total_time_str})")
                self.subtitle_label.setVisible(True)
            else:
                remaining_time = max(0, self.estimated_total_time - elapsed_time)
                remaining_minutes = int(remaining_time / 60)
                remaining_seconds = int(remaining_time % 60)
                self.progress_text.setText(f"Generating Base Language...\n {remaining_minutes}m {remaining_seconds}s remaining")
                # Show progress in subtitle area for base language generation
                self.subtitle_label.setText(f"GENERATING BASE SUBTITLES.... ({remaining_minutes}m {remaining_seconds}s remaining)")
                self.subtitle_label.setVisible(True)

    def _finalize_generation(self, future, output_path):
        self.generate_button.setEnabled(True)
        self.language_selector_combo.setEnabled(True)  # Re-enable language dropdown
        try:
            result = future.result()
            if result:
                self._show_toast("✅ Subtitles generated and loaded!")
                try:
                    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                        self.mpv_player.sub_add(output_path)
                        print(f"THREAD LOG: ✅ Subtitle file loaded successfully: {output_path}")
                    else:
                        print(f"THREAD LOG: ❌ Subtitle file is empty or doesn't exist: {output_path}")
                        self._show_toast("Subtitle file is empty or corrupted")
                except Exception as e:
                    print(f"Error loading generated subtitle file: {e}")
                    print(f"THREAD LOG: File exists: {os.path.exists(output_path)}")
                    print(f"THREAD LOG: File size: {os.path.getsize(output_path) if os.path.exists(output_path) else 'N/A'}")
                    self._show_toast("Subtitles generated but failed to load")
            else:
                self.progress_text.setText("❌ Generation failed.")
                self._show_toast("Error generating subtitles. Check console for details.")
        except Exception as e:
            if "cancelled" in str(e).lower() or "interrupted" in str(e).lower():
                self._show_toast("⚠️ Subtitle generation interrupted")
                self.progress_text.setText("Generation interrupted")
            else:
                self._show_toast(f"An error occurred: {str(e)}")
                self.progress_text.setText(f"Error: {e}")
        
        QTimer.singleShot(3000, lambda: [
            self.progress_bar.setVisible(False), 
            self.progress_text.setVisible(False),
            self._on_language_changed(self.language_selector_combo.currentText())
        ])

    def _generate_subtitles_from_audio(self, video_path, lang_code, output_path):
        # Get correct base path for both script and EXE
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        try:
            print(f"THREAD LOG: Starting audio transcribe process.")
            audio_path = os.path.join(tempfile.gettempdir(), f"audio_{os.path.basename(video_path)}.mp3")
            # Try different ffmpeg paths (EXE-compatible)
            ffmpeg_paths = [
                os.path.join(base_path, "ffmpeg", "ffmpeg.exe"),  # Bundled ffmpeg folder
                os.path.join(base_path, "ffmpeg.exe"),  # Bundled root folder
                "ffmpeg",  # System PATH (fallback)
                "C:\\ffmpeg\\bin\\ffmpeg.exe",  # Common install location
                os.path.join(os.environ.get('PROGRAMFILES', ''), 'ffmpeg', 'bin', 'ffmpeg.exe'),  # Program Files
            ]
            
            ffmpeg_cmd = None
            for path in ffmpeg_paths:
                try:
                    subprocess.run([path, "-version"], capture_output=True, check=True)
                    ffmpeg_cmd = path
                    break
                except:
                    continue
            
            if not ffmpeg_cmd:
                raise FileNotFoundError("FFmpeg not found in any expected location")
            
            command = [ffmpeg_cmd, "-i", video_path, "-vn", "-acodec", "libmp3lame", "-ac", "1", "-ar", "16000", "-b:a", "128k", "-y", audio_path]
            subprocess.run(command, check=True, capture_output=True, text=True)
            print("THREAD LOG: ✅ Audio extraction successful.")
            
            model_path = os.path.join(base_path, "whisper")
            # Lazy import WhisperModel only when needed
            from faster_whisper import WhisperModel
            model = WhisperModel(model_path, local_files_only=True, device="cpu", compute_type="int8")
            
            # Check if ONNX is available for VAD filtering
            try:
                import onnxruntime
                vad_available = True
            except:
                vad_available = False
                print("THREAD LOG: VAD filtering disabled (ONNX not available)")
            
            segments_generator, info = model.transcribe(audio_path, language=lang_code, vad_filter=vad_available)
            print(f"THREAD LOG: ✅ transcribe complete.")
            
            post_processed_segments = []
            for segment in segments_generator:
                post_processed_segments.append({'start': segment.start, 'end': segment.end, 'text': segment.text.strip()})
            
            self._write_srt_file(output_path, post_processed_segments)

            os.unlink(audio_path)
            print("THREAD LOG: ✅ Temporary audio file deleted.")
            return True
            
        except Exception as e:
            error_msg = f"THREAD LOG: ERROR: An unexpected error occurred: {str(e)}"
            logging.error(error_msg)
            print(error_msg)
            return False

    def _translate_subtitles_from_english(self, english_srt_path, target_lang_code, output_path):
        try:
            print(f"THREAD LOG: Starting translation from English SRT to {target_lang_code}.")
            sys.stdout.flush()
            
            subtitles_with_timestamps = []
            with open(english_srt_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            chunks = content.strip().split("\n\n")
            
            for chunk in chunks:
                lines = chunk.split("\n")
                if len(lines) >= 3:
                    timestamps = lines[1]
                    text = " ".join(lines[2:])
                    subtitles_with_timestamps.append({'timestamps': timestamps, 'text': text})

            print(f"THREAD LOG: Parsed {len(subtitles_with_timestamps)} subtitle segments.")
            sys.stdout.flush()
            
            # Initialize EasyNMT with error handling
            if self.easy_nmt_model is None:
                print(f"THREAD LOG: Initializing EasyNMT model...")
                sys.stdout.flush()
                try:
                    from easynmt import EasyNMT
                    self.easy_nmt_model = EasyNMT('opus-mt')
                    self.easy_nmt_model.sentence_splitter = lambda text, lang: [text]
                    print(f"THREAD LOG: ✅ EasyNMT model initialized successfully.")
                    sys.stdout.flush()
                except Exception as init_error:
                    print(f"THREAD LOG: ❌ EasyNMT initialization failed: {init_error}")
                    sys.stdout.flush()
                    return False

            print(f"THREAD LOG: Starting batch translation...")
            sys.stdout.flush()
            
            all_english_text = [sub['text'] for sub in subtitles_with_timestamps]
            translated_text_block = self.easy_nmt_model.translate(all_english_text, source_lang="en", target_lang=target_lang_code)
            
            print(f"THREAD LOG: ✅ Batch translation completed.")
            sys.stdout.flush()
            
            translated_subtitles = [{'timestamps': subtitles_with_timestamps[i]['timestamps'], 'text': translated_text_block[i]} for i in range(len(subtitles_with_timestamps))]

            with open(output_path, "w", encoding="utf-8") as srt_file:
                for i, sub in enumerate(translated_subtitles):
                    srt_file.write(f"{i + 1}\n")
                    srt_file.write(f"{sub['timestamps']}\n")
                    srt_file.write(f"{sub['text']}\n\n")

            print(f"THREAD LOG: ✅ Translation to {target_lang_code} complete.")
            sys.stdout.flush()
            
            # Clear model from memory to reduce RAM usage
            if self.easy_nmt_model is not None:
                del self.easy_nmt_model
                self.easy_nmt_model = None
                print(f"THREAD LOG: ✅ EasyNMT model cleared from memory.")
                sys.stdout.flush()
            
            return True

        except Exception as e:
            print(f"THREAD LOG: ❌ ERROR: An unexpected error occurred during translation: {str(e)}")
            sys.stdout.flush()
            import traceback
            print(f"THREAD LOG: Full traceback: {traceback.format_exc()}")
            sys.stdout.flush()
            
            # Clear model from memory even on failure
            if self.easy_nmt_model is not None:
                del self.easy_nmt_model
                self.easy_nmt_model = None
                print(f"THREAD LOG: ✅ EasyNMT model cleared from memory after error.")
                sys.stdout.flush()
            
            return False

    def _write_srt_file(self, output_path, segments):
        with open(output_path, "w", encoding="utf-8") as srt_file:
            for i, segment in enumerate(segments):
                start = segment['start']
                end = segment['end']
                text = segment['text'].strip()
                
                srt_file.write(f"{i + 1}\n")
                srt_file.write(f"{self._format_time_srt(start)} --> {self._format_time_srt(end)}\n")
                srt_file.write(f"{text}\n\n")

    def _update_status_bar(self, message):
        print(f"GUI_STATUS: {message}")

    def _show_toast(self, message):
        self.toast_label.setText(message)
        self.toast_label.setVisible(True)
        QTimer.singleShot(3000, lambda: self.toast_label.setVisible(False))

    def _get_language_name(self, code):
        for name, c in self.languages_list.items():
            if c == code:
                return name
        return code

    def _get_language_code(self, language):
        language_map = {
            "English": "en", "Spanish": "es", "French": "fr", "German": "de",
            "Italian": "it", "Japanese": "jap", "Russian": "ru",
            "Arabic": "ar", "Chinese": "zh", "Hindi": "hi",
            "Dutch": "nl", "Swedish": "sv", "Ukrainian": "uk", "Urdu": "ur"
        }
        return language_map.get(language, "en")
    
    def _get_subtitle_path(self, video_path, lang_code):
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        directory = os.path.dirname(video_path)
        return os.path.join(directory, f"{base_name}.{lang_code}.srt")

# The main application entry point remains the same
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZestSyncPlayer()
    
    # Handle command line arguments for "Open with"
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path) and file_path.lower().endswith(('.mp4', '.mkv', '.avi')):
            window._add_media_files([file_path])
    
    window.show()
    sys.exit(app.exec())