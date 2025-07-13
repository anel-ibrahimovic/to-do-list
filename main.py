import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import json
import os

file_path = os.path.expanduser("~/tasks.json")

def save_tasks():
    with open(file_path, 'w') as f:
        json.dump(tasks, f, default=str)

def load_tasks():
    try:
        with open(file_path, 'r') as f:
            loaded = json.load(f)
            for task in loaded:
                task['due_date'] = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
            return loaded
    except FileNotFoundError:
        return []

tasks = load_tasks()

def refresh_listbox():
    listbox.delete(0, tk.END)
    for task in sorted(tasks, key=lambda t: t['due_date']):
        status = "✓" if task['status'] == "Completed" else "✗"
        listbox.insert(tk.END, f"{task['title']} ({task['due_date']}) [{status}]")

def add_task():
    title = simpledialog.askstring("Title", "Enter task title:")
    if not title:
        return

    if any(t['title'].lower() == title.lower() for t in tasks):
        messagebox.showerror("Duplicate", "A task with this title already exists.")
        return

    desc = simpledialog.askstring("Description", "Enter description:")
    priority = simpledialog.askstring("Priority", "Priority (high/medium/low):")
    due_date_str = simpledialog.askstring("Due Date", "Due date (YYYY-MM-DD):")

    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
    except:
        messagebox.showerror("Error", "Invalid date format.")
        return

    tasks.append({
        'title': title,
        'description': desc or "",
        'priority': priority or "low",
        'due_date': due_date,
        'status': "Incomplete"
    })
    save_tasks()
    refresh_listbox()

def delete_task():
    selected = listbox.curselection()
    if not selected:
        return
    index = selected[0]
    task_title = listbox.get(index).split(" (")[0]
    for t in tasks:
        if t['title'] == task_title:
            tasks.remove(t)
            break
    save_tasks()
    refresh_listbox()

def complete_task():
    selected = listbox.curselection()
    if not selected:
        return
    index = selected[0]
    title = listbox.get(index).split(" (")[0]
    for t in tasks:
        if t['title'] == title:
            t['status'] = "Completed"
            break
    save_tasks()
    refresh_listbox()

def view_task_details():
    selected = listbox.curselection()
    if not selected:
        return
    index = selected[0]
    title = listbox.get(index).split(" (")[0]
    for t in tasks:
        if t['title'] == title:
            info = (
                f"Title: {t['title']}\n"
                f"Description: {t['description']}\n"
                f"Priority: {t['priority']}\n"
                f"Due Date: {t['due_date']}\n"
                f"Status: {t['status']}"
            )
            messagebox.showinfo("Task Details", info)
            break

def edit_task():
    selected = listbox.curselection()
    if not selected:
        return
    index = selected[0]
    current_title = listbox.get(index).split(" (")[0]

    for t in tasks:
        if t['title'] == current_title:
            new_title = simpledialog.askstring("Edit Title", "New title:", initialvalue=t['title'])
            if not new_title:
                return
            if new_title.lower() != t['title'].lower() and any(x['title'].lower() == new_title.lower() for x in tasks):
                messagebox.showerror("Duplicate", "Another task with this title exists.")
                return

            new_desc = simpledialog.askstring("Edit Description", "New description:", initialvalue=t['description'])
            new_priority = simpledialog.askstring("Edit Priority", "Priority (high/medium/low):", initialvalue=t['priority'])
            new_due_date = simpledialog.askstring("Edit Due Date", "New due date (YYYY-MM-DD):", initialvalue=str(t['due_date']))

            try:
                new_due_date_obj = datetime.strptime(new_due_date, "%Y-%m-%d").date()
            except:
                messagebox.showerror("Error", "Invalid date. Keeping old one.")
                new_due_date_obj = t['due_date']

            t.update({
                'title': new_title,
                'description': new_desc,
                'priority': new_priority,
                'due_date': new_due_date_obj
            })
            save_tasks()
            refresh_listbox()
            break

root = tk.Tk()
root.title("To-Do List (GUI)")

listbox = tk.Listbox(root, width=60, height=15)
listbox.pack(padx=10, pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Add Task", width=12, command=add_task).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Edit Task", width=12, command=edit_task).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete Task", width=12, command=delete_task).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Complete", width=12, command=complete_task).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Details", width=12, command=view_task_details).grid(row=0, column=4, padx=5)
tk.Button(btn_frame, text="Exit", width=12, command=root.destroy).grid(row=0, column=5, padx=5)

refresh_listbox()
root.mainloop()
