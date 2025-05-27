import unittest
from collections import namedtuple
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from hand_tracking import HandTracker

MockLandmark = namedtuple('MockLandmark', ['x', 'y'])

class MockLandmarkList:
    def __init__(self, values):
        self.landmark = values

class TestGestureRecognition(unittest.TestCase):
    def setUp(self):
        self.tracker = HandTracker()

    def test_drawing_gesture(self):
        # Only index finger up
        landmarks = [MockLandmark(0.0, 0.9)] * 21
        landmarks[8] = MockLandmark(0.5, 0.4)   
        landmarks[6] = MockLandmark(0.5, 0.5)   
        landmarks[12] = MockLandmark(0.5, 0.6)  
        landmarks[10] = MockLandmark(0.5, 0.5)  
        landmarks[16] = MockLandmark(0.5, 0.6)
        landmarks[14] = MockLandmark(0.5, 0.5)
        landmarks[20] = MockLandmark(0.5, 0.6)
        landmarks[18] = MockLandmark(0.5, 0.5)

        mock_input = MockLandmarkList(landmarks)
        self.assertEqual(self.tracker.recognize_gesture(mock_input), "drawing")

    def test_erase_gesture(self):
        # Index + middle up
        landmarks = [MockLandmark(0.0, 0.9)] * 21
        landmarks[8] = MockLandmark(0.5, 0.4)   
        landmarks[6] = MockLandmark(0.5, 0.5)
        landmarks[12] = MockLandmark(0.5, 0.4)  
        landmarks[10] = MockLandmark(0.5, 0.5)
        # Others down
        landmarks[16] = MockLandmark(0.5, 0.6)
        landmarks[14] = MockLandmark(0.5, 0.5)
        landmarks[20] = MockLandmark(0.5, 0.6)
        landmarks[18] = MockLandmark(0.5, 0.5)

        mock_input = MockLandmarkList(landmarks)
        self.assertEqual(self.tracker.recognize_gesture(mock_input), "erase")

    def test_idle_gesture(self):
        # All fingers down
        landmarks = [MockLandmark(0.0, 0.6)] * 21
        landmarks[6] = MockLandmark(0.0, 0.5)  
        landmarks[10] = MockLandmark(0.0, 0.5)
        landmarks[14] = MockLandmark(0.0, 0.5)
        landmarks[18] = MockLandmark(0.0, 0.5)

        mock_input = MockLandmarkList(landmarks)
        self.assertEqual(self.tracker.recognize_gesture(mock_input), "idle")
