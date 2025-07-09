import os
from dotenv import load_dotenv
from typing import Final

load_dotenv()

class Config:
    """Configuration class for workout tracker"""
    
    # API Configuration
    NUTRITIONIX_ENDPOINT: Final[str] = "https://trackapi.nutritionix.com/v2/natural/exercise"
    NUTRITIONIX_APP_ID: Final[str] = os.getenv("NUTRITIONIX_APP_ID", "")
    NUTRITIONIX_API_KEY: Final[str] = os.getenv("NUTRITIONIX_API_KEY", "")
    
    # User Profile
    GENDER: Final[str] = os.getenv("GENDER", "male")
    HEIGHT_CM: Final[float] = float(os.getenv("HEIGHT_CM", 175.0))
    WEIGHT_KG: Final[float] = float(os.getenv("WEIGHT_KG", 70.0))
    AGE: Final[int] = int(os.getenv("AGE", 25))
    
    # Data Storage
    CSV_FILENAME: Final[str] = "workout_log.csv"
    LOG_FILENAME: Final[str] = "workout_tracker.log"