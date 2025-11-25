import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


@dataclass
class Course:
    """Represents a single course in the gradebook."""
    course_code: str
    course_name: str
    credits: int
    semester: str
    score: float


class Gradebook:
    """
    Stores all courses in memory and provides persistence to a JSON file.
    This class does not perform business validation logic.
    """

    def __init__(self, storage_path: str) -> None:
        self.storage_path: str = storage_path
        self.courses: Dict[str, Course] = {}

    @classmethod
    def load(cls, storage_path: str) -> "Gradebook":
        """
        Load gradebook data from a JSON file.
        If the file does not exist or is corrupted, an empty gradebook is returned.
        """
        gradebook = cls(storage_path)
        try:
            with open(storage_path, "r", encoding="utf-8") as file:
                raw_data = json.load(file)

            if isinstance(raw_data, list):
                for item in raw_data:
                    try:
                        course = Course(
                            course_code=str(item["course_code"]),
                            course_name=str(item["course_name"]),
                            credits=int(item["credits"]),
                            semester=str(item["semester"]),
                            score=float(item["score"])
                        )
                        gradebook.courses[course.course_code] = course
                    except (KeyError, TypeError, ValueError):
                        # Skip invalid items
                        continue
        except FileNotFoundError:
            # No existing file: start with empty gradebook
            pass
        except json.JSONDecodeError:
            # Corrupted file: ignore contents and start empty
            pass

        return gradebook

    def save(self) -> None:
        """
        Save current gradebook data to the JSON file.
        """
        data_to_save: List[dict] = [asdict(course) for course in self.courses.values()]
        with open(self.storage_path, "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, indent=4, ensure_ascii=False)

    def add_course(self, course: Course) -> None:
        """
        Add or replace a course by its course code.
        Business logic (duplicate checking) is handled in the operations layer.
        """
        self.courses[course.course_code] = course

    def remove_course(self, course_code: str) -> None:
        """
        Remove a course from the gradebook if it exists.
        """
        if course_code in self.courses:
            del self.courses[course_code]

    def get_course(self, course_code: str) -> Optional[Course]:
        """
        Retrieve a single course by its code.
        """
        return self.courses.get(course_code)

    def get_all_courses(self) -> List[Course]:
        """
        Return all courses as a list, sorted by course code.
        """
        return sorted(self.courses.values(), key=lambda c: c.course_code)

    def get_courses_by_semester(self, semester: str) -> List[Course]:
        """
        Return all courses in a specific semester.
        """
        return [course for course in self.courses.values() if course.semester == semester]
