"""
Student Model - Handles all student-related database operations
ENHANCED: Added comprehensive data retrieval for student details
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from datetime import datetime


@dataclass
class StudentData:
    """Student data blueprint"""
    id: Optional[int] = None
    lrn: str = ""
    full_name: str = ""
    first_name: str = ""
    last_name: str = ""
    middle_name: Optional[str] = None
    email: str = ""
    contact_number: str = ""
    strand: str = ""
    track: str = "Academic"
    grade_level: str = "11"
    section_id: Optional[int] = None
    section_name: Optional[str] = None
    payment_status: str = "Pending"
    payment_mode: str = "Full Payment"
    status: str = "Enrolled"
    enrollment_date: Optional[datetime] = None
    gender: str = "Male"
    address: str = "N/A"
    date_of_birth: Optional[str] = None
    guardian_name: Optional[str] = None
    guardian_contact: Optional[str] = None
    last_school: Optional[str] = None

    def is_valid(self) -> bool:
        """Validate student data"""
        return bool(
            self.lrn and len(self.lrn) == 12 and
            self.first_name and
            self.last_name and
            self.email and '@' in self.email and
            self.strand
        )

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'lrn': self.lrn,
            'full_name': self.full_name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'email': self.email,
            'contact_number': self.contact_number,
            'strand': self.strand,
            'track': self.track,
            'grade_level': self.grade_level,
            'section_id': self.section_id,
            'section_name': self.section_name,
            'payment_status': self.payment_status,
            'payment_mode': self.payment_mode,
            'status': self.status,
            'enrollment_date': self.enrollment_date,
            'gender': self.gender,
            'address': self.address,
            'date_of_birth': self.date_of_birth,
            'guardian_name': self.guardian_name,
            'guardian_contact': self.guardian_contact,
            'last_school': self.last_school
        }


class Student:
    """Student model - Database operations for students"""

    def __init__(self, db):
        self.db = db

    def add_student(self, data: StudentData) -> Tuple[bool, str]:
        """Add a new student"""
        if not data.is_valid():
            return False, "Invalid student data"

        try:
            cursor = self.db.cursor()

            # Check if LRN exists
            cursor.execute("SELECT id FROM students WHERE lrn=%s", (data.lrn,))
            if cursor.fetchone():
                cursor.close()
                return False, "LRN already exists"

            # AUTO-ASSIGN SECTION: If no section_id provided, find one automatically
            if not data.section_id:
                print(f"No section assigned, finding available section for {data.strand}...")

                # Import Section model
                from models.section import Section
                section_model = Section(self.db)

                # Find available section for this strand
                available_section = section_model.find_available_section(data.strand)

                if available_section:
                    data.section_id = available_section.id
                    print(f"✅ Auto-assigned to section: {available_section.section_name} (ID: {available_section.id})")
                else:
                    print(f"⚠️ Warning: No available section found for {data.strand}")
                    # You can either:
                    # 1. Continue without section (current behavior)
                    # 2. Return error: return False, f"No available section for {data.strand}"

            query = """
                    INSERT INTO students
                    (lrn, full_name, first_name, last_name, middle_name, email, contact_number,
                     address, date_of_birth, gender, guardian_name, guardian_contact,
                     last_school, strand, track, grade_level, section_id,
                     status, enrollment_date, payment_status, payment_mode)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            'Enrolled', NOW(), 'Pending', %s) \
                    """

            values = (
                data.lrn,
                data.full_name,
                data.first_name,
                data.last_name,
                data.middle_name,
                data.email,
                data.contact_number,
                data.address,
                data.date_of_birth,
                data.gender,
                data.guardian_name,
                data.guardian_contact,
                data.last_school,
                data.strand,
                data.track,
                data.grade_level,
                data.section_id,  # This will now have a value
                data.payment_mode
            )

            cursor.execute(query, values)
            self.db.commit()
            cursor.close()

            return True, "Student enrolled successfully"

        except Exception as e:
            print(f"Error adding student: {e}")
            import traceback
            traceback.print_exc()
            return False, str(e)

    def get_all_students(self) -> List[StudentData]:
        """Get all enrolled students"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT s.*, sec.section_name
                FROM students s
                LEFT JOIN sections sec ON s.section_id = sec.id
                WHERE s.status = 'Enrolled'
                ORDER BY s.enrollment_date DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()

            return [StudentData(**row) for row in rows]

        except Exception as e:
            print(f"Error getting students: {e}")
            return []

    def get_student_by_id(self, student_id: int) -> Optional[StudentData]:
        """Get complete student information by ID"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT s.id, s.lrn, s.full_name, s.first_name, s.last_name, s.middle_name,
                       s.email, s.contact_number, s.address, s.date_of_birth, s.gender,
                       s.guardian_name, s.guardian_contact, s.last_school,
                       s.strand, s.track, s.grade_level, s.section_id,
                       s.payment_status, s.payment_mode, s.status, s.enrollment_date,
                       sec.section_name
                FROM students s
                LEFT JOIN sections sec ON s.section_id = sec.id
                WHERE s.id = %s
            """
            cursor.execute(query, (student_id,))
            row = cursor.fetchone()
            cursor.close()

            if row:
                return StudentData(**row)
            return None

        except Exception as e:
            print(f"Error getting student: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_students_by_section(self, section_id: int) -> List[Dict]:
        """Get all students in a specific section"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT s.id, s.full_name AS name, s.email, s.strand,
                       COALESCE(s.payment_status, 'Pending') AS payment_status,
                       DATE_FORMAT(s.enrollment_date, '%Y-%m-%d') AS date
                FROM students s
                WHERE s.section_id = %s AND s.status = 'Enrolled'
                ORDER BY s.full_name
            """
            cursor.execute(query, (section_id,))
            students = cursor.fetchall()
            cursor.close()
            return students

        except Exception as e:
            print(f"Error getting students by section: {e}")
            return []

    def get_recent_enrollments(self, limit: int = 10) -> List[Dict]:
        """Get most recent enrollments"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT id, full_name, strand,
                       DATE_FORMAT(enrollment_date, '%Y-%m-%d %H:%i') as date,
                       status
                FROM students
                WHERE status = 'Enrolled'
                ORDER BY enrollment_date DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            enrollments = cursor.fetchall()
            cursor.close()
            return enrollments

        except Exception as e:
            print(f"Error getting recent enrollments: {e}")
            return []

    def get_enrollments_by_date(self, date_filter, limit: int = 50) -> List[Dict]:
        """Get enrollments filtered by date"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT full_name, strand,
                       DATE_FORMAT(enrollment_date, '%Y-%m-%d %H:%i:%s') as date,
                       status
                FROM students
                WHERE status = 'Enrolled' AND enrollment_date >= %s
                ORDER BY enrollment_date DESC
                LIMIT %s
            """
            cursor.execute(query, (date_filter, limit))
            enrollments = cursor.fetchall()
            cursor.close()
            return enrollments

        except Exception as e:
            print(f"Error getting enrollments by date: {e}")
            return []

    def update_payment_status(self, student_id: int, new_status: str) -> bool:
        """Update student payment status"""
        try:
            cursor = self.db.cursor()
            query = "UPDATE students SET payment_status = %s WHERE id = %s"
            cursor.execute(query, (new_status, student_id))
            self.db.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error updating payment status: {e}")
            return False

    def update_student(self, student_id: int, data: Dict, user_id: int = None) -> Tuple[bool, str]:
        """Update student information - ENHANCED"""
        try:
            cursor = self.db.cursor()

            # Track old values for audit
            cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
            old_data = cursor.fetchone()

            # Build update query
            updates = []
            values = []

            # All updatable fields
            fields = [
                'first_name', 'middle_name', 'last_name', 'full_name',
                'gender', 'date_of_birth', 'address', 'contact_number',
                'email', 'guardian_name', 'guardian_contact', 'last_school',
                'strand', 'track', 'grade_level', 'section_id',
                'payment_status', 'status', 'status_reason'
            ]

            for field in fields:
                if field in data:
                    updates.append(f"{field} = %s")
                    values.append(data[field])

            if not updates:
                return False, "No data to update"

            # Add timestamp
            updates.append("status_changed_date = NOW()")
            if user_id:
                updates.append("status_changed_by = %s")
                values.append(user_id)

            values.append(student_id)
            query = f"UPDATE students SET {', '.join(updates)} WHERE id = %s"

            cursor.execute(query, values)

            # Log status change if status was updated
            if 'status' in data and old_data:
                old_status = old_data[15]  # Adjust index based on your table
                new_status = data['status']
                if old_status != new_status:
                    cursor.execute("""
                                   INSERT INTO student_status_history
                                       (student_id, old_status, new_status, reason, changed_by)
                                   VALUES (%s, %s, %s, %s, %s)
                                   """, (student_id, old_status, new_status,
                                         data.get('status_reason'), user_id))

            # Log section change if section_id was updated
            if 'section_id' in data and old_data:
                old_section = old_data[16]  # Adjust index
                new_section = data['section_id']
                if old_section != new_section:
                    # Mark old assignment as inactive
                    if old_section:
                        cursor.execute("""
                                       UPDATE section_assignments
                                       SET is_current   = FALSE,
                                           removed_date = NOW()
                                       WHERE student_id = %s
                                         AND section_id = %s
                                         AND is_current = TRUE
                                       """, (student_id, old_section))

                    # Create new assignment
                    if new_section:
                        cursor.execute("""
                                       INSERT INTO section_assignments
                                           (student_id, section_id, assigned_by, is_current)
                                       VALUES (%s, %s, %s, TRUE)
                                       """, (student_id, new_section, user_id))

            self.db.commit()
            cursor.close()

            return True, "Student updated successfully"

        except Exception as e:
            print(f"Error updating student: {e}")
            import traceback
            traceback.print_exc()
            return False, str(e)

    def delete_student(self, student_id: int) -> bool:
        """Delete a student"""
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            self.db.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error deleting student: {e}")
            return False

    def get_enrollment_stats(self, date_filter=None) -> Dict:
        """Get enrollment statistics with optional date filtering"""
        try:
            cursor = self.db.cursor(dictionary=True)

            # Build WHERE clause for date filtering
            date_condition = ""
            params = []
            if date_filter:
                date_condition = " AND enrollment_date >= %s"
                params = [date_filter]

            # Total enrolled
            query = f"SELECT COUNT(*) as count FROM students WHERE status='Enrolled'{date_condition}"
            cursor.execute(query, params)
            total = cursor.fetchone()['count']

            # Get total capacity per strand from sections
            cursor.execute("""
                SELECT strand, SUM(capacity) as total_capacity
                FROM sections
                WHERE status = 'Active'
                GROUP BY strand
            """)
            strand_capacities = {row['strand']: row['total_capacity'] for row in cursor.fetchall()}

            # Calculate total slots
            total_slots = sum(strand_capacities.values())

            # Get enrolled count per strand with date filter
            query = f"""
                SELECT strand, COUNT(*) as enrolled
                FROM students 
                WHERE status='Enrolled'{date_condition}
                GROUP BY strand
            """
            cursor.execute(query, params)
            enrolled_by_strand = {row['strand']: row['enrolled'] for row in cursor.fetchall()}

            # Build strand data
            strands = ['STEM', 'ABM', 'HUMSS', 'GAS', 'TVL']
            strand_list = []
            for strand in strands:
                total_slots_strand = strand_capacities.get(strand, 0)
                enrolled = enrolled_by_strand.get(strand, 0)
                strand_list.append({
                    'name': strand,
                    'enrolled': enrolled,
                    'total_slots': total_slots_strand
                })

            cursor.close()

            return {
                'total_enrolled': total,
                'total_slots': total_slots,
                'available_slots': total_slots - total,
                'by_strand': strand_list
            }

        except Exception as e:
            print(f"Error getting enrollment stats: {e}")
            return {
                'total_enrolled': 0,
                'total_slots': 500,
                'available_slots': 500,
                'by_strand': []
            }

    def search_students(self, query: str) -> List[Dict]:
        """Search students by name, email, or strand"""
        try:
            cursor = self.db.cursor(dictionary=True)
            search_query = f"%{query.lower()}%"

            sql = """
                SELECT id, full_name, email, strand, payment_status,
                       DATE_FORMAT(enrollment_date, '%Y-%m-%d') as date
                FROM students
                WHERE status = 'Enrolled' 
                AND (LOWER(full_name) LIKE %s 
                     OR LOWER(email) LIKE %s 
                     OR LOWER(strand) LIKE %s)
                ORDER BY enrollment_date DESC
                LIMIT 50
            """
            cursor.execute(sql, (search_query, search_query, search_query))
            results = cursor.fetchall()
            cursor.close()
            return results

        except Exception as e:
            print(f"Error searching students: {e}")
            return []


def advanced_search(self, filters: dict) -> List[Dict]:
    """Advanced search with multiple filters"""
    try:
        cursor = self.db.cursor(dictionary=True)

        query = """
                SELECT id, \
                       full_name, \
                       email, \
                       strand, \
                       grade_level,
                       payment_status, \
                       status, \
                       gender,
                       DATE_FORMAT(enrollment_date, '%Y-%m-%d') as date
                FROM students
                WHERE 1=1 \
                """
        params = []

        # Name/LRN/Email search
        if filters.get('name'):
            query += """ AND (
                LOWER(full_name) LIKE %s 
                OR LOWER(email) LIKE %s 
                OR lrn LIKE %s
            )"""
            search_term = f"%{filters['name'].lower()}%"
            params.extend([search_term, search_term, search_term])

        # Strand filter
        if filters.get('strand'):
            query += " AND strand = %s"
            params.append(filters['strand'])

        # Grade level filter
        if filters.get('grade_level'):
            query += " AND grade_level = %s"
            params.append(filters['grade_level'])

        # Status filter
        if filters.get('status'):
            query += " AND status = %s"
            params.append(filters['status'])

        # Payment status filter
        if filters.get('payment_status'):
            query += " AND payment_status = %s"
            params.append(filters['payment_status'])

        # Gender filter
        if filters.get('gender'):
            query += " AND gender = %s"
            params.append(filters['gender'])

        query += " ORDER BY enrollment_date DESC LIMIT 100"

        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()

        return results

    except Exception as e:
        print(f"Error in advanced search: {e}")
        import traceback
        traceback.print_exc()
        return []