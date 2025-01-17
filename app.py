import streamlit as st
import matplotlib.pyplot as plt
from datetime import date, datetime
from habit_tracker import HabitTracker
from medication_tracker import MedicationTracker
from period_tracker import PeriodTracker

# main function to run the app
def main():
    # initialize all trackers
    habit_tracker = HabitTracker()
    medication_tracker = MedicationTracker()
    period_tracker = PeriodTracker()

    st.title("Sama: Habit, Medication, and Period Tracker")

    # Habit Tracker Section
    st.header("Habit Tracker")
    habit_name = st.text_input("Enter habit name")
    habit_frequency = st.selectbox("Select frequency", ["daily", "weekly", "monthly"])

    # Add a new habit
    if st.button("Add habit"):
        if habit_name:
            habit_tracker.add_habit(habit_name, habit_frequency)
            st.success(f"Habit '{habit_name}' added!")

    # Edit an existing habit
    habit_to_edit = st.selectbox(
        "Select habit to edit", list(habit_tracker.habits.keys()) if habit_tracker.habits else ["No habits"]
    )
    new_frequency = st.selectbox("Select new frequency", ["daily", "weekly", "monthly"])
    if st.button("Edit habit"):
        if habit_to_edit != "No habits":
            habit_tracker.habits[habit_to_edit]["frequency"] = new_frequency
            habit_tracker.save_habits()
            st.success(f"Habit '{habit_to_edit}' updated to '{new_frequency}' frequency!")

    # Mark habit as completed
    habit_to_mark = st.selectbox(
        "Select habit to mark as completed", list(habit_tracker.habits.keys()) if habit_tracker.habits else ["No habits"]
    )
    if st.button("Mark completed"):
        if habit_to_mark != "No habits":
            habit_tracker.mark_completed(habit_to_mark)
            st.success(f"Habit '{habit_to_mark}' marked as completed!")

    if st.button("Reset habits"):
        habit_tracker.reset_habits()
        st.success("All habits have been reset!")

    # Plot habit streaks
    plot_habit_streaks(habit_tracker)

    # Medication Tracker Section
    st.header("Medication Tracker")
    medication_name = st.text_input("Enter medication name")
    dose = st.number_input("Enter dose", min_value=1, step=1)
    frequency = st.selectbox("Select frequency", ["daily", "weekly", "as needed"])
    start_date = st.date_input("Start date", value=date.today())
    end_date = st.date_input("End date", value=date.today())

    # Add a new medication
    if st.button("Add medication"):
        if medication_name and dose > 0:
            medication_tracker.add_medication(medication_name, dose, frequency, start_date, end_date)
            st.success(f"Medication '{medication_name}' added!")

    # Mark medication as taken
    if medication_tracker.medications:
        med_to_mark = st.selectbox("Select medication to mark as taken", 
                                  [med["name"] for med in medication_tracker.medications])
        if st.button("Mark as taken"):
            medication_tracker.mark_as_taken(med_to_mark)
            st.success(f"Medication '{med_to_mark}' marked as taken!")

    # Reset medications
    if st.button("Reset medications"):
        medication_tracker.reset_medications()
        st.success("All medications have been reset!")
        st.rerun()

    # Plot medication doses
    plot_medication_doses(medication_tracker)

    # Period Tracker Section
    st.header("Period Tracker")

    cycle_length = st.number_input("Enter cycle length (days)", min_value=21, max_value=35, value=28, step=1)
    menstrual_length = st.number_input("Enter menstrual length (days)", min_value=3, max_value=7, value=5, step=1)

    period_tracker = PeriodTracker(cycle_length=cycle_length, menstrual_length=menstrual_length)

    # input for the last period start date
    last_period_date = st.date_input("Last period start date", value=date.today())
    if st.button("Update last period date"):
        period_tracker.update_last_period_start_date(last_period_date)
        st.success(f"Last period date updated to {last_period_date}")

    # predict and show the next period start date
    next_period = period_tracker.predict_next_period()
    if next_period:
        st.write(f"Next predicted period start date: {next_period}")
    else:
        st.warning("Please set a valid last period date to predict the next period.")

    # current phase
    current_date = date.today()
    current_phase = period_tracker.get_current_phase(current_date)
    st.write(f"Current phase: {current_phase}")

    # cycle phases
    plot_cycle_phases(period_tracker)

# plot habit streaks
def plot_habit_streaks(habit_tracker):
    if not habit_tracker.habits:
        st.warning("No habits to display.")
        return

    habit_names = list(habit_tracker.habits.keys())
    streaks = [habit["streak"] for habit in habit_tracker.habits.values()]

    habit_names = [str(habit_name) for habit_name in habit_names]
    streaks = [int(streak) for streak in streaks]

    # bar chart
    plt.figure(figsize=(10, 5))
    plt.bar(habit_names, streaks, color='skyblue')
    plt.xlabel('Habit')
    plt.ylabel('Streak')
    plt.title('Habit Completion Streaks')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(plt)

# function to plot medication doses
def plot_medication_doses(medication_tracker):
    if not medication_tracker.medications:
        st.warning("No medications to display.")
        return

    # convert dates to datetime objects for plotting
    dates = []
    med_names = []
    
    for med in medication_tracker.medications:
        if med.get("last_taken"):
            dates.append(datetime.strptime(med["last_taken"], "%Y-%m-%d"))
            med_names.append(med["name"])
    
    if not dates:
        st.warning("No medication doses recorded yet.")
        return
        
    #scatter plot
    plt.figure(figsize=(10, 5))
    plt.scatter(dates, med_names, color='lightgreen', s=100)
    plt.xlabel('Date')
    plt.ylabel('Medication')
    plt.title('Medication Doses Taken')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(plt)

# plotting cycle phases
def plot_cycle_phases(period_tracker):
    cycle_length = period_tracker.cycle_length
    menstrual_length = period_tracker.menstrual_length
    
    luteal_length = 14
    follicular_length = cycle_length - (menstrual_length + luteal_length)

    phases = ["Menstrual", "Follicular", "Ovulation", "Luteal"]
    lengths = [menstrual_length, follicular_length, 1, luteal_length]
    colors = ["green", "lightpink", "gold", "lightskyblue"]

    plt.figure(figsize=(8, 8))
    plt.pie(lengths, labels=phases, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.title("Cycle Phases")
    st.pyplot(plt)

if __name__ == "__main__":
    main()