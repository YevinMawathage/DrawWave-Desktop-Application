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
        finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky tips
        finger_pips = [6, 10, 14, 18]  # Corresponding pip (middle) joints

        # Check if thumb is up (using the Y position relative to other joints)
        thumb_tip = landmarks.landmark[4]  # Thumb tip
        thumb_cmc = landmarks.landmark[1]  # Thumb CMC joint (base)
        
        # Thumb is up when the tip is significantly higher (lower Y) than the base
        # In camera coordinates, lower Y means higher position (top of screen is Y=0)
        thumb_up = (thumb_cmc.y - thumb_tip.y) > 0.1

        # Check which fingers are extended
        fingers_up = []
        for tip_idx, pip_idx in zip(finger_tips, finger_pips):
            tip_y = landmarks.landmark[tip_idx].y
            pip_y = landmarks.landmark[pip_idx].y
            fingers_up.append(tip_y < pip_y)  # True if finger is extended

        index_up, middle_up, ring_up, pinky_up = fingers_up
        
        # Color picking gesture: thumbs up, other fingers down (making a "👍" sign)
        if thumb_up and not any(fingers_up):
            return "clear"
        # Erase gesture: index and middle fingers up (making a "✌" sign)
        elif index_up and middle_up and not ring_up and not pinky_up:
            return "erase"
        # Drawing gesture: only index finger up (pointing "👆")
        elif index_up and not middle_up and not ring_up and not pinky_up:
            return "drawing"
        # Idle gesture: any other configuration
        else:
            return "idle"
