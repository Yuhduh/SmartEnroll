"""
Classrooms Controller - Uses Section and Student Models directly
UPDATED: Added student details view functionality
"""
from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QMenu, QMessageBox, QTableWidget
from PyQt6.QtGui import QAction
from views.classrooms_page import ClassroomsPageUI
from views.student_details_dialog import StudentDetailsDialog


class ClassroomsController(QObject):

    def __init__(self, database):
        super().__init__()

        # Store database reference
        self.db = database

        # Create view
        self.view = ClassroomsPageUI()

        # Current state
        self.current_classroom_data = None
        self.current_section_id = None

        # Ensure we can find the table widget
        self._ensure_table_access()

        # Setup context menu
        self._setup_context_menu()

        # Connect signals
        self._connect_signals()

        # Load initial data
        self.refresh_classrooms()

    def _ensure_table_access(self):
        """Try to find the students table if attribute is missing"""
        if not hasattr(self.view, 'students_table'):
            print("⚠️ 'students_table' attribute missing. Attempting to find QTableWidget...")
            tables = self.view.findChildren(QTableWidget)
            if tables:
                print(f"✅ Found table widget: {tables[0]}")
                self.view.students_table = tables[0]
            else:
                print("❌ CRITICAL: No QTableWidget found in ClassroomsPageUI!")

    def _setup_context_menu(self):
        """Enable right-click menu on the students table"""
        if hasattr(self.view, 'students_table'):
            self.view.students_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.view.students_table.customContextMenuRequested.connect(self.show_context_menu)

            # NEW: Enable double-click to view details
            self.view.students_table.cellDoubleClicked.connect(self.handle_view_student_details)

    def _connect_signals(self):
        """Connect UI signals to controller methods"""
        if hasattr(self.view, 'view_buttons'):
            for btn in self.view.view_buttons:
                btn.clicked.connect(lambda checked, b=btn: self.switch_view(b))

        self.view.classroom_selected.connect(self.load_classroom_students)
        self.view.strand_filter_changed.connect(self.filter_classrooms)
        self.view.filter_combo.currentTextChanged.connect(self.filter_classrooms)

    def get_view(self) -> QWidget:
        return self.view

    def switch_view(self, button):
        """Handle view button clicks"""
        if hasattr(self.view, 'view_buttons'):
            for btn in self.view.view_buttons:
                btn.setChecked(False)
            button.setChecked(True)

        if button.text() == "All Sections":
            self.view.switch_to_sections_view()
            self.refresh_classrooms()
        else:
            self.view.switch_to_students_view()
            if self.current_section_id:
                self._populate_current_students()

    def refresh_classrooms(self):
        """Load classroom data using Section Model"""
        try:
            sections = self.db.sections.get_all_sections()

            self.current_classroom_data = []
            for section in sections:
                self.current_classroom_data.append({
                    'id': section.id,
                    'section': section.section_name,
                    'strand': section.strand,
                    'adviser_name': section.adviser_name or 'Not assigned',
                    'adviser_email': section.adviser_email or '',
                    'room_number': section.room_number or 'TBA',
                    'capacity': section.capacity,
                    'student_count': section.student_count,
                    'available': section.available_slots
                })

            self.populate_classrooms_table(self.current_classroom_data)

        except Exception as e:
            print(f"Error loading classrooms: {e}")
            import traceback
            traceback.print_exc()

    def populate_classrooms_table(self, classrooms):
        """Populate the classrooms table"""
        try:
            if not hasattr(self.view, 'classrooms_table'):
                return

            table = self.view.classrooms_table
            table.setRowCount(0)

            for row, classroom in enumerate(classrooms):
                table.insertRow(row)

                section_item = QTableWidgetItem(classroom['section'])
                section_item.setData(Qt.ItemDataRole.UserRole, classroom['id'])
                table.setItem(row, 0, section_item)

                table.setItem(row, 1, QTableWidgetItem(classroom['strand']))
                table.setItem(row, 2, QTableWidgetItem(classroom['adviser_name']))
                table.setItem(row, 3, QTableWidgetItem(classroom['room_number']))
                table.setItem(row, 4, QTableWidgetItem(str(classroom['student_count'])))
                table.setItem(row, 5, QTableWidgetItem(str(classroom['capacity'])))

                available_item = QTableWidgetItem(str(classroom['available']))
                if classroom['available'] <= 0:
                    available_item.setForeground(Qt.GlobalColor.red)
                table.setItem(row, 6, available_item)

        except Exception as e:
            print(f"Error populating classrooms table: {e}")

    def filter_classrooms(self):
        """Filter the displayed classrooms"""
        if not self.current_classroom_data:
            return

        strand = self.view.filter_combo.currentText()
        search = ""
        if hasattr(self.view, 'search_input'):
            search = self.view.search_input.text().lower()

        filtered = []
        for c in self.current_classroom_data:
            if strand != "All" and c['strand'] != strand:
                continue

            if search:
                text = f"{c['section']} {c['adviser_name']}".lower()
                if search not in text:
                    continue

            filtered.append(c)

        self.populate_classrooms_table(filtered)

    def load_classroom_students(self, section_id: int, section_name: str):
        """Load students for the selected classroom"""
        try:
            self.current_section_id = section_id
            section = self.db.sections.get_section_by_id(section_id)

            if hasattr(self.view, 'info_badge'):
                student_count = len(self.db.students.get_students_by_section(section_id))
                self.view.info_badge.setText(
                    f"Selected: {section_name} - {student_count} students (Click 'Student Details' to view)"
                )

            if hasattr(self.view, 'view_buttons') and len(self.view.view_buttons) > 1:
                if self.view.view_buttons[1].isChecked():
                    self._populate_current_students()

        except Exception as e:
            print(f"Error loading students: {e}")
            import traceback
            traceback.print_exc()

    def _populate_current_students(self):
        """Helper method to populate students for current selection"""
        try:
            if not self.current_section_id:
                return

            section = self.db.sections.get_section_by_id(self.current_section_id)
            students = self.db.students.get_students_by_section(self.current_section_id)

            if section and hasattr(self.view, 'teacher_info_card'):
                if section.adviser_name:
                    self.view.teacher_name_label.setText(f"👨‍🏫 Adviser: {section.adviser_name}")
                    self.view.teacher_email_label.setText(f"📧 Email: {section.adviser_email or 'N/A'}")
                    self.view.teacher_info_card.setVisible(True)
                else:
                    self.view.teacher_info_card.setVisible(False)

            if hasattr(self.view, 'students_table'):
                table = self.view.students_table
                table.setRowCount(0)

                for row, student in enumerate(students):
                    table.insertRow(row)

                    # Store student ID in UserRole for details view
                    name_item = QTableWidgetItem(student['name'])
                    name_item.setData(Qt.ItemDataRole.UserRole, student['id'])
                    table.setItem(row, 0, name_item)

                    table.setItem(row, 1, QTableWidgetItem(student['email']))

                    item_strand = QTableWidgetItem(student['strand'])
                    item_strand.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(row, 2, item_strand)

                    payment_text = student['payment_status'] if student['payment_status'] else 'Pending'
                    item_pay = QTableWidgetItem(payment_text)
                    item_pay.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    if payment_text == 'Paid':
                        item_pay.setForeground(Qt.GlobalColor.darkGreen)
                    table.setItem(row, 3, item_pay)

                    item_date = QTableWidgetItem(str(student['date']))
                    item_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    table.setItem(row, 4, item_date)

            if hasattr(self.view, 'info_badge'):
                self.view.info_badge.setText(f"{section.section_name} - {len(students)} students")

        except Exception as e:
            print(f"Error populating students: {e}")
            import traceback
            traceback.print_exc()

    def handle_view_student_details(self, row: int, column: int):
        """Handle double-click on student row to view details"""
        if not hasattr(self.view, 'students_table'):
            return

        item = self.view.students_table.item(row, 0)
        if item:
            student_id = item.data(Qt.ItemDataRole.UserRole)
            if student_id:
                self.show_student_details(student_id)

    def show_student_details(self, student_id: int):
        """Show detailed student information dialog"""
        try:
            student = self.db.students.get_student_by_id(student_id)

            if not student:
                QMessageBox.warning(
                    self.view,
                    "Error",
                    "Student not found in database."
                )
                return

            student_data = student.to_dict()
            dialog = StudentDetailsDialog(student_data, self.view)
            dialog.payment_updated.connect(self.handle_payment_update)
            dialog.exec()

        except Exception as e:
            print(f"Error showing student details: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Failed to load student details:\n{str(e)}"
            )

    def handle_payment_update(self, student_id: int, new_status: str):
        """Handle payment status update from details dialog"""
        try:
            success = self.db.students.update_payment_status(student_id, new_status)

            if success:
                print(f"✅ Payment status updated: Student {student_id} -> {new_status}")
                # Refresh the current view
                self._populate_current_students()
            else:
                QMessageBox.critical(
                    self.view,
                    "Update Failed",
                    "Failed to update payment status in database."
                )

        except Exception as e:
            print(f"Error updating payment: {e}")
            import traceback
            traceback.print_exc()

    def show_context_menu(self, position):
        """Show context menu with View Details option"""
        if not hasattr(self.view, 'students_table'):
            return

        item = self.view.students_table.itemAt(position)
        if not item:
            return

        row = item.row()
        student_id_item = self.view.students_table.item(row, 0)
        if not student_id_item:
            return

        student_id = student_id_item.data(Qt.ItemDataRole.UserRole)

        menu = QMenu()

        # NEW: View Details action
        view_details_action = QAction("👁 View Student Details", self.view)
        view_details_action.triggered.connect(lambda: self.show_student_details(student_id))
        menu.addAction(view_details_action)

        menu.addSeparator()

        mark_paid_action = QAction("✅ Mark as Paid", self.view)
        mark_pending_action = QAction("⏳ Mark as Pending", self.view)

        menu.addAction(mark_paid_action)
        menu.addAction(mark_pending_action)

        action = menu.exec(self.view.students_table.viewport().mapToGlobal(position))

        if action == mark_paid_action:
            self.update_student_payment(row, "Paid")
        elif action == mark_pending_action:
            self.update_student_payment(row, "Pending")

    def update_student_payment(self, row, new_status):
        """Update payment status in database and UI using Student Model"""
        try:
            students = self.db.students.get_students_by_section(self.current_section_id)

            if row < len(students):
                student_id = students[row]['id']
                student_name = students[row]['name']

                success = self.db.students.update_payment_status(student_id, new_status)

                if success:
                    payment_item = QTableWidgetItem(new_status)
                    payment_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    if new_status == 'Paid':
                        payment_item.setForeground(Qt.GlobalColor.darkGreen)
                    else:
                        payment_item.setForeground(Qt.GlobalColor.black)

                    if hasattr(self.view, 'students_table'):
                        self.view.students_table.setItem(row, 3, payment_item)

                    QMessageBox.information(
                        self.view,
                        "Success",
                        f"Payment status for {student_name} updated to {new_status}."
                    )
                else:
                    QMessageBox.warning(self.view, "Error", "Failed to update payment status.")

        except Exception as e:
            print(f"Error updating payment: {e}")
            QMessageBox.critical(self.view, "Error", f"An error occurred: {str(e)}")