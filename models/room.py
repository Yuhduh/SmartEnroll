"""
Room Model - Handles all room-related database operations
"""
from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass
class RoomData:
    """Room data blueprint"""
    id: Optional[int] = None
    room_number: str = ""
    building: str = ""
    capacity: int = 40
    status: str = "Active"

    def is_valid(self) -> bool:
        """Validate room data"""
        return bool(
            self.room_number and
            self.building and
            self.capacity > 0
        )

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'room_number': self.room_number,
            'building': self.building,
            'capacity': self.capacity,
            'status': self.status
        }


class Room:
    """Room model - Database operations for rooms"""

    def __init__(self, db):
        self.db = db

    def get_all_rooms(self) -> List[dict]:
        """Get all rooms"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT id, room_number, building, capacity, status, created_at
                FROM rooms
                WHERE status = 'Active'
                ORDER BY building, room_number
            """
            cursor.execute(query)
            rooms = cursor.fetchall()
            cursor.close()
            return rooms

        except Exception as e:
            print(f"Error getting rooms: {e}")
            return []

    def get_room_by_id(self, room_id: int) -> Optional[RoomData]:
        """Get room by ID"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = "SELECT * FROM rooms WHERE id = %s"
            cursor.execute(query, (room_id,))
            row = cursor.fetchone()
            cursor.close()

            if row:
                return RoomData(**row)
            return None

        except Exception as e:
            print(f"Error getting room: {e}")
            return None

    def add_room(self, room_number: str, building: str, capacity: int) -> Tuple[bool, str]:
        """Add a new room"""
        try:
            cursor = self.db.cursor()

            # Check if room already exists
            cursor.execute(
                "SELECT id FROM rooms WHERE room_number = %s AND building = %s",
                (room_number, building)
            )
            if cursor.fetchone():
                cursor.close()
                return False, f"Room {room_number} in {building} already exists"

            # Insert new room
            query = """
                INSERT INTO rooms (room_number, building, capacity, status, created_at)
                VALUES (%s, %s, %s, 'Active', NOW())
            """
            cursor.execute(query, (room_number, building, capacity))
            self.db.commit()
            cursor.close()

            return True, "Room added successfully"

        except Exception as e:
            print(f"Error adding room: {e}")
            return False, f"Failed to add room: {str(e)}"

    def delete_room(self, room_id: int) -> Tuple[bool, str]:
        """Delete a room"""
        try:
            cursor = self.db.cursor()

            # Check if room is assigned to any section
            cursor.execute(
                "SELECT COUNT(*) FROM sections WHERE room_number IN (SELECT room_number FROM rooms WHERE id = %s)",
                (room_id,)
            )
            count = cursor.fetchone()[0]

            if count > 0:
                cursor.close()
                return False, f"Cannot delete: Room is assigned to {count} section(s)"

            # Delete room
            cursor.execute("DELETE FROM rooms WHERE id = %s", (room_id,))
            self.db.commit()
            cursor.close()

            return True, "Room deleted successfully"

        except Exception as e:
            print(f"Error deleting room: {e}")
            return False, f"Failed to delete room: {str(e)}"

    def update_room(self, room_id: int, room_number: str, building: str, capacity: int) -> Tuple[bool, str]:
        """Update room details"""
        try:
            cursor = self.db.cursor()

            query = """
                UPDATE rooms 
                SET room_number = %s, building = %s, capacity = %s
                WHERE id = %s
            """
            cursor.execute(query, (room_number, building, capacity, room_id))
            self.db.commit()
            cursor.close()

            return True, "Room updated successfully"

        except Exception as e:
            print(f"Error updating room: {e}")
            return False, f"Failed to update room: {str(e)}"