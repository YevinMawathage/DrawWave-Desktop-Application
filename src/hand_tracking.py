import mediapipe as mp
import cv2
from collections import deque

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.tip_history = deque(maxlen=5)  # For smoothing index fingertip
        
        
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
    # Finger tip and pip landmark indices
        finger_tips = [8, 12, 16, 20]
        finger_pips = [6, 10, 14, 18]

        fingers_up = []
        for tip_idx, pip_idx in zip(finger_tips, finger_pips):
            tip_y = landmarks.landmark[tip_idx].y
            pip_y = landmarks.landmark[pip_idx].y
            fingers_up.append(tip_y < pip_y)  # True if finger is extended

        index_up, middle_up, ring_up, pinky_up = fingers_up

        if index_up and middle_up and not ring_up and not pinky_up:
            return "erase"
        elif index_up and not middle_up and not ring_up and not pinky_up:
            return "drawing"
        else:
            return "idle"
