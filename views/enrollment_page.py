from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QComboBox, QPushButton, QFrame,
                             QScrollArea, QDateEdit, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor


class EnrollmentPageUI(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Create clean, modern UI with improved aesthetics"""
        # Main scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea { 
                border: none; 
                background-color: #F5F7FA;
            }
        """)

        # Container widget
        container = QWidget()
        container.setStyleSheet("background-color: #F5F7FA;")
        self.main_layout = QVBoxLayout(container)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(24)

        # ===== HEADER SECTION =====
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(8)
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel("New Student Enrollment")
        self.title_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #1A1A2E; background: transparent;")

        self.subtitle_label = QLabel("Complete the form below to enroll a new student")
        self.subtitle_label.setFont(QFont("Segoe UI", 12))
        self.subtitle_label.setStyleSheet("color: #6B7280; background: transparent;")

        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.subtitle_label)
        self.main_layout.addWidget(header_widget)

        # ===== LIMITS CARD =====
        self.limits_card = self._create_limits_card()
        self.main_layout.addWidget(self.limits_card)

        # ===== FORM SECTION =====
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                border: none;
            }
        """)
        self._add_shadow(form_frame)

        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(32)

        # === SECTION 1: Basic Information ===
        form_layout.addWidget(self._create_section_header("👤 Basic Information"))

        # LRN (Full Width)
        lrn_layout = self._create_field_layout("Learner Reference Number (LRN)", required=True)
        self.lrn_input = QLineEdit()
        self.lrn_input.setPlaceholderText("Enter 12-digit LRN (e.g., 123456789012)")
        self.lrn_input.setStyleSheet(self._input_style())
        self.lrn_input.setFixedHeight(48)
        self.lrn_input.setMaxLength(12)
        lrn_layout.addWidget(self.lrn_input)
        form_layout.addLayout(lrn_layout)

        # Name Row
        name_layout = QHBoxLayout()
        name_layout.setSpacing(16)

        fname_col = self._create_field_layout("First Name", required=True)
        self.fname_input = QLineEdit()
        self.fname_input.setPlaceholderText("Given name")
        self.fname_input.setStyleSheet(self._input_style())
        self.fname_input.setFixedHeight(48)
        fname_col.addWidget(self.fname_input)

        mname_col = self._create_field_layout("Middle Name")
        self.mname_input = QLineEdit()
        self.mname_input.setPlaceholderText("Optional")
        self.mname_input.setStyleSheet(self._input_style())
        self.mname_input.setFixedHeight(48)
        mname_col.addWidget(self.mname_input)

        lname_col = self._create_field_layout("Last Name", required=True)
        self.lname_input = QLineEdit()
        self.lname_input.setPlaceholderText("Surname")
        self.lname_input.setStyleSheet(self._input_style())
        self.lname_input.setFixedHeight(48)
        lname_col.addWidget(self.lname_input)

        name_layout.addLayout(fname_col, 1)
        name_layout.addLayout(mname_col, 1)
        name_layout.addLayout(lname_col, 1)
        form_layout.addLayout(name_layout)

        # Personal Info Row
        personal_layout = QHBoxLayout()
        personal_layout.setSpacing(16)

        gender_col = self._create_field_layout("Gender", required=True)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female"])
        self.gender_combo.setStyleSheet(self._combo_style())
        self.gender_combo.setFixedHeight(48)
        gender_col.addWidget(self.gender_combo)

        dob_col = self._create_field_layout("Date of Birth", required=True)
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setDisplayFormat("MMMM dd, yyyy")
        self.dob_input.setDate(QDate.currentDate().addYears(-16))
        self.dob_input.setStyleSheet(self._combo_style())
        self.dob_input.setFixedHeight(48)
        dob_col.addWidget(self.dob_input)

        personal_layout.addLayout(gender_col, 1)
        personal_layout.addLayout(dob_col, 1)
        form_layout.addLayout(personal_layout)

        # === SECTION 2: Contact Information ===
        form_layout.addWidget(self._create_section_header("📧 Contact Information"))

        # Address
        address_layout = self._create_field_layout("Complete Address", required=True)
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Street, Barangay, City/Municipality, Province")
        self.address_input.setStyleSheet(self._input_style())
        self.address_input.setFixedHeight(48)
        address_layout.addWidget(self.address_input)
        form_layout.addLayout(address_layout)

        # Contact Row
        contact_layout = QHBoxLayout()
        contact_layout.setSpacing(16)

        contact_col = self._create_field_layout("Contact Number", required=True)
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("09XXXXXXXXX")
        self.contact_input.setStyleSheet(self._input_style())
        self.contact_input.setFixedHeight(48)
        self.contact_input.setMaxLength(11)
        contact_col.addWidget(self.contact_input)

        email_col = self._create_field_layout("Email Address", required=True)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("student@example.com")
        self.email_input.setStyleSheet(self._input_style())
        self.email_input.setFixedHeight(48)
        email_col.addWidget(self.email_input)

        contact_layout.addLayout(contact_col, 1)
        contact_layout.addLayout(email_col, 1)
        form_layout.addLayout(contact_layout)

        # === SECTION 3: Guardian Information ===
        form_layout.addWidget(self._create_section_header("👨‍👩‍👧 Guardian Information"))

        guardian_layout = QHBoxLayout()
        guardian_layout.setSpacing(16)

        guardian_name_col = self._create_field_layout("Guardian's Full Name")
        self.guardian_name_input = QLineEdit()
        self.guardian_name_input.setPlaceholderText("Parent or guardian name")
        self.guardian_name_input.setStyleSheet(self._input_style())
        self.guardian_name_input.setFixedHeight(48)
        guardian_name_col.addWidget(self.guardian_name_input)

        guardian_contact_col = self._create_field_layout("Guardian's Contact")
        self.guardian_contact_input = QLineEdit()
        self.guardian_contact_input.setPlaceholderText("09XXXXXXXXX")
        self.guardian_contact_input.setStyleSheet(self._input_style())
        self.guardian_contact_input.setFixedHeight(48)
        self.guardian_contact_input.setMaxLength(11)
        guardian_contact_col.addWidget(self.guardian_contact_input)

        guardian_layout.addLayout(guardian_name_col, 1)
        guardian_layout.addLayout(guardian_contact_col, 1)
        form_layout.addLayout(guardian_layout)

        # === SECTION 4: Academic Information ===
        form_layout.addWidget(self._create_section_header("🎓 Academic Information"))

        # Last School
        last_school_layout = self._create_field_layout("Last School Attended")
        self.last_school_input = QLineEdit()
        self.last_school_input.setPlaceholderText("Previous school name")
        self.last_school_input.setStyleSheet(self._input_style())
        self.last_school_input.setFixedHeight(48)
        last_school_layout.addWidget(self.last_school_input)
        form_layout.addLayout(last_school_layout)

        # Academic Row
        academic_layout = QHBoxLayout()
        academic_layout.setSpacing(16)

        strand_col = self._create_field_layout("Strand", required=True)
        self.strand_combo = QComboBox()
        self.strand_combo.addItems(["STEM", "ABM", "HUMSS", "GAS", "TVL", "ICT"])
        self.strand_combo.setStyleSheet(self._combo_style())
        self.strand_combo.setFixedHeight(48)
        strand_col.addWidget(self.strand_combo)

        grade_col = self._create_field_layout("Grade Level", required=True)
        self.grade_combo = QComboBox()
        self.grade_combo.addItems(["11", "12"])
        self.grade_combo.setStyleSheet(self._combo_style())
        self.grade_combo.setFixedHeight(48)
        grade_col.addWidget(self.grade_combo)

        payment_col = self._create_field_layout("Payment Mode", required=True)
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["Full Payment", "Installment", "Voucher", "Scholarship"])
        self.payment_combo.setStyleSheet(self._combo_style())
        self.payment_combo.setFixedHeight(48)
        payment_col.addWidget(self.payment_combo)

        academic_layout.addLayout(strand_col, 1)
        academic_layout.addLayout(grade_col, 1)
        academic_layout.addLayout(payment_col, 1)
        form_layout.addLayout(academic_layout)

        # Info note
        info_note = QLabel("ℹ️  Section will be automatically assigned based on strand and availability")
        info_note.setStyleSheet("""
            color: #6B7280; 
            font-size: 11px; 
            background-color: #F3F4F6;
            padding: 12px 16px;
            border-radius: 8px;
        """)
        info_note.setWordWrap(True)
        form_layout.addWidget(info_note)

        self.main_layout.addWidget(form_frame)

        # ===== ACTION BUTTONS =====
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.clear_btn = QPushButton("Clear Form")
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.setStyleSheet(self._secondary_button_style())
        self.clear_btn.setMinimumHeight(48)
        self.clear_btn.setFixedWidth(140)

        self.print_btn = QPushButton("📄 Print")
        self.print_btn.setEnabled(False)
        self.print_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.print_btn.setStyleSheet(self._secondary_button_style())
        self.print_btn.setMinimumHeight(48)
        self.print_btn.setFixedWidth(140)

        self.enroll_btn = QPushButton("✓ Enroll Student")
        self.enroll_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.enroll_btn.setStyleSheet(self._primary_button_style())
        self.enroll_btn.setMinimumHeight(48)
        self.enroll_btn.setFixedWidth(180)

        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.print_btn)
        btn_layout.addWidget(self.enroll_btn)

        self.main_layout.addLayout(btn_layout)
        self.main_layout.addStretch()

        # Set scroll widget
        scroll.setWidget(container)

        # Main layout
        main_container_layout = QVBoxLayout(self)
        main_container_layout.setContentsMargins(0, 0, 0, 0)
        main_container_layout.addWidget(scroll)

    def _create_section_header(self, text: str) -> QLabel:
        """Create a section header with clean styling"""
        label = QLabel(text)
        label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        label.setStyleSheet("""
            color: #1A1A2E; 
            background: transparent; 
            padding-bottom: 8px;
            border-bottom: 2px solid #E5E7EB;
        """)
        return label

    def _create_field_layout(self, label_text: str, required: bool = False) -> QVBoxLayout:
        """Create a field layout with label"""
        layout = QVBoxLayout()
        layout.setSpacing(8)

        label_html = label_text
        if required:
            label_html += " <span style='color: #EF4444;'>*</span>"

        label = QLabel(label_html)
        label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        label.setStyleSheet("color: #374151; background: transparent;")
        layout.addWidget(label)

        return layout

    def _create_limits_card(self) -> QFrame:
        """Create modern enrollment limits card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #EFF6FF, stop:1 #DBEAFE);
                border-radius: 12px;
                border: none;
            }
        """)
        self._add_shadow(card, blur=15, offset=2)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)

        icon_label = QLabel("📊")
        icon_label.setStyleSheet("font-size: 24px; background: transparent;")

        self.limits_text = QLabel("Loading enrollment data...")
        self.limits_text.setFont(QFont("Segoe UI", 11))
        self.limits_text.setStyleSheet("color: #1E40AF; background: transparent;")

        layout.addWidget(icon_label)
        layout.addWidget(self.limits_text)
        layout.addStretch()
        return card

    def _input_style(self) -> str:
        """Modern input field stylesheet"""
        return """
            QLineEdit {
                background-color: #FFFFFF;
                border: 2px solid #E5E7EB;
                padding: 12px 16px;
                border-radius: 10px;
                font-size: 13px;
                color: #1F2937;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus {
                background-color: #FFFFFF;
                border: 2px solid #3B82F6;
                outline: none;
            }
            QLineEdit:hover {
                border: 2px solid #D1D5DB;
            }
        """

    def _combo_style(self) -> str:
        """Modern combobox stylesheet"""
        return """
            QComboBox, QDateEdit {
                background-color: #FFFFFF;
                border: 2px solid #E5E7EB;
                padding: 12px 16px;
                border-radius: 10px;
                font-size: 13px;
                color: #1F2937;
                font-family: 'Segoe UI';
            }
            QComboBox:focus, QDateEdit:focus {
                border: 2px solid #3B82F6;
            }
            QComboBox:hover, QDateEdit:hover {
                border: 2px solid #D1D5DB;
            }
            QComboBox::drop-down, QDateEdit::drop-down {
                border: none;
                width: 32px;
            }
            QComboBox::down-arrow, QDateEdit::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #6B7280;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 2px solid #3B82F6;
                border-radius: 8px;
                selection-background-color: #EFF6FF;
                selection-color: #1F2937;
                padding: 4px;
                outline: none;
            }
        """

    def _primary_button_style(self) -> str:
        """Primary button style"""
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3B82F6, stop:1 #2563EB);
                color: white;
                border: none;
                padding: 14px 28px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2563EB, stop:1 #1D4ED8);
            }
            QPushButton:pressed {
                background: #1E40AF;
            }
            QPushButton:disabled {
                background: #D1D5DB;
                color: #9CA3AF;
            }
        """

    def _secondary_button_style(self) -> str:
        """Secondary button style"""
        return """
            QPushButton {
                background-color: #FFFFFF;
                color: #374151;
                border: 2px solid #E5E7EB;
                padding: 14px 28px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 600;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background-color: #F9FAFB;
                border: 2px solid #D1D5DB;
            }
            QPushButton:pressed {
                background-color: #F3F4F6;
            }
            QPushButton:disabled {
                background-color: #F3F4F6;
                color: #9CA3AF;
                border: 2px solid #E5E7EB;
            }
        """

    def _add_shadow(self, widget: QWidget, blur: int = 20, offset: int = 4):
        """Add subtle shadow effect to widget"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blur)
        shadow.setXOffset(0)
        shadow.setYOffset(offset)
        shadow.setColor(QColor(0, 0, 0, 25))
        widget.setGraphicsEffect(shadow)