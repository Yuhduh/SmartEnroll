"""
Academic Year Model - Handles school year and semester management
"""
from dataclasses import dataclass
from typing import Optional, List, Tuple
from datetime import date


@dataclass
class AcademicYearData:
    """Academic year data blueprint"""
    id: Optional[int] = None
    year_name: str = ""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    semester: str = "Full Year"
    is_active: bool = False

    def is_valid(self) -> bool:
        """Validate academic year data"""
        return bool(
            self.year_name and
            self.start_date and
            self.end_date and
            self.start_date < self.end_date
        )

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'year_name': self.year_name,
            'start_date': str(self.start_date) if self.start_date else None,
            'end_date': str(self.end_date) if self.end_date else None,
            'semester': self.semester,
            'is_active': self.is_active
        }


class AcademicYear:
    """Academic Year model - Database operations"""

    def __init__(self, db):
        self.db = db

    def get_all_years(self) -> List[dict]:
        """Get all academic years"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                    SELECT id, year_name, start_date, end_date, semester, is_active
                    FROM academic_years
                    ORDER BY start_date DESC \
                    """
            cursor.execute(query)
            years = cursor.fetchall()
            cursor.close()
            return years
        except Exception as e:
            print(f"Error getting academic years: {e}")
            return []

    def get_active_year(self) -> Optional[dict]:
        """Get the currently active academic year"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                    SELECT id, year_name, start_date, end_date, semester, is_active
                    FROM academic_years
                    WHERE is_active = TRUE LIMIT 1 \
                    """
            cursor.execute(query)
            year = cursor.fetchone()
            cursor.close()
            return year
        except Exception as e:
            print(f"Error getting active year: {e}")
            return None

    def add_year(self, year_name: str, start_date: date, end_date: date,
                 semester: str = "Full Year") -> Tuple[bool, str]:
        """Add a new academic year"""
        try:
            cursor = self.db.cursor()

            # Check if year already exists
            cursor.execute("SELECT id FROM academic_years WHERE year_name = %s", (year_name,))
            if cursor.fetchone():
                cursor.close()
                return False, f"Academic year '{year_name}' already exists"

            # Insert new year (inactive by default)
            query = """
                    INSERT INTO academic_years (year_name, start_date, end_date, semester, is_active)
                    VALUES (%s, %s, %s, %s, FALSE) \
                    """
            cursor.execute(query, (year_name, start_date, end_date, semester))
            self.db.commit()
            cursor.close()

            return True, "Academic year added successfully"

        except Exception as e:
            print(f"Error adding academic year: {e}")
            return False, f"Failed to add academic year: {str(e)}"

    def set_active_year(self, year_id: int) -> Tuple[bool, str]:
        """Set a year as active (deactivates all others)"""
        try:
            cursor = self.db.cursor()

            # Deactivate all years
            cursor.execute("UPDATE academic_years SET is_active = FALSE")

            # Activate selected year
            cursor.execute("UPDATE academic_years SET is_active = TRUE WHERE id = %s", (year_id,))

            self.db.commit()
            cursor.close()

            return True, "Active academic year updated"

        except Exception as e:
            print(f"Error setting active year: {e}")
            return False, f"Failed to set active year: {str(e)}"

    def delete_year(self, year_id: int) -> Tuple[bool, str]:
        """Delete an academic year"""
        try:
            cursor = self.db.cursor()

            # Check if year has students
            cursor.execute("SELECT COUNT(*) FROM students WHERE academic_year_id = %s", (year_id,))
            student_count = cursor.fetchone()[0]

            if student_count > 0:
                cursor.close()
                return False, f"Cannot delete: {student_count} students enrolled in this academic year"

            # Check if it's the active year
            cursor.execute("SELECT is_active FROM academic_years WHERE id = %s", (year_id,))
            result = cursor.fetchone()
            if result and result[0]:
                cursor.close()
                return False, "Cannot delete the active academic year"

            # Delete year
            cursor.execute("DELETE FROM academic_years WHERE id = %s", (year_id,))
            self.db.commit()
            cursor.close()

            return True, "Academic year deleted successfully"

        except Exception as e:
            print(f"Error deleting academic year: {e}")
            return False, f"Failed to delete academic year: {str(e)}"

    def get_year_stats(self, year_id: int) -> dict:
        """Get statistics for a specific academic year"""
        try:
            cursor = self.db.cursor(dictionary=True)

            # Total students
            cursor.execute("""
                           SELECT COUNT(*) as total_students
                           FROM students
                           WHERE academic_year_id = %s
                             AND status = 'Enrolled'
                           """, (year_id,))
            stats = cursor.fetchone()

            # By strand
            cursor.execute("""
                           SELECT strand, COUNT(*) as count
                           FROM students
                           WHERE academic_year_id = %s AND status = 'Enrolled'
                           GROUP BY strand
                           """, (year_id,))
            by_strand = cursor.fetchall()

            cursor.close()

            return {
                'total_students': stats['total_students'],
                'by_strand': by_strand
            }

        except Exception as e:
            print(f"Error getting year stats: {e}")
            return {'total_students': 0, 'by_strand': []}