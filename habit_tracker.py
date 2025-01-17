import csv
from datetime import datetime

class HabitTracker:
    def __init__(self, filename="habits.csv"):
        self.filename = filename
        self.habits = self.load_habits()  # load habits from the file when the object is created

    def load_habits(self):
        try:
            with open(self.filename, mode='r') as file:
                reader = csv.DictReader(file)
                # check if the 'name' column exists to avoid errors
                if 'name' not in reader.fieldnames:
                    print("error: the csv file does not contain a 'name' column.")
                    return {}
                # map habits by their name for easier access
                habits = {row["name"]: row for row in reader}
                return habits
        except FileNotFoundError:
            # create the file if it doesn't exist
            with open(self.filename, mode='w', newline='') as file:
                fieldnames = ["name", "frequency", "streak", "last_completed"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()  # write the header row
            return {}  # return an empty dictionary if the file is new or doesn't exist

    def save_habits(self):
        try:
            with open(self.filename, mode='w', newline='') as file:
                fieldnames = ["name", "frequency", "streak", "last_completed"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()  # write the header row
                writer.writerows(self.habits.values())  # write all habit data to the file
        except Exception as e:
            print(f"error saving habits: {e}")  # handle errors during save

    def add_habit(self, name, frequency):
        # add a new habit to the habits dictionary
        self.habits[name] = {"name": name, "frequency": frequency, "streak": 0, "last_completed": ""}
        self.save_habits()  # save the updated habits list

    def mark_completed(self, name):
        if name in self.habits:
            habit = self.habits[name]
            last_completed = habit["last_completed"]
            today = datetime.now().date().strftime("%Y-%m-%d")
            if last_completed != today:  # prevent updating if the habit was already marked today
                habit["last_completed"] = today
                habit["streak"] = int(habit["streak"]) + 1  # increment streak
            self.save_habits()  # save after updating
    
    def reset_habits(self):
        self.habits = {}  # clear the habits dictionary
        self.save_habits()  # save the reset state to the file

    def get_habits(self):
        return self.habits  # return the current habits dictionary
