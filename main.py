import os
import json
import datetime


TASKS_FILE = 'tasks.json'
def check_tasks_file_exists():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w') as f:
            f.write("[]")
            print(f"{TASKS_FILE} file created.")
    else:
        print(f"{TASKS_FILE} file already exists.")

def load_tasks():
    with open(TASKS_FILE, "r") as f:
        tasks = json.load(f)
        return tasks
    
def list_all_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}")

def get_next_id(tasks):
    if not tasks:
        return 1
    max_id = max(int(task['id']) for task in tasks)
    return max_id + 1

def add_task(description):
    tasks = load_tasks()
    for task in tasks:
        if task['description'] == description:
            print("Task already exists.")
            return
        
    if description.strip() == "":
        print("Task description cannot be empty.")
        return
    
    new_task = {
        "id": (get_next_id(tasks)),
        "description": description,
        "status": "todo",
        "createdAt": datetime.datetime.now().isoformat(),
        "updatedAt": datetime.datetime.isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print("Task added successfully.")
    

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)




def main():
    check_tasks_file_exists()
    list_all_tasks()

if __name__ == "__main__":
    main()