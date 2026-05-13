import os
import json
import datetime
import argparse


TASKS_FILE = "tasks.json" # defining the file name for storing tasks to avoid hardcoding it multiple times in the code
VALID_STATUSES = {"todo", "in-progress", "done"} # defining valid statuses for tasks to ensure consistency and avoid typos when marking tasks with different statuses


def check_tasks_file_exists(): # function to check if the tasks file exists, and if not, create it with an empty list as the initial content
    if not os.path.exists(TASKS_FILE): 
        with open(TASKS_FILE, "w") as f:
            f.write("[]")


def load_tasks(): # function to load tasks from the tasks file, ensuring that the file exists before attempting to read it
    check_tasks_file_exists()
    with open(TASKS_FILE, "r") as f:
        tasks = json.load(f)
        return tasks


def save_tasks(tasks): # function to save the list of tasks back to the tasks file, using JSON formatting with indentation for readability
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def get_next_id(tasks): # function to determine the next unique ID for a new task by finding the maximum existing ID and adding 1, or returning 1 if there are no tasks
    if not tasks:
        return 1
    max_id = max(task["id"] for task in tasks) # generator expression to find the maximum ID among existing tasks
    return max_id + 1


def find_task_by_id(tasks, task_id): # function to search for a task in the list of tasks by its ID, returning the task if found or None if not found
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def add_task(description): # function to add a new task with the provided description, ensuring that the description is not empty and assigning a unique ID and timestamps for creation and last update
    tasks = load_tasks()

    if description.strip() == "":
        print("Task description cannot be empty.")
        return

    now = datetime.datetime.now().isoformat() # stored the current timestamp in ISO format to be used for both createdAt and updatedAt fields of the new task, so that they have the same initial value when the task is created

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


def update_task(task_id, new_description): # function to update the description of an existing task identified by its ID, ensuring that the new description is not empty and updating the last updated timestamp if the task is found and successfully updated
    tasks = load_tasks()

    if new_description.strip() == "":
        print("Task description cannot be empty.")
        return

    task = find_task_by_id(tasks, task_id)

    if task is None:
        print(f"Task with ID {task_id} not found.")
        return

    task["description"] = new_description
    task["updatedAt"] = datetime.datetime.now().isoformat()

    save_tasks(tasks)
    print(f"Task {task_id} updated successfully.")


def delete_task(task_id): # function to delete an existing task identified by its ID, ensuring that the task exists before attempting to remove it
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)

    if task is None:
        print(f"Task with ID {task_id} not found.")
        return

    tasks.remove(task) # removing the task from the list of tasks if it is found, and then saving the updated list back to the tasks file to persist the deletion
    save_tasks(tasks)
    print(f"Task {task_id} deleted successfully.")


def mark_task(task_id, status): # function to mark an existing task with a new status, ensuring that the provided status is valid and that the task exists before updating its status and last updated timestamp
    print(f'Choose a status from {VALID_STATUSES}')
    if status not in VALID_STATUSES:
        print(f"Invalid status: {status}")
        return

    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)

    if task is None:
        print(f"Task with ID {task_id} not found.")
        return

    task["status"] = status
    task["updatedAt"] = datetime.datetime.now().isoformat()

    save_tasks(tasks)
    print(f"Task {task_id} marked as {status}.")


def list_tasks(status=None):
    tasks = load_tasks()

    if status is not None:
        tasks = [task for task in tasks if task["status"] == status]

    if not tasks:
        if status:
            print(f"No tasks found with status '{status}'.")
        else:
            print("No tasks found.")
        return

    for task in tasks:
        print(f"ID: {task['id']}")
        print(f"Description: {task['description']}")
        print(f"Status: {task['status']}")
        print(f"Created At: {task['createdAt']}")
        print(f"Updated At: {task['updatedAt']}")
        print("-" * 30) 


def main():
    parser = argparse.ArgumentParser(prog="task-cli", description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")

    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("description", help="New task description")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    mark_in_progress_parser = subparsers.add_parser(
        "mark-in-progress",
        help="Mark a task as in progress"
    )
    mark_in_progress_parser.add_argument("id", type=int, help="Task ID")

    mark_done_parser = subparsers.add_parser(
        "mark-done",
        help="Mark a task as done"
    )
    mark_done_parser.add_argument("id", type=int, help="Task ID")

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "status",
        nargs="?",
        choices=["todo", "in-progress", "done"],
        help="Optional status filter"
    )

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "update":
        update_task(args.id, args.description)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "mark-in-progress":
        mark_task(args.id, "in-progress")
    elif args.command == "mark-done":
        mark_task(args.id, "done")
    elif args.command == "list":
        list_tasks(args.status)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()