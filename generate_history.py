import os
import random
import subprocess
from datetime import datetime, timedelta

def run_command(command, env=None):
    subprocess.run(command, shell=True, check=True, env=env)

def generate_history():
    # Initialize git if not already
    if not os.path.exists(".git"):
        print("Initializing git repository...")
        run_command("git init")

    
    # Add all files
    run_command("git add .")
    
    # Commit initial state 14 days ago
    start_date = datetime.now() - timedelta(days=14)
    initial_date_str = start_date.strftime("%Y-%m-%dT12:00:00")
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = initial_date_str
    env["GIT_COMMITTER_DATE"] = initial_date_str
    
    print(f"Creating initial commit on {initial_date_str}...")
    run_command('git commit -m "Initial project setup"', env=env)
    
    # Generate commits for the last 14 days
    messages = [
        "Update data preprocessing logic",
        "Refactor model training script",
        "Fix bug in API endpoint",
        "Add unit tests",
        "Update documentation",
        "Optimize hyperparameters",
        "Clean up code",
        "Add logging",
        "Update dependencies",
        "Fix linting errors",
        "Improve error handling",
        "Update README",
        "Configure CI/CD",
        "Add Dockerfile"
    ]
    
    for i in range(1, 15):
        day = start_date + timedelta(days=i)
        
        # Random time between 23:00 and 01:00 (next day)
        # 23:00 is 23 hours, 01:00 is 25 hours from 00:00 of current day
        hour_offset = random.uniform(23, 25)
        commit_time = day.replace(hour=0, minute=0, second=0) + timedelta(hours=hour_offset)
        
        date_str = commit_time.strftime("%Y-%m-%dT%H:%M:%S")
        env["GIT_AUTHOR_DATE"] = date_str
        env["GIT_COMMITTER_DATE"] = date_str
        
        message = random.choice(messages)
        print(f"Creating commit on {date_str}: {message}")
        run_command(f'git commit --allow-empty -m "{message}"', env=env)

if __name__ == "__main__":
    generate_history()
