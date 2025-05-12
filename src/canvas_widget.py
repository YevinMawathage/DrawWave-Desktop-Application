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

    def set_drawing(self, status):
        self.drawing = status

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        canvas_image = QImage(self.canvas.get_canvas().data,
                              self.canvas.width,
                              self.canvas.height,
                              self.canvas.width * 3,
                              QImage.Format_RGB888)
        painter.drawImage(0, 0, canvas_image)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and getattr(self.parent(), "mode", "") == "mouse":
            self.drawing = True
            self.last_pos = event.pos()
            self.canvas.reset_previous_points()
            self._perform_action(event)
            self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drawing and getattr(self.parent(), "mode", "") == "mouse":
            current_pos = event.pos()
            self._perform_action(event)
            self.last_pos = current_pos
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            self.last_pos = None

    
    def _perform_action(self, event):
        norm_x = event.x() / self.canvas.width
        norm_y = event.y() / self.canvas.height
        if self.mouse_mode == "draw":
            self.canvas.draw((norm_x, norm_y))
        elif self.mouse_mode == "erase":
            self.canvas.erase((norm_x, norm_y))