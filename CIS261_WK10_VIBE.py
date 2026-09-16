#Cheree Gardenhire-Givens
#CIS261
#WK10 VIBE Coding

"""Student Grade Calculator.

The program stores student records as dictionaries in a list and persists
them in a pipe-delimited text file.
"""

import os
import sys
import termios
import tty


FILE_NAME = "student_grades.txt"


def calculate_average(test1, test2, test3):
	"""Return the average of three test scores."""
	return (test1 + test2 + test3) / 3


def calculate_grade(average):
	"""Return a letter grade based on an average score."""
	if average >= 90:
		return "A"
	if average >= 80:
		return "B"
	if average >= 70:
		return "C"
	if average >= 60:
		return "D"
	return "F"


def load_students():
	"""Load valid student records from the data file."""
	students = []

	if not os.path.exists(FILE_NAME):
		return students

	try:
		with open(FILE_NAME, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				line = line.strip()
				if not line:
					continue

				fields = line.split("|")
				if len(fields) != 7:
					print(f"Warning: Skipping invalid record on line {line_number}.")
					continue

				try:
					test1 = float(fields[2])
					test2 = float(fields[3])
					test3 = float(fields[4])
					average = float(fields[5])
				except ValueError:
					print(f"Warning: Skipping invalid scores on line {line_number}.")
					continue

				students.append({
					"name": fields[0],
					"id": fields[1],
					"test1": test1,
					"test2": test2,
					"test3": test3,
					"average": average,
					"grade": fields[6],
				})
	except OSError as error:
		print(f"Error loading student records: {error}")

	return students


def save_students(students):
	"""Save all student records in the required pipe-delimited format."""
	try:
		with open(FILE_NAME, "w", encoding="utf-8") as file:
			for student in students:
				file.write(
					f"{student['name']}|{student['id']}|"
					f"{student['test1']:.2f}|{student['test2']:.2f}|"
					f"{student['test3']:.2f}|{student['average']:.2f}|"
					f"{student['grade']}\n"
				)
		return True
	except OSError as error:
		print(f"Error saving student records: {error}")
		return False


def get_score(test_number):
	"""Prompt until the user enters a score from 0 through 100."""
	while True:
		try:
			score = float(input(f"Enter Test {test_number} score (0-100): ").strip())
			if 0 <= score <= 100:
				return score
			print("Please enter a score between 0 and 100.")
		except ValueError:
			print("Please enter a valid number.")


def add_student(students):
	"""Prompt for and append one student record."""
	print("\nAdd Student")
	name = input("Enter student name: ").strip()
	while not name:
		print("Student name cannot be blank.")
		name = input("Enter student name: ").strip()

	student_id = input("Enter student ID: ").strip()
	while not student_id:
		print("Student ID cannot be blank.")
		student_id = input("Enter student ID: ").strip()

	test1 = get_score(1)
	test2 = get_score(2)
	test3 = get_score(3)
	average = calculate_average(test1, test2, test3)

	students.append({
		"name": name,
		"id": student_id,
		"test1": test1,
		"test2": test2,
		"test3": test3,
		"average": average,
		"grade": calculate_grade(average),
	})
	print(f"Student added. Average: {average:.2f}, Grade: {calculate_grade(average)}")


def display_students(students):
	"""Display all student records in a formatted table."""
	if not students:
		print("\nNo student records found.")
		return

	print("\nStudent Records")
	print("-" * 91)
	print(
		f"{'Name':<22}{'ID':<14}{'Test 1':>9}{'Test 2':>9}"
		f"{'Test 3':>9}{'Average':>11}{'Grade':>8}"
	)
	print("-" * 91)
	for student in students:
		print(
			f"{student['name'][:21]:<22}{student['id'][:13]:<14}"
			f"{student['test1']:>9.2f}{student['test2']:>9.2f}"
			f"{student['test3']:>9.2f}{student['average']:>11.2f}"
			f"{student['grade']:>8}"
		)
	print("-" * 91)


def display_statistics(students):
	"""Display highest, lowest, and overall class averages."""
	if not students:
		print("\nNo student records available for statistics.")
		return

	averages = [student["average"] for student in students]
	highest = max(averages)
	lowest = min(averages)
	class_average = sum(averages) / len(averages)
	print("\nClass Statistics")
	print(f"Highest average: {highest:.2f}")
	print(f"Lowest average:  {lowest:.2f}")
	print(f"Class average:   {class_average:.2f}")


def search_student(students):
	"""Find and display students whose names match the search text."""
	search_name = input("\nEnter student name to search: ").strip().lower()
	matches = [
		student for student in students
		if search_name in student["name"].lower()
	]

	if not matches:
		print("No matching students found.")
		return

	display_students(matches)


def display_menu():
	"""Display the main menu."""
	print("\nStudent Grade Calculator")
	print("1. Add New Student")
	print("2. Display All Students")
	print("3. Search Student by Name")
	print("4. View Class Statistics")
	print("5. Save and Exit")
	print("Press the ESC key at any time at the menu to save and exit")


def get_menu_choice():
	"""Read a menu choice and detect a physical ESC key immediately."""
	if not sys.stdin.isatty():
		choice = input("\nSelect an option: ")
		return choice.strip().lower()

	print("\nSelect an option: ", end="", flush=True)
	file_descriptor = sys.stdin.fileno()
	original_settings = termios.tcgetattr(file_descriptor)
	characters = []

	try:
		tty.setcbreak(file_descriptor)
		while True:
			character = sys.stdin.read(1)
			if character == "\x1b":
				print()
				return "\x1b"
			if character in ("\n", "\r"):
				print()
				return "".join(characters).strip().lower()
			if character in ("\x08", "\x7f"):
				if characters:
					characters.pop()
					print("\b \b", end="", flush=True)
				continue
			characters.append(character)
			print(character, end="", flush=True)
	finally:
		termios.tcsetattr(file_descriptor, termios.TCSADRAIN, original_settings)


def main():
	"""Run the student grade calculator."""
	students = load_students()
	print(f"Loaded {len(students)} student record(s).")

	while True:
		display_menu()
		try:
			choice = get_menu_choice()
		except (EOFError, KeyboardInterrupt):
			print("\nExiting program.")
			save_students(students)
			break

		if choice in ("\x1b", "esc", "exit"):
			if save_students(students):
				print(f"Saved {len(students)} student record(s). Goodbye!")
			break
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			search_student(students)
		elif choice == "4":
			display_statistics(students)
		elif choice == "5":
			if save_students(students):
				print(f"Saved {len(students)} student record(s). Goodbye!")
			break
		else:
			print("Invalid option. Please choose 1, 2, 3, 4, 5, or ESC.")


if __name__ == "__main__":
	main()