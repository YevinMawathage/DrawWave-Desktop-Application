import mediapipe as mp
import cv2
from collections import deque

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=0,  
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.tip_history = deque(maxlen=3)  
        self._cached_landmarks = None
        self._last_gesture = None
        
        
    def get_smoothed_tip(self, tip):
        self.tip_history.append((tip.x, tip.y))
        avg_x = sum(p[0] for p in self.tip_history) / len(self.tip_history)
        avg_y = sum(p[1] for p in self.tip_history) / len(self.tip_history)
        return (avg_x, avg_y)
        

    def detect_hands(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = self.hands.process(image_rgb)
        if result.multi_hand_landmarks:
            for landmarks in result.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(image, landmarks, self.mp_hands.HAND_CONNECTIONS)
        return image, result

    def recognize_gesture(self, landmarks):
      
        if landmarks == self._cached_landmarks and self._last_gesture:
            return self._last_gesture

        import numpy as np
        
        positions = np.array([[lm.x, lm.y] for lm in landmarks.landmark])
        
        thumb_up = (positions[1][1] - positions[4][1]) > 0.1
        
        tips = positions[[8, 12, 16, 20]]
        pips = positions[[6, 10, 14, 18]]
        fingers_up = tips[:, 1] < pips[:, 1]
        
        if thumb_up and not np.any(fingers_up):
            gesture = "clear"
        elif fingers_up[0] and fingers_up[1] and not fingers_up[2] and not fingers_up[3]:
            gesture = "erase"
        elif fingers_up[0] and not np.any(fingers_up[1:]):
            gesture = "drawing"
        else:
            gesture = "idle"
            
        self._cached_landmarks = landmarks
        self._last_gesture = gesture
        return gesture
