"""
Central Database Manager for SmartEnroll
Initializes all model classes with database connection
"""
import mysql.connector
from mysql.connector import Error
from database.config import ACTIVE_CONFIG
from models.student import Student
from models.teacher import Teacher
from models.section import Section
from models.room import Room
from models.user import User
from models.academic_year import AcademicYear
from models.payment import Payment



class Database:
    """Central database manager that initializes all models"""

    def __init__(self):
        self.db = self._create_connection()

        if self.db is not None:
            # Initialize all models with database connection
            self.students = Student(self.db)
            self.teachers = Teacher(self.db)
            self.sections = Section(self.db)
            self.academic_years = AcademicYear(self.db)
            self.payments = Payment(self.db)
            self.rooms = Room(self.db)
            self.users = User(self.db)

            print("✅ Database initialized successfully")
            print(f"   - Academic Years model: {self.academic_years}")
            print(f"   - Payments model: {self.payments}")
            print(f"   - Students model: {self.students}")
            print(f"   - Teachers model: {self.teachers}")
            print(f"   - Sections model: {self.sections}")
            print(f"   - Rooms model: {self.rooms}")
            print(f"   - Users model: {self.users}")
        else:
            print("❌ Database connection failed!")

    def _create_connection(self):
        """Create MySQL database connection"""
        db = None
        try:
            db = mysql.connector.connect(
                host=ACTIVE_CONFIG['host'],
                user=ACTIVE_CONFIG['user'],
                password=ACTIVE_CONFIG['password'],
                database=ACTIVE_CONFIG['database'],
                autocommit=True
            )
            print(f"✅ Connected to database: {ACTIVE_CONFIG['database']}")
        except Error as e:
            print(f"❌ Database connection error: {e}")
            db = None
        return db

    def test_connection(self) -> bool:
        """Test if database connection is active"""
        if self.db and self.db.is_connected():
            return True
        return False

    def close(self):
        """Close database connection"""
        if self.db and self.db.is_connected():
            self.db.close()
            print("✅ Database connection closed")

    def initialize_tables(self):
        """Initialize all database tables"""
        if not self.db:
            print("❌ No database connection")
            return False

        try:
            cursor = self.db.cursor()

            # Users table
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS users
                           (
                               id
                               INT
                               AUTO_INCREMENT
                               PRIMARY
                               KEY,
                               username
                               VARCHAR
                           (
                               50
                           ) UNIQUE NOT NULL,
                               password_hash VARCHAR
                           (
                               64
                           ) NOT NULL,
                               role ENUM
                           (
                               'staff',
                               'admin'
                           ) DEFAULT 'staff',
                               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                               )
                           """)

            # Teachers table
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS teachers
                           (
                               id
                               INT
                               AUTO_INCREMENT
                               PRIMARY
                               KEY,
                               full_name
                               VARCHAR
                           (
                               100
                           ) NOT NULL,
                               email VARCHAR
                           (
                               100
                           ) UNIQUE,
                               contact_number VARCHAR
                           (
                               20
                           ),
                               department VARCHAR
                           (
                               100
                           ),
                               specialization VARCHAR
                           (
                               100
                           ),
                               status ENUM
                           (
                               'Active',
                               'Inactive'
                           ) DEFAULT 'Active',
                               hire_date DATE,
                               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                               )
                           """)

            # Rooms table
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS rooms
                           (
                               id
                               INT
                               AUTO_INCREMENT
                               PRIMARY
                               KEY,
                               room_number
                               VARCHAR
                           (
                               20
                           ) NOT NULL,
                               building VARCHAR
                           (
                               50
                           ) NOT NULL,
                               capacity INT DEFAULT 40,
                               status ENUM
                           (
                               'Active',
                               'Inactive'
                           ) DEFAULT 'Active',
                               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                               UNIQUE KEY unique_room
                           (
                               room_number,
                               building
                           )
                               )
                           """)

            # Sections table
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS sections
                           (
                               id
                               INT
                               AUTO_INCREMENT
                               PRIMARY
                               KEY,
                               section_name
                               VARCHAR
                           (
                               50
                           ) NOT NULL,
                               grade_level ENUM
                           (
                               '11',
                               '12'
                           ) DEFAULT '11',
                               track VARCHAR
                           (
                               50
                           ) NOT NULL,
                               strand VARCHAR
                           (
                               100
                           ) NOT NULL,
                               capacity INT DEFAULT 40,
                               teacher_id INT,
                               adviser_id INT,
                               room_number VARCHAR
                           (
                               20
                           ),
                               status ENUM
                           (
                               'Active',
                               'Inactive'
                           ) DEFAULT 'Active',
                               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                               FOREIGN KEY
                           (
                               teacher_id
                           ) REFERENCES teachers
                           (
                               id
                           ) ON DELETE SET NULL,
                               FOREIGN KEY
                           (
                               adviser_id
                           ) REFERENCES teachers
                           (
                               id
                           )
                             ON DELETE SET NULL
                               )
                           """)

            # Students table
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS students
                           (
                               id
                               INT
                               AUTO_INCREMENT
                               PRIMARY
                               KEY,
                               lrn
                               VARCHAR
                           (
                               12
                           ) UNIQUE NOT NULL,
                               full_name VARCHAR
                           (
                               100
                           ) NOT NULL,
                               first_name VARCHAR
                           (
                               50
                           ) NOT NULL,
                               last_name VARCHAR
                           (
                               50
                           ) NOT NULL,
                               middle_name VARCHAR
                           (
                               50
                           ),
                               gender ENUM
                           (
                               'Male',
                               'Female'
                           ) NOT NULL,
                               date_of_birth DATE,
                               address TEXT,
                               contact_number VARCHAR
                           (
                               20
                           ),
                               guardian_name VARCHAR
                           (
                               100
                           ),
                               guardian_contact VARCHAR
                           (
                               20
                           ),
                               last_school VARCHAR
                           (
                               100
                           ),
                               email VARCHAR
                           (
                               100
                           ) UNIQUE NOT NULL,
                               track VARCHAR
                           (
                               50
                           ) NOT NULL,
                               strand VARCHAR
                           (
                               100
                           ) NOT NULL,
                               grade_level ENUM
                           (
                               '11',
                               '12'
                           ) DEFAULT '11',
                               section_id INT,
                               payment_status ENUM
                           (
                               'Pending',
                               'Paid',
                               'Partial'
                           ) DEFAULT 'Pending',
                               status ENUM
                           (
                               'Pending',
                               'Enrolled',
                               'Dropped'
                           ) DEFAULT 'Pending',
                               enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                               FOREIGN KEY
                           (
                               section_id
                           ) REFERENCES sections
                           (
                               id
                           ) ON DELETE SET NULL
                               )
                           """)

            cursor.close()
            print("✅ Database tables initialized")
            return True

        except Error as e:
            print(f"❌ Error initializing tables: {e}")
            return False