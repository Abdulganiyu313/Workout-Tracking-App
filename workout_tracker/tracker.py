import csv
import logging
from datetime import datetime
from typing import List, Dict, Optional
import requests
from .config import Config

class WorkoutTracker:
    """Main class for tracking workouts"""
    
    def __init__(self):
        self.config = Config()
        self._setup_logging()
        self.session = requests.Session()
        self.session.headers.update({
            "x-app-id": self.config.NUTRITIONIX_APP_ID,
            "x-app-key": self.config.NUTRITIONIX_API_KEY,
            "Content-Type": "application/json"
        })

    def _setup_logging(self):
        """Configure logging system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config.LOG_FILENAME),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_exercise_data(self, exercise_text: str) -> Optional[List[Dict]]:
        """Fetch exercise data from Nutritionix API"""
        try:
            params = {
                "query": exercise_text,
                "gender": self.config.GENDER,
                "weight_kg": self.config.WEIGHT_KG,
                "height_cm": self.config.HEIGHT_CM,
                "age": self.config.AGE
            }
            
            response = self.session.post(
                self.config.NUTRITIONIX_ENDPOINT,
                json=params
            )
            response.raise_for_status()
            return response.json().get("exercises", [])
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            return None

    def log_workout(self, exercise_data: Dict) -> bool:
        """Log workout to CSV file"""
        try:
            # Create file if not exists
            try:
                with open(self.config.CSV_FILENAME, 'x', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Date", "Time", "Exercise", "Duration (min)", "Calories"])
            except FileExistsError:
                pass
            
            # Append workout
            with open(self.config.CSV_FILENAME, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    exercise_data["date"],
                    exercise_data["time"],
                    exercise_data["exercise"],
                    exercise_data["duration"],
                    exercise_data["calories"]
                ])
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to log workout: {e}")
            return False

    def process_workout(self, exercise_text: str) -> bool:
        """Main method to process workout input"""
        exercises = self.get_exercise_data(exercise_text)
        if not exercises:
            self.logger.warning("No exercise data received")
            return False

        now = datetime.now()
        current_date = now.strftime("%d/%m/%Y")
        current_time = now.strftime("%H:%M:%S")

        success = True
        for exercise in exercises:
            workout = {
                "date": current_date,
                "time": current_time,
                "exercise": exercise["name"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"]
            }
            
            if not self.log_workout(workout):
                success = False
                continue
                
            self.logger.info(
                f"Logged {workout['exercise']}: "
                f"{workout['duration']} min, {workout['calories']} cal"
            )
        
        return success