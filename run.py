#!/usr/bin/env python3
from workout_tracker import WorkoutTracker

def main():
    print("Workout Tracker")
    tracker = WorkoutTracker()
    
    while True:
        try:
            exercise = input("\nEnter your workout (or 'quit' to exit): ")
            if exercise.lower() == 'quit':
                break
                
            tracker.process_workout(exercise)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()