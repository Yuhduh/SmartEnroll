from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QTableWidget, QHeaderView, QScrollArea,
                             QSizePolicy, QApplication, QTableWidgetItem, QComboBox, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class ClassroomsPageUI(QWidget):
    # Signals
    classroom_selected = pyqtSignal(int, str)  # section_id, section_name
    strand_filter_changed = pyqtSignal(str)  # strand name or "All"
    view_changed = pyqtSignal(str)  # "sections" or "students"

    def __init__(self):
        super().__init__()
        self.view_buttons = []
        self.current_view = "sections"
        self.setup_ui()

    def setup_ui(self):
        """Create all UI elements with responsive sizing"""
        screen = QApplication.primaryScreen().geometry()
        is_small_screen = screen.width() < 1600

        margin = 20 if is_small_screen else 30
        spacing = 15 if is_small_screen else 20

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(margin, margin, margin, margin)
        self.main_layout.setSpacing(spacing)

        # 1. Header Section
        header_layout = QHBoxLayout()

        title = QLabel("Classroom Management")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #2C3E50;")

        header_layout.addWidget(title)
        header_layout.addStretch()

        self.main_layout.addLayout(header_layout)

        # 2. View Selection Buttons (like reports)
        view_layout = QHBoxLayout()
        view_layout.setSpacing(12)

        views = [
            ("All Sections", "sections"),
            ("Student Details", "students")
        ]

        self.view_buttons = []
        for label, view_type in views:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setProperty("view_type", view_type)
            btn.setStyleSheet(self._view_button_style(view_type == "sections"))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(45)
            btn.setMinimumWidth(180)
            view_layout.addWidget(btn)
            self.view_buttons.append(btn)

        # Set first button as checked
        self.view_buttons[0].setChecked(True)

        view_layout.addStretch()
        self.main_layout.addLayout(view_layout)

        # 3. Filter & Info Row
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)

        # Info badge (will show current selection info)
        self.info_badge = QLabel("Select a section to view details")
        self.info_badge.setStyleSheet("""
            color: #365486; 
            background-color: #E8F4F8;
            padding: 8px 15px; 
            border-radius: 6px;
            border: 1px solid #7FC7D9; 
            font-weight: bold;
        """)
        filter_layout.addWidget(self.info_badge)

        filter_layout.addStretch()

        # Strand Filter
        filter_label = QLabel("Filter by Strand:")
        filter_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        filter_label.setStyleSheet("color: #2C3E50; border: none;")
        filter_layout.addWidget(filter_label)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "STEM", "ABM", "HUMSS", "GAS", "TVL"])
        self.filter_combo.setStyleSheet(self._combo_style(is_small_screen))
        filter_layout.addWidget(self.filter_combo)

        self.main_layout.addLayout(filter_layout)

        # 4. Content Area (Scroll)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        # Content Card
        self.content_card = QFrame()
        self.content_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E8ECF1;
            }
        """)
        self.content_layout = QVBoxLayout(self.content_card)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(15)

        # Create placeholder initially
        self._create_sections_view()

        self.scroll.setWidget(self.content_card)
        self.main_layout.addWidget(self.scroll, stretch=1)

    def _create_sections_view(self):
        """Create the sections/classrooms table view"""
        # Clear existing content
        self._clear_content()

        # Title
        sections_title = QLabel("All Sections / Classrooms")
        sections_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        sections_title.setStyleSheet("color: #34495E; border: none;")
        self.content_layout.addWidget(sections_title)

        # Sections Table
        self.classrooms_table = QTableWidget()
        self.classrooms_table.setColumnCount(7)  # Section, Strand, Adviser, Room, Enrolled, Capacity, Available
        self.classrooms_table.setHorizontalHeaderLabels([
            "Section", "Strand", "Adviser", "Room", "Enrolled", "Capacity", "Available"
        ])
        self.classrooms_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.classrooms_table.verticalHeader().setVisible(False)
        self.classrooms_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.classrooms_table.setAlternatingRowColors(True)
        self.classrooms_table.setShowGrid(False)
        self.classrooms_table.setStyleSheet(self._table_style())
        self.classrooms_table.setMinimumHeight(400)

        # Connect selection signal
        self.classrooms_table.itemSelectionChanged.connect(self._on_classroom_selected)

        self.content_layout.addWidget(self.classrooms_table)

    def _create_students_view(self):
        """Create the student details view"""
        # Clear existing content
        self._clear_content()

        # Title with section name
        self.student_list_label = QLabel("Student List - Select a section")
        self.student_list_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.student_list_label.setStyleSheet("color: #34495E; border: none;")
        self.content_layout.addWidget(self.student_list_label)

        # Teacher info card
        self.teacher_info_card = QFrame()
        self.teacher_info_card.setStyleSheet("""
            QFrame {
                background-color: #E8F4F8;
                border-radius: 8px;
                border: 1px solid #7FC7D9;
                padding: 10px;
            }
        """)
        self.teacher_info_layout = QVBoxLayout(self.teacher_info_card)
        self.teacher_info_layout.setContentsMargins(10, 10, 10, 10)
        self.teacher_info_layout.setSpacing(5)

        self.teacher_name_label = QLabel("👨‍🏫 Adviser: Not assigned")
        self.teacher_name_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.teacher_name_label.setStyleSheet("color: #2C3E50; border: none;")

        self.teacher_email_label = QLabel("📧 Email: -")
        self.teacher_email_label.setFont(QFont("Segoe UI", 10))
        self.teacher_email_label.setStyleSheet("color: #7F8C8D; border: none;")

        self.teacher_info_layout.addWidget(self.teacher_name_label)
        self.teacher_info_layout.addWidget(self.teacher_email_label)

        self.teacher_info_card.setVisible(False)  # Hidden by default
        self.content_layout.addWidget(self.teacher_info_card)

        # Students Table
        self.students_table = QTableWidget()
        self.students_table.setColumnCount(5)  # Name, Email, Strand, Payment, Date
        self.students_table.setHorizontalHeaderLabels(["Student Name", "Email", "Strand", "Payment", "Enrolled Date"])
        self.students_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.students_table.verticalHeader().setVisible(False)
        self.students_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.students_table.setAlternatingRowColors(True)
        self.students_table.setShowGrid(False)
        self.students_table.setStyleSheet(self._table_style())
        self.students_table.setMinimumHeight(400)

        self.content_layout.addWidget(self.students_table)

    def _clear_content(self):
        """Clear the content layout"""
        while self.content_layout.count() > 0:
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

    def _on_classroom_selected(self):
        """Handle classroom selection"""
        selected_rows = self.classrooms_table.selectedItems()
        if selected_rows:
            row = selected_rows[0].row()
            section_id = self.classrooms_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
            section_name = self.classrooms_table.item(row, 0).text()

            # Switch to students view automatically
            self.switch_to_students_view()

            # Emit signal to load student data
            self.classroom_selected.emit(section_id, section_name)

    def switch_to_sections_view(self):
        """Switch to sections view"""
        self.current_view = "sections"
        self._create_sections_view()
        self.info_badge.setText("All sections overview")

        # Update button states
        for btn in self.view_buttons:
            is_active = btn.property("view_type") == "sections"
            btn.setChecked(is_active)
            btn.setStyleSheet(self._view_button_style(is_active))

    def switch_to_students_view(self):
        """Switch to students view"""
        self.current_view = "students"
        self._create_students_view()

        # Update button states
        for btn in self.view_buttons:
            is_active = btn.property("view_type") == "students"
            btn.setChecked(is_active)
            btn.setStyleSheet(self._view_button_style(is_active))

    def _view_button_style(self, selected: bool) -> str:
        """Return view button stylesheet"""
        border_color = "#365486" if selected else "#E8ECF1"
        bg_color = "#DCF2F1" if selected else "white"
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: #2C3E50;
                border: 2px solid {border_color};
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }}
            QPushButton:hover {{ border-color: #7FC7D9; }}
        """

    def _combo_style(self, is_small_screen: bool) -> str:
        """Return combobox stylesheet"""
        font_size = 12 if is_small_screen else 13
        padding = 8 if is_small_screen else 10

        return f"""
            QComboBox {{
                background-color: #E8F4F8;
                border: 2px solid #5DADE2;
                padding: {padding}px;
                border-radius: 6px;
                min-width: 150px;
                color: #2C3E50;
                font-size: {font_size}px;
            }}
            QComboBox:hover {{
                background-color: #D4EAF7;
                border-color: #3498DB;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #3498DB;
                margin-right: 10px;
            }}
        """

    def _table_style(self) -> str:
        return """
            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #F0F0F0;
            }
            QHeaderView::section {
                background-color: #F8F9FA;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #365486;
                font-weight: bold;
                color: #2C3E50;
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