"""
Dashboard Controller - Uses Student Model directly
UPDATED: Added student details view functionality with better error handling
"""
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton,
                             QMessageBox, QTableWidgetItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from views.dashboard_page import DashboardPageUI
from views.student_details_dialog import StudentDetailsDialog
from views.edit_student_dialog import EditStudentDialog


class DashboardController(QObject):
    def __init__(self, database):
        super().__init__()

        # Store database reference
        self.db = database

        # Create view
        self.view = DashboardPageUI()

        # Connect signals
        self._connect_signals()

        # Load initial data
        self.refresh_data()

    def get_view(self) -> QWidget:
        return self.view

    def _connect_signals(self):
        """Connect UI signals safely"""
        # Search functionality
        if hasattr(self.view, 'search_requested'):
            self.view.search_requested.connect(self.handle_search)

        if hasattr(self.view, 'clear_search_requested'):
            self.view.clear_search_requested.connect(self.refresh_data)

        if hasattr(self.view, 'advanced_search_btn'):
            self.view.advanced_search_btn.clicked.connect(self.show_advanced_search)

        # Edit/Delete functionality
        if hasattr(self.view, 'edit_requested'):
            self.view.edit_requested.connect(self.handle_edit_student)

        if hasattr(self.view, 'delete_requested'):
            self.view.delete_requested.connect(self.handle_delete_student)

        # NEW: Double-click to view details
        if hasattr(self.view, 'activity_table'):
            self.view.activity_table.cellDoubleClicked.connect(self.handle_view_student_details)

    def handle_advanced_search(self, filters: dict):
        """Handle advanced search request"""
        try:
            print(f"\n=== ADVANCED SEARCH ===")
            print(f"Filters: {filters}")

            # Use advanced_search method from Student model
            results = self.db.students.advanced_search(filters)
            print(f"Found {len(results)} results")

            # Display results in table
            self.view.activity_table.setRowCount(0)

            for row, data in enumerate(results):
                student_id = data.get('id')
                if not student_id:
                    continue

                self.view.activity_table.insertRow(row)

                # Name with ID
                name_item = QTableWidgetItem(data['full_name'])
                name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                name_item.setData(Qt.ItemDataRole.UserRole, student_id)
                self.view.activity_table.setItem(row, 0, name_item)

                # Strand
                strand_item = QTableWidgetItem(data['strand'])
                strand_item.setFlags(strand_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                strand_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.view.activity_table.setItem(row, 1, strand_item)

                # Date
                date_item = QTableWidgetItem(data['date'])
                date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.view.activity_table.setItem(row, 2, date_item)

                # Actions
                action_widget = self._create_action_buttons(student_id, data['full_name'])
                self.view.activity_table.setCellWidget(row, 3, action_widget)

                self.view.activity_table.setRowHeight(row, 50)

            # Update header
            if hasattr(self.view, 'set_search_results_mode'):
                self.view.set_search_results_mode(len(results))

            QMessageBox.information(
                self.view,
                "Search Complete",
                f"Found {len(results)} student(s) matching your criteria"
            )

            print("=== ADVANCED SEARCH COMPLETE ===\n")

        except Exception as e:
            print(f"Error in advanced search: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.view,
                "Search Error",
                f"An error occurred during search:\n{str(e)}"
            )

    def show_advanced_search(self):
        """Show advanced search dialog"""
        try:
            from views.advanced_search_dialog import AdvancedSearchDialog

            dialog = AdvancedSearchDialog(self.view)
            dialog.search_requested.connect(self.handle_advanced_search)
            dialog.exec()

        except Exception as e:
            print(f"Error showing advanced search: {e}")
            import traceback
            traceback.print_exc()

    def refresh_data(self):
        """Fetch latest data and update UI using Student Model"""
        try:
            print("\n=== DASHBOARD REFRESH DEBUG ===")

            # Get stats from Student Model
            stats = self.db.students.get_enrollment_stats()
            print(f"Stats retrieved: {stats}")

            # Update stat cards
            self._update_stat_card("total_students", str(stats.get('total_enrolled', 0)))
            available = stats.get('available_slots', 0)
            total = stats.get('total_slots', 500)
            self._update_stat_card("available_slots", f"{available} / {total}")

            # Update Strand Grid
            self._update_strand_grid(stats.get('by_strand', []))

            # Update Activity Table
            self._update_activity_table()

            # Set to recent mode
            if hasattr(self.view, 'set_recent_mode'):
                self.view.set_recent_mode()

            print("=== DASHBOARD REFRESH COMPLETE ===\n")

        except Exception as e:
            print(f"Error refreshing dashboard: {e}")
            import traceback
            traceback.print_exc()

    def _update_stat_card(self, card_name: str, value: str):
        """Update a stat card value"""
        try:
            if card_name == "total_students":
                card = self.view.total_card
            elif card_name == "available_slots":
                card = self.view.available_card
            else:
                return

            # Find the value label in the card
            value_label = card.findChild(QLabel, "value_label")
            if value_label:
                value_label.setText(value)
        except Exception as e:
            print(f"Error updating stat card: {e}")

    def _update_strand_grid(self, strand_data):
        """Populate the strand distribution grid"""
        # Clear existing widgets
        while self.view.strand_grid.count():
            item = self.view.strand_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        strand_colors = {
            'STEM': '#E74C3C', 'ABM': '#F1C40F', 'HUMSS': '#3498DB',
            'GAS': '#2ECC71', 'TVL': '#9B59B6'
        }

        row, col = 0, 0
        for strand in strand_data:
            strand_info = {
                'name': strand['name'],
                'count': strand['enrolled'],
                'color': strand_colors.get(strand['name'], '#95A5A6')
            }
            widget = self._create_strand_widget(strand_info)
            self.view.strand_grid.addWidget(widget, row, col)

            col += 1
            if col > 2:
                col = 0
                row += 1

    def _create_strand_widget(self, strand: dict) -> QWidget:
        """Create a strand display widget"""
        from PyQt6.QtWidgets import QWidget

        widget = QWidget()
        widget.setObjectName("StrandCard")
        widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        widget.setStyleSheet("""
            QWidget#StrandCard { 
                background-color: white; 
                border-radius: 10px; 
                border: 1px solid #E8ECF1;
            }
        """)

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)

        header = QHBoxLayout()
        indicator = QLabel("●")
        indicator.setStyleSheet(f"color: {strand['color']}; font-size: 16px; border: none; background: transparent;")

        name = QLabel(strand['name'])
        name.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        name.setStyleSheet("border: none; background: transparent; color: #2C3E50;")

        header.addWidget(indicator)
        header.addWidget(name)
        header.addStretch()

        count = QLabel(f"{strand['count']} Students")
        count.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        count.setStyleSheet("color: #2C3E50; border: none; background: transparent;")

        layout.addLayout(header)
        layout.addWidget(count)
        return widget

    def _update_activity_table(self):
        """Load recent enrollments from Student Model"""
        try:
            print("\n=== ACTIVITY TABLE UPDATE DEBUG ===")

            # Get recent enrollments from Student Model
            enrollments = self.db.students.get_recent_enrollments(10)
            print(f"Found {len(enrollments)} recent enrollments")

            # Clear and set row count
            self.view.activity_table.setRowCount(0)

            for row, data in enumerate(enrollments):
                print(f"Row {row}: ID={data.get('id')}, Name={data.get('full_name')}")

                # VERIFY student_id exists
                student_id = data.get('id')
                if not student_id:
                    print(f"⚠️ WARNING: Student at row {row} has no ID! Data: {data}")
                    continue

                self.view.activity_table.insertRow(row)

                # Name - STORE ID IN USEROLE
                name_item = QTableWidgetItem(data['full_name'])
                name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                name_item.setData(Qt.ItemDataRole.UserRole, student_id)  # Store ID here
                self.view.activity_table.setItem(row, 0, name_item)

                # VERIFY the ID was stored
                stored_id = name_item.data(Qt.ItemDataRole.UserRole)
                print(f"  → Stored ID in UserRole: {stored_id}")

                # Strand
                strand_item = QTableWidgetItem(data['strand'])
                strand_item.setFlags(strand_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                strand_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.view.activity_table.setItem(row, 1, strand_item)

                # Date
                date_str = str(data['date']) if data['date'] else 'N/A'
                date_item = QTableWidgetItem(date_str)
                date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.view.activity_table.setItem(row, 2, date_item)

                # Action buttons
                action_widget = self._create_action_buttons(student_id, data['full_name'])
                self.view.activity_table.setCellWidget(row, 3, action_widget)

                # Set row height for better visibility
                self.view.activity_table.setRowHeight(row, 50)

            print(f"Activity table now has {self.view.activity_table.rowCount()} rows")
            print("=== ACTIVITY TABLE UPDATE COMPLETE ===\n")

        except Exception as e:
            print(f"❌ Error updating activity table: {e}")
            import traceback
            traceback.print_exc()

    def _create_action_buttons(self, student_id, student_name):
        """Create action buttons with View Details button"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # NEW: View Details button
        view_btn = QPushButton("View")
        view_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        view_btn.setStyleSheet("background-color: #16A085; color: white; border-radius: 4px; padding: 4px 8px;")
        view_btn.clicked.connect(lambda: self.show_student_details(student_id))

        edit_btn = QPushButton("Edit")
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setStyleSheet("background-color: #3498DB; color: white; border-radius: 4px; padding: 4px 8px;")
        edit_btn.clicked.connect(lambda: self._safe_emit(self.view.edit_requested, student_id, student_name))

        delete_btn = QPushButton("Delete")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setStyleSheet("background-color: #E74C3C; color: white; border-radius: 4px; padding: 4px 8px;")
        delete_btn.clicked.connect(lambda: self._safe_emit(self.view.delete_requested, student_id, student_name))

        layout.addWidget(view_btn)
        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)
        layout.addStretch()
        return widget

    def _safe_emit(self, signal, *args):
        """Helper to emit signals only if they exist"""
        try:
            signal.emit(*args)
        except AttributeError:
            print("Signal not found in View")

    def handle_view_student_details(self, row: int, column: int):
        """Handle double-click on table row to view student details"""
        print(f"\n=== DOUBLE-CLICK DEBUG ===")
        print(f"Row clicked: {row}, Column: {column}")

        # Get student ID from the first column's UserRole data
        item = self.view.activity_table.item(row, 0)
        if item:
            student_id = item.data(Qt.ItemDataRole.UserRole)
            print(f"Retrieved student_id from UserRole: {student_id}")
            print(f"Student_id type: {type(student_id)}")

            if student_id:
                self.show_student_details(student_id)
            else:
                print("❌ ERROR: No student_id found in UserRole!")
                QMessageBox.warning(
                    self.view,
                    "Error",
                    "Could not retrieve student ID from table.\nPlease try refreshing the dashboard."
                )
        else:
            print("❌ ERROR: No item found at row 0!")

        print("=== DOUBLE-CLICK DEBUG END ===\n")

    def show_student_details(self, student_id: int):
        """Show detailed student information dialog"""
        print(f"\n=== SHOW STUDENT DETAILS DEBUG ===")
        print(f"Attempting to fetch student with ID: {student_id}")
        print(f"Student ID type: {type(student_id)}")


        try:
            # Verify database connection
            if not self.db or not self.db.test_connection():
                print("❌ ERROR: Database connection lost!")
                QMessageBox.critical(
                    self.view,
                    "Database Error",
                    "Lost connection to database. Please restart the application."
                )
                return

            # Get complete student data
            print("Calling db.students.get_student_by_id()...")
            student = self.db.students.get_student_by_id(student_id)
            print(f"Result: {student}")

            if not student:
                print(f"❌ ERROR: Student with ID {student_id} not found in database!")

                # Double-check if student exists at all
                all_students = self.db.students.get_all_students()
                student_ids = [s.id for s in all_students]
                print(f"Available student IDs in database: {student_ids}")

                QMessageBox.warning(
                    self.view,
                    "Student Not Found",
                    f"Student with ID {student_id} was not found in the database.\n\n"
                    f"This may happen if the student was recently deleted.\n"
                    f"Please refresh the dashboard and try again."
                )
                return

            print(f"✅ Student found: {student.full_name}")

            # Convert to dictionary for dialog
            student_data = student.to_dict()
            print(f"Student data keys: {student_data.keys()}")

            # Create and show dialog
            dialog = StudentDetailsDialog(student_data, self.view)

            # Connect signals
            dialog.payment_updated.connect(self.handle_payment_update)
            dialog.payment_record_requested.connect(self.handle_record_payment)

            dialog.exec()

            print("=== SHOW STUDENT DETAILS COMPLETE ===\n")

        except Exception as e:
            print(f"❌ EXCEPTION in show_student_details: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Failed to load student details:\n\n{str(e)}\n\n"
                f"Student ID: {student_id}\n"
                f"Please check the console for more details."
            )

    def handle_record_payment(self, student_id: int):
        """Handle payment recording request"""
        try:
            from views.record_payment_dialog import RecordPaymentDialog
            from models.payment import PaymentData

            # Get student data
            student = self.db.students.get_student_by_id(student_id)
            if not student:
                QMessageBox.warning(self.view, "Error", "Student not found")
                return

            student_data = student.to_dict()

            # Get payment summary
            payment_summary = self.db.payments.get_payment_summary(student_id)

            # Show payment dialog
            payment_dialog = RecordPaymentDialog(student_data, payment_summary, self.view)
            payment_dialog.payment_recorded.connect(self.process_payment)
            payment_dialog.exec()

        except Exception as e:
            print(f"Error showing payment dialog: {e}")
            import traceback
            traceback.print_exc()

    def process_payment(self, student_id: int, payment_data: dict):
        """Process and save payment, then generate receipt"""
        try:
            from models.payment import PaymentData
            from utils.receipt_generator import generate_payment_receipt
            import os

            # Create PaymentData object
            payment = PaymentData(
                student_id=payment_data['student_id'],
                amount=payment_data['amount'],
                payment_date=payment_data['payment_date'],
                payment_method=payment_data['payment_method'],
                payment_type=payment_data['payment_type'],
                reference_number=payment_data.get('reference_number'),
                notes=payment_data.get('notes')
            )

            # TODO: Get actual user_id from session
            user_id = 1

            # Save payment to database
            success, message, payment_id = self.db.payments.add_payment(payment, user_id)

            if not success:
                QMessageBox.critical(
                    self.view,
                    "Payment Failed",
                    f"Failed to record payment:\n{message}"
                )
                return

            # Get complete payment data for receipt
            payments = self.db.payments.get_student_payments(student_id)
            if not payments:
                QMessageBox.warning(self.view, "Error", "Could not retrieve payment data")
                return

            payment_record = payments[0]  # Most recent

            # Get student data
            student = self.db.students.get_student_by_id(student_id)
            student_data = student.to_dict()

            # Generate receipt PDF
            receipt_path = generate_payment_receipt(payment_record, student_data)

            if receipt_path:
                reply = QMessageBox.information(
                    self.view,
                    "✅ Payment Recorded Successfully",
                    f"<b>Payment has been recorded successfully!</b><br><br>"
                    f"<b>Receipt Number:</b> {message.split(': ')[1]}<br>"
                    f"<b>Amount:</b> ₱{payment.amount:,.2f}<br><br>"
                    f"Receipt saved to: {receipt_path}<br><br>"
                    f"Would you like to open the receipt now?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )

                if reply == QMessageBox.StandardButton.Yes:
                    # Open PDF
                    if os.name == 'nt':  # Windows
                        os.startfile(receipt_path)
                    elif os.name == 'posix':  # macOS/Linux
                        import subprocess
                        subprocess.call(('open' if os.uname().sysname == 'Darwin' else 'xdg-open', receipt_path))

            # Refresh dashboard
            self.refresh_data()

        except Exception as e:
            print(f"Error processing payment: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Failed to process payment:\n{str(e)}"
            )

    def handle_payment_update(self, student_id: int, new_status: str):
        """Handle payment status update from details dialog"""
        try:
            success = self.db.students.update_payment_status(student_id, new_status)

            if success:
                print(f"✅ Payment status updated: Student {student_id} -> {new_status}")
                # Refresh the table to show updated data
                self.refresh_data()
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

    def handle_search(self, query: str):
        """Handle search requests using Student Model"""
        try:
            print(f"\n=== SEARCH DEBUG ===")
            print(f"Search query: '{query}'")

            # Search using Student Model
            results = self.db.students.search_students(query)
            print(f"Found {len(results)} search results")

            # Update table with search results
            self.view.activity_table.setRowCount(0)
            for row, data in enumerate(results):
                print(f"Search result {row}: ID={data.get('id')}, Name={data.get('full_name')}")

                student_id = data.get('id')
                if not student_id:
                    print(f"⚠️ WARNING: Search result at row {row} has no ID!")
                    continue

                self.view.activity_table.insertRow(row)

                # Name - STORE ID
                name_item = QTableWidgetItem(data['full_name'])
                name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                name_item.setData(Qt.ItemDataRole.UserRole, student_id)
                self.view.activity_table.setItem(row, 0, name_item)

                # Strand
                strand_item = QTableWidgetItem(data['strand'])
                strand_item.setFlags(strand_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                strand_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.view.activity_table.setItem(row, 1, strand_item)

                # Date
                date_str = str(data['date']) if data['date'] else 'N/A'
                date_item = QTableWidgetItem(date_str)
                date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.view.activity_table.setItem(row, 2, date_item)

                action_widget = self._create_action_buttons(student_id, data['full_name'])
                self.view.activity_table.setCellWidget(row, 3, action_widget)

                # Set row height
                self.view.activity_table.setRowHeight(row, 50)


            # Update header
            if hasattr(self.view, 'set_search_results_mode'):
                self.view.set_search_results_mode(len(results))

            print("=== SEARCH COMPLETE ===\n")

        except Exception as e:
            print(f"❌ Error searching students: {e}")
            import traceback
            traceback.print_exc()

    def handle_edit_student(self, student_id, current_name):
        """Handle edit student request"""
        try:
            # Get student data
            student = self.db.students.get_student_by_id(student_id)
            if not student:
                QMessageBox.warning(self.view, "Error", "Student not found")
                return

            # Get available sections
            sections = self.db.sections.get_all_sections()
            sections_list = [s.to_dict() for s in sections]

            # Show edit dialog

            dialog = EditStudentDialog(student.to_dict(), sections_list, self.view)
            dialog.student_updated.connect(self.handle_student_update)
            dialog.exec()

        except Exception as e:
            print(f"Error in handle_edit_student: {e}")
            import traceback
            traceback.print_exc()

    def handle_student_update(self, student_id: int, updated_data: dict):
        """Handle student update from edit dialog"""
        try:
            # Get current user ID (you may need to pass this from main_controller)
            user_id = 1  # TODO: Get from session

            success, message = self.db.students.update_student(student_id, updated_data, user_id)

            if success:
                QMessageBox.information(
                    self.view,
                    "✅ Success",
                    "Student information updated successfully!"
                )
                self.refresh_data()
            else:
                QMessageBox.critical(
                    self.view,
                    "Error",
                    f"Failed to update student:\n{message}"
                )

        except Exception as e:
            print(f"Error updating student: {e}")
            import traceback
            traceback.print_exc()

    def handle_delete_student(self, student_id, student_name):
        """Handle delete student request"""
        reply = QMessageBox.question(
            self.view, "Confirm Delete",
            f"Are you sure you want to delete {student_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            # Use Student Model to delete
            if self.db.students.delete_student(student_id):
                self.refresh_data()
                QMessageBox.information(self.view, "Success", "Student deleted successfully.")
            else:
                QMessageBox.critical(self.view, "Error", "Failed to delete student.")