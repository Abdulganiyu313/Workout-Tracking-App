import unittest
from unittest.mock import patch, MagicMock
from workout_tracker.tracker import WorkoutTracker
from datetime import datetime

class TestWorkoutTracker(unittest.TestCase):
    @patch('requests.Session')
    def test_get_exercise_data(self, mock_session):
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "exercises": [{"name": "running", "duration_min": 30, "nf_calories": 300}]
        }
        mock_session.return_value.post.return_value = mock_response
        
        # Test
        tracker = WorkoutTracker()
        result = tracker.get_exercise_data("ran 3 miles")
        
        # Assertions
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "running")

    @patch('builtins.open')
    def test_log_workout(self, mock_open):
        tracker = WorkoutTracker()
        workout = {
            "date": "01/01/2023",
            "time": "12:00:00",
            "exercise": "Test",
            "duration": 10,
            "calories": 100
        }
        self.assertTrue(tracker.log_workout(workout))