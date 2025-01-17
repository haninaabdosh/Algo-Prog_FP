import csv
import matplotlib.pyplot as plt
from datetime import datetime

class MedicationTracker:
    # Initialize with a filename and load existing medications
    def __init__(self, filename="medications.csv"):
        self.filename = filename
        self.medications = self.load_medications()  # Load medications when the object is created

    # Load medications from the file, create file if not found
    def load_medications(self):
        try:
            with open(self.filename, mode='r') as file:
                reader = csv.DictReader(file)
                return [row for row in reader]
        except FileNotFoundError:
            with open(self.filename, mode='w', newline='') as file:
                fieldnames = ["name", "dosage", "frequency", "start_date", "end_date", "last_taken"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
            return []

    # Save medications to the file
    def save_medications(self):
        try:
            with open(self.filename, mode='w', newline='') as file:
                fieldnames = ["name", "dosage", "frequency", "start_date", "end_date", "last_taken"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.medications)
        except Exception as e:
            print(f"Error saving medications: {e}")

    # to add a new medication and save to the file
    def add_medication(self, name, dosage, frequency, start_date, end_date):
        self.medications.append({
            "name": name,
            "dosage": dosage,
            "frequency": frequency,
            "start_date": start_date,
            "end_date": end_date,
            "last_taken": ""
        })
        self.save_medications()

    # to mark a specific medication as taken
    def mark_as_taken(self, name):
        today = datetime.now().strftime("%Y-%m-%d")
        for med in self.medications:
            if med["name"] == name:
                med["last_taken"] = today
                self.save_medications()
                print(f"Medication '{name}' marked as taken on {today}.")
                return
        print(f"Medication '{name}' not found.")

    # resets the list of medications
    def reset_medications(self):
        """Clears all medications and updates the file."""
        self.medications = []
        self.save_medications()

    # to generate a scatter plot for medications taken
    def generate_scatter_plot(self):
        taken_dates = []
        medication_names = []

        for med in self.medications:
            if med["last_taken"]:
                taken_dates.append(datetime.strptime(med["last_taken"], "%Y-%m-%d"))
                medication_names.append(med["name"])

        if taken_dates:
            plt.scatter(taken_dates, medication_names)
            plt.xlabel("Date")
            plt.ylabel("Medications")
            plt.title("Scatter Plot of Medications Taken")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        else:
            print("No medications have been marked as taken.")
