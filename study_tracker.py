# study_tracker.py

import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pygame

# ---------- Configuration ----------
FILE_NAME = "study_log.csv"
GOAL_FILE = "goal.txt"
DAILY_GOAL = 90  # Will be overwritten by load_daily_goal() if file exists

# ---------- Sound Setup ----------
pygame.mixer.init()

def play_sound(filename):
    try:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"🔇 Sound error: {e}")

# ---------- Data Handling ----------
def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)
    return pd.DataFrame(columns=["Date", "Minutes"])

def save_data(df):
    df.to_csv(FILE_NAME, index=False)

# ---------- Goal Handling ----------
def load_daily_goal():
    global DAILY_GOAL
    if os.path.exists(GOAL_FILE):
        try:
            with open(GOAL_FILE, "r") as f:
                DAILY_GOAL = int(f.read().strip())
        except:
            print("⚠️ Failed to read goal file, using default.")

def set_daily_goal():
    global DAILY_GOAL
    new_goal = input("Enter your new daily goal (in minutes): ")
    if new_goal.isdigit() and int(new_goal) > 0:
        DAILY_GOAL = int(new_goal)
        with open(GOAL_FILE, "w") as f:
            f.write(str(DAILY_GOAL))
        print(f"✅ Daily goal updated to {DAILY_GOAL} minutes.")
    else:
        print("❌ Invalid input. Please enter a positive number.")

# ---------- Core Features ----------
def add_study_entry():
    minutes = input("How many minutes did you study today? ")
    if not minutes.isdigit():
        print("❌ Please enter a valid number.")
        return

    minutes = int(minutes)
    today = datetime.today().strftime('%Y-%m-%d')
    df = load_data()

    new_row = pd.DataFrame([{"Date": today, "Minutes": minutes}])
    df = pd.concat([df, new_row], ignore_index=True)
    save_data(df)
    print("✅ Entry saved!")

    if minutes >= DAILY_GOAL:
        play_sound("success.mp3")
        print(f"🎉 Great job! You reached your {DAILY_GOAL}-minute goal!")
    else:
        play_sound("fail.mp3")
        print(f"⏱ You studied {DAILY_GOAL - minutes} minute(s) less than your goal today.")

def show_summary():
    df = load_data()
    if df.empty:
        print("No data found.")
        return

    total_minutes = df["Minutes"].sum()
    avg_minutes = df["Minutes"].mean()
    total_days = len(df)
    met_goal_days = len(df[df["Minutes"] >= DAILY_GOAL])

    print("\n📊 Study Summary:")
    print(f"Total days tracked: {total_days}")
    print(f"Total minutes studied: {total_minutes}")
    print(f"Average minutes per day: {avg_minutes:.2f}")
    print(f"🎯 Days you met your goal ({DAILY_GOAL} min): {met_goal_days}/{total_days}")

def plot_chart():
    df = load_data()
    if df.empty:
        print("No data to plot.")
        return

    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values("Date", inplace=True)

    colors = ["green" if m >= DAILY_GOAL else "skyblue" for m in df["Minutes"]]

    plt.figure(figsize=(10, 5))
    plt.bar(df["Date"].dt.strftime("%Y-%m-%d"), df["Minutes"], color=colors, label="Study Time")
    plt.axhline(y=DAILY_GOAL, color='red', linestyle='--', label=f"Goal: {DAILY_GOAL} min")

    plt.xlabel("Date")
    plt.ylabel("Minutes Studied")
    plt.title("Study Time Tracker")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def export_to_excel():
    df = load_data()
    if df.empty:
        print("No data to export.")
        return

    filename = "study_log_export.xlsx"
    summary_data = {
        "Total Days Tracked": [len(df)],
        "Total Minutes Studied": [df["Minutes"].sum()],
        "Average Minutes per Day": [df["Minutes"].mean()],
        "Daily Goal (min)": [DAILY_GOAL],
        "Days Goal Met": [len(df[df["Minutes"] >= DAILY_GOAL])]
    }
    summary_df = pd.DataFrame(summary_data)

    try:
        with pd.ExcelWriter(filename, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Study Log", index=False)
            summary_df.to_excel(writer, sheet_name="Summary", index=False)
        print(f"✅ Data and summary exported to {filename}")
    except Exception as e:
        print(f"❌ Failed to export: {e}")

# ---------- Main Menu ----------
def main():
    while True:
        print("\n📚 Study Tracker Menu")
        print("1. Add Study Entry")
        print("2. View Summary")
        print("3. Plot Chart")
        print("4. Set Daily Goal")
        print("5. Export to Excel")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_study_entry()
        elif choice == "2":
            show_summary()
        elif choice == "3":
            plot_chart()
        elif choice == "4":
            set_daily_goal()
        elif choice == "5":
            export_to_excel()
        elif choice == "6":
            print("👋 Goodbye! Keep learning!")
            break
        else:
            print("❌ Invalid choice. Try again.")

# ---------- Start App ----------
if __name__ == "__main__":
    load_daily_goal()
    main()
