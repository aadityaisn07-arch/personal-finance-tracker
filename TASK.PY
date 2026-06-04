# Smart Task Manager
# A productivity application with priority management and deadline tracking
# Author: Your Name
# Built with Python 3

import json
import os
from datetime import datetime, date

DATA_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"tasks": [], "next_id": 1}

def save_tasks(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_priority_symbol(priority):
    symbols = {"high": "🔴 HIGH", "medium": "🟡 MEDIUM", "low": "🟢 LOW"}
    return symbols.get(priority.lower(), "🟡 MEDIUM")

def get_status_symbol(status):
    symbols = {"pending": "⏳ Pending", "in_progress": "🔄 In Progress", "completed": "✅ Completed"}
    return symbols.get(status, "⏳ Pending")

def days_until_deadline(deadline_str):
    try:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()
        today = date.today()
        delta = (deadline - today).days
        if delta < 0:
            return f"⚠️  OVERDUE by {abs(delta)} days"
        elif delta == 0:
            return "🚨 DUE TODAY"
        elif delta <= 3:
            return f"⚠️  Due in {delta} days"
        else:
            return f"📅 {delta} days remaining"
    except:
        return "No deadline"

def add_task(data):
    print("\n--- ADD NEW TASK ---")
    title = input("Task Title: ").strip()
    description = input("Description: ").strip()

    print("Priority (high/medium/low): ", end="")
    priority = input().strip().lower()
    if priority not in ["high", "medium", "low"]:
        priority = "medium"

    print("Category (work/personal/study/health/other): ", end="")
    category = input().strip()

    deadline = input("Deadline (YYYY-MM-DD) or press Enter to skip: ").strip()
    if not deadline:
        deadline = "No deadline"

    task = {
        "id": data["next_id"],
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "status": "pending",
        "deadline": deadline,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "completed_at": None,
        "notes": []
    }

    data["tasks"].append(task)
    data["next_id"] += 1
    save_tasks(data)
    print(f"\n✓ Task '{title}' added with ID #{task['id']}")

def view_all_tasks(data, filter_status=None, filter_priority=None):
    tasks = data["tasks"]

    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]
    if filter_priority:
        tasks = [t for t in tasks if t["priority"] == filter_priority]

    if not tasks:
        print("\nNo tasks found.")
        return

    priority_order = {"high": 0, "medium": 1, "low": 2}
    tasks = sorted(tasks, key=lambda x: (priority_order.get(x["priority"], 1), x["id"]))

    print("\n" + "="*80)
    print(f"  TASK LIST ({len(tasks)} tasks)")
    print("="*80)

    for task in tasks:
        print(f"\n  ID: #{task['id']}  |  {get_priority_symbol(task['priority'])}  |  {get_status_symbol(task['status'])}")
        print(f"  Title: {task['title']}")
        print(f"  Category: {task['category'].upper()}")
        if task["deadline"] != "No deadline":
            print(f"  Deadline: {task['deadline']}  {days_until_deadline(task['deadline'])}")
        if task["description"]:
            print(f"  Description: {task['description'][:60]}{'...' if len(task['description']) > 60 else ''}")
        print("  " + "-"*76)

def update_task_status(data):
    view_all_tasks(data)
    try:
        task_id = int(input("\nEnter Task ID to update: "))
        task = next((t for t in data["tasks"] if t["id"] == task_id), None)

        if not task:
            print(f"Task #{task_id} not found.")
            return

        print(f"\nCurrent Status: {get_status_symbol(task['status'])}")
        print("\nNew Status:")
        print("1. Pending")
        print("2. In Progress")
        print("3. Completed")

        choice = input("Enter choice (1-3): ").strip()
        status_map = {"1": "pending", "2": "in_progress", "3": "completed"}

        if choice in status_map:
            task["status"] = status_map[choice]
            if choice == "3":
                task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_tasks(data)
            print(f"\n✓ Task #{task_id} updated to {get_status_symbol(task['status'])}")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid task ID.")

