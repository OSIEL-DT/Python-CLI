import json
import os
from datetime import datetime

DATA_FILE = 'task_data.json'


class TaskManager:
    def __init__(self):
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from JSON file"""
        if not os.path.exists(DATA_FILE):
            self.tasks = []
        else:
            with open(DATA_FILE, 'r') as file:
                self.tasks = json.load(file)

    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(DATA_FILE, 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, title, description, due_date):
        """Add a new task"""
        new_task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description,
            'due_date': due_date,
            'created_at': str(datetime.now()),
            'completed': False
        }
        self.tasks.append(new_task)
        self.save_tasks()
        print(f"Task '{title}' added successfully!")

    def remove_task(self, task_id):
        """Remove a task by ID"""
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self.save_tasks()
        print(f"Task with ID {task_id} removed successfully!")

    def update_task(self, task_id, title=None, description=None, due_date=None, completed=None):
        """Update task details"""
        task = next((task for task in self.tasks if task['id'] == task_id), None)
        if task:
            if title:
                task['title'] = title
            if description:
                task['description'] = description
            if due_date:
                task['due_date'] = due_date
            if completed is not None:
                task['completed'] = completed
            self.save_tasks()
            print(f"Task with ID {task_id} updated successfully!")
        else:
            print(f"Task with ID {task_id} not found!")

    def list_tasks(self, show_completed=False):
        """List all tasks"""
        tasks = self.tasks if show_completed else [task for task in self.tasks if not task['completed']]
        for task in tasks:
            status = 'Completed' if task['completed'] else 'Pending'
            print(f"[{task['id']}] {task['title']} - Due: {task['due_date']} - Status: {status}")

    def mark_completed(self, task_id):
        """Mark a task as completed"""
        task = next((task for task in self.tasks if task['id'] == task_id), None)
        if task:
            task['completed'] = True
            self.save_tasks()
            print(f"Task with ID {task_id} marked as completed!")
        else:
            print(f"Task with ID {task_id} not found!")

    def list_overdue_tasks(self):
        """List overdue tasks"""
        current_date = datetime.now()
        overdue_tasks = [task for task in self.tasks if datetime.strptime(task['due_date'], "%Y-%m-%d") < current_date and not task['completed']]
        if overdue_tasks:
            print("Overdue Tasks:")
            for task in overdue_tasks:
                print(f"[{task['id']}] {task['title']} - Due: {task['due_date']}")
        else:
            print("No overdue tasks.")


def main():
    manager = TaskManager()

    while True:
        print("\nTask Manager Menu:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Update Task")
        print("4. List Tasks")
        print("5. Mark Task as Completed")
        print("6. List Overdue Tasks")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            manager.add_task(title, description, due_date)

        elif choice == '2':
            task_id = int(input("Enter task ID to remove: "))
            manager.remove_task(task_id)

        elif choice == '3':
            task_id = int(input("Enter task ID to update: "))
            title = input("Enter new title (or press Enter to skip): ")
            description = input("Enter new description (or press Enter to skip): ")
            due_date = input("Enter new due date (YYYY-MM-DD, or press Enter to skip): ")
            completed = input("Mark as completed? (yes/no/skip): ").lower()
            completed = None if completed == 'skip' else completed == 'yes'
            manager.update_task(task_id, title, description, due_date, completed)

        elif choice == '4':
            show_completed = input("Show completed tasks? (yes/no): ").lower() == 'yes'
            manager.list_tasks(show_completed)

        elif choice == '5':
            task_id = int(input("Enter task ID to mark as completed: "))
            manager.mark_completed(task_id)

        elif choice == '6':
            manager.list_overdue_tasks()

        elif choice == '0':
            print("Exiting Task Manager.")
            break

        else:
            print("Invalid option. Please choose a valid option.")


if __name__ == '__main__':
    main()
