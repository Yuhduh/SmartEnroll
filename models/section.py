"""
Section Model - Handles all section-related database operations
"""
from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass
class SectionData:
    """Section data blueprint"""
    id: Optional[int] = None
    section_name: str = ""
    strand: str = ""
    track: str = "Academic"
    capacity: int = 40
    student_count: int = 0
    room_number: Optional[str] = None
    teacher_id: Optional[int] = None
    teacher_name: Optional[str] = None
    adviser_id: Optional[int] = None
    adviser_name: Optional[str] = None
    adviser_email: Optional[str] = None
    status: str = "Active"

    @property
    def available_slots(self) -> int:
        """Calculate available slots"""
        return self.capacity - self.student_count

    @property
    def is_full(self) -> bool:
        """Check if section is full"""
        return self.student_count >= self.capacity

    @property
    def fill_percentage(self) -> float:
        """Get fill percentage"""
        if self.capacity == 0:
            return 0.0
        return (self.student_count / self.capacity) * 100

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'section_name': self.section_name,
            'strand': self.strand,
            'track': self.track,
            'capacity': self.capacity,
            'student_count': self.student_count,
            'available_slots': self.available_slots,
            'room_number': self.room_number,
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher_name,
            'adviser_id': self.adviser_id,
            'adviser_name': self.adviser_name,
            'adviser_email': self.adviser_email,
            'status': self.status,
            'is_full': self.is_full,
            'fill_percentage': self.fill_percentage
        }


class Section:
    """Section model - Database operations for sections/classrooms"""

    def __init__(self, db):
        self.db = db

    def get_all_sections(self) -> List[SectionData]:
        """Get all active sections with details"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                    SELECT s.id,
                           s.section_name,
                           s.strand,
                           s.track,
                           s.capacity,
                           s.room_number,
                           s.status,
                           s.teacher_id,
                           s.adviser_id,
                           t.full_name   AS teacher_name,
                           adv.full_name AS adviser_name,
                           adv.email     AS adviser_email,
                           COUNT(st.id)  AS student_count
                    FROM sections s
                             LEFT JOIN teachers t ON s.teacher_id = t.id
                             LEFT JOIN teachers adv ON s.adviser_id = adv.id
                             LEFT JOIN students st ON st.section_id = s.id AND st.status = 'Enrolled'
                    WHERE s.status = 'Active'
                    GROUP BY s.id, s.section_name, s.strand, s.track, s.capacity,
                             s.room_number, s.status, s.teacher_id, s.adviser_id,
                             t.full_name, adv.full_name, adv.email
                    ORDER BY s.strand, s.section_name \
                    """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()

            return [SectionData(**row) for row in rows]

        except Exception as e:
            print(f"Error getting sections: {e}")
            return []

    def get_section_by_id(self, section_id: int) -> Optional[SectionData]:
        """Get section by ID"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                    SELECT s.id,
                           s.section_name,
                           s.strand,
                           s.track,
                           s.capacity,
                           s.room_number,
                           s.status,
                           s.teacher_id,
                           s.adviser_id,
                           t.full_name   AS teacher_name,
                           adv.full_name AS adviser_name,
                           adv.email     AS adviser_email,
                           COUNT(st.id)  AS student_count
                    FROM sections s
                             LEFT JOIN teachers t ON s.teacher_id = t.id
                             LEFT JOIN teachers adv ON s.adviser_id = adv.id
                             LEFT JOIN students st ON st.section_id = s.id AND st.status = 'Enrolled'
                    WHERE s.id = %s
                    GROUP BY s.id \
                    """
            cursor.execute(query, (section_id,))
            row = cursor.fetchone()
            cursor.close()

            if row:
                return SectionData(**row)
            return None

        except Exception as e:
            print(f"Error getting section: {e}")
            return None

    def get_sections_by_strand(self, strand: str, status: str = 'Active') -> List[SectionData]:
        """Get sections filtered by strand"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                    SELECT s.id,
                           s.section_name,
                           s.strand,
                           s.capacity,
                           s.room_number,
                           COUNT(st.id) AS student_count
                    FROM sections s
                             LEFT JOIN students st ON st.section_id = s.id AND st.status = 'Enrolled'
                    WHERE s.strand = %s \
                      AND s.status = %s
                    GROUP BY s.id, s.section_name, s.strand, s.capacity, s.room_number
                    ORDER BY s.section_name \
                    """
            cursor.execute(query, (strand, status))
            rows = cursor.fetchall()
            cursor.close()

            return [SectionData(**row) for row in rows]

        except Exception as e:
            print(f"Error getting sections by strand: {e}")
            return []

    def find_available_section(self, strand: str) -> Optional[SectionData]:
        """Find best available section for a strand"""
        try:
            sections = self.get_sections_by_strand(strand)

            # Filter only sections with available slots
            available = [s for s in sections if not s.is_full]

            if not available:
                return None

            # Return section with most available slots
            return max(available, key=lambda s: s.available_slots)

        except Exception as e:
            print(f"Error finding available section: {e}")
            return None

    def add_section(self, data: SectionData) -> Tuple[bool, str]:
        """Add a new section"""
        try:
            cursor = self.db.cursor()

            # Check if section exists
            cursor.execute(
                "SELECT id FROM sections WHERE section_name = %s AND strand = %s",
                (data.section_name, data.strand)
            )
            if cursor.fetchone():
                cursor.close()
                return False, f"Section '{data.section_name}' for {data.strand} already exists"

            query = """
                    INSERT INTO sections (section_name, strand, track, capacity,
                                          room_number, teacher_id, adviser_id, status, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, 'Active', NOW()) \
                    """

            values = (
                data.section_name,
                data.strand,
                data.track,
                data.capacity,
                data.room_number,
                data.teacher_id,
                data.adviser_id
            )

            cursor.execute(query, values)
            self.db.commit()
            cursor.close()

            return True, "Section added successfully"

        except Exception as e:
            print(f"Error adding section: {e}")
            return False, f"Failed to add section: {str(e)}"

    def delete_section(self, section_id: int) -> Tuple[bool, str]:
        """Delete a section"""
        try:
            cursor = self.db.cursor()

            # Check if section has students
            cursor.execute("SELECT COUNT(*) FROM students WHERE section_id = %s", (section_id,))
            count = cursor.fetchone()[0]

            if count > 0:
                cursor.close()
                return False, f"Cannot delete: Section has {count} enrolled student(s)"

            cursor.execute("DELETE FROM sections WHERE id = %s", (section_id,))
            self.db.commit()
            cursor.close()

            return True, "Section deleted successfully"

        except Exception as e:
            print(f"Error deleting section: {e}")
            return False, f"Failed to delete section: {str(e)}"