import json
from datetime import datetime, timedelta

TASK_FILE = "tasks.json"


def load_tasks():
    try:
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=4)


def add_task():
    description = input("Enter task description: ")
    due_date = input("Enter due date (YYYY-MM-DD) or leave blank: ")
    task = {"description": description, "due_date": due_date, "completed": False}
    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully!")


def view_tasks(filter_type=None):
    if not tasks:
        print("No tasks available.")
        return

    today = datetime.today().date()
    for i, task in enumerate(tasks, 1):
        due_date = task["due_date"]
        due_str = f"(Due: {due_date})" if due_date else ""
        completed = "[Completed]" if task["completed"] else "[Pending]"

        if filter_type == "completed" and not task["completed"]:
            continue
        if filter_type == "pending" and task["completed"]:
            continue
        if filter_type == "due_soon" and due_date:
            task_date = datetime.strptime(due_date, "%Y-%m-%d").date()
            if task_date > today + timedelta(days=3):
                continue

        print(f"{i}. {task['description']} {due_str} {completed}")


def mark_completed():
    view_tasks("pending")
    try:
        index = int(input("Enter task number to mark as completed: ")) - 1
        tasks[index]["completed"] = True
        save_tasks(tasks)
        print("Task marked as completed!")
    except (IndexError, ValueError):
        print("Invalid input!")


def edit_task():
    view_tasks()
    try:
        index = int(input("Enter task number to edit: ")) - 1
        new_description = input("Enter new description (or press Enter to keep unchanged): ")
        new_due_date = input("Enter new due date (YYYY-MM-DD) or press Enter to keep unchanged: ")

        if new_description:
            tasks[index]["description"] = new_description
        if new_due_date:
            tasks[index]["due_date"] = new_due_date

        save_tasks(tasks)
        print("Task updated!")
    except (IndexError, ValueError):
        print("Invalid input!")


def delete_task():
    view_tasks()
    try:
        index = int(input("Enter task number to delete: ")) - 1
        del tasks[index]
        save_tasks(tasks)
        print("Task deleted!")
    except (IndexError, ValueError):
        print("Invalid input!")


def main():
    global tasks
    tasks = load_tasks()
    while True:
        print("\nTo-Do List Manager")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. View Completed Tasks")
        print("4. View Pending Tasks")
        print("5. View Tasks Due Soon")
        print("6. Mark Task as Completed")
        print("7. Edit Task")
        print("8. Delete Task")
        print("9. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            view_tasks("completed")
        elif choice == "4":
            view_tasks("pending")
        elif choice == "5":
            view_tasks("due_soon")
        elif choice == "6":
            mark_completed()
        elif choice == "7":
            edit_task()
        elif choice == "8":
            delete_task()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
