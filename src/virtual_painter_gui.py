from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QFileDialog, QColorDialog, QShortcut, QToolButton
from PyQt5.QtGui import QImage, QPixmap, QFont, QKeySequence, QIcon, QColor
from PyQt5.QtCore import QTimer, Qt
import cv2
import time
from canvas import Canvas
from canvas_widget import CanvasWidget
from hand_tracking import HandTracker
from database import Database

class VirtualPainterGUI(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize database
        self.db = Database("virtual_painter.db")
        
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
        self.setWindowIcon(QIcon('virtual_painter.png'))
        
        # Initialize camera variables
        self.available_cameras = self.find_available_cameras(max_index=4)
        
        if self.available_cameras:
            # Load last used camera index from database if available
            saved_camera_index = self.db.get_setting('camera_index')
            
            if saved_camera_index and int(saved_camera_index) in self.available_cameras:
                self.camera_index = int(saved_camera_index)
            else:
                self.camera_index = self.available_cameras[0]
                
            self.capture = cv2.VideoCapture(self.camera_index)
            print(f"[CAMERA] Using camera index {self.camera_index}")
        else:
            self.capture = None
            self.camera_index = 0
            print("No camera found.")
        
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
        
        # Camera switch button with circular icon
        self.switch_camera_btn = QToolButton()
        self.switch_camera_btn.setText("📷")
        self.switch_camera_btn.setToolTip("Switch to next camera")
        self.switch_camera_btn.setFixedSize(40, 40)  # Fixed circular size
        
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
            
        # Special style for circular camera button
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
        
        # Add stretch to center buttons
        control_panel.addStretch()
        control_panel.addWidget(self.mouse_btn)
        control_panel.insertWidget(2, self.mouse_erase_btn)
        control_panel.addWidget(self.gesture_btn)
        control_panel.addWidget(self.clear_btn)
        control_panel.addWidget(self.color_btn)
        control_panel.addWidget(self.color_preview)
        control_panel.addWidget(self.save_btn)
        # Only show the camera button if there are cameras available
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
        
        # Initialize webcam timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera_feed)
        self.timer.start(33)  # ~30 FPS
        
        
        
        undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        undo_shortcut.setContext(Qt.ApplicationShortcut)  # ✅ Global shortcut context
        undo_shortcut.activated.connect(self.perform_undo)
                
    def perform_undo(self):
        self.canvas.undo()            
        self.canvas_widget.update()
        
        
        
    def enable_mouse_erase_mode(self):
        self.mode = "mouse"
        self.canvas_widget.mouse_mode = "erase"
        
        # Stop the camera feed if it's running
        if self.capture is not None:
            self.capture.release()
            self.capture = None
        
        # Clear any cursor display and revert to standard canvas display
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

        # Remove debug prints to reduce overhead
        # print("Camera working?", ret)
        # print("[INFO] Camera frame captured.")
            
        if ret:
            frame = cv2.flip(frame, 1)
            frame, result = self.hand_tracker.detect_hands(frame)

            if result.multi_hand_landmarks:
                # Remove debug print
                # print("[INFO] Hand detected.")
                landmarks = result.multi_hand_landmarks[0]
                gesture = self.hand_tracker.recognize_gesture(landmarks)
                
                # Update cursor position to track index finger tip
                index_tip = landmarks.landmark[8]
                self.canvas.set_cursor_position(index_tip.x, index_tip.y)
                
                self.handle_gesture(gesture, landmarks)
                
            # Optimize canvas update frequency
            if not hasattr(self, "_frame_counter"):
                self._frame_counter = 0
            self._frame_counter += 1
            if self._frame_counter % 3 == 0:  # Increase update rate to ~20 FPS
                # Get canvas with cursor for display only in gesture mode
                canvas_with_cursor = self.canvas.draw_cursor()
                self.canvas_widget.update_canvas(canvas_with_cursor)    

            # Convert the frame to a format suitable for displaying in PyQt
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
        
        # Track if we're holding the color picking gesture
        if not hasattr(self, "_color_pick_active"):
            self._color_pick_active = False
            self._color_pick_frames = 0  # Count frames to avoid accidental triggers
            self._last_color_pick_time = 0  # Timestamp of last color pick
        
        # 👍 Color Pick Mode: Thumbs up gesture
        if gesture == "color_pick":
            self._color_pick_frames += 1
            
            # Get current time for throttling
            current_time = time.time()
            time_since_last = current_time - self._last_color_pick_time
            
            # Only trigger after holding gesture for 20 frames (about 0.7 seconds)
            # And make sure we haven't triggered color picker in the last 3 seconds
            if self._color_pick_frames >= 20 and time_since_last > 3.0 and not self._color_pick_active:
                self._color_pick_active = True
                self._color_pick_frames = 0
                self._last_color_pick_time = current_time
                
                # Show a visual feedback that color picker is activated
                print("[GESTURE] Color picker activated with thumbs up gesture 👍")
                
                # Call color picker in a non-blocking way
                QTimer.singleShot(100, self.pick_color)
            return
        else:
            # Reset color pick tracking when not in color pick gesture
            self._color_pick_active = False
            self._color_pick_frames = 0
        
        # ✌️ Erase Mode: Index and middle fingers up
        if gesture == "erase":
            midpoint = (
                (index_tip.x + middle_tip.x) / 2,
                (index_tip.y + middle_tip.y) / 2
            )
            # Reduce number of erase points for better performance
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

        # ☝️ Draw Mode: Only index finger up
        elif gesture == "drawing":
            self.canvas.draw((index_tip.x, index_tip.y))
        
        # 💤 Idle Mode: No finger action
        elif gesture == "idle":
            self.canvas.reset_previous_points()

            
            

        
    def back_button_click(self):
        if self.capture is not None:
            self.capture.release()  # Release the camera
        if hasattr(self, 'timer'):
            self.timer.stop()  # Stop the timer
        self.close()  # Close the current screen
        from start_screen import StartScreen
        self.start_screen = StartScreen()  # Go back to the start screen
        self.start_screen.show()


    def enable_mouse_mode(self):
        self.mode = "mouse"
        self.canvas_widget.mouse_mode = "draw"
        
        # Stop the camera feed if it's running
        if self.capture is not None:
            self.capture.release()
            self.capture = None
        
        # Clear any cursor display and revert to standard canvas display
        self.canvas_widget.current_display_canvas = None
        self.canvas_widget.update()
        
        print("[MODE] Mouse Drawing Enabled")

    def enable_gesture_mode(self):
        self.mode = "gesture"
        if self.capture is not None:
            self.capture.release()
        
        # Start the webcam with the current camera index
        self.capture = cv2.VideoCapture(self.camera_index)
        
        # Reset canvas drawing points for clean state
        self.canvas.reset_previous_points()
        
        print("[MODE] Gesture Drawing Enabled")
        
    def find_available_cameras(self, max_index=4):
        """Find all available camera indices"""
        available_indices = []
        for idx in range(max_index + 1):
            cap = cv2.VideoCapture(idx)
            if cap.isOpened():
                available_indices.append(idx)
                cap.release()
        return available_indices
        
    def switch_camera(self):
        """Switch to the next available camera"""
        if self.mode != "gesture":
            # Enable gesture mode first if we're not in it
            self.enable_gesture_mode()
            return
            
        # Try the next camera index (0-4)
        next_index = (self.camera_index + 1) % 5
        
        # Release current camera
        if self.capture is not None:
            self.capture.release()
            
        # Try to open the next camera
        self.capture = cv2.VideoCapture(next_index)
        
        # Check if camera opened successfully
        if self.capture.isOpened():
            self.camera_index = next_index
            # Add the new index to available cameras if not already there
            if next_index not in self.available_cameras:
                self.available_cameras.append(next_index)
            print(f"[CAMERA] Switched to camera index {self.camera_index}")
        else:
            # If camera failed to open, try the next one recursively
            self.camera_index = next_index  # Set this so we don't get stuck
            self.switch_camera()
            return
        
        # Save camera index to database
        self.db.save_setting('camera_index', str(self.camera_index))

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
            # Convert to BGR for OpenCV
            r, g, b = color.red(), color.green(), color.blue()
            self.canvas.change_color((r, g, b))
            
            # Update preview
            self.color_preview.setStyleSheet(f"""
                QLabel {{
                    background-color: {color.name()};
                    border-radius: 16px;
                    border: 2px solid #c7d2fe;
                }}
            """)
            
            # Save color to database
            self.db.save_setting('last_color', str((r, g, b)))
            
           

            
            
            
            
            
            
            
            
            