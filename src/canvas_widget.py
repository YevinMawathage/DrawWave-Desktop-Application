from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QImage, QMouseEvent
from PyQt5.QtCore import Qt

class CanvasWidget(QWidget):
    def __init__(self, canvas, parent=None):
        super().__init__(parent)
        self.canvas = canvas
        self.drawing = False
        self.last_pos = None
        self.mouse_mode = "erase"
        self.current_display_canvas = None

    def set_drawing(self, status):
        self.drawing = status

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Use the canvas with cursor if available, otherwise use the normal canvas
        canvas_data = self.current_display_canvas if self.current_display_canvas is not None else self.canvas.get_canvas()
        
        canvas_image = QImage(canvas_data.data,
                              self.canvas.width,
                              self.canvas.height,
                              self.canvas.width * 3,
                              QImage.Format_RGB888)
        painter.drawImage(0, 0, canvas_image)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.parent().mode == "mouse":
            self.drawing = True
            self.last_pos = event.pos()
            self.canvas.reset_previous_points()
            self._perform_action(event)
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drawing and self.parent().mode == "mouse":
            current_pos = event.pos()
            self._perform_action(event)
            self.last_pos = current_pos
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            self.last_pos = None
            
    def update_canvas(self, canvas_data):
        """Update the canvas with the provided canvas data (with cursor)"""
        self.current_display_canvas = canvas_data
        self.update()

    
    def _perform_action(self, event):
        # Convert mouse coordinates to normalized canvas coordinates
        norm_x = max(0, min(1, event.x() / self.canvas.width))
        norm_y = max(0, min(1, event.y() / self.canvas.height))
        
        if self.mouse_mode == "draw":
            self.canvas.draw((norm_x, norm_y))
        elif self.mouse_mode == "erase":
            self.canvas.erase((norm_x, norm_y))