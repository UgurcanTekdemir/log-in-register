import json
from datetime import datetime

class Task:
    def _init_(self, title, description, due_date, priority):
        self.title = title
        self.description = description
        self.due_date = datetime.strptime(due_date, '%Y-%m-%d')
        self.priority = priority
        self.status = "Pending"

    def display_details(self):
        print(f"Title: {self.title}\nDescription: {self.description}\nDue Date: {self.due_date.strftime('%Y-%m-%d')}\nPriority: {self.priority}\nStatus: {self.status}\n")

    def update_status(self, new_status):
        self.status = new_status

    def update_task(self, title, description, due_date, priority):
        self.title = title
        self.description = description
        self.due_date = datetime.strptime(due_date, '%Y-%m-%d')
        self.priority = priority

class TaskList:
    def _init_(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def display_tasks(self, status=None):
        if status:
            filtered_tasks = [task for task in self.tasks if task.status == status]
        else:
            filtered_tasks = self.tasks

        for task in filtered_tasks:
            task.display_details()

    def find_task_by_title(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def update_task(self, title, new_title, description, due_date, priority):
        task = self.find_task_by_title(title)
        if task:
            task.update_task(new_title, description, due_date, priority)

class User:
    def _init_(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.assigned_tasks = []

    def view_tasks(self):
        for task in self.assigned_tasks:
            task.display_details()

    def mark_task_complete(self, task):
        task.update_status("Completed")


def save_tasks_to_file(task_list, filename):
    with open(filename, 'w') as file:
        tasks_data = []
        for task in task_list.tasks:
            task_data = {
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date.strftime('%Y-%m-%d'),
                'priority': task.priority,
                'status': task.status
            }
            tasks_data.append(task_data)
        json.dump(tasks_data, file)


def load_tasks_from_file(filename):
    try:
        with open(filename, 'r') as file:
            tasks_data = json.load(file)
            task_list = TaskList()
            for task_data in tasks_data:
                task = Task(
                    task_data['title'],
                    task_data['description'],
                    task_data['due_date'],
                    task_data['priority']
                )
                task.status = task_data['status']
                task_list.add_task(task)
            return task_list
    except FileNotFoundError:
        return TaskList()


# Example Usage:
filename = 'tasks_data.json'
task_list = load_tasks_from_file(filename)

while True:
    print("\n===== Task Calendar =====")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. View Tasks")
    print("4. Update Task")
    print("5. Save and Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        title = input("Enter task title: ")
        description = input("Enter task description: ")
        due_date = input("Enter due date (YYYY-MM-DD): ")
        priority = input("Enter priority: ")

        new_task = Task(title, description, due_date, priority)
        task_list.add_task(new_task)

    elif choice == '2':
        title = input("Enter title of the task to remove: ")
        task_to_remove = task_list.find_task_by_title(title)
        if task_to_remove:
            task_list.remove_task(task_to_remove)
            print(f"Task '{title}' removed successfully.")
        else:
            print(f"Task '{title}' not found.")

    elif choice == '3':
        print("\n===== Your Tasks =====")
        task_list.display_tasks()

    elif choice == '4':
        title = input("Enter title of the task to update: ")
        task_to_update = task_list.find_task_by_title(title)
        if task_to_update:
            print("\nEnter new task details:")
            new_title = input("New Title: ")
            new_description = input("New Description: ")
            new_due_date = input("New Due Date (YYYY-MM-DD): ")
            new_priority = input("New Priority: ")

            task_list.update_task(title, new_title, new_description, new_due_date, new_priority)
            print(f"Task '{title}' updated successfully.")
        else:
            print(f"Task '{title}' not found.")

    elif choice == '5':
        save_tasks_to_file(task_list, filename)
        print("Tasks saved. Exiting...")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 5.")