import cv2
import numpy as np
from PIL import Image
from database import Database

class Canvas:
    def __init__(self, width=640, height=480, db=None):
        self.width = width
        self.height = height
        self.canvas = np.ones((height, width, 3), dtype=np.uint8) * 255
        self.previous_point_gesture = None
        self.previous_point_erase = None
        self.brush_size = 10
        self.color = (0, 0, 0)
        self.history = []
        self.redo_stack = []
        self.cursor_position = (0, 0)
        self.history_limit = 1  # Added limit to history stack
        self.db = db
        
    def set_cursor_position(self, x, y):
        self.cursor_position = (int(x * self.width), int(y * self.height))

    def draw_cursor(self):
        cursor_radius = 5
        temp_canvas = self.canvas.copy()  # Draw cursor on a temporary copy
        cv2.circle(temp_canvas, self.cursor_position, cursor_radius, (255, 0, 0), -1)
        return temp_canvas  # Return for display without saving to history


    def draw(self, current_point, color=None):
        current_point = (int(current_point[0] * self.width), int(current_point[1] * self.height))

        if self.previous_point_gesture is None:
            self.previous_point_gesture = current_point
            return

        if self.previous_point_gesture != current_point:
            cv2.line(self.canvas, self.previous_point_gesture, current_point, self.color, self.brush_size)

            # ✅ Save to DB
            if self.db:
                self.db.save_action("draw", [self.previous_point_gesture, current_point], self.color)

            self.history.append(self.canvas.copy())
            self.redo_stack.clear()
            self.previous_point_gesture = current_point
    


    def erase(self, current_point):
        current_point = (int(current_point[0] * self.width), int(current_point[1] * self.height))

        if self.previous_point_erase is None:
            self.previous_point_erase = current_point

        if self.previous_point_erase != current_point:
            cv2.line(self.canvas, self.previous_point_erase, current_point, (255, 255, 255), self.brush_size + 10)

            # ✅ Save erase to DB
            if self.db:
                self.db.save_action("erase", [self.previous_point_erase, current_point], (255, 255, 255))

            self.history.append(self.canvas.copy())
            self.redo_stack.clear()
            self.previous_point_erase = current_point
        


    def reset_previous_points(self):
        self.previous_point_gesture = None
        self.previous_point_erase = None

    def change_color(self, new_color):
        self.color = tuple(new_color[:3])

    def change_brush_size(self, new_size):
        self.brush_size = new_size

    def save(self, file_path):
        image = Image.fromarray(self.canvas)
        image.save(file_path)

        
    def clear(self):
        self.canvas = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255
        self.history = []
        self.redo_stack = []
        self.reset_previous_points()
        
    def save(self, file_path):
        try:
            image = Image.fromarray(self.canvas)
            image.save(file_path)
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
        
        
    def undo(self):
        if self.db:
            action = self.db.undo_last_action()
            if action:
                self.redraw_from_history()

    def redraw_from_history(self):
        self.canvas = np.ones((self.height, self.width, 3), dtype=np.uint8) * 255
        self.history.clear()
        self.redo_stack.clear()

        actions = self.db.get_all_actions()
        for act in actions:
            if act['action_type'] == 'draw' or act['action_type'] == 'erase':
                pt1, pt2 = act['points']
                color = tuple(act['color']) if act['color'] else (255, 255, 255)
                cv2.line(self.canvas,
                        (int(pt1[0]), int(pt1[1])),
                        (int(pt2[0]), int(pt2[1])),
                        color,
                        self.brush_size if act['action_type'] == 'draw' else self.brush_size + 10)
                self.history.append(self.canvas.copy())
        

    def get_canvas(self):
        return self.canvas
