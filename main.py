from datetime import datetime
import json
import os

file_path = os.path.expanduser("~/tasks.json")

def save_tasks():
    with open(file_path, 'w') as f:
        json.dump(tasks, f, default=str)

def load_tasks():
    global tasks
    try:
        with open(file_path, 'r') as f:
            loaded_tasks = json.load(f)
            for task in loaded_tasks:
                task['due_date'] = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
            tasks = loaded_tasks
    except FileNotFoundError:
        tasks = []

tasks = []

def add_task():
    title = input("Enter task title: ")

    if any(task['title'].lower() == title.lower() for task in tasks):
        print("A task with this title already exists. Please use a different title.")
        return

    description = input("Enter task description: ")
    priority = input("Set task priority (high/medium/low): ")

    while True:
        due_date = input("Enter task due date (YYYY-MM-DD): ")
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    status = "Incomplete"

    task = {
        'title': title,
        'description': description,
        'priority': priority,
        'due_date': due_date,
        'status': status
    }

    tasks.append(task)
    print("Task added successfully!")

def status_update():
    status_input = input("Select a task to mark as completed (write task title): ")
    found = False
    for task in tasks:
        if task['title'].lower() == status_input.lower():
            task['status'] = "Completed"
            found = True
            print(f"Task '{status_input}' marked as completed.")
            break
    if not found:
        print(f"Task '{status_input}' not found.")

def view_tasks():
    if not tasks:
        print("No tasks to display")
        return
    for i, task in enumerate(sorted(tasks, key=lambda x: x['due_date']), 1):
        print(f"{i}. Title: {task['title']}")
        print(f"   Description: {task['description']}")
        print(f"   Priority: {task['priority']}")
        print(f"   Due Date: {task['due_date']}")
        print(f"   Status: {task['status']}")
        print("--------")

def edit_task():
    title_input = input("Enter the title of the task to edit: ")
    for task in tasks:
        if task['title'].lower() == title_input.lower():
            print("Leave input empty to keep the current value.")
            new_title = input(f"New title [{task['title']}]: ") or task['title']

            if new_title.lower() != task['title'].lower() and any(
                t['title'].lower() == new_title.lower() for t in tasks
            ):
                print("Another task with this title already exists. Edit cancelled.")
                return

            new_desc = input(f"New description [{task['description']}]: ") or task['description']
            new_priority = input(f"New priority [{task['priority']}]: ") or task['priority']
            new_due_date = input(f"New due date (YYYY-MM-DD) [{task['due_date']}]: ")
            try:
                if new_due_date:
                    new_due_date = datetime.strptime(new_due_date, "%Y-%m-%d").date()
                else:
                    new_due_date = task['due_date']
            except ValueError:
                print("Invalid date. Keeping the old one.")
                new_due_date = task['due_date']

            task.update({
                'title': new_title,
                'description': new_desc,
                'priority': new_priority,
                'due_date': new_due_date
            })
            print("Task updated successfully!")
            return
    print(f"No task found with title '{title_input}'.")

def delete_task():
    delete_input = input("Select a task to delete (write task title): ")
    found = False
    for task in tasks:
        if task['title'].lower() == delete_input.lower():
            tasks.remove(task)
            found = True
            print(f"Task '{delete_input}' deleted successfully.")
            break
    if not found:
        print(f"Task '{delete_input}' not found.")

def main():
    while True:
        print("To Do List")
        print("---------")
        print("1. Add Task")
        print("2. Mark Task as Completed")
        print("3. View Tasks")
        print("4. Edit Task")
        print("5. Delete Task")
        print("6. Exit")
        print("---------")
        choice = input("Enter your choice: ")

        try:
            choice = int(choice)
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 6.")
            continue

        if choice == 1:
            add_task()
        elif choice == 2:
            status_update()
        elif choice == 3:
            view_tasks()
        elif choice == 4:
            edit_task()
        elif choice == 5:
            delete_task()
        elif choice == 6:
            print("Thank You For Using To Do List!")
            save_tasks()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    load_tasks()
    main()
