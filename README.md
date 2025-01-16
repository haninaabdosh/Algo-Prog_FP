# Sama: A Wellness Tracking Application

**Sama** is a simple and user-friendly app I created to help track habits, periods, and medications. It uses **Streamlit** to provide an interactive interface and stores data in CSV files so it’s easy to manage. It uses  **Matplotlib** for visualizing data, and **datetime** for handling dates and times. This application is designed to make wellness management more accessible and organized.

## Overview

The app includes:

- **Habit Tracker**: For logging and keeping up with daily habits.
- **Period Tracker**: To track menstrual cycles and stay informed of current phases.
- **Medication Tracker**: For managing medications.

### Project Structure

The app is structured as follows:

- **`app.py`**: The main file that integrates all the modules and launches the app.
- **Data Files**:
    - `habits.csv`: Stores data for the Habit Tracker.
    - `medications.csv`: Stores data for the Medication Tracker.
    - `periods.csv`: Stores data for the Period Tracker.

If the data files (`habits.csv`, `medications.csv`, `periods.csv`) are missing, the app will create them automatically during its first run. However, this will not be necessary as the files have already been included in the ZIP file.

## How to Run the App

1. **Download the Files**:
    - Download the ZIP file for this project and extract it to a folder on your computer.
2. **Install Python and Streamlit**:
    - Ensure that **Python 3.8 or higher** is installed on your computer.
        - To check your Python version, run:
            
            ```bash
            python --version
            ```
            
    - Install the required libraries:
        - Open your terminal or command prompt and run:
            
            ```bash
            
            pip install streamlit matplotlib
            
            ```
            
3. **Run the App**:
    - Open your terminal or command prompt and go to the folder where `app.py` is located.
    - Run the app with:
        
        ```bash
        streamlit run app.py
        
        ```
        
4. **Open in Your Browser**:
    - After running the command, a local URL  will pop up in the terminal.
    - Open it in your browser, and you’re good to go!
