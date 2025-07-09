import pandas as pd
from typing import Optional
from .config import Config

def generate_report() -> Optional[pd.DataFrame]:
    """Generate workout summary report"""
    try:
        df = pd.read_csv(Config.CSV_FILENAME)
        return df.groupby('Exercise').agg({
            'Duration (min)': 'sum',
            'Calories': 'sum'
        }).sort_values('Duration (min)', ascending=False)
    except Exception as e:
        print(f"Error generating report: {e}")
        return None