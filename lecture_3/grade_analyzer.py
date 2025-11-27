students = []  # List of dictionaries: each dict has 'name' (str) and 'grades' (list)


def intro():
    """Print the main menu options."""
    print("--- Student Grade Analyzer ---\n"
          "1. Add a new student\n"
          "2. Add a grades for a student\n"
          "3. Show report (all students)\n"
          "4. Find top performer\n5. Exit")


def main():
    """
    Main loop of the program. Displays menu, handles user input,
    and calls corresponding functions based on choice.
    """

    while True:
        intro()

        # Input validation loop
        while True:
            choice = input("Enter your choice: ").strip()  # type: str

            try:
                choice_num = int(choice)  # type: int
                if 1 <= choice_num <= 5:
                    break
                else:
                    print("Please enter a number from 1 to 5.\n")
            except ValueError:
                print("Invalid input. Please enter a digit from 1 to 5.\n")

        match choice_num:
            case 1:
                create_student()
            case 2:
                add_grades()
            case 3:
                show_report()
            case 4:
                top_performer()
            case 5:
                break


def create_student():
    """
    Adds a new student to the global students list.
    Validates that the name contains only letters, spaces, or hyphens,
    is not empty, and does not already exist in the list.
    """

    while True:
        name = input("Enter student name: ").strip()  # type: str

        try:
            # Check each character
            for ch in name:
                if not (ch.isalpha() or ch in (" ", "-")):
                    raise ValueError("Name contains invalid characters")

            if name == "":
                raise ValueError("Name cannot be empty")

            # Check for duplicates
            for student in students:
                if student["name"].lower() == name.lower():
                    raise ValueError("Student with this name already exists")

            # Valid name, exit loop
            break

        except ValueError as e:
            print(f"Invalid name: {e}. Use letters only (spaces and hyphens allowed).")

    student_data = {"name": name, "grades": []}  # type: dict
    students.append(student_data)


def add_grades():
    """
    Adds grades for an existing student.
    Prompts user for student name, verifies existence,
    then repeatedly asks for grades (0-100) until 'done' is entered.
    """

    student_name = input("Enter a student name: ").strip()  # type: str

    # student search
    student = None  # type: dict or None
    for s in students:
        if s["name"].lower() == student_name.lower():
            student = s
            break

    if student is None:
        print("There is no student with that name on the list. Add the student first.")
        return  # end the function

    # enter grades
    while True:
        grade_input = input("Enter a grade (or 'done' to finish): ").strip()  # type: str

        if grade_input.lower() == "done":
            return

        try:
            grade = int(grade_input)
            if not (0 <= grade <= 100):
                raise ValueError("Grade must be from 0 to 100")

            student["grades"].append(grade)

        except ValueError as e:
            print(f"Invalid input: {e}. Try again.")


def show_report():
    """
    Prints the report for all students, showing their average grades.
    Handles ZeroDivisionError if a student has no grades.
    Calculates and displays max, min, and overall average grade.
    """

    if not students:
        print("There are no students in the list.")
        return

    # list of averages only for students with grades
    averages = []  # type: list

    # all grades of all students
    all_grades = []  # type: list

    for student in students:
        grades = student["grades"]  # type: list

        try:
            if len(grades) == 0:
                raise ZeroDivisionError

            avg = sum(grades) / len(grades)
            averages.append(avg)
            all_grades.extend(grades)

            print(f"{student['name'].title()}'s average grade is {avg:.2f}")

        except ZeroDivisionError:
            print(f"{student['name'].title()}'s average grade is N/A")

    print()

    # Check: is there even one rating at all
    if not all_grades:
        print("No grades available for any student.\n")
        return

    # Calculate statistics
    max_avg = max(averages)
    min_avg = min(averages)
    overall_avg = sum(all_grades) / len(all_grades)

    print(f"Max average: {max_avg:.2f}")
    print(f"Min average: {min_avg:.2f}")
    print(f"Overall average grade: {overall_avg:.2f}\n")


def top_performer():
    """
    Finds the student(s) with the highest average grade.
    Handles cases with no students or no grades.
    Prints all students who share the top average.
    """

    if not students:
        print("No students in the list.\n")
        return

    # create a list of students with at least one grade
    students_with_grades = [s for s in students if s["grades"]]

    if not students_with_grades:
        print("No grades available for any student.\n")
        return

    # Find the student with the maximum average
    max_avg = max(
        students_with_grades,
        key=lambda s: sum(s["grades"]) / len(s["grades"])
    )

    # calculate max_average itself
    max_average_value = sum(max_avg["grades"]) / len(max_avg["grades"])

    # Find all students with the same max average
    top_students = [
        s for s in students_with_grades
        if sum(s["grades"]) / len(s["grades"]) == max_average_value
    ]

    # Display the result
    print("\nTop performer(s):")
    for s in top_students:
        print(f"{s['name'].title()} with average grade {max_average_value:.2f}")
    print()


main()
