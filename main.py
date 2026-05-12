import os
import json
import datetime
import argparse


TASKS_FILE = "tasks.json"
VALID_STATUSES = {"todo", "in-progress", "done"}


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


def get_next_id(tasks):
    if not tasks:
        return 1
    max_id = max(task["id"] for task in tasks)
    return max_id + 1


def find_task_by_id(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


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


def update_task(task_id, new_description):
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


def delete_task(task_id):
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)

    if task is None:
        print(f"Task with ID {task_id} not found.")
        return

    tasks.remove(task)
    save_tasks(tasks)
    print(f"Task {task_id} deleted successfully.")


def mark_task(task_id, status):
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