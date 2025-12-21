"""
Student Details Dialog - View and Edit Student Information
Shows complete student data with payment status management
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QGridLayout, QComboBox,
                             QLineEdit, QScrollArea, QWidget, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class StudentDetailsDialog(QDialog):
    payment_updated = pyqtSignal(int, str)
    payment_record_requested = pyqtSignal(int)
    """Dialog for viewing and editing student details"""

    # Signals
    payment_updated = pyqtSignal(int, str)  # student_id, new_status
    student_updated = pyqtSignal(int, dict)  # student_id, updated_data

    def __init__(self, student_data: dict, parent=None):
        super().__init__(parent)
        self.student_data = student_data
        self.edit_mode = False
        self.setup_ui()

    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle(f"Student Details - {self.student_data.get('full_name', 'Unknown')}")
        self.setMinimumSize(700, 600)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header Section
        header = self._create_header()
        main_layout.addWidget(header)

        # Scrollable Content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #F5F7FA; }")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Personal Information Section
        content_layout.addWidget(self._create_section_header("👤 Personal Information"))
        content_layout.addWidget(self._create_personal_info_section())

        # Contact Information Section
        content_layout.addWidget(self._create_section_header("📧 Contact Information"))
        content_layout.addWidget(self._create_contact_info_section())

        # Guardian Information Section
        content_layout.addWidget(self._create_section_header("👨‍👩‍👧 Guardian Information"))
        content_layout.addWidget(self._create_guardian_info_section())

        # Academic Information Section
        content_layout.addWidget(self._create_section_header("🎓 Academic Information"))
        content_layout.addWidget(self._create_academic_info_section())

        # Payment Information Section
        content_layout.addWidget(self._create_section_header("💳 Payment Information"))
        content_layout.addWidget(self._create_payment_section())

        content_layout.addStretch()

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # Action Buttons
        button_layout = self._create_button_layout()
        main_layout.addLayout(button_layout)

        self.record_payment_btn.clicked.connect(lambda: self.payment_record_requested.emit(self.student_data['id']))

    def _create_header(self) -> QFrame:
        """Create header with student name and status"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #365486, stop:1 #2C3E50);
                border: none;
            }
        """)
        header.setFixedHeight(100)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 20, 30, 20)

        # Student Name
        name_label = QLabel(self.student_data.get('full_name', 'Unknown Student'))
        name_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        name_label.setStyleSheet("color: white; background: transparent; border: none;")

        # LRN Badge
        lrn_badge = QLabel(f"LRN: {self.student_data.get('lrn', 'N/A')}")
        lrn_badge.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: bold;
            border: none;
        """)

        # Status Badge
        status = self.student_data.get('status', 'Enrolled')
        status_color = '#27AE60' if status == 'Enrolled' else '#E74C3C'
        status_badge = QLabel(f"● {status}")
        status_badge.setStyleSheet(f"""
            background-color: transparent;
            color: {status_color};
            padding: 8px 16px;
            border-radius: 8px;
            border: 3px solid {status_color};
            font-size: 13px;
            font-weight: bold;
        """)

        layout.addWidget(name_label)
        layout.addStretch()
        layout.addWidget(lrn_badge)
        layout.addWidget(status_badge)

        return header

    def _create_section_header(self, title: str) -> QLabel:
        """Create section header label"""
        label = QLabel(title)
        label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        label.setStyleSheet("""
            color: #2C3E50;
            background: transparent;
            border: none;
            padding: 10px 0px;
            border-bottom: 2px solid #E5E7EB;
        """)
        return label

    def _create_info_card(self) -> QFrame:
        """Create a styled card for information"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #E5E7EB;
            }
        """)
        return card

    def _create_personal_info_section(self) -> QFrame:
        """Create personal information section"""
        card = self._create_info_card()
        layout = QGridLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Full Name
        self._add_info_row(layout, 0, "Full Name:", self.student_data.get('full_name', 'N/A'))

        # Gender
        self._add_info_row(layout, 1, "Gender:", self.student_data.get('gender', 'N/A'))

        # Date of Birth
        dob = self.student_data.get('date_of_birth', 'N/A')
        self._add_info_row(layout, 2, "Date of Birth:", str(dob) if dob else 'N/A')

        # Age (calculate if DOB available)
        if dob and dob != 'N/A':
            try:
                from datetime import datetime
                dob_date = datetime.strptime(str(dob), '%Y-%m-%d')
                age = (datetime.now() - dob_date).days // 365
                self._add_info_row(layout, 3, "Age:", f"{age} years old")
            except:
                pass

        return card

    def _create_contact_info_section(self) -> QFrame:
        """Create contact information section"""
        card = self._create_info_card()
        layout = QGridLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Email
        self._add_info_row(layout, 0, "Email:", self.student_data.get('email', 'N/A'))

        # Contact Number
        self._add_info_row(layout, 1, "Contact Number:", self.student_data.get('contact_number', 'N/A'))

        # Address
        address = self.student_data.get('address', 'N/A')
        self._add_info_row(layout, 2, "Address:", address, multiline=True)

        return card

    def _create_guardian_info_section(self) -> QFrame:
        """Create guardian information section"""
        card = self._create_info_card()
        layout = QGridLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Guardian Name
        guardian_name = self.student_data.get('guardian_name', 'Not provided')
        self._add_info_row(layout, 0, "Guardian Name:", guardian_name or 'Not provided')

        # Guardian Contact
        guardian_contact = self.student_data.get('guardian_contact', 'Not provided')
        self._add_info_row(layout, 1, "Guardian Contact:", guardian_contact or 'Not provided')

        return card

    def _create_academic_info_section(self) -> QFrame:
        """Create academic information section"""
        card = self._create_info_card()
        layout = QGridLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Strand
        self._add_info_row(layout, 0, "Strand:", self.student_data.get('strand', 'N/A'))

        # Track
        self._add_info_row(layout, 1, "Track:", self.student_data.get('track', 'N/A'))

        # Section
        section_name = self.student_data.get('section_name', 'Not yet assigned')
        self._add_info_row(layout, 2, "Section:", section_name or 'Not yet assigned')

        # Grade Level
        self._add_info_row(layout, 3, "Grade Level:", self.student_data.get('grade_level', '11'))

        # Enrollment Date
        enrollment_date = self.student_data.get('enrollment_date', 'N/A')
        if enrollment_date:
            try:
                from datetime import datetime
                date_obj = datetime.strptime(str(enrollment_date)[:19], '%Y-%m-%d %H:%M:%S')
                formatted_date = date_obj.strftime('%B %d, %Y at %I:%M %p')
                self._add_info_row(layout, 4, "Enrollment Date:", formatted_date)
            except:
                self._add_info_row(layout, 4, "Enrollment Date:", str(enrollment_date))

        return card

    def _create_payment_section(self) -> QFrame:
        """Create payment information section with update capability"""
        # CREATE CARD AND LAYOUT FIRST
        card = self._create_info_card()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Current Payment Status
        status_layout = QHBoxLayout()

        status_label = QLabel("Payment Status:")
        status_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        status_label.setStyleSheet("color: #374151; background: transparent; border: none;")

        current_status = self.student_data.get('payment_status', 'Pending')

        # Status display badge
        self.status_display = QLabel(current_status)
        status_color = '#27AE60' if current_status == 'Paid' else '#F39C12'
        self.status_display.setStyleSheet(f"""
            background-color: transparent;
            color: {status_color};
            padding: 8px 20px;
            border: 3px solid {status_color};
            border-radius: 6px;
            font-weight: bold;
        """)

        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_display)
        status_layout.addStretch()

        layout.addLayout(status_layout)

        # Payment Status Update Section
        update_layout = QHBoxLayout()

        update_label = QLabel("Update Status:")
        update_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        update_label.setStyleSheet("color: #6B7280; background: transparent; border: none;")

        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["Pending", "Paid", "Partial"])
        self.payment_combo.setCurrentText(current_status)
        self.payment_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #E5E7EB;
                padding: 8px 12px;
                border-radius: 6px;
                min-width: 150px;
            }
            QComboBox:hover {
                border: 2px solid #3B82F6;
            }
        """)

        self.update_payment_btn = QPushButton("💾 Update Payment")
        self.update_payment_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_payment_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
        """)
        self.update_payment_btn.clicked.connect(self._on_update_payment)

        update_layout.addWidget(update_label)
        update_layout.addWidget(self.payment_combo)
        update_layout.addWidget(self.update_payment_btn)
        update_layout.addStretch()

        layout.addLayout(update_layout)

        # Payment Mode
        payment_mode = self.student_data.get('payment_mode', 'Not specified')
        mode_label = QLabel(f"Payment Mode: {payment_mode}")
        mode_label.setStyleSheet("color: #6B7280; font-size: 11px; background: transparent; border: none;")
        layout.addWidget(mode_label)

        # Add some spacing
        layout.addSpacing(20)

        # NOW ADD THE RECORD PAYMENT BUTTON
        self.record_payment_btn = QPushButton("💳 Record New Payment")
        self.record_payment_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #229954; }
        """)
        self.record_payment_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.record_payment_btn.setMinimumHeight(45)

        # Add button to the layout
        layout.addWidget(self.record_payment_btn)

        return card

    def _add_info_row(self, layout: QGridLayout, row: int, label_text: str, value_text: str, multiline: bool = False):
        """Add an information row to the grid layout"""
        # Label
        label = QLabel(label_text)
        label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        label.setStyleSheet("color: #6B7280; background: transparent; border: none;")
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        # Value
        value = QLabel(value_text)
        value.setFont(QFont("Segoe UI", 10))
        value.setStyleSheet("color: #1F2937; background: transparent; border: none;")
        value.setWordWrap(multiline)
        if multiline:
            value.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(label, row, 0)
        layout.addWidget(value, row, 1)

    def _create_button_layout(self) -> QHBoxLayout:
        """Create action buttons layout"""
        layout = QHBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)

        # Close Button
        self.close_btn = QPushButton("Close")
        self.close_btn.setMinimumWidth(120)
        self.close_btn.setMinimumHeight(40)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        self.close_btn.clicked.connect(self.accept)

        layout.addStretch()
        layout.addWidget(self.close_btn)

        return layout

    def _on_update_payment(self):
        """Handle payment status update"""
        new_status = self.payment_combo.currentText()
        current_status = self.student_data.get('payment_status', 'Pending')

        if new_status == current_status:
            QMessageBox.information(
                self,
                "No Change",
                "Payment status is already set to this value."
            )
            return

        # Confirm update
        reply = QMessageBox.question(
            self,
            "Confirm Payment Update",
            f"Update payment status from '{current_status}' to '{new_status}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Emit signal to controller
            student_id = self.student_data.get('id')
            self.payment_updated.emit(student_id, new_status)

            # Update display
            self.student_data['payment_status'] = new_status
            status_color = '#27AE60' if new_status == 'Paid' else '#F39C12'
            self.status_display.setText(new_status)
            self.status_display.setStyleSheet(f"""
                background-color: {status_color};
                color: white;
                padding: 8px 20px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            """)

            QMessageBox.information(
                self,
                "✅ Success",
                f"Payment status updated to '{new_status}' successfully!"
            )