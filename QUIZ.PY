# Interactive Quiz Game
# A multi-category quiz with scoring, timer, and performance analysis
# Author: Your Name
# Built with Python 3

import json
import os
import time
import random
from datetime import datetime

SCORES_FILE = "quiz_scores.json"

QUESTIONS = {
    "Computer Science": [
        {"question": "What does CPU stand for?", "options": ["A. Central Processing Unit", "B. Computer Processing Unit", "C. Central Program Utility", "D. Core Processing Unit"], "answer": "A", "explanation": "CPU stands for Central Processing Unit, the primary component that executes instructions."},
        {"question": "Which data structure uses LIFO principle?", "options": ["A. Queue", "B. Stack", "C. Array", "D. LinkedList"], "answer": "B", "explanation": "Stack uses Last In First Out (LIFO) - the last element added is the first to be removed."},
        {"question": "What is the time complexity of binary search?", "options": ["A. O(n)", "B. O(n²)", "C. O(log n)", "D. O(1)"], "answer": "C", "explanation": "Binary search has O(log n) complexity as it halves the search space with each step."},
        {"question": "Which language is primarily used for web styling?", "options": ["A. Python", "B. JavaScript", "C. CSS", "D. SQL"], "answer": "C", "explanation": "CSS (Cascading Style Sheets) is used to style and layout web pages."},
        {"question": "What does API stand for?", "options": ["A. Applied Programming Interface", "B. Application Programming Interface", "C. Advanced Program Integration", "D. Automated Processing Interface"], "answer": "B", "explanation": "API stands for Application Programming Interface, allowing software applications to communicate."},
    ],
    "Science": [
        {"question": "What is the chemical symbol for Gold?", "options": ["A. Go", "B. Gd", "C. Au", "D. Ag"], "answer": "C", "explanation": "Gold's symbol Au comes from the Latin word 'Aurum'."},
        {"question": "What is the speed of light approximately?", "options": ["A. 300,000 km/s", "B. 150,000 km/s", "C. 500,000 km/s", "D. 100,000 km/s"], "answer": "A", "explanation": "Light travels at approximately 299,792 km/s, rounded to 300,000 km/s."},
        {"question": "What is the powerhouse of the cell?", "options": ["A. Nucleus", "B. Ribosome", "C. Mitochondria", "D. Chloroplast"], "answer": "C", "explanation": "Mitochondria produce ATP energy for the cell through cellular respiration."},
        {"question": "What planet is known as the Red Planet?", "options": ["A. Venus", "B. Jupiter", "C. Saturn", "D. Mars"], "answer": "D", "explanation": "Mars appears red due to iron oxide (rust) on its surface."},
        {"question": "What is the atomic number of Carbon?", "options": ["A. 8", "B. 6", "C. 12", "D. 4"], "answer": "B", "explanation": "Carbon has atomic number 6, meaning it has 6 protons in its nucleus."},
    ],
    "Mathematics": [
        {"question": "What is the value of π (pi) approximately?", "options": ["A. 3.14", "B. 3.41", "C. 3.12", "D. 3.16"], "answer": "A", "explanation": "Pi (π) ≈ 3.14159... commonly rounded to 3.14"},
        {"question": "What is the square root of 144?", "options": ["A. 11", "B. 14", "C. 12", "D. 13"], "answer": "C", "explanation": "√144 = 12 because 12 × 12 = 144"},
        {"question": "What is 15% of 200?", "options": ["A. 25", "B. 30", "C. 35", "D. 40"], "answer": "B", "explanation": "15% of 200 = (15/100) × 200 = 30"},
        {"question": "What is the sum of angles in a triangle?", "options": ["A. 90°", "B. 270°", "C. 360°", "D. 180°"], "answer": "D", "explanation": "The sum of interior angles in any triangle always equals 180 degrees."},
        {"question": "What is 2^10?", "options": ["A. 512", "B. 1024", "C. 2048", "D. 256"], "answer": "B", "explanation": "2^10 = 2×2×2×2×2×2×2×2×2×2 = 1024"},
    ],
    "General Knowledge": [
        {"question": "Which is the largest ocean on Earth?", "options": ["A. Atlantic", "B. Indian", "C. Pacific", "D. Arctic"], "answer": "C", "explanation": "The Pacific Ocean is the largest, covering more than 30% of Earth's surface."},
        {"question": "Who painted the Mona Lisa?", "options": ["A. Michelangelo", "B. Vincent van Gogh", "C. Leonardo da Vinci", "D. Pablo Picasso"], "answer": "C", "explanation": "The Mona Lisa was painted by Leonardo da Vinci between 1503-1519."},
        {"question": "What is the capital of Italy?", "options": ["A. Milan", "B. Venice", "C. Rome", "D. Naples"], "answer": "C", "explanation": "Rome is the capital and largest city of Italy."},
        {"question": "How many continents are there on Earth?", "options": ["A. 5", "B. 6", "C. 7", "D. 8"], "answer": "C", "explanation": "Earth has 7 continents: Africa, Antarctica, Asia, Australia, Europe, North America, South America."},
        {"question": "Which element has the symbol 'O'?", "options": ["A. Gold", "B. Osmium", "C. Oganesson", "D. Oxygen"], "answer": "D", "explanation": "O is the chemical symbol for Oxygen, the third most abundant element in the universe."},
    ]
}

