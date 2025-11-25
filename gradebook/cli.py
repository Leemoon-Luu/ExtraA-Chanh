from typing import Optional

from .operations import (
    GradebookService,
    DuplicateCourseError,
    CourseNotFoundError,
    ValidationError,
)


def read_int(prompt: str) -> int:
    """
    Read an integer from the user, repeating until valid.
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            return value
        except ValueError:
            print("Invalid integer. Please try again.")


def read_float(prompt: str) -> float:
    """
    Read a float from the user, repeating until valid.
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            return value
        except ValueError:
            print("Invalid number. Please try again.")


def print_menu() -> None:
    """
    Print the main menu options.
    """
    print("\n===== Student Gradebook Menu =====")
    print("1. Add a course")
    print("2. Update a course")
    print("3. Delete a course")
    print("4. View gradebook")
    print("5. Calculate overall GPA")
    print("6. Calculate GPA by semester")
    print("0. Exit")
    print("==================================")


def handle_add_course(service: GradebookService) -> None:
    """
    Handle adding a new course via CLI prompts.
    """
    print("\n--- Add Course ---")
    course_code = input("Course code: ").strip()
    course_name = input("Course name: ").strip()
    credits = read_int("Number of credits: ")
    semester = input("Semester: ").strip()
    score = read_float("Score (0-10): ")

    try:
        service.add_course(course_code, course_name, credits, semester, score)
        print("Course added successfully.")
    except DuplicateCourseError as error:
        print(f"Error: {error}")
    except ValidationError as error:
        print(f"Validation error: {error}")


def handle_update_course(service: GradebookService) -> None:
    """
    Handle updating an existing course via CLI prompts.
    """
    print("\n--- Update Course ---")
    course_code = input("Course code to update: ").strip()

    try:
        existing_course = service.gradebook.get_course(course_code)
        if existing_course is None:
            raise CourseNotFoundError(f"Course with code '{course_code}' does not exist.")

        print("Leave a field empty to keep the current value.")

        new_name_raw = input(f"New course name [{existing_course.course_name}]: ").strip()
        new_name: Optional[str] = new_name_raw if new_name_raw else None

        new_credits_raw = input(f"New number of credits [{existing_course.credits}]: ").strip()
        if new_credits_raw:
            try:
                new_credits: Optional[int] = int(new_credits_raw)
            except ValueError:
                print("Invalid credits value. Update cancelled.")
                return
        else:
            new_credits = None

        new_semester_raw = input(f"New semester [{existing_course.semester}]: ").strip()
        new_semester: Optional[str] = new_semester_raw if new_semester_raw else None

        new_score_raw = input(f"New score [{existing_course.score}]: ").strip()
        if new_score_raw:
            try:
                new_score: Optional[float] = float(new_score_raw)
            except ValueError:
                print("Invalid score value. Update cancelled.")
                return
        else:
            new_score = None

        service.update_course(
            course_code=course_code,
            course_name=new_name,
            credits=new_credits,
            semester=new_semester,
            score=new_score
        )
        print("Course updated successfully.")
    except CourseNotFoundError as error:
        print(f"Error: {error}")
    except ValidationError as error:
        print(f"Validation error: {error}")


def handle_delete_course(service: GradebookService) -> None:
    """
    Handle deleting a course via CLI prompts.
    """
    print("\n--- Delete Course ---")
    course_code = input("Course code to delete: ").strip()
    try:
        service.delete_course(course_code)
        print("Course deleted successfully.")
    except CourseNotFoundError as error:
        print(f"Error: {error}")


def handle_view_gradebook(service: GradebookService) -> None:
    """
    Display all courses in a tabular format.
    """
    print("\n--- Gradebook ---")
    courses = service.list_courses()
    if not courses:
        print("No courses found.")
        return

    # Header
    header = f"{'Code':<10} {'Name':<30} {'Credits':<8} {'Semester':<10} {'Score':<6}"
    print(header)
    print("-" * len(header))

    # Rows
    for course in courses:
        print(
            f"{course.course_code:<10} "
            f"{course.course_name:<30} "
            f"{course.credits:<8} "
            f"{course.semester:<10} "
            f"{course.score:<6.2f}"
        )


def handle_overall_gpa(service: GradebookService) -> None:
    """
    Display the overall weighted GPA.
    """
    print("\n--- Overall GPA ---")
    gpa = service.calculate_overall_gpa()
    if gpa is None:
        print("No courses or total credits to compute GPA.")
    else:
        print(f"Overall GPA (0-10 scale): {gpa:.2f}")


def handle_semester_gpa(service: GradebookService) -> None:
    """
    Display the GPA for each semester.
    """
    print("\n--- GPA by Semester ---")
    semester_gpa = service.calculate_semester_gpa()
    if not semester_gpa:
        print("No semester data to compute GPA.")
        return

    for semester, gpa in sorted(semester_gpa.items()):
        print(f"Semester {semester}: {gpa:.2f}")


def main() -> None:
    """
    Entry point for the command-line gradebook application.
    """
    service = GradebookService("gradebook.json")

    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            handle_add_course(service)
        elif choice == "2":
            handle_update_course(service)
        elif choice == "3":
            handle_delete_course(service)
        elif choice == "4":
            handle_view_gradebook(service)
        elif choice == "5":
            handle_overall_gpa(service)
        elif choice == "6":
            handle_semester_gpa(service)
        elif choice == "0":
            print("Exit!")
            break
        else:
            print("Invalid option. Please select a valid menu item.")


if __name__ == "__main__":
    main()
