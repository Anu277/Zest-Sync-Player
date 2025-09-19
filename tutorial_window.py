import sys
import os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon
import qtawesome as qta

class TutorialWindow(QDialog):
    finished = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("How to Use Zest Sync Player")
        self.setFixedSize(1200, 900)
        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        
        # Tutorial images and descriptions
        self.tutorial_data = [
            {
                "image": "assets/manual/1.jpg",
                "title": "Step 1: Import Your Videos",
                "description": "Click the '+' button in the sidebar to import video files (MP4, MKV, AVI) or entire folders."
            },
            {
                "image": "assets/manual/3.jpg", 
                "title": "Step 2: Subtitles and Language",
                "description": "Subtile switch with ON/OFF. Choose your target language from 14 options and accuracy mode (Fast for movies, Slow for anime/dubbed content)."
            },
            {
                "image": "assets/manual/4.jpg",
                "title": "Step 3: Manual Override", 
                "description": "If you have your own subtitle file load it from here"
            },
            {
                "image": "assets/manual/5.png",
                "title": "Step 4: Enjoy Your Video",
                "description": "Use keyboard shortcuts: K (play/pause), J/L (skip), U/I (volume), F (fullscreen)."
            }
        ]
        
        self.current_step = 0
        self.setup_ui()
        self.load_current_step()
        
    def setup_ui(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #f0f0f0;
                font-family: Roboto;
            }
            QLabel {
                color: #f0f0f0;
                background-color: transparent;
            }
            QPushButton {
                background-color: #e50914;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 80px;
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
        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #e50914; margin-bottom: 10px;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        
        # Image container
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 2px solid #333; border-radius: 10px; background-color: #2a2a2a;")
        self.image_label.setMinimumHeight(700)
        layout.addWidget(self.image_label)
        
        # Description
        self.desc_label = QLabel()
        self.desc_label.setStyleSheet("font-size: 16px; color: #e50914; margin: 10px 0;")
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)
        
        # Progress indicator
        self.progress_label = QLabel()
        self.progress_label.setStyleSheet("font-size: 12px; color: #888;")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.progress_label)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        
        self.prev_btn = QPushButton("Previous")
        self.prev_btn.setIcon(qta.icon("fa5s.chevron-left", color="white"))
        self.prev_btn.clicked.connect(self.previous_step)
        
        self.skip_btn = QPushButton("Skip Tutorial")
        self.skip_btn.setStyleSheet("background-color: #666; min-width: 120px;")
        self.skip_btn.clicked.connect(self.skip_tutorial)
        
        self.next_btn = QPushButton("Next")
        self.next_btn.setIcon(qta.icon("fa5s.chevron-right", color="white"))
        self.next_btn.clicked.connect(self.next_step)
        
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.skip_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_btn)
        
        layout.addLayout(nav_layout)
        
    def load_current_step(self):
        step_data = self.tutorial_data[self.current_step]
        
        # Update title and description
        self.title_label.setText(step_data["title"])
        self.desc_label.setText(step_data["description"])
        
        # Update progress
        self.progress_label.setText(f"Step {self.current_step + 1} of {len(self.tutorial_data)}")
        
        # Load image
        if getattr(sys, 'frozen', False):
            image_path = os.path.join(sys._MEIPASS, step_data["image"])
        else:
            image_path = step_data["image"]
            
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(920, 690, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setText(f"Tutorial Image {self.current_step + 1}\n(Image not found)")
            self.image_label.setStyleSheet("font-size: 18px; color: #888; border: 2px dashed #555;")
        
        # Update button states
        self.prev_btn.setEnabled(self.current_step > 0)
        
        if self.current_step == len(self.tutorial_data) - 1:
            self.next_btn.setText("Get Started")
            self.next_btn.setIcon(qta.icon("fa5s.play", color="white"))
        else:
            self.next_btn.setText("Next")
            self.next_btn.setIcon(qta.icon("fa5s.chevron-right", color="white"))
            
    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.load_current_step()
            
    def next_step(self):
        if self.current_step < len(self.tutorial_data) - 1:
            self.current_step += 1
            self.load_current_step()
        else:
            self.finish_tutorial()
            
    def skip_tutorial(self):
        self.finish_tutorial()
        
    def finish_tutorial(self):
        self.finished.emit()
        self.accept()
        
    def center_on_screen(self):
        from PyQt6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)