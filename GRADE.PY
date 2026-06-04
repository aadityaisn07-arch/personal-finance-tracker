# Student Grade Analyzer
# Analyzes student performance and generates detailed reports
# Author: Your Name
# Built with Python 3

import json
import os
import statistics
from datetime import datetime

DATA_FILE = "students.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"students": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_grade_letter(percentage):
    if percentage >= 90:
        return "A+", "Outstanding"
    elif percentage >= 80:
        return "A", "Excellent"
    elif percentage >= 70:
        return "B", "Good"
    elif percentage >= 60:
        return "C", "Average"
    elif percentage >= 50:
        return "D", "Below Average"
    else:
        return "F", "Fail"

def add_student(data):
    print("\n--- ADD NEW STUDENT ---")
    name = input("Student Name: ").strip()
    roll = input("Roll Number: ").strip()

    subjects = {}
    print("\nEnter marks for each subject (out of 100):")
    subject_list = ["Mathematics", "Physics", "Chemistry", "English", "Computer Science"]

    for subject in subject_list:
        while True:
            try:
                marks = float(input(f"  {subject}: "))
                if 0 <= marks <= 100:
                    subjects[subject] = marks
                    break
                else:
                    print("  Please enter marks between 0 and 100")
            except ValueError:
                print("  Please enter a valid number")

    total = sum(subjects.values())
    percentage = total / len(subjects)
    grade_letter, grade_desc = get_grade_letter(percentage)

    student = {
        "name": name,
        "roll": roll,
        "subjects": subjects,
        "total": total,
        "percentage": round(percentage, 2),
        "grade": grade_letter,
        "grade_description": grade_desc,
        "date_added": datetime.now().strftime("%Y-%m-%d")
    }

    data["students"].append(student)
    save_data(data)

    print(f"\n✓ Student {name} added successfully!")
    print(f"  Percentage: {percentage:.2f}%")
    print(f"  Grade: {grade_letter} - {grade_desc}")

def view_all_students(data):
    if not data["students"]:
        print("\nNo students found.")
        return

    print("\n" + "="*80)
    print(f"{'Roll':<10} {'Name':<20} {'Total':<10} {'Percentage':<15} {'Grade':<10} {'Result'}")
    print("="*80)

    for s in sorted(data["students"], key=lambda x: x["percentage"], reverse=True):
        result = "PASS" if s["percentage"] >= 50 else "FAIL"
        print(f"{s['roll']:<10} {s['name']:<20} {s['total']:<10.1f} {s['percentage']:<15.2f}% {s['grade']:<10} {result}")
    print("="*80)

def view_student_detail(data):
    roll = input("\nEnter Roll Number: ").strip()
    student = next((s for s in data["students"] if s["roll"] == roll), None)

    if not student:
        print(f"Student with roll number {roll} not found.")
        return

    print("\n" + "="*50)
    print(f"  STUDENT REPORT CARD")
    print("="*50)
    print(f"  Name:       {student['name']}")
    print(f"  Roll No:    {student['roll']}")
    print(f"  Date:       {student['date_added']}")
    print("-"*50)
    print("  SUBJECT WISE MARKS")
    print("-"*50)

    for subject, marks in student["subjects"].items():
        bar = "█" * int(marks / 5)
        status = "✓" if marks >= 50 else "✗"
        print(f"  {status} {subject:<20} {marks:>6.1f}/100  {bar}")

    print("-"*50)
    print(f"  Total Marks:    {student['total']:.1f}/{len(student['subjects']) * 100}")
    print(f"  Percentage:     {student['percentage']:.2f}%")
    print(f"  Grade:          {student['grade']} - {student['grade_description']}")
    print(f"  Result:         {'PASS ✓' if student['percentage'] >= 50 else 'FAIL ✗'}")
    print("="*50)

def class_statistics(data):
    if not data["students"]:
        print("\nNo students found.")
        return

    percentages = [s["percentage"] for s in data["students"]]
    passed = [s for s in data["students"] if s["percentage"] >= 50]

    print("\n" + "="*50)
    print("  CLASS STATISTICS")
    print("="*50)
    print(f"  Total Students:    {len(data['students'])}")
    print(f"  Passed:            {len(passed)}")
    print(f"  Failed:            {len(data['students']) - len(passed)}")
    print(f"  Pass Percentage:   {(len(passed)/len(data['students'])*100):.1f}%")
    print("-"*50)
    print(f"  Highest Score:     {max(percentages):.2f}%")
    print(f"  Lowest Score:      {min(percentages):.2f}%")
    print(f"  Class Average:     {statistics.mean(percentages):.2f}%")
    print(f"  Median Score:      {statistics.median(percentages):.2f}%")

    if len(percentages) > 1:
        print(f"  Std Deviation:     {statistics.stdev(percentages):.2f}")

    topper = max(data["students"], key=lambda x: x["percentage"])
    print(f"\n  Class Topper:      {topper['name']} ({topper['percentage']:.2f}%)")
    print("="*50)

def subject_analysis(data):
    if not data["students"]:
        print("\nNo students found.")
        return

    subjects = list(data["students"][0]["subjects"].keys()) if data["students"] else []

    print("\n" + "="*60)
    print("  SUBJECT-WISE ANALYSIS")
    print("="*60)
    print(f"{'Subject':<25} {'Average':<12} {'Highest':<12} {'Lowest':<10} {'Pass%'}")
    print("-"*60)

    for subject in subjects:
        marks_list = [s["subjects"][subject] for s in data["students"]]
        passed_sub = sum(1 for m in marks_list if m >= 50)
        print(f"{subject:<25} {statistics.mean(marks_list):<12.1f} {max(marks_list):<12.1f} {min(marks_list):<10.1f} {(passed_sub/len(marks_list)*100):.1f}%")
    print("="*60)

def main():
    print("\n" + "="*50)
    print("    STUDENT GRADE ANALYZER")
    print("    Academic Performance System")
    print("="*50)

    data = load_data()

    while True:
        print("\nMAIN MENU")
        print("-"*35)
        print("1. Add New Student")
        print("2. View All Students")
        print("3. View Student Detail Report")
        print("4. Class Statistics")
        print("5. Subject-wise Analysis")
        print("6. Exit")
        print("-"*35)

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            add_student(data)
        elif choice == "2":
            view_all_students(data)
        elif choice == "3":
            view_student_detail(data)
        elif choice == "4":
            class_statistics(data)
        elif choice == "5":
            subject_analysis(data)
        elif choice == "6":
            print("\nExiting Grade Analyzer. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter 1-6.")

if __name__ == "__main__":
    main()
