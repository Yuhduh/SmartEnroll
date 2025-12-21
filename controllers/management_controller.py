"""
Management Controller - Uses Teacher, Room, and Section Models directly
FIXED: Room saving issue and added department display
"""
from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import QWidget, QMessageBox, QPushButton, QHBoxLayout, QTableWidgetItem
from views.management_page import ManagementPageUI


class ManagementController(QObject):
    """Controller for managing teachers, rooms, and sections"""

    def __init__(self, database):
        super().__init__()

        # Store database reference
        self.db = database

        # Create view
        self.view = ManagementPageUI()

        # Connect signals
        self._connect_signals()

        # Load initial data
        self.refresh_all_data()

    def _connect_signals(self):
        """Connect UI signals to controller methods"""
        # Teacher signals
        self.view.add_teacher_requested.connect(self.add_teacher)

        # Room signals
        self.view.add_room_requested.connect(self.add_room)

        # Section signals
        self.view.add_section_requested.connect(self.add_section)

        # Tab change signal
        self.view.tab_widget.currentChanged.connect(self.on_tab_changed)

    def get_view(self) -> QWidget:
        """Return the view widget"""
        return self.view

    def on_tab_changed(self, index: int):
        """Handle tab change"""
        if index == 0:  # Teachers tab
            self.refresh_teachers()
        elif index == 1:  # Rooms tab
            self.refresh_rooms()
        elif index == 2:  # Sections tab
            self.refresh_sections()
            self.refresh_section_dropdowns()

    def refresh_all_data(self):
        """Refresh all data"""
        self.refresh_teachers()
        self.refresh_rooms()
        self.refresh_sections()
        self.refresh_section_dropdowns()

    # ==================== TEACHER METHODS ====================

    def refresh_teachers(self):
        """Refresh teachers table with DEPARTMENT column - FIXED"""
        try:
            teachers = self.db.teachers.get_all_teachers()

            # Update table column count if needed
            if self.view.teachers_table.columnCount() != 7:
                self.view.teachers_table.setColumnCount(7)
                self.view.teachers_table.setHorizontalHeaderLabels([
                    "ID", "Name", "Email", "Contact", "Department", "Specialization", "Actions"
                ])

                # Set column widths
                from PyQt6.QtWidgets import QHeaderView
                header = self.view.teachers_table.horizontalHeader()
                header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
                self.view.teachers_table.setColumnWidth(0, 60)
                header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
                header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
                header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
                self.view.teachers_table.setColumnWidth(3, 130)
                header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
                header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
                header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
                self.view.teachers_table.setColumnWidth(6, 100)

            self.view.teachers_table.setRowCount(0)

            for row, teacher in enumerate(teachers):
                self.view.teachers_table.insertRow(row)

                # ID
                self.view.teachers_table.setItem(row, 0, self._create_table_item(str(teacher['id'])))

                # Name
                self.view.teachers_table.setItem(row, 1, self._create_table_item(teacher['full_name']))

                # Email
                self.view.teachers_table.setItem(row, 2, self._create_table_item(teacher['email']))

                # Contact
                self.view.teachers_table.setItem(row, 3, self._create_table_item(teacher['contact_number']))

                # Department - FIXED: Added this column
                department = teacher.get('department', '-')
                if not department or department.strip() == '':
                    department = '-'
                self.view.teachers_table.setItem(row, 4, self._create_table_item(department))

                # Specialization
                self.view.teachers_table.setItem(row, 5, self._create_table_item(teacher['specialization']))

                # Actions
                actions_widget = self._create_delete_button(
                    teacher['id'],
                    teacher['full_name'],
                    'teacher'
                )
                self.view.teachers_table.setCellWidget(row, 6, actions_widget)

                self.view.teachers_table.setRowHeight(row, 50)

        except Exception as e:
            print(f"Error refreshing teachers: {e}")
            import traceback
            traceback.print_exc()

    def add_teacher(self, data: dict):
        """Add a new teacher using Teacher Model"""
        try:
            # Validate inputs
            if not all([data['name'], data['email'], data['contact'], data['specialization']]):
                QMessageBox.warning(
                    self.view,
                    "Invalid Input",
                    "Name, Email, Contact, and Specialization are required!"
                )
                return

            # Validate email format
            if '@' not in data['email']:
                QMessageBox.warning(
                    self.view,
                    "Invalid Email",
                    "Please enter a valid email address."
                )
                return

            # Add to database using Teacher Model with department
            success, message = self.db.teachers.add_teacher(
                data['name'],
                data['email'],
                data['contact'],
                data['specialization'],
                data.get('department', '')
            )

            if success:
                QMessageBox.information(
                    self.view,
                    "✅ Success",
                    f"Teacher '{data['name']}' added successfully!"
                )
                self.view.clear_teacher_form()
                self.refresh_teachers()
                self.refresh_section_dropdowns()
            else:
                QMessageBox.critical(
                    self.view,
                    "Error",
                    message
                )

        except Exception as e:
            print(f"Error adding teacher: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.view,
                "Error",
                f"An error occurred: {str(e)}"
            )

    def delete_teacher(self, teacher_id: int, teacher_name: str):
        """Delete a teacher using Teacher Model"""
        try:
            reply = QMessageBox.question(
                self.view,
                "Confirm Deletion",
                f"Are you sure you want to delete teacher '{teacher_name}'?\n\n"
                "This action cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                success, message = self.db.teachers.delete_teacher(teacher_id)

                if success:
                    QMessageBox.information(
                        self.view,
                        "Success",
                        f"✅ Teacher '{teacher_name}' deleted successfully!"
                    )
                    self.refresh_teachers()
                    self.refresh_section_dropdowns()
                else:
                    QMessageBox.critical(
                        self.view,
                        "Error",
                        message
                    )

        except Exception as e:
            print(f"Error deleting teacher: {e}")
            import traceback
            traceback.print_exc()

    # ==================== ROOM METHODS ====================

    def refresh_rooms(self):
        """Refresh rooms table using Room Model"""
        try:
            rooms = self.db.rooms.get_all_rooms()

            self.view.rooms_table.setRowCount(0)

            for row, room in enumerate(rooms):
                self.view.rooms_table.insertRow(row)

                # ID
                self.view.rooms_table.setItem(row, 0, self._create_table_item(str(room['id'])))

                # Room Number
                self.view.rooms_table.setItem(row, 1, self._create_table_item(room['room_number']))

                # Building
                self.view.rooms_table.setItem(row, 2, self._create_table_item(room['building']))

                # Capacity
                item = self._create_table_item(str(room['capacity']))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.view.rooms_table.setItem(row, 3, item)

                # Actions
                actions_widget = self._create_delete_button(
                    room['id'],
                    f"{room['room_number']} ({room['building']})",
                    'room'
                )
                self.view.rooms_table.setCellWidget(row, 4, actions_widget)

                self.view.rooms_table.setRowHeight(row, 50)

        except Exception as e:
            print(f"Error refreshing rooms: {e}")
            import traceback
            traceback.print_exc()

    def add_room(self, data: dict):
        """Add a new room using Room Model"""
        try:
            # Validate inputs
            if not all([data['room_number'], data['building'], data['capacity']]):
                QMessageBox.warning(
                    self.view,
                    "Invalid Input",
                    "All fields are required!"
                )
                return

            # Validate capacity is a number
            try:
                capacity = int(data['capacity'])
                if capacity <= 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(
                    self.view,
                    "Invalid Capacity",
                    "Capacity must be a positive number."
                )
                return

            # Add to database using Room Model
            success, message = self.db.rooms.add_room(
                data['room_number'],
                data['building'],
                capacity
            )

            if success:
                QMessageBox.information(
                    self.view,
                    "✅ Success",
                    f"Room {data['room_number']} added successfully!"
                )
                self.view.clear_room_form()
                self.refresh_rooms()
                self.refresh_section_dropdowns()
            else:
                QMessageBox.critical(
                    self.view,
                    "Error",
                    message
                )

        except Exception as e:
            print(f"Error adding room: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.view,
                "Error",
                f"An error occurred: {str(e)}"
            )

    def delete_room(self, room_id: int, room_name: str):
        """Delete a room using Room Model"""
        try:
            reply = QMessageBox.question(
                self.view,
                "Confirm Deletion",
                f"Are you sure you want to delete room '{room_name}'?\n\n"
                "This action cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                success, message = self.db.rooms.delete_room(room_id)

                if success:
                    QMessageBox.information(
                        self.view,
                        "Success",
                        f"✅ Room '{room_name}' deleted successfully!"
                    )
                    self.refresh_rooms()
                    self.refresh_section_dropdowns()
                else:
                    QMessageBox.critical(
                        self.view,
                        "Error",
                        message
                    )

        except Exception as e:
            print(f"Error deleting room: {e}")
            import traceback
            traceback.print_exc()

    # ==================== SECTION METHODS ====================

    def refresh_sections(self):
        """Refresh sections table - FIXED to show room properly"""
        try:
            print("DEBUG: Refreshing sections table...")
            sections = self.db.sections.get_all_sections()
            print(f"DEBUG: Found {len(sections)} sections")

            self.view.sections_table.setRowCount(0)

            for row, section in enumerate(sections):
                print(f"DEBUG: Section {row}: {section.section_name}, Room: {section.room_number}")
                self.view.sections_table.insertRow(row)

                # ID
                self.view.sections_table.setItem(row, 0, self._create_table_item(str(section.id)))

                # Section Name
                self.view.sections_table.setItem(row, 1, self._create_table_item(section.section_name))

                # Strand
                item = self._create_table_item(section.strand)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.view.sections_table.setItem(row, 2, item)

                # Capacity
                capacity_text = f"{section.student_count}/{section.capacity}"
                item = self._create_table_item(capacity_text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.view.sections_table.setItem(row, 3, item)

                # Room - FIXED: Show room properly
                room_text = section.room_number if section.room_number else '-'
                print(f"DEBUG: Displaying room: {room_text}")
                self.view.sections_table.setItem(row, 4, self._create_table_item(room_text))

                # Teacher/Adviser
                teacher_text = section.teacher_name if section.teacher_name else 'Not assigned'
                self.view.sections_table.setItem(row, 5, self._create_table_item(teacher_text))

                # Actions
                actions_widget = self._create_delete_button(
                    section.id,
                    section.section_name,
                    'section'
                )
                self.view.sections_table.setCellWidget(row, 6, actions_widget)

                self.view.sections_table.setRowHeight(row, 50)

            print(f"DEBUG: Sections table now has {self.view.sections_table.rowCount()} rows")

        except Exception as e:
            print(f"Error refreshing sections: {e}")
            import traceback
            traceback.print_exc()

    def refresh_section_dropdowns(self):
        """Refresh room and teacher dropdowns"""
        try:
            # Refresh room dropdown with availability status
            self.view.section_room_combo.clear()
            self.view.section_room_combo.addItem("No Room", None)

            rooms = self.db.rooms.get_all_rooms()

            # Get all sections to check which rooms are occupied
            sections = self.db.sections.get_all_sections()
            occupied_rooms = {}
            for section in sections:
                if section.room_number:
                    occupied_rooms[section.room_number] = section.section_name

            for room in rooms:
                room_key = room['room_number']

                # Check if room is occupied
                if room_key in occupied_rooms:
                    display = f"{room['room_number']} ({room['building']}) - ⚠️ OCCUPIED by {occupied_rooms[room_key]}"
                    self.view.section_room_combo.addItem(display, f"occupied_{room['id']}")
                else:
                    display = f"{room['room_number']} ({room['building']}) - Capacity: {room['capacity']}"
                    # Store room data as dictionary
                    room_data = {
                        'id': room['id'],
                        'room_number': room['room_number'],
                        'capacity': room['capacity']
                    }
                    self.view.section_room_combo.addItem(display, room_data)

            # Refresh teacher dropdown
            self.view.section_teacher_combo.clear()
            self.view.section_teacher_combo.addItem("No Adviser", None)

            teachers = self.db.teachers.get_all_teachers()
            for teacher in teachers:
                display = f"{teacher['full_name']} - {teacher['specialization']}"
                self.view.section_teacher_combo.addItem(display, teacher['id'])

        except Exception as e:
            print(f"Error refreshing dropdowns: {e}")
            import traceback
            traceback.print_exc()

    def add_section(self, data: dict):
        """Add a new section with proper room handling - FIXED"""
        try:
            print("DEBUG: add_section called")
            print(f"DEBUG: Data received: {data}")

            # Validate inputs
            if not all([data['section_name'], data['strand'], data['capacity']]):
                QMessageBox.warning(
                    self.view,
                    "Invalid Input",
                    "Section name, strand, and capacity are required!"
                )
                return

            # Validate capacity
            try:
                section_capacity = int(data['capacity'])
                if section_capacity <= 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(
                    self.view,
                    "Invalid Capacity",
                    "Section capacity must be a positive number."
                )
                return

            # FIXED: Handle room data properly
            room_id = data['room_id']
            room_number = None
            room_capacity = None

            if room_id:
                print(f"DEBUG: room_id type: {type(room_id)}, value: {room_id}")

                # Check if occupied
                if isinstance(room_id, str) and room_id.startswith("occupied_"):
                    QMessageBox.critical(
                        self.view,
                        "❌ Room Already Occupied",
                        "The selected room is already assigned to another section!\n\n"
                        "Please choose a different room or select 'No Room'."
                    )
                    return

                # FIXED: Extract room data from dictionary
                if isinstance(room_id, dict):
                    actual_room_id = room_id['id']
                    room_number = room_id['room_number']
                    room_capacity = room_id['capacity']
                    print(f"DEBUG: Extracted - ID: {actual_room_id}, Number: {room_number}, Capacity: {room_capacity}")

                    # Validate capacity
                    if section_capacity > room_capacity:
                        QMessageBox.critical(
                            self.view,
                            "❌ Capacity Exceeds Room Limit",
                            f"<b>Section capacity ({section_capacity}) exceeds room capacity ({room_capacity})!</b><br><br>"
                            f"The room can only accommodate <b>{room_capacity} students</b>.<br><br>"
                            f"Please either:<br>"
                            f"• Reduce the section capacity to {room_capacity} or less<br>"
                            f"• Choose a larger room<br>"
                            f"• Select 'No Room'"
                        )
                        return
                else:
                    # Fallback: try to get room from database
                    room = self.db.rooms.get_room_by_id(room_id)
                    if room:
                        room_number = room.room_number
                        room_capacity = room.capacity

            # Determine track
            track = 'Academic' if data['strand'] in ['STEM', 'ABM', 'HUMSS', 'GAS'] else 'TVL'

            # Create section data
            from models.section import SectionData
            section_data = SectionData(
                section_name=data['section_name'],
                strand=data['strand'],
                track=track,
                capacity=section_capacity,
                room_number=room_number,  # FIXED: Now properly set
                teacher_id=data['teacher_id'],
                adviser_id=data['teacher_id']
            )

            print(f"DEBUG: Section data - room_number: {section_data.room_number}")
            print("DEBUG: Calling db.sections.add_section...")

            # Add section
            success, message = self.db.sections.add_section(section_data)
            print(f"DEBUG: add_section returned: success={success}, message={message}")

            if success:
                success_msg = (
                    f"<b>Section '{data['section_name']}' added successfully!</b><br><br>"
                    f"<b>Strand:</b> {data['strand']}<br>"
                    f"<b>Capacity:</b> {section_capacity} students<br>"
                    f"<b>Room:</b> {room_number if room_number else 'No room assigned'}"
                )

                if room_number and room_capacity:
                    success_msg += f" (Room capacity: {room_capacity})"

                QMessageBox.information(
                    self.view,
                    "✅ Success",
                    success_msg
                )

                # Clear and refresh
                self.view.clear_section_form()
                print("DEBUG: Refreshing sections after add...")
                self.refresh_sections()
                self.refresh_section_dropdowns()
                print("DEBUG: Section add completed successfully")
            else:
                QMessageBox.critical(
                    self.view,
                    "Error",
                    message
                )

        except Exception as e:
            print(f"Error adding section: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.view,
                "Error",
                f"An error occurred: {str(e)}"
            )

    def delete_section(self, section_id: int, section_name: str):
        """Delete a section using Section Model"""
        try:
            reply = QMessageBox.question(
                self.view,
                "Confirm Deletion",
                f"Are you sure you want to delete section '{section_name}'?\n\n"
                "This action cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                success, message = self.db.sections.delete_section(section_id)

                if success:
                    QMessageBox.information(
                        self.view,
                        "Success",
                        f"✅ Section '{section_name}' deleted successfully!"
                    )
                    self.refresh_sections()
                    self.refresh_section_dropdowns()
                else:
                    QMessageBox.critical(
                        self.view,
                        "Error",
                        message
                    )

        except Exception as e:
            print(f"Error deleting section: {e}")
            import traceback
            traceback.print_exc()

    # ==================== HELPER METHODS ====================

    def _create_table_item(self, text: str) -> QTableWidgetItem:
        """Create a non-editable table item"""
        item = QTableWidgetItem(text)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        return item

    def _create_delete_button(self, item_id: int, item_name: str, item_type: str) -> QWidget:
        """Create delete button widget"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)

        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                padding: 1px 12px;
                border-radius: 6px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Connect to appropriate delete method
        if item_type == 'teacher':
            delete_btn.clicked.connect(lambda: self.delete_teacher(item_id, item_name))
        elif item_type == 'room':
            delete_btn.clicked.connect(lambda: self.delete_room(item_id, item_name))
        elif item_type == 'section':
            delete_btn.clicked.connect(lambda: self.delete_section(item_id, item_name))

        layout.addWidget(delete_btn)
        layout.addStretch()

        return widget