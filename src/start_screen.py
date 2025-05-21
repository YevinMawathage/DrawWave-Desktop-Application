from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QLinearGradient, QPalette, QColor, QBrush, QIcon
import sys
import os
from resource_path import resource_path

from virtual_painter_gui import VirtualPainterGUI

class StartScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DrawWave")
        self.setFixedSize(640, 480)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0 y1:0, x2:1 y2:1,
                    stop:0 #f8fafc, stop:1 #dbeafe
                );
            }
        """)
        icon_path = resource_path('virtual_painter.png')
        self.setWindowIcon(QIcon(icon_path))

        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(60, 60, 60, 60)

        # Title
        title_label = QLabel("DrawWave")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 35, QFont.Bold))
        title_label.setStyleSheet("color: #1e293b; letter-spacing: 2px;")
        layout.addWidget(title_label)

        # Optional subtitle
        subtitle = QLabel("Create. Gesture. Imagine.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setStyleSheet("color: #64748b;")
        layout.addWidget(subtitle)

        # Spacer
        layout.addStretch(1)

        # Start button
        start_button = QPushButton("Start")
        start_button.setFixedHeight(48)
        start_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        start_button.setCursor(Qt.PointingHandCursor)
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border-radius: 6px;
                padding: 0 40px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #818cf8;
            }
        """)
        start_button.clicked.connect(self.start_button_click)
        layout.addWidget(start_button, alignment=Qt.AlignCenter)

        # Spacer
        layout.addStretch(2)

        self.setLayout(layout)

    def start_button_click(self):
        self.close()
        self.painter_gui = VirtualPainterGUI()
        self.painter_gui.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartScreen()
    window.show()
    sys.exit(app.exec_())