def add_note_to_task(data):
    try:
        task_id = int(input("\nEnter Task ID to add note: "))
        task = next((t for t in data["tasks"] if t["id"] == task_id), None)

        if not task:
            print(f"Task #{task_id} not found.")
            return

        note = input("Enter your note: ").strip()
        task["notes"].append({
            "note": note,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        save_tasks(data)
        print(f"\n✓ Note added to Task #{task_id}")
    except ValueError:
        print("Please enter a valid task ID.")

def delete_task(data):
    try:
        task_id = int(input("\nEnter Task ID to delete: "))
        task = next((t for t in data["tasks"] if t["id"] == task_id), None)

        if not task:
            print(f"Task #{task_id} not found.")
            return

        confirm = input(f"Delete '{task['title']}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            data["tasks"] = [t for t in data["tasks"] if t["id"] != task_id]
            save_tasks(data)
            print(f"\n✓ Task #{task_id} deleted successfully!")
        else:
            print("Deletion cancelled.")
    except ValueError:
        print("Please enter a valid task ID.")

def productivity_stats(data):
    tasks = data["tasks"]
    if not tasks:
        print("\nNo tasks found.")
        return

    total = len(tasks)
    completed = sum(1 for t in tasks if t["status"] == "completed")
    in_progress = sum(1 for t in tasks if t["status"] == "in_progress")
    pending = sum(1 for t in tasks if t["status"] == "pending")
    high_priority = sum(1 for t in tasks if t["priority"] == "high" and t["status"] != "completed")

    print("\n" + "="*50)
    print("  PRODUCTIVITY STATISTICS")
    print("="*50)
    print(f"  Total Tasks:        {total}")
    print(f"  Completed:          {completed} ({(completed/total*100):.1f}%)")
    print(f"  In Progress:        {in_progress}")
    print(f"  Pending:            {pending}")
    print(f"  High Priority Left: {high_priority}")

    completion_bar = "█" * completed + "░" * (total - completed)
    print(f"\n  Progress: [{completion_bar}] {(completed/total*100):.0f}%")

    categories = {}
    for task in tasks:
        cat = task["category"]
        categories[cat] = categories.get(cat, 0) + 1

    print("\n  TASKS BY CATEGORY:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"    {cat.upper():<15} {count} tasks")
    print("="*50)

def main():
    print("\n" + "="*50)
    print("    SMART TASK MANAGER")
    print("    Your Personal Productivity System")
    print("="*50)

    data = load_tasks()

    while True:
        pending_count = sum(1 for t in data["tasks"] if t["status"] == "pending")
        high_priority_count = sum(1 for t in data["tasks"] if t["priority"] == "high" and t["status"] != "completed")

        print(f"\nMAIN MENU  |  📋 {pending_count} pending  |  🔴 {high_priority_count} high priority")
        print("-"*45)
        print("1. Add New Task")
        print("2. View All Tasks")
        print("3. View Pending Tasks")
        print("4. View High Priority Tasks")
        print("5. Update Task Status")
        print("6. Add Note to Task")
        print("7. Delete Task")
        print("8. Productivity Statistics")
        print("9. Exit")
        print("-"*45)

        choice = input("Enter choice (1-9): ").strip()

        if choice == "1":
            add_task(data)
        elif choice == "2":
            view_all_tasks(data)
        elif choice == "3":
            view_all_tasks(data, filter_status="pending")
        elif choice == "4":
            view_all_tasks(data, filter_priority="high")
        elif choice == "5":
            update_task_status(data)
        elif choice == "6":
            add_note_to_task(data)
        elif choice == "7":
            delete_task(data)
        elif choice == "8":
            productivity_stats(data)
        elif choice == "9":
            print("\nStay productive! Goodbye.")
            break
        else:
            print("\nInvalid choice. Please enter 1-9.")

if __name__ == "__main__":
    main()
