from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QFileDialog, QColorDialog, QShortcut, QToolButton
from PyQt5.QtGui import QImage, QPixmap, QFont, QKeySequence, QIcon, QColor
from PyQt5.QtCore import QTimer, Qt
import cv2
import time
import os
from resource_path import resource_path
from canvas import Canvas
from canvas_widget import CanvasWidget
from hand_tracking import HandTracker
from database import Database

class VirtualPainterGUI(QWidget):
    def __init__(self):
        super().__init__()
        
        
        db_path = resource_path('virtual_painter.db')
        self.db = Database(db_path)
        
        self.setWindowTitle("DrawWave")
        self.setGeometry(100, 100, 1280, 720)
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
        
        self.available_cameras = self.find_available_cameras(max_index=4)
        
        if self.available_cameras:
            saved_camera_index = self.db.get_setting('camera_index')
            
            if saved_camera_index and int(saved_camera_index) in self.available_cameras:
                self.camera_index = int(saved_camera_index)
            else:
                self.camera_index = self.available_cameras[0]
                
            try:
                self.capture = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
                time.sleep(0.5)  
                if self.capture.isOpened():
                    print(f"[CAMERA] Using camera index {self.camera_index}")
                else:
                    print("[WARNING] Camera failed to initialize")
                    self.capture = None
            except Exception as e:
                print(f"[ERROR] Camera initialization error: {e}")
                self.capture = None
        else:
            self.capture = None
            self.camera_index = 0
            print("[WARNING] No cameras found")
        
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(32, 32)
        self.color_preview.setStyleSheet("""
            QLabel {
                background-color: black;
                border-radius: 16px;
                border: 2px solid #c7d2fe;
            }
        """)    
 
        # Initialize components
        self.hand_tracker = HandTracker()
        self.canvas = Canvas(db=self.db)
        self.mode = "gesture"
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Top section: Camera and Canvas
        top_section = QHBoxLayout()
        top_section.setSpacing(20)
        
            # Camera feed with styled frame
        self.camera_feed_label = QLabel(self)
        self.camera_feed_label.setFixedSize(640, 480)
        self.camera_feed_label.setStyleSheet("""
            QLabel {
                background: #ffffff;
                border-radius: 10px;
                border: 2px solid #c7d2fe;
            }
        """)
        top_section.addWidget(self.camera_feed_label)
        
        # Canvas widget with styled frame
        self.canvas_widget = CanvasWidget(self.canvas)
        self.canvas_widget.setFixedSize(640, 480)
        self.canvas_widget.setStyleSheet("""
            QWidget {
                background: #ffffff;
                border-radius: 10px;
                border: 2px solid #c7d2fe;
            }
        """)
        top_section.addWidget(self.canvas_widget)
        
        main_layout.addLayout(top_section)
        
        # Bottom control panel
        control_panel = QHBoxLayout()
        control_panel.setContentsMargins(0, 10, 0, 0)
        control_panel.setSpacing(20)
        
        # Mode buttons
        self.mouse_btn = QPushButton("Mouse Draw")
        self.mouse_erase_btn = QPushButton("Erase")
        self.gesture_btn = QPushButton("Gesture Draw")
        self.back_btn = QPushButton("Back")
        
        self.clear_btn = QPushButton("Clear")
        self.save_btn = QPushButton("Save")
        self.color_btn = QPushButton(" Change Color")
        
        # Camera switch button 
        self.switch_camera_btn = QToolButton()
        self.switch_camera_btn.setText("📷")
        self.switch_camera_btn.setToolTip("Switch to next camera")
        self.switch_camera_btn.setFixedSize(40, 40)  
        
        # Style buttons to match start screen
        button_style = """
            QPushButton {
                background-color: #6366f1;
                color: white;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #818cf8;
            }
            QPushButton:pressed {
                background-color: #4f46e5;
            }
        """
        
        # Style for normal buttons
        for btn in [self.mouse_btn, self.mouse_erase_btn, self.gesture_btn, self.back_btn, 
                   self.clear_btn, self.save_btn, self.color_btn]:
            btn.setStyleSheet(button_style)
            btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
            btn.setCursor(Qt.PointingHandCursor)
            
        
        self.switch_camera_btn.setStyleSheet("""
            QToolButton {
                background-color: #FFFFFF;
                color: white;
                border-radius: 20px;  /* Half of the fixed size for perfect circle */
                font-size: 16px;
            }
            QToolButton:hover {
                background-color: #818cf8;
            }
            QToolButton:pressed {
                background-color: #4f46e5;
            }
        """)
        self.switch_camera_btn.setCursor(Qt.PointingHandCursor)
        
     
        control_panel.addStretch()
        control_panel.addWidget(self.mouse_btn)
        control_panel.insertWidget(2, self.mouse_erase_btn)
        control_panel.addWidget(self.gesture_btn)
        control_panel.addWidget(self.clear_btn)
        control_panel.addWidget(self.color_btn)
        control_panel.addWidget(self.color_preview)
        control_panel.addWidget(self.save_btn)
        
        if self.available_cameras:
            control_panel.addWidget(self.switch_camera_btn)
        control_panel.addWidget(self.back_btn)
        control_panel.addStretch()
        
        main_layout.addLayout(control_panel)
        
        # Set main layout
        self.setLayout(main_layout)
        
        # Connect signals
        self.mouse_btn.clicked.connect(self.enable_mouse_mode)
        self.mouse_erase_btn.clicked.connect(self.enable_mouse_erase_mode)
        self.gesture_btn.clicked.connect(self.enable_gesture_mode)
        self.clear_btn.clicked.connect(self.clear_canvas)
        self.save_btn.clicked.connect(self.save_canvas)
        self.color_btn.clicked.connect(self.pick_color)
        self.back_btn.clicked.connect(self.back_button_click)
        self.switch_camera_btn.clicked.connect(self.switch_camera)
        
        
        
        # Load saved settings
        saved_color = self.db.get_setting('last_color')
        if saved_color:
            r, g, b = eval(saved_color)
            self.canvas.change_color((r, g, b))
            self.color_preview.setStyleSheet(f"""
                QLabel {{
                    background-color: rgb({r},{g},{b});
                    border-radius: 16px;
                    border: 2px solid #c7d2fe;
                }}
            """)
        
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera_feed)
        self.timer.start(33)  # ~30 FPS
        
        
        
        undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        undo_shortcut.setContext(Qt.ApplicationShortcut)  
        undo_shortcut.activated.connect(self.perform_undo)
                
    def perform_undo(self):
        self.canvas.undo()            
        self.canvas_widget.update()
        
        
        
    def enable_mouse_erase_mode(self):
        self.mode = "mouse"
        self.canvas_widget.mouse_mode = "erase"
        
        
        if self.capture is not None:
            self.capture.release()
            self.capture = None
        
        
        self.canvas_widget.current_display_canvas = None
        self.canvas_widget.update()
        
        print("[MODE] Mouse Erase Enabled")
    
        
    
    def update_camera_feed(self):
        if self.mode != "gesture":
            return

        ret, frame = self.capture.read()
        if not ret:
            print("❌ Could not access the webcam.")
            return

     
            
        if ret:
            frame = cv2.flip(frame, 1)
            frame, result = self.hand_tracker.detect_hands(frame)

            if result.multi_hand_landmarks:
               
                landmarks = result.multi_hand_landmarks[0]
                gesture = self.hand_tracker.recognize_gesture(landmarks)
                
               
                index_tip = landmarks.landmark[8]
                self.canvas.set_cursor_position(index_tip.x, index_tip.y)
                
                self.handle_gesture(gesture, landmarks)
                
            if not hasattr(self, "_frame_counter"):
                self._frame_counter = 0
            self._frame_counter += 1
            if self._frame_counter % 3 == 0:  
                canvas_with_cursor = self.canvas.draw_cursor()
                self.canvas_widget.update_canvas(canvas_with_cursor)    

            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_BGR888)
            pixmap = QPixmap.fromImage(q_img)
            self.camera_feed_label.setPixmap(pixmap)
            
            
            
            
            
            
    def handle_gesture(self, gesture, landmarks, smoothed_tip=None):
        index_tip = landmarks.landmark[8]
        middle_tip = landmarks.landmark[12]
        ring_tip = landmarks.landmark[16]
        pinky_tip = landmarks.landmark[20]
        
        if not hasattr(self, "_clear_frames"):
            self._clear_frames = 0
            self._last_clear_time = 0
        
        if not hasattr(self, "_color_pick_active"):
            self._color_pick_active = False
            self._color_pick_frames = 0  
            self._last_color_pick_time = 0  

        if gesture == "clear":
            self._clear_frames += 1
            current_time = time.time()
            time_since_last = current_time - self._last_clear_time
                
            if self._clear_frames >= 30 and time_since_last > 3.0:
                self._clear_frames = 0
                self._last_clear_time = current_time
                print("[GESTURE] Canvas cleared with thumbs up gesture 👍")
                self.clear_canvas()  # Clear the canvas
            return
        else:
            self._clear_frames = 0
        
        if gesture == "erase":
            midpoint = (
                (index_tip.x + middle_tip.x) / 2,
                (index_tip.y + middle_tip.y) / 2
            )
            offsets = [
                (0, 0),
                (0.01, 0), (-0.01, 0),
                (0, 0.01), (0, -0.01)
            ]
            for dx, dy in offsets:
                erase_point = (midpoint[0] + dx, midpoint[1] + dy)
                self.canvas.erase(erase_point)
            self.canvas.reset_previous_points()
            return

        elif gesture == "drawing":
            self.canvas.draw((index_tip.x, index_tip.y))
        
        elif gesture == "idle":
            self.canvas.reset_previous_points()

            
            

        
    def back_button_click(self):
        if self.capture is not None:
            self.capture.release()  # Release the camera
        if hasattr(self, 'timer'):
            self.timer.stop()  # Stop the timer
        self.close()  # Close the current screen
        from start_screen import StartScreen
        self.start_screen = StartScreen()  
        self.start_screen.show()


    def enable_mouse_mode(self):
        self.mode = "mouse"
        self.canvas_widget.mouse_mode = "draw"
        
        if self.capture is not None:
            self.capture.release()
            self.capture = None
        
        self.canvas_widget.current_display_canvas = None
        self.canvas_widget.update()
        
        print("[MODE] Mouse Drawing Enabled")

    def enable_gesture_mode(self):
        """Enable gesture mode with improved camera handling"""
        self.mode = "gesture"
        
        if self.capture is not None:
            self.capture.release()
            self.capture = None
        
        try:
            self.capture = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
            
            if not self.capture.isOpened():
                raise Exception("Failed to open camera")
                
            ret, _ = self.capture.read()
            if not ret:
                raise Exception("Failed to read from camera")
                
            self.canvas.reset_previous_points()
            print(f"[MODE] Gesture Drawing Enabled (Camera {self.camera_index})")
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize camera: {e}")
            available_cameras = self.find_available_cameras()
            if available_cameras and self.camera_index in available_cameras:
                next_index = (available_cameras.index(self.camera_index) + 1) % len(available_cameras)
                self.camera_index = available_cameras[next_index]
                print(f"[CAMERA] Switching to camera index {self.camera_index}")
                self.enable_gesture_mode()  # Try again with new camera
            else:
                print("[ERROR] No working cameras found")
                self.mode = "mouse"  # Fall back to mouse mode
                self.canvas_widget.mouse_mode = "draw"
        
    def find_available_cameras(self, max_index=2):
        """Find all available camera indices with better error handling"""
        available_indices = []
        for idx in range(max_index + 1):
            try:
                cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
                if cap.isOpened():
                    ret, _ = cap.read()
                    if ret:
                        available_indices.append(idx)
                cap.release()
            except Exception as e:
                print(f"[WARNING] Error checking camera {idx}: {e}")
                continue
        return available_indices
        
    def switch_camera(self):
        """Switch to the next available camera within a fixed range (0-2)"""
        if self.mode != "gesture":
            self.enable_gesture_mode()
            return
            
        max_camera_index = 2
        next_index = (self.camera_index + 1) % (max_camera_index + 1)
        
        if self.capture is not None:
            self.capture.release()
            self.capture = None
            
        try:
            self.capture = cv2.VideoCapture(next_index, cv2.CAP_DSHOW)
            
            if self.capture.isOpened():
                ret, _ = self.capture.read()
                if ret:
                    self.camera_index = next_index
                    print(f"[CAMERA] Switched to camera index {self.camera_index}")
                    self.db.save_setting('camera_index', str(self.camera_index))
                    return
                    
            raise Exception("Failed to initialize camera")
            
        except Exception as e:
            print(f"[ERROR] Failed to switch to camera {next_index}: {e}")
            self.camera_index = next_index
            self.capture = None
            
            remaining_attempts = max_camera_index
            while remaining_attempts > 0:
                try:
                    next_index = (next_index + 1) % (max_camera_index + 1)
                    self.capture = cv2.VideoCapture(next_index, cv2.CAP_DSHOW)
                    if self.capture.isOpened():
                        ret, _ = self.capture.read()
                        if ret:
                            self.camera_index = next_index
                            print(f"[CAMERA] Switched to camera index {self.camera_index}")
                            self.db.save_setting('camera_index', str(self.camera_index))
                            return
                    self.capture = None
                except Exception as e:
                    print(f"[ERROR] Failed to switch to camera {next_index}: {e}")
                remaining_attempts -= 1
                
            print("[ERROR] No working cameras found")
            self.mode = "mouse"
            self.canvas_widget.mouse_mode = "draw"

    def clear_canvas(self):
        self.canvas.clear()
        self.canvas_widget.update()

    def save_canvas(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(
            self, 
            "Save Drawing", 
            "", 
            "PNG Files (*.png)", 
            options=options
        )
        if fileName:
            if not fileName.endswith('.png'):
                fileName += '.png'
            self.canvas.save(fileName)
            # Save to database
            self.db.save_drawing(
                filename=fileName,
                color=self.canvas.color,
                mode=self.mode
            )

    def pick_color(self):
        """Handle color selection with preview"""
        color = QColorDialog.getColor()
        if color.isValid():
            r, g, b = color.red(), color.green(), color.blue()
            self.canvas.change_color((r, g, b))
            
            self.color_preview.setStyleSheet(f"""
                QLabel {{
                    background-color: {color.name()};
                    border-radius: 16px;
                    border: 2px solid #c7d2fe;
                }}
            """)
            
            self.db.save_setting('last_color', str((r, g, b)))