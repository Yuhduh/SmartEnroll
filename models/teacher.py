"""
Teacher Model - Handles all teacher-related database operations
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, List, Tuple, Dict


@dataclass
class TeacherData:
    """Teacher data model"""
    id: Optional[int] = None
    full_name: str = ""
    email: str = ""
    contact_number: str = ""
    specialization: str = ""
    department: str = ""
    hire_date: Optional[date] = None
    status: str = "Active"
    created_at: Optional[datetime] = None

    def is_valid(self) -> bool:
        """Validate teacher data"""
        return bool(
            self.full_name and
            self.email and
            self.contact_number and
            self.specialization
        )

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'contact_number': self.contact_number,
            'specialization': self.specialization,
            'department': self.department,
            'hire_date': self.hire_date,
            'status': self.status,
            'created_at': self.created_at
        }


class Teacher:
    """Teacher model - Database operations for teachers"""

    def __init__(self, db):
        self.db = db

    def get_all_teachers(self) -> List[Dict]:
        """Get all teachers"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT id, full_name, email, contact_number, 
                       department, specialization, hire_date, status, created_at
                FROM teachers
                ORDER BY full_name
            """
            cursor.execute(query)
            teachers = cursor.fetchall()
            cursor.close()
            return teachers

        except Exception as e:
            print(f"Error getting teachers: {e}")
            return []

    def get_teacher_by_id(self, teacher_id: int) -> Optional[TeacherData]:
        """Get teacher by ID"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = "SELECT * FROM teachers WHERE id = %s"
            cursor.execute(query, (teacher_id,))
            row = cursor.fetchone()
            cursor.close()

            if row:
                return TeacherData(**row)
            return None

        except Exception as e:
            print(f"Error getting teacher: {e}")
            return None

    def add_teacher(self, name: str, email: str, contact: str, specialization: str, department: str = "") -> Tuple[bool, str]:
        """Add a new teacher"""
        try:
            cursor = self.db.cursor()

            # Check if email already exists
            cursor.execute("SELECT id FROM teachers WHERE email = %s", (email,))
            if cursor.fetchone():
                cursor.close()
                return False, "A teacher with this email already exists"

            # Insert new teacher
            query = """
                INSERT INTO teachers (full_name, email, contact_number, department,
                                    specialization, hire_date, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, 'Active', NOW())
            """
            cursor.execute(query, (name, email, contact, department, specialization, date.today()))
            self.db.commit()
            cursor.close()

            return True, "Teacher added successfully"

        except Exception as e:
            print(f"Error adding teacher: {e}")
            return False, f"Failed to add teacher: {str(e)}"

    def delete_teacher(self, teacher_id: int) -> Tuple[bool, str]:
        """Delete a teacher"""
        try:
            cursor = self.db.cursor()

            # Check if teacher is assigned to any section
            cursor.execute(
                "SELECT COUNT(*) FROM sections WHERE teacher_id = %s OR adviser_id = %s",
                (teacher_id, teacher_id)
            )
            count = cursor.fetchone()[0]

            if count > 0:
                cursor.close()
                return False, f"Cannot delete: Teacher is assigned to {count} section(s). Please reassign first."

            # Delete teacher
            cursor.execute("DELETE FROM teachers WHERE id = %s", (teacher_id,))
            self.db.commit()
            cursor.close()

            return True, "Teacher deleted successfully"

        except Exception as e:
            print(f"Error deleting teacher: {e}")
            return False, f"Failed to delete teacher: {str(e)}"

    def update_teacher(self, teacher_id: int, name: str, email: str, contact: str, 
                      specialization: str, department: str = "") -> Tuple[bool, str]:
        """Update teacher details"""
        try:
            cursor = self.db.cursor()

            query = """
                UPDATE teachers 
                SET full_name = %s, email = %s, contact_number = %s, 
                    department = %s, specialization = %s
                WHERE id = %s
            """
            cursor.execute(query, (name, email, contact, department, specialization, teacher_id))
            self.db.commit()
            cursor.close()

            return True, "Teacher updated successfully"

        except Exception as e:
            print(f"Error updating teacher: {e}")
            return False, f"Failed to update teacher: {str(e)}"

    def get_available_teachers(self) -> List[Dict]:
        """Get teachers that are not assigned to any active section"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT t.id, t.full_name, t.specialization
                FROM teachers t
                LEFT JOIN sections s ON (t.id = s.teacher_id OR t.id = s.adviser_id) 
                                     AND s.status = 'Active'
                WHERE t.status = 'Active' AND s.id IS NULL
                ORDER BY t.full_name
            """
            cursor.execute(query)
            teachers = cursor.fetchall()
            cursor.close()
            return teachers

        except Exception as e:
            print(f"Error getting available teachers: {e}")
            return []

    def get_teacher_sections(self, teacher_id: int) -> List[Dict]:
        """Get all sections assigned to a teacher"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT id, section_name, strand, capacity
                FROM sections
                WHERE (teacher_id = %s OR adviser_id = %s) AND status = 'Active'
                ORDER BY section_name
            """
            cursor.execute(query, (teacher_id, teacher_id))
            sections = cursor.fetchall()
            cursor.close()
            return sections

        except Exception as e:
            print(f"Error getting teacher sections: {e}")
            return []