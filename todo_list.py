import tkinter as tk
from tkinter import messagebox, filedialog
import json
from datetime import datetime

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("800x600")
        self.root.configure(bg="#e0f7fa")

        self.tasks = []

        self.load_tasks()

        self.setup_ui()
        self.update_tasks_listbox()

    def setup_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        frame = tk.Frame(self.root, bg="#e0f7fa")
        frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        frame.columnconfigure((0, 1, 2), weight=1)

        tk.Label(frame, text="Task:", bg="#e0f7fa", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.task_entry = tk.Entry(frame, width=30)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        tk.Label(frame, text="Description:", bg="#e0f7fa", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.description_entry = tk.Entry(frame, width=30)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        tk.Label(frame, text="Due Date (YYYY-MM-DD):", bg="#e0f7fa", font=("Helvetica", 12)).grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.due_date_entry = tk.Entry(frame, width=30)
        self.due_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        tk.Label(frame, text="Priority:", bg="#e0f7fa", font=("Helvetica", 12)).grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.priority_var = tk.StringVar(value="Medium")
        self.priority_menu = tk.OptionMenu(frame, self.priority_var, "High", "Medium", "Low")
        self.priority_menu.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        tk.Label(frame, text="Category:", bg="#e0f7fa", font=("Helvetica", 12)).grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.category_var = tk.StringVar(value="General")
        self.category_menu = tk.OptionMenu(frame, self.category_var, "Work", "Personal", "General")
        self.category_menu.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

        self.add_task_button = tk.Button(frame, text="Add Task", command=self.add_task, bg="#00796b", fg="#ffffff", font=("Helvetica", 12))
        self.add_task_button.grid(row=5, column=1, padx=5, pady=15, sticky='ew')

        listbox_frame = tk.Frame(self.root, bg="#e0f7fa")
        listbox_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)

        self.tasks_listbox = tk.Listbox(listbox_frame, width=100, height=15, selectmode=tk.SINGLE, bg="#ffffff", fg="#000000", font=("Helvetica", 12))
        self.tasks_listbox.grid(row=0, column=0, sticky='nsew')

        button_frame = tk.Frame(self.root, bg="#e0f7fa")
        button_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        button_frame.columnconfigure((0, 1, 2), weight=1)

        self.complete_task_button = tk.Button(button_frame, text="Mark as Completed", command=self.mark_task_completed, bg="#388e3c", fg="#ffffff", font=("Helvetica", 12))
        self.complete_task_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.remove_task_button = tk.Button(button_frame, text="Remove Task", command=self.remove_task, bg="#d32f2f", fg="#ffffff", font=("Helvetica", 12))
        self.remove_task_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.save_tasks_button = tk.Button(button_frame, text="Save Tasks", command=self.save_tasks, bg="#fbc02d", fg="#000000", font=("Helvetica", 12))
        self.save_tasks_button.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

    def add_task(self):
        task = self.task_entry.get()
        description = self.description_entry.get()
        due_date = self.due_date_entry.get()
        priority = self.priority_var.get()
        category = self.category_var.get()

        if task and due_date:
            try:
                due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
                self.tasks.append({
                    "task": task,
                    "description": description,
                    "due_date": due_date,
                    "priority": priority,
                    "category": category,
                    "completed": False
                })
                self.task_entry.delete(0, tk.END)
                self.description_entry.delete(0, tk.END)
                self.due_date_entry.delete(0, tk.END)
                self.update_tasks_listbox()
            except ValueError:
                messagebox.showwarning("Warning", "Invalid date format. Use YYYY-MM-DD.")
        else:
            messagebox.showwarning("Warning", "Task and Due Date are required.")

    def update_tasks_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "Completed" if task["completed"] else "Pending"
            self.tasks_listbox.insert(tk.END, f"{task['task']} ({task['category']}) [{task['priority']}] Due: {task['due_date']} - {status}")

    def mark_task_completed(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            self.tasks[task_index]["completed"] = True
            self.update_tasks_listbox()
        else:
            messagebox.showwarning("Warning", "You must select a task to mark as completed.")

    def remove_task(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            task_index = selected_task_index[0]
            self.tasks.pop(task_index)
            self.update_tasks_listbox()
        else:
            messagebox.showwarning("Warning", "You must select a task to remove.")

    def save_tasks(self):
        with filedialog.asksaveasfile(mode='w', defaultextension=".json") as file:
            json.dump(self.tasks, file)
            messagebox.showinfo("Info", "Tasks saved successfully!")

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
