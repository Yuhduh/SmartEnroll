from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QPushButton, QTableWidget, QHeaderView,
                             QLineEdit, QComboBox, QScrollArea, QApplication, QTabWidget)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class ManagementPageUI(QWidget):
    """UI for managing teachers, rooms, and sections"""

    # Signals
    add_teacher_requested = pyqtSignal(dict)
    delete_teacher_requested = pyqtSignal(int, str)
    add_room_requested = pyqtSignal(dict)
    delete_room_requested = pyqtSignal(int, str)
    add_section_requested = pyqtSignal(dict)
    delete_section_requested = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Create all UI elements"""
        screen = QApplication.primaryScreen().geometry()
        is_small_screen = screen.width() < 1600

        margin = 20 if is_small_screen else 30
        spacing = 15 if is_small_screen else 20

        # Main scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        # Container widget
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(margin, margin, margin, margin)
        layout.setSpacing(spacing)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("Resource Management")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #2C3E50;")

        subtitle = QLabel("Manage teachers, rooms, and sections")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #7F8C8D;")

        header_layout.addWidget(title)
        header_layout.addStretch()

        layout.addLayout(header_layout)
        layout.addWidget(subtitle)

        # Tab Widget for different management sections
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E8ECF1;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #F8F9FA;
                color: #2C3E50;
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #365486;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background-color: #E8ECF1;
            }
        """)

        # Create tabs
        self.teachers_tab = self._create_teachers_tab(is_small_screen)
        self.rooms_tab = self._create_rooms_tab(is_small_screen)
        self.sections_tab = self._create_sections_tab(is_small_screen)

        self.tab_widget.addTab(self.teachers_tab, "👨‍🏫 Teachers")
        self.tab_widget.addTab(self.rooms_tab, "🏫 Rooms")
        self.tab_widget.addTab(self.sections_tab, "📚 Sections")

        layout.addWidget(self.tab_widget)

        scroll.setWidget(container)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def _create_teachers_tab(self, is_small_screen: bool) -> QWidget:
        """Create teachers management tab - FIXED: Added department field"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Add Teacher Form
        add_frame = QFrame()
        add_frame.setStyleSheet("""
            QFrame {
                background-color: #E8F4F8;
                border-radius: 10px;
                border: 1px solid #7FC7D9;
            }
        """)
        add_layout = QVBoxLayout(add_frame)
        add_layout.setContentsMargins(20, 20, 20, 20)
        add_layout.setSpacing(15)

        add_title = QLabel("Add New Teacher")
        add_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        add_title.setStyleSheet("color: #2C3E50; border: none;")
        add_layout.addWidget(add_title)

        # FIXED: Added Department field - Form fields now in two rows
        # Row 1: Name, Email, Contact
        form_row1 = QHBoxLayout()
        form_row1.setSpacing(15)

        self.teacher_name_input = QLineEdit()
        self.teacher_name_input.setPlaceholderText("Full Name *")
        self.teacher_name_input.setStyleSheet(self._input_style(is_small_screen))

        self.teacher_email_input = QLineEdit()
        self.teacher_email_input.setPlaceholderText("Email Address *")
        self.teacher_email_input.setStyleSheet(self._input_style(is_small_screen))

        self.teacher_contact_input = QLineEdit()
        self.teacher_contact_input.setPlaceholderText("Contact Number *")
        self.teacher_contact_input.setStyleSheet(self._input_style(is_small_screen))

        form_row1.addWidget(self.teacher_name_input, 2)
        form_row1.addWidget(self.teacher_email_input, 2)
        form_row1.addWidget(self.teacher_contact_input, 1)

        # Row 2: Department, Specialization, Button
        form_row2 = QHBoxLayout()
        form_row2.setSpacing(15)

        self.teacher_department_input = QLineEdit()
        self.teacher_department_input.setPlaceholderText("Department (e.g., Science, Math)")
        self.teacher_department_input.setStyleSheet(self._input_style(is_small_screen))

        self.teacher_specialization_input = QLineEdit()
        self.teacher_specialization_input.setPlaceholderText("Specialization/Subject *")
        self.teacher_specialization_input.setStyleSheet(self._input_style(is_small_screen))

        self.add_teacher_btn = QPushButton("Add")
        self.add_teacher_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_teacher_btn.setStyleSheet(self._button_style("#27AE60", is_small_screen))
        self.add_teacher_btn.clicked.connect(self._on_add_teacher)

        form_row2.addWidget(self.teacher_department_input, 2)
        form_row2.addWidget(self.teacher_specialization_input, 2)
        form_row2.addWidget(self.add_teacher_btn, 1)

        add_layout.addLayout(form_row1)
        add_layout.addLayout(form_row2)
        layout.addWidget(add_frame)

        # Teachers Table
        self.teachers_table = QTableWidget()
        self.teachers_table.setColumnCount(6)
        self.teachers_table.setHorizontalHeaderLabels([
            "ID", "Name", "Email", "Contact", "Specialization", "Actions"
        ])

        header = self.teachers_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.teachers_table.setColumnWidth(0, 60)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.teachers_table.setColumnWidth(3, 130)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        self.teachers_table.setColumnWidth(5, 100)

        self.teachers_table.verticalHeader().setVisible(False)
        self.teachers_table.setAlternatingRowColors(True)
        self.teachers_table.setStyleSheet(self._table_style())

        layout.addWidget(self.teachers_table)

        return widget

    def _create_rooms_tab(self, is_small_screen: bool) -> QWidget:
        """Create rooms management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Add Room Form
        add_frame = QFrame()
        add_frame.setStyleSheet("""
            QFrame {
                background-color: #FFF4E6;
                border-radius: 10px;
                border: 1px solid #FFB84D;
            }
        """)
        add_layout = QVBoxLayout(add_frame)
        add_layout.setContentsMargins(20, 20, 20, 20)
        add_layout.setSpacing(15)

        add_title = QLabel("Add New Room")
        add_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        add_title.setStyleSheet("color: #2C3E50; border: none;")
        add_layout.addWidget(add_title)

        # Form fields
        form_layout = QHBoxLayout()
        form_layout.setSpacing(15)

        self.room_number_input = QLineEdit()
        self.room_number_input.setPlaceholderText("Room Number (e.g., 101, 202) *")
        self.room_number_input.setStyleSheet(self._input_style(is_small_screen))

        self.room_building_input = QLineEdit()
        self.room_building_input.setPlaceholderText("Building (e.g., Main, Annex) *")
        self.room_building_input.setStyleSheet(self._input_style(is_small_screen))

        self.room_capacity_input = QLineEdit()
        self.room_capacity_input.setPlaceholderText("Capacity *")
        self.room_capacity_input.setStyleSheet(self._input_style(is_small_screen))

        self.add_room_btn = QPushButton("Add Room")
        self.add_room_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_room_btn.setStyleSheet(self._button_style("#F39C12", is_small_screen))
        self.add_room_btn.clicked.connect(self._on_add_room)

        form_layout.addWidget(self.room_number_input, 1)
        form_layout.addWidget(self.room_building_input, 1)
        form_layout.addWidget(self.room_capacity_input, 1)
        form_layout.addWidget(self.add_room_btn, 1)

        add_layout.addLayout(form_layout)
        layout.addWidget(add_frame)

        # Rooms Table
        self.rooms_table = QTableWidget()
        self.rooms_table.setColumnCount(5)
        self.rooms_table.setHorizontalHeaderLabels([
            "ID", "Room Number", "Building", "Room Capacity", "Actions"
        ])

        header = self.rooms_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.rooms_table.setColumnWidth(0, 60)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.rooms_table.setColumnWidth(3, 100)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.rooms_table.setColumnWidth(4, 100)

        self.rooms_table.verticalHeader().setVisible(False)
        self.rooms_table.setAlternatingRowColors(True)
        self.rooms_table.setStyleSheet(self._table_style())

        layout.addWidget(self.rooms_table)

        return widget

    def _create_sections_tab(self, is_small_screen: bool) -> QWidget:
        """Create sections management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Add Section Form
        add_frame = QFrame()
        add_frame.setStyleSheet("""
            QFrame {
                background-color: #E8F8F5;
                border-radius: 10px;
                border: 1px solid #76D7C4;
            }
        """)
        add_layout = QVBoxLayout(add_frame)
        add_layout.setContentsMargins(20, 20, 20, 20)
        add_layout.setSpacing(15)

        add_title = QLabel("Add New Section")
        add_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        add_title.setStyleSheet("color: #2C3E50; border: none;")
        add_layout.addWidget(add_title)

        # Form fields
        form_layout = QHBoxLayout()
        form_layout.setSpacing(15)

        self.section_name_input = QLineEdit()
        self.section_name_input.setPlaceholderText("Section Name (e.g., Einstein, Newton) *")
        self.section_name_input.setStyleSheet(self._input_style(is_small_screen))

        self.section_strand_combo = QComboBox()
        self.section_strand_combo.addItems(["STEM", "ABM", "HUMSS", "GAS", "TVL"])
        self.section_strand_combo.setStyleSheet(self._combo_style(is_small_screen))

        self.section_capacity_input = QLineEdit()
        self.section_capacity_input.setPlaceholderText("Capacity *")
        self.section_capacity_input.setStyleSheet(self._input_style(is_small_screen))

        # FIXED: Room combo now includes availability status
        self.section_room_combo = QComboBox()
        self.section_room_combo.addItem("No Room", None)
        self.section_room_combo.setStyleSheet(self._combo_style(is_small_screen))

        self.section_teacher_combo = QComboBox()
        self.section_teacher_combo.addItem("No Adviser", None)
        self.section_teacher_combo.setStyleSheet(self._combo_style(is_small_screen))

        self.add_section_btn = QPushButton("Add Section")
        self.add_section_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_section_btn.setStyleSheet(self._button_style("#16A085", is_small_screen))
        self.add_section_btn.clicked.connect(self._on_add_section)

        form_layout.addWidget(self.section_name_input, 2)
        form_layout.addWidget(self.section_strand_combo, 1)
        form_layout.addWidget(self.section_capacity_input, 1)
        form_layout.addWidget(self.section_room_combo, 1)
        form_layout.addWidget(self.section_teacher_combo, 2)
        form_layout.addWidget(self.add_section_btn, 1)

        add_layout.addLayout(form_layout)
        layout.addWidget(add_frame)

        # Sections Table
        self.sections_table = QTableWidget()
        self.sections_table.setColumnCount(7)
        self.sections_table.setHorizontalHeaderLabels([
            "ID", "Section", "Strand", "Capacity", "Room", "Adviser", "Actions"
        ])

        header = self.sections_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.sections_table.setColumnWidth(0, 60)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.sections_table.setColumnWidth(2, 100)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.sections_table.setColumnWidth(3, 100)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.sections_table.setColumnWidth(6, 100)

        self.sections_table.verticalHeader().setVisible(False)
        self.sections_table.setAlternatingRowColors(True)
        self.sections_table.setStyleSheet(self._table_style())

        layout.addWidget(self.sections_table)

        return widget

    def _on_add_teacher(self):
        """Handle add teacher button click - FIXED: Include department"""
        data = {
            'name': self.teacher_name_input.text().strip(),
            'email': self.teacher_email_input.text().strip(),
            'contact': self.teacher_contact_input.text().strip(),
            'department': self.teacher_department_input.text().strip(),
            'specialization': self.teacher_specialization_input.text().strip()
        }
        self.add_teacher_requested.emit(data)

    def _on_add_room(self):
        """Handle add room button click"""
        data = {
            'room_number': self.room_number_input.text().strip(),
            'building': self.room_building_input.text().strip(),
            'capacity': self.room_capacity_input.text().strip()
        }
        self.add_room_requested.emit(data)

    def _on_add_section(self):
        """Handle add section button click"""
        room_id = self.section_room_combo.currentData()
        teacher_id = self.section_teacher_combo.currentData()

        data = {
            'section_name': self.section_name_input.text().strip(),
            'strand': self.section_strand_combo.currentText(),
            'capacity': self.section_capacity_input.text().strip(),
            'room_id': room_id,
            'teacher_id': teacher_id
        }
        self.add_section_requested.emit(data)

    def clear_teacher_form(self):
        """Clear teacher form inputs"""
        self.teacher_name_input.clear()
        self.teacher_email_input.clear()
        self.teacher_contact_input.clear()
        self.teacher_department_input.clear()
        self.teacher_specialization_input.clear()

    def clear_room_form(self):
        """Clear room form inputs"""
        self.room_number_input.clear()
        self.room_building_input.clear()
        self.room_capacity_input.clear()

    def clear_section_form(self):
        """Clear section form inputs"""
        self.section_name_input.clear()
        self.section_strand_combo.setCurrentIndex(0)
        self.section_capacity_input.clear()
        self.section_room_combo.setCurrentIndex(0)
        self.section_teacher_combo.setCurrentIndex(0)

    def _input_style(self, is_small_screen: bool) -> str:
        """Return input field stylesheet"""
        font_size = 12 if is_small_screen else 13
        padding = 8 if is_small_screen else 12

        return f"""
            QLineEdit {{
                background-color: white;
                border: 2px solid #E0E0E0;
                padding: {padding}px;
                border-radius: 6px;
                font-size: {font_size}px;
            }}
            QLineEdit:focus {{
                border: 2px solid #365486;
            }}
        """

    def _combo_style(self, is_small_screen: bool) -> str:
        """Return combobox stylesheet"""
        font_size = 12 if is_small_screen else 13
        padding = 8 if is_small_screen else 12

        return f"""
            QComboBox {{
                background-color: white;
                border: 2px solid #E0E0E0;
                padding: {padding}px;
                border-radius: 6px;
                font-size: {font_size}px;
            }}
            QComboBox:focus {{
                border: 2px solid #365486;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 10px;
            }}
        """

    def _button_style(self, bg_color: str, is_small_screen: bool) -> str:
        """Return button stylesheet"""
        font_size = 12 if is_small_screen else 13
        padding = "8px 15px" if is_small_screen else "10px 20px"

        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                padding: {padding};
                border-radius: 6px;
                font-size: {font_size}px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                opacity: 0.9;
            }}
        """

    def _table_style(self) -> str:
        """Return table stylesheet"""
        return """
            QTableWidget {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                gridline-color: #F0F0F0;
            }
            QHeaderView::section {
                background-color: #365486;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #F0F0F0;
                color: #34495E;
            }
            QTableWidget::item:selected {
                background-color: #E8F4F8;
                color: #2C3E50;
            }
        """