"""
CLI Quiz App - GitHub-ready Version
Features:
- Categories: Easy, Medium, Hard
- Random question selection per session
- Timer per question (default 15s)
- High scores saved with category
- Colored output for questions and answers
"""

import random
import json
import threading
from colorama import init, Fore, Style

init(autoreset=True)  # enables colored text

# -----------------------------
# Load questions from JSON file
# -----------------------------
def load_questions(filename="questions.json"):
    with open(filename, "r") as f:
        return json.load(f)

# -----------------------------
# Display main menu
# -----------------------------
def show_menu():
    print("\n==============================")
    print("      CLI QUIZ APP MENU        ")
    print("==============================")
    print("1) Play Quiz")
    print("2) View High Scores")
    print("3) Exit")

# -----------------------------
# Choose category
# -----------------------------
def choose_category(questions):
    categories = list({q["category"] for q in questions})
    print("\nSelect a category:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}) {cat}")
    choice = input(f"Enter 1-{len(categories)}: ")
    while not choice.isdigit() or int(choice) not in range(1, len(categories)+1):
        choice = input(f"Enter 1-{len(categories)}: ")
    return categories[int(choice)-1]

# -----------------------------
# Timed input function
# -----------------------------
def timed_input(prompt, timeout=15):
    """
    Waits for user input for 'timeout' seconds.
    Returns None if user does not answer in time.
    """
    answer = [None]

    def ask():
        answer[0] = input(prompt).upper()

    thread = threading.Thread(target=ask)
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        print(Fore.RED + "\n⏱ Time's up! No answer entered.")
        return None
    return answer[0]

# -----------------------------
# Play quiz for selected category
# -----------------------------
def play_quiz(questions, num_questions=3, time_per_question=15):
    category = choose_category(questions)
    filtered_questions = [q for q in questions if q["category"] == category]
    random.shuffle(filtered_questions)
    selected_questions = filtered_questions[:num_questions]
    score = 0

    print(f"\nYou chose category: {Fore.MAGENTA}{category}{Style.RESET_ALL}")

    for q in selected_questions:
        print("\n" + Fore.CYAN + q["question"])
        for option in q["options"]:
            print(option)

        user_answer = timed_input(f"Your answer (A/B/C/D) [{time_per_question}s]: ", timeout=time_per_question)
        if user_answer is None:
            print(Fore.RED + f"❌ Time expired! Correct answer: {q['answer']}")
            continue

        while user_answer not in ["A", "B", "C", "D"]:
            user_answer = timed_input("Please enter A, B, C, or D: ", timeout=time_per_question)
            if user_answer is None:
                print(Fore.RED + f"❌ Time expired! Correct answer: {q['answer']}")
                break

        if user_answer == q["answer"]:
            print(Fore.GREEN + "✅ Correct!")
            score += 1
        elif user_answer in ["A", "B", "C", "D"]:
            print(Fore.RED + f"❌ Wrong! Correct answer: {q['answer']}")

    print(f"\nYour final score is {score}/{len(selected_questions)}")

    # Save high score
    name = input("Enter your name to save your score: ")
    with open("scores.txt", "a") as f:
        f.write(f"{name} ({category}): {score}/{len(selected_questions)}\n")

# -----------------------------
# View high scores
# -----------------------------
def view_high_scores():
    print("\n🏆 High Scores 🏆")
    try:
        with open("scores.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("No scores yet. Play the quiz first!")

# -----------------------------
# Main program loop
# -----------------------------
def main():
    questions = load_questions("questions.json")
    while True:
        show_menu()
        choice = input("Choose an option (1-3): ")
        if choice == "1":
            play_quiz(questions, num_questions=3, time_per_question=15)
        elif choice == "2":
            view_high_scores()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
