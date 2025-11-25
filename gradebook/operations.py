from typing import Dict, List, Optional

from .data import Gradebook, Course


class GradebookError(Exception):
    """Base class for gradebook-related errors."""


class DuplicateCourseError(GradebookError):
    """Raised when trying to add a course with an existing course code."""


class CourseNotFoundError(GradebookError):
    """Raised when a course cannot be found by its code."""


class ValidationError(GradebookError):
    """Raised when input data does not meet validation rules."""


class GradebookService:
    """
    Provides operations on a Gradebook, including validation, GPA calculations, and automatic persistence.
    """

    def __init__(self, storage_path: str = "gradebook.json") -> None:
        self.gradebook: Gradebook = Gradebook.load(storage_path)


    def _validate_course_data(
        self,
        course_code: str,
        course_name: str,
        credits: int,
        semester: str,
        score: float
    ) -> None:
        """
        Validate course data before adding or updating.
        """
        if not course_code.strip():
            raise ValidationError("Course code must not be empty.")
        if not course_name.strip():
            raise ValidationError("Course name must not be empty.")
        if not semester.strip():
            raise ValidationError("Semester must not be empty.")

        if credits <= 0:
            raise ValidationError("Credits must be a positive integer.")
        if score < 0.0 or score > 10.0:
            raise ValidationError("Score must be between 0 and 10.")


    def add_course(
        self,
        course_code: str,
        course_name: str,
        credits: int,
        semester: str,
        score: float
    ) -> None:
        """
        Add a new course to the gradebook.
        Raises DuplicateCourseError if the code already exists.
        """
        self._validate_course_data(course_code, course_name, credits, semester, score)

        if self.gradebook.get_course(course_code) is not None:
            raise DuplicateCourseError(f"Course with code '{course_code}' already exists.")

        new_course = Course(
            course_code=course_code,
            course_name=course_name,
            credits=credits,
            semester=semester,
            score=score
        )
        self.gradebook.add_course(new_course)
        self.gradebook.save()


    def update_course(
        self,
        course_code: str,
        course_name: Optional[str] = None,
        credits: Optional[int] = None,
        semester: Optional[str] = None,
        score: Optional[float] = None
    ) -> None:
        """
        Update an existing course by its code.
        Fields that are None are left unchanged.
        """
        existing_course = self.gradebook.get_course(course_code)
        if existing_course is None:
            raise CourseNotFoundError(f"Course with code '{course_code}' does not exist.")

        updated_course_name = course_name if course_name is not None else existing_course.course_name
        updated_credits = credits if credits is not None else existing_course.credits
        updated_semester = semester if semester is not None else existing_course.semester
        updated_score = score if score is not None else existing_course.score

        self._validate_course_data(
            course_code,
            updated_course_name,
            updated_credits,
            updated_semester,
            updated_score
        )

        updated_course = Course(
            course_code=course_code,
            course_name=updated_course_name,
            credits=updated_credits,
            semester=updated_semester,
            score=updated_score
        )

        self.gradebook.add_course(updated_course)
        self.gradebook.save()


    def delete_course(self, course_code: str) -> None:
        """
        Delete a course by code.
        Raises CourseNotFoundError if not found.
        """
        if self.gradebook.get_course(course_code) is None:
            raise CourseNotFoundError(f"Course with code '{course_code}' does not exist.")
        self.gradebook.remove_course(course_code)
        self.gradebook.save()


    def list_courses(self) -> List[Course]:
        """
        Return all courses in the gradebook.
        """
        return self.gradebook.get_all_courses()


    def calculate_overall_gpa(self) -> Optional[float]:
        """
        Calculate the overall weighted GPA.
        Returns None if there are no courses or total credits is zero.
        GPA is computed as sum(score * credits) / sum(credits).
        """
        courses = self.gradebook.get_all_courses()
        if not courses:
            return None

        total_weighted_score = 0.0
        total_credits = 0

        for course in courses:
            total_weighted_score += course.score * course.credits
            total_credits += course.credits

        if total_credits == 0:
            return None

        return total_weighted_score / total_credits


    def calculate_semester_gpa(self) -> Dict[str, float]:
        """
        Calculate weighted GPA for each semester.
        Returns a dictionary mapping semester -> GPA.
        """
        semester_totals: Dict[str, float] = {}
        semester_credits: Dict[str, int] = {}

        for course in self.gradebook.get_all_courses():
            if course.semester not in semester_totals:
                semester_totals[course.semester] = 0.0
                semester_credits[course.semester] = 0
            semester_totals[course.semester] += course.score * course.credits
            semester_credits[course.semester] += course.credits

        semester_gpa: Dict[str, float] = {}
        for semester, total_score in semester_totals.items():
            credits = semester_credits[semester]
            if credits > 0:
                semester_gpa[semester] = total_score / credits

        return semester_gpa