def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r") as f:
            return json.load(f)
    return {"sessions": []}

def save_scores(data):
    with open(SCORES_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_performance_rating(percentage):
    if percentage >= 90:
        return "🏆 EXCELLENT! You are a genius!"
    elif percentage >= 75:
        return "⭐ GREAT WORK! You know your stuff!"
    elif percentage >= 60:
        return "👍 GOOD JOB! Keep practicing!"
    elif percentage >= 40:
        return "📚 KEEP STUDYING! You can do better!"
    else:
        return "💪 DON'T GIVE UP! Practice makes perfect!"

def display_question(question_num, total, q_data, time_limit=30):
    print(f"\n{'='*60}")
    print(f"  Question {question_num}/{total}")
    print(f"{'='*60}")
    print(f"\n  {q_data['question']}\n")

    for option in q_data['options']:
        print(f"  {option}")

    print(f"\n  ⏱️  Time limit: {time_limit} seconds")
    print(f"{'='*60}")

    start_time = time.time()
    answer = input("  Your answer (A/B/C/D): ").strip().upper()
    elapsed = time.time() - start_time

    return answer, elapsed

def run_quiz(category, questions, time_limit, scores_data, player_name):
    random.shuffle(questions)
    selected = questions[:5]

    correct = 0
    wrong = 0
    skipped = 0
    total_time = 0
    results = []

    print(f"\n{'='*60}")
    print(f"  🎯 QUIZ: {category.upper()}")
    print(f"  Player: {player_name}")
    print(f"  Questions: {len(selected)}")
    print(f"  Time per question: {time_limit}s")
    print(f"{'='*60}")
    input("\n  Press Enter to start...")

    for i, question in enumerate(selected, 1):
        answer, elapsed = display_question(i, len(selected), question, time_limit)
        total_time += elapsed

        if elapsed > time_limit:
            print(f"\n  ⏰ TIME'S UP!")
            result = "timeout"
            skipped += 1
        elif answer == question["answer"]:
            print(f"\n  ✅ CORRECT! Well done!")
            print(f"  📖 {question['explanation']}")
            result = "correct"
            correct += 1
        elif answer in ["A", "B", "C", "D"]:
            print(f"\n  ❌ WRONG! Correct answer: {question['answer']}")
            print(f"  📖 {question['explanation']}")
            result = "wrong"
            wrong += 1
        else:
            print(f"\n  ⏭️  Invalid input — skipped")
            result = "skipped"
            skipped += 1

        results.append({
            "question": question["question"],
            "your_answer": answer,
            "correct_answer": question["answer"],
            "result": result,
            "time_taken": round(elapsed, 1)
        })

        time.sleep(1.5)

    percentage = (correct / len(selected)) * 100

    print(f"\n{'='*60}")
    print(f"  QUIZ COMPLETE!")
    print(f"{'='*60}")
    print(f"  Player:    {player_name}")
    print(f"  Category:  {category}")
    print(f"  Score:     {correct}/{len(selected)} ({percentage:.0f}%)")
    print(f"  Correct:   {correct}")
    print(f"  Wrong:     {wrong}")
    print(f"  Skipped:   {skipped}")
    print(f"  Time:      {total_time:.1f} seconds")
    print(f"\n  {get_performance_rating(percentage)}")
    print(f"{'='*60}")

    session = {
        "player": player_name,
        "category": category,
        "score": correct,
        "total": len(selected),
        "percentage": round(percentage, 1),
        "time_taken": round(total_time, 1),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "results": results
    }
    scores_data["sessions"].append(session)
    save_scores(scores_data)

    return percentage

def view_leaderboard(scores_data):
    if not scores_data["sessions"]:
        print("\nNo quiz sessions found.")
        return

    print(f"\n{'='*70}")
    print(f"  🏆 LEADERBOARD — ALL TIME HIGH SCORES")
    print(f"{'='*70}")
    print(f"{'Rank':<6} {'Player':<20} {'Category':<20} {'Score':<10} {'%':<8} {'Date'}")
    print("-"*70)

    sorted_sessions = sorted(scores_data["sessions"], key=lambda x: x["percentage"], reverse=True)

    for i, session in enumerate(sorted_sessions[:10], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
        print(f"{medal:<6} {session['player']:<20} {session['category']:<20} {session['score']}/{session['total']:<6} {session['percentage']:<8.1f}% {session['date']}")
    print("="*70)

def player_stats(scores_data, player_name):
    player_sessions = [s for s in scores_data["sessions"] if s["player"].lower() == player_name.lower()]

    if not player_sessions:
        print(f"\nNo records found for {player_name}.")
        return

    percentages = [s["percentage"] for s in player_sessions]

    print(f"\n{'='*55}")
    print(f"  PLAYER STATS — {player_name.upper()}")
    print(f"{'='*55}")
    print(f"  Total Quizzes:    {len(player_sessions)}")
    print(f"  Average Score:    {sum(percentages)/len(percentages):.1f}%")
    print(f"  Best Score:       {max(percentages):.1f}%")
    print(f"  Worst Score:      {min(percentages):.1f}%")

    print(f"\n  PERFORMANCE BY CATEGORY:")
    categories = {}
    for s in player_sessions:
        cat = s["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(s["percentage"])

    for cat, scores_list in categories.items():
        avg = sum(scores_list)/len(scores_list)
        print(f"    {cat:<22} Avg: {avg:.1f}%  ({len(scores_list)} attempts)")
    print("="*55)

def main():
    print("\n" + "="*60)
    print("    🎮 INTERACTIVE QUIZ GAME")
    print("    Test Your Knowledge Across Multiple Categories")
    print("="*60)

    player_name = input("\n  Enter your name: ").strip()
    if not player_name:
        player_name = "Player"

    scores_data = load_scores()
    time_limit = 30

    while True:
        print(f"\n  Welcome, {player_name}!")
        print("\nMAIN MENU")
        print("-"*40)
        print("1. Start Quiz — Computer Science")
        print("2. Start Quiz — Science")
        print("3. Start Quiz — Mathematics")
        print("4. Start Quiz — General Knowledge")
        print("5. Start Random Category Quiz")
        print("6. View Leaderboard")
        print("7. View My Stats")
        print("8. Change Time Limit (Current: {}s)".format(time_limit))
        print("9. Exit")
        print("-"*40)

        choice = input("Enter choice (1-9): ").strip()

        if choice == "1":
            run_quiz("Computer Science", QUESTIONS["Computer Science"].copy(), time_limit, scores_data, player_name)
        elif choice == "2":
            run_quiz("Science", QUESTIONS["Science"].copy(), time_limit, scores_data, player_name)
        elif choice == "3":
            run_quiz("Mathematics", QUESTIONS["Mathematics"].copy(), time_limit, scores_data, player_name)
        elif choice == "4":
            run_quiz("General Knowledge", QUESTIONS["General Knowledge"].copy(), time_limit, scores_data, player_name)
        elif choice == "5":
            random_category = random.choice(list(QUESTIONS.keys()))
            print(f"\n  🎲 Random category selected: {random_category}")
            run_quiz(random_category, QUESTIONS[random_category].copy(), time_limit, scores_data, player_name)
        elif choice == "6":
            view_leaderboard(scores_data)
        elif choice == "7":
            player_stats(scores_data, player_name)
        elif choice == "8":
            try:
                new_limit = int(input("Enter new time limit in seconds (10-120): "))
                if 10 <= new_limit <= 120:
                    time_limit = new_limit
                    print(f"✓ Time limit updated to {time_limit} seconds")
                else:
                    print("Please enter a value between 10 and 120.")
            except ValueError:
                print("Please enter a valid number.")
        elif choice == "9":
            print(f"\n  Thanks for playing, {player_name}! Goodbye! 🎮")
            break
        else:
            print("\nInvalid choice. Please enter 1-9.")

if __name__ == "__main__":
    main()
