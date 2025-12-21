"""
Edit Student Dialog - Comprehensive student editing interface
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QLineEdit, QComboBox,
                             QScrollArea, QWidget, QMessageBox, QDateEdit, QTextEdit)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont


class EditStudentDialog(QDialog):
    """Dialog for editing student information"""

    student_updated = pyqtSignal(int, dict)  # student_id, updated_data

    def __init__(self, student_data: dict, sections: list, parent=None):
        super().__init__(parent)
        self.student_data = student_data
        self.sections = sections
        self.setup_ui()
        self.populate_data()

    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle(f"Edit Student - {self.student_data.get('full_name', 'Unknown')}")
        self.setMinimumSize(900, 700)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
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

        # SECTION 1: Personal Information
        content_layout.addWidget(self._create_section_header("👤 Personal Information"))

        # LRN (Read-only)
        lrn_layout = self._create_field_row("LRN:", is_readonly=True)
        self.lrn_display = QLabel(self.student_data.get('lrn', 'N/A'))
        self.lrn_display.setStyleSheet("color: #6B7280; font-size: 13px; padding: 8px;")
        lrn_layout.addWidget(self.lrn_display)
        content_layout.addLayout(lrn_layout)

        # Name Row
        name_row = QHBoxLayout()
        name_row.setSpacing(15)

        fname_layout = self._create_field_col("First Name *")
        self.fname_input = QLineEdit()
        self.fname_input.setStyleSheet(self._input_style())
        self.fname_input.setMinimumHeight(40)
        fname_layout.addWidget(self.fname_input)

        mname_layout = self._create_field_col("Middle Name")
        self.mname_input = QLineEdit()
        self.mname_input.setStyleSheet(self._input_style())
        self.mname_input.setMinimumHeight(40)
        mname_layout.addWidget(self.mname_input)

        lname_layout = self._create_field_col("Last Name *")
        self.lname_input = QLineEdit()
        self.lname_input.setStyleSheet(self._input_style())
        self.lname_input.setMinimumHeight(40)
        lname_layout.addWidget(self.lname_input)

        name_row.addLayout(fname_layout)
        name_row.addLayout(mname_layout)
        name_row.addLayout(lname_layout)
        content_layout.addLayout(name_row)

        # Gender & DOB Row
        personal_row = QHBoxLayout()
        personal_row.setSpacing(15)

        gender_layout = self._create_field_col("Gender *")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female"])
        self.gender_combo.setStyleSheet(self._combo_style())
        self.gender_combo.setMinimumHeight(40)
        gender_layout.addWidget(self.gender_combo)

        dob_layout = self._create_field_col("Date of Birth *")
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDisplayFormat("MMMM dd, yyyy")
        self.dob_input.setStyleSheet(self._combo_style())
        self.dob_input.setMinimumHeight(40)
        dob_layout.addWidget(self.dob_input)

        personal_row.addLayout(gender_layout)
        personal_row.addLayout(dob_layout)
        content_layout.addLayout(personal_row)

        # SECTION 2: Contact Information
        content_layout.addWidget(self._create_section_header("📧 Contact Information"))

        # Address
        address_layout = self._create_field_col("Complete Address *")
        self.address_input = QLineEdit()
        self.address_input.setStyleSheet(self._input_style())
        self.address_input.setMinimumHeight(40)
        address_layout.addWidget(self.address_input)
        content_layout.addLayout(address_layout)

        # Contact & Email Row
        contact_row = QHBoxLayout()
        contact_row.setSpacing(15)

        contact_layout = self._create_field_col("Contact Number *")
        self.contact_input = QLineEdit()
        self.contact_input.setStyleSheet(self._input_style())
        self.contact_input.setMinimumHeight(40)
        self.contact_input.setMaxLength(11)
        contact_layout.addWidget(self.contact_input)

        email_layout = self._create_field_col("Email Address *")
        self.email_input = QLineEdit()
        self.email_input.setStyleSheet(self._input_style())
        self.email_input.setMinimumHeight(40)
        email_layout.addWidget(self.email_input)

        contact_row.addLayout(contact_layout)
        contact_row.addLayout(email_layout)
        content_layout.addLayout(contact_row)

        # SECTION 3: Guardian Information
        content_layout.addWidget(self._create_section_header("👨‍👩‍👧 Guardian Information"))

        guardian_row = QHBoxLayout()
        guardian_row.setSpacing(15)

        gname_layout = self._create_field_col("Guardian's Name")
        self.guardian_name_input = QLineEdit()
        self.guardian_name_input.setStyleSheet(self._input_style())
        self.guardian_name_input.setMinimumHeight(40)
        gname_layout.addWidget(self.guardian_name_input)

        gcontact_layout = self._create_field_col("Guardian's Contact")
        self.guardian_contact_input = QLineEdit()
        self.guardian_contact_input.setStyleSheet(self._input_style())
        self.guardian_contact_input.setMinimumHeight(40)
        self.guardian_contact_input.setMaxLength(11)
        gcontact_layout.addWidget(self.guardian_contact_input)

        guardian_row.addLayout(gname_layout)
        guardian_row.addLayout(gcontact_layout)
        content_layout.addLayout(guardian_row)

        # SECTION 4: Academic Information
        content_layout.addWidget(self._create_section_header("🎓 Academic Information"))

        # Academic Row 1
        academic_row1 = QHBoxLayout()
        academic_row1.setSpacing(15)

        strand_layout = self._create_field_col("Strand *")
        self.strand_combo = QComboBox()
        self.strand_combo.addItems(["STEM", "ABM", "HUMSS", "GAS", "TVL"])
        self.strand_combo.setStyleSheet(self._combo_style())
        self.strand_combo.setMinimumHeight(40)
        strand_layout.addWidget(self.strand_combo)

        grade_layout = self._create_field_col("Grade Level *")
        self.grade_combo = QComboBox()
        self.grade_combo.addItems(["11", "12"])
        self.grade_combo.setStyleSheet(self._combo_style())
        self.grade_combo.setMinimumHeight(40)
        grade_layout.addWidget(self.grade_combo)

        section_layout = self._create_field_col("Section")
        self.section_combo = QComboBox()
        self.section_combo.addItem("No Section", None)
        for section in self.sections:
            display = f"{section['section_name']} ({section['strand']}) - {section['available_slots']} slots"
            self.section_combo.addItem(display, section['id'])
        self.section_combo.setStyleSheet(self._combo_style())
        self.section_combo.setMinimumHeight(40)
        section_layout.addWidget(self.section_combo)

        academic_row1.addLayout(strand_layout)
        academic_row1.addLayout(grade_layout)
        academic_row1.addLayout(section_layout)
        content_layout.addLayout(academic_row1)

        # Last School
        last_school_layout = self._create_field_col("Last School Attended")
        self.last_school_input = QLineEdit()
        self.last_school_input.setStyleSheet(self._input_style())
        self.last_school_input.setMinimumHeight(40)
        last_school_layout.addWidget(self.last_school_input)
        content_layout.addLayout(last_school_layout)

        # SECTION 5: Status Management
        content_layout.addWidget(self._create_section_header("📋 Student Status"))

        status_row = QHBoxLayout()
        status_row.setSpacing(15)

        status_layout = self._create_field_col("Status *")
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Enrolled", "Pending", "Dropped", "Transferred", "Graduated"])
        self.status_combo.setStyleSheet(self._combo_style())
        self.status_combo.setMinimumHeight(40)
        status_layout.addWidget(self.status_combo)

        payment_layout = self._create_field_col("Payment Status *")
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["Pending", "Partial", "Paid"])
        self.payment_combo.setStyleSheet(self._combo_style())
        self.payment_combo.setMinimumHeight(40)
        payment_layout.addWidget(self.payment_combo)

        status_row.addLayout(status_layout)
        status_row.addLayout(payment_layout)
        content_layout.addLayout(status_row)

        # Status Reason
        reason_layout = self._create_field_col("Status Change Reason (if applicable)")
        self.status_reason_input = QTextEdit()
        self.status_reason_input.setStyleSheet(self._input_style())
        self.status_reason_input.setMaximumHeight(80)
        self.status_reason_input.setPlaceholderText("Enter reason for status change...")
        reason_layout.addWidget(self.status_reason_input)
        content_layout.addLayout(reason_layout)

        content_layout.addStretch()

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # Action Buttons
        button_layout = self._create_button_layout()
        main_layout.addLayout(button_layout)

    def _create_header(self) -> QFrame:
        """Create header"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498DB, stop:1 #2C3E50);
                border: none;
            }
        """)
        header.setFixedHeight(80)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 20, 30, 20)

        title = QLabel(f"Edit Student Information")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")

        lrn_badge = QLabel(f"LRN: {self.student_data.get('lrn', 'N/A')}")
        lrn_badge.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 8px 16px;
            border-radius: 8px;
            font-weight: bold;
        """)

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(lrn_badge)

        return header

    def _create_section_header(self, text: str) -> QLabel:
        """Create section header"""
        label = QLabel(text)
        label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        label.setStyleSheet("""
            color: #2C3E50;
            background: transparent;
            padding: 10px 0px;
            border-bottom: 2px solid #E5E7EB;
        """)
        return label

    def _create_field_row(self, label_text: str, is_readonly: bool = False) -> QHBoxLayout:
        """Create field row layout"""
        layout = QHBoxLayout()
        layout.setSpacing(10)

        label = QLabel(label_text)
        label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        label.setStyleSheet("color: #374151; background: transparent;")
        label.setFixedWidth(150)
        layout.addWidget(label)

        return layout

    def _create_field_col(self, label_text: str) -> QVBoxLayout:
        """Create field column layout"""
        layout = QVBoxLayout()
        layout.setSpacing(8)

        label = QLabel(label_text)
        label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        label.setStyleSheet("color: #374151; background: transparent;")
        layout.addWidget(label)

        return layout

    def _input_style(self) -> str:
        """Input field style"""
        return """
            QLineEdit, QTextEdit {
                background-color: white;
                border: 2px solid #E5E7EB;
                padding: 10px;
                border-radius: 8px;
                font-size: 13px;
                color: #1F2937;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #3B82F6;
            }
        """

    def _combo_style(self) -> str:
        """Combobox style"""
        return """
            QComboBox, QDateEdit {
                background-color: white;
                border: 2px solid #E5E7EB;
                padding: 10px;
                border-radius: 8px;
                font-size: 13px;
                color: #1F2937;
            }
            QComboBox:focus, QDateEdit:focus {
                border: 2px solid #3B82F6;
            }
        """

    def _create_button_layout(self) -> QHBoxLayout:
        """Create action buttons"""
        layout = QHBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setMinimumWidth(120)
        self.cancel_btn.setMinimumHeight(45)
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #4B5563; }
        """)
        self.cancel_btn.clicked.connect(self.reject)

        self.save_btn = QPushButton("💾 Save Changes")
        self.save_btn.setMinimumWidth(180)
        self.save_btn.setMinimumHeight(45)
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #2563EB; }
        """)
        self.save_btn.clicked.connect(self.save_changes)

        layout.addWidget(self.cancel_btn)
        layout.addStretch()
        layout.addWidget(self.save_btn)

        return layout

    def populate_data(self):
        """Populate form with existing student data"""
        self.fname_input.setText(self.student_data.get('first_name', ''))
        self.mname_input.setText(self.student_data.get('middle_name', '') or '')
        self.lname_input.setText(self.student_data.get('last_name', ''))

        gender = self.student_data.get('gender', 'Male')
        self.gender_combo.setCurrentText(gender)

        dob = self.student_data.get('date_of_birth')
        if dob:
            if isinstance(dob, str):
                from datetime import datetime
                dob = datetime.strptime(dob, '%Y-%m-%d').date()
            self.dob_input.setDate(QDate(dob.year, dob.month, dob.day))

        self.address_input.setText(self.student_data.get('address', ''))
        self.contact_input.setText(self.student_data.get('contact_number', ''))
        self.email_input.setText(self.student_data.get('email', ''))
        self.guardian_name_input.setText(self.student_data.get('guardian_name', '') or '')
        self.guardian_contact_input.setText(self.student_data.get('guardian_contact', '') or '')
        self.last_school_input.setText(self.student_data.get('last_school', '') or '')

        self.strand_combo.setCurrentText(self.student_data.get('strand', 'STEM'))
        self.grade_combo.setCurrentText(self.student_data.get('grade_level', '11'))

        # Set section
        section_id = self.student_data.get('section_id')
        if section_id:
            for i in range(self.section_combo.count()):
                if self.section_combo.itemData(i) == section_id:
                    self.section_combo.setCurrentIndex(i)
                    break

        self.status_combo.setCurrentText(self.student_data.get('status', 'Enrolled'))
        self.payment_combo.setCurrentText(self.student_data.get('payment_status', 'Pending'))

    def save_changes(self):
        """Validate and save changes"""
        # Validate required fields
        if not all([
            self.fname_input.text().strip(),
            self.lname_input.text().strip(),
            self.address_input.text().strip(),
            self.contact_input.text().strip(),
            self.email_input.text().strip()
        ]):
            QMessageBox.warning(
                self,
                "Validation Error",
                "Please fill in all required fields marked with *"
            )
            return

        # Validate email
        if '@' not in self.email_input.text():
            QMessageBox.warning(
                self,
                "Invalid Email",
                "Please enter a valid email address"
            )
            return

        # Build updated data
        updated_data = {
            'first_name': self.fname_input.text().strip(),
            'middle_name': self.mname_input.text().strip(),
            'last_name': self.lname_input.text().strip(),
            'full_name': f"{self.fname_input.text().strip()} {self.mname_input.text().strip()} {self.lname_input.text().strip()}".replace(
                '  ', ' '),
            'gender': self.gender_combo.currentText(),
            'date_of_birth': self.dob_input.date().toString('yyyy-MM-dd'),
            'address': self.address_input.text().strip(),
            'contact_number': self.contact_input.text().strip(),
            'email': self.email_input.text().strip(),
            'guardian_name': self.guardian_name_input.text().strip() or None,
            'guardian_contact': self.guardian_contact_input.text().strip() or None,
            'last_school': self.last_school_input.text().strip() or None,
            'strand': self.strand_combo.currentText(),
            'grade_level': self.grade_combo.currentText(),
            'section_id': self.section_combo.currentData(),
            'status': self.status_combo.currentText(),
            'payment_status': self.payment_combo.currentText(),
            'status_reason': self.status_reason_input.toPlainText().strip() or None
        }

        # Emit signal with student ID and updated data
        student_id = self.student_data.get('id')
        self.student_updated.emit(student_id, updated_data)
        self.accept()