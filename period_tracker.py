import csv
from datetime import datetime, timedelta

class PeriodTracker:
    def __init__(self, cycle_length=None, menstrual_length=None, filename="periods.csv"):
        """
        initializes the PeriodTracker with the cycle length, menstrual length, and last period date.
        cycle_length and menstrual_length are input by the user or default to normal settings.
        """
        self.filename = filename
        
        # cycle_length and menstrual_length are not provided, this uses default values
        self.cycle_length = cycle_length or 28  # default cycle length is 28 days
        self.menstrual_length = menstrual_length or 5  # default menstrual length is 5 days
        
        self.last_period_start_date = self.load_last_period_date()

    def load_last_period_date(self):
        """Load the last period start date from a CSV file."""
        try:
            with open(self.filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    return datetime.strptime(row["last_period_start_date"], "%Y-%m-%d").date()
        except FileNotFoundError:
            # Create the file if it doesn't exist
            with open(self.filename, mode='w', newline='') as file:
                fieldnames = ["last_period_start_date"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
            return None
        except Exception as e:
            print(f"Error loading last period date: {e}")
            return None

    def save_last_period_date(self, date):
        """Save the last period start date to a CSV file."""
        try:
            with open(self.filename, mode='w', newline='') as file:
                fieldnames = ["last_period_start_date"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({"last_period_start_date": date.strftime("%Y-%m-%d")})
        except Exception as e:
            print(f"Error saving last period date: {e}")

    def predict_next_period(self):
        """Predict the next period start date based on the current cycle length."""
        if not self.last_period_start_date:
            return None
        return self.last_period_start_date + timedelta(days=self.cycle_length)

    def update_last_period_start_date(self, date):
        """Update the last period start date and save it."""
        self.last_period_start_date = date
        self.save_last_period_date(date)

    def get_current_phase(self, current_date):
        """
        Determines the current phase of the menstrual cycle based on the current date and last period start date.
        The phases are:
        - Menstrual Phase
        - Follicular Phase
        - Ovulation Phase
        - Luteal Phase
        """
        if not self.last_period_start_date:
            return "No last period date set."

        # to calculate the number of days passed since the last period
        days_since_last_period = (current_date - self.last_period_start_date).days

        # this defines phase end days based on cycle length and menstrual length
        menstrual_end = self.menstrual_length
        follicular_end = menstrual_end + (self.cycle_length // 2)  # Roughly half the cycle
        ovulation_end = follicular_end + 1  # Ovulation phase lasts 1 day
        luteal_end = ovulation_end + (self.cycle_length - (menstrual_end + follicular_end + 1))

        # to know which phase the current date falls into
        if days_since_last_period < menstrual_end:
            return "Menstrual Phase"
        elif days_since_last_period < follicular_end:
            return "Follicular Phase"
        elif days_since_last_period < ovulation_end:
            return "Ovulation Phase"
        elif days_since_last_period < luteal_end:
            return "Luteal Phase"
        else:
            return "Cycle has reset or invalid date"
