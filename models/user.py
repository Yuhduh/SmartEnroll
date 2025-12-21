"""
User Model - Handles all user-related database operations
"""
import hashlib
from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict
from datetime import datetime


@dataclass
class UserData:
    """User data blueprint"""
    id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    role: str = "staff"
    created_at: Optional[datetime] = None

    def is_valid(self) -> bool:
        """Validate user data"""
        return bool(
            self.username and
            len(self.username) >= 3 and
            self.role in ['staff', 'admin']
        )

    def to_dict(self) -> dict:
        """Convert to dictionary (without password)"""
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at
        }


class User:
    """User model - Database operations for users"""

    def __init__(self, db):
        self.db = db

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_user(self, username: str, password: str) -> Optional[Dict]:
        """Validate user credentials and return user info"""
        try:
            cursor = self.db.cursor(dictionary=True)
            hashed = self._hash_password(password)

            query = """
                    SELECT id, username, role
                    FROM users
                    WHERE username = %s \
                      AND password_hash = %s \
                    """
            cursor.execute(query, (username, hashed))
            user = cursor.fetchone()
            cursor.close()

            return user

        except Exception as e:
            print(f"Error validating user: {e}")
            return None

    def get_all_users(self) -> List[dict]:
        """Get all users (without passwords)"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                    SELECT id, \
                           username, \
                           role,
                           DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') as created_at
                    FROM users
                    ORDER BY id DESC \
                    """
            cursor.execute(query)
            users = cursor.fetchall()
            cursor.close()
            return users

        except Exception as e:
            print(f"Error getting users: {e}")
            return []

    def get_user_by_id(self, user_id: int) -> Optional[UserData]:
        """Get user by ID"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            cursor.close()

            if row:
                return UserData(**row)
            return None

        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    def add_user(self, username: str, password: str, role: str) -> Tuple[bool, str]:
        """Add a new user with hashed password"""
        try:
            # Validate password length
            if len(password) < 6:
                return False, "Password must be at least 6 characters"

            cursor = self.db.cursor()

            # Check if username exists
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                cursor.close()
                return False, "Username already exists"

            # Hash password and insert
            hashed = self._hash_password(password)
            query = """
                    INSERT INTO users (username, password_hash, role, created_at)
                    VALUES (%s, %s, %s, NOW()) \
                    """
            cursor.execute(query, (username, hashed, role))
            self.db.commit()
            cursor.close()

            return True, "User added successfully"

        except Exception as e:
            print(f"Error adding user: {e}")
            return False, f"Failed to add user: {str(e)}"

    def delete_user(self, user_id: int) -> Tuple[bool, str]:
        """Delete a user"""
        try:
            cursor = self.db.cursor()

            # Prevent deleting the last admin
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
            admin_count = cursor.fetchone()[0]

            if admin_count <= 1:
                cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
                user_role = cursor.fetchone()
                if user_role and user_role[0] == 'admin':
                    cursor.close()
                    return False, "Cannot delete the last admin user"

            # Delete user
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.db.commit()
            cursor.close()

            return True, "User deleted successfully"

        except Exception as e:
            print(f"Error deleting user: {e}")
            return False, f"Failed to delete user: {str(e)}"

    def update_password(self, user_id: int, new_password: str) -> Tuple[bool, str]:
        """Update user password"""
        try:
            if len(new_password) < 6:
                return False, "Password must be at least 6 characters"

            cursor = self.db.cursor()
            hashed = self._hash_password(new_password)

            query = "UPDATE users SET password_hash = %s WHERE id = %s"
            cursor.execute(query, (hashed, user_id))
            self.db.commit()
            cursor.close()

            return True, "Password updated successfully"

        except Exception as e:
            print(f"Error updating password: {e}")
            return False, f"Failed to update password: {str(e)}"

    def create_default_admin(self) -> Tuple[bool, str]:
        """Create default admin user if none exists"""
        try:
            cursor = self.db.cursor()

            # Check if admin exists
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
            if cursor.fetchone()[0] > 0:
                cursor.close()
                return False, "Default admin already exists"

            # Create admin
            hashed = self._hash_password('admin123')
            query = """
                    INSERT INTO users (username, password_hash, role, created_at)
                    VALUES ('admin', %s, 'admin', NOW()) \
                    """
            cursor.execute(query, (hashed,))
            self.db.commit()
            cursor.close()

            return True, "Default admin created (username: admin, password: admin123)"

        except Exception as e:
            print(f"Error creating default admin: {e}")
            return False, str(e)