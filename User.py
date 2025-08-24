import json
import os

# File name for the JSON log
JSON_FILE = "Userlog.json"

# Function to load the user log from JSON file
def load_user_log():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}  # Return empty dict if file doesn't exist

# Function to save the user log to JSON file
def save_user_log(user_log):
    with open(JSON_FILE, 'w') as file:
        json.dump(user_log, file, indent=4)

# Main program
def main():
    user_log = load_user_log()
    
    # Ask user for choice
    print("Choose an action:")
    print("1. Add a user")
    print("2. Remove a user")
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == '1':
        # Add user
        username = input("Enter username: ").strip()
        if username in user_log:
            print(f"Username '{username}' already exists.")
        else:
            ip = input("Enter public IP address: ").strip()
            user_log[username] = ip
            print(f"Added '{username}' with IP '{ip}'.")
    
    elif choice == '2':
        # Remove user
        username = input("Enter username to remove: ").strip()
        if username in user_log:
            del user_log[username]
            print(f"Removed '{username}'.")
        else:
            print(f"Username '{username}' not found.")
    
    else:
        print("Invalid choice. No action taken.")
    
    # Save changes
    save_user_log(user_log)
    print("User log updated.")

if __name__ == "__main__":
    main()
