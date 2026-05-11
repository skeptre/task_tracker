import os
import json
import datetime


TASKS_FILE = "tasks.json"


def check_tasks_file_exists():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w") as f:
            f.write("[]")


def load_tasks():
    check_tasks_file_exists()
    with open(TASKS_FILE, "r") as f:
        tasks = json.load(f)
        return tasks


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


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
    max_id = max(task["id"] for task in tasks)
    return max_id + 1


def add_task(description):
    tasks = load_tasks()

    if description.strip() == "":
        print("Task description cannot be empty.")
        return

    now = datetime.datetime.now().isoformat()

    new_task = {
        "id": get_next_id(tasks),
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_task['id']})")


def main():
    check_tasks_file_exists()
    add_task("Test task")
    list_all_tasks()


if __name__ == "__main__":
    main()