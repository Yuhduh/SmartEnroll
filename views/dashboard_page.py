
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QGridLayout, QTableWidget,
                             QHeaderView, QLineEdit, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from datetime import datetime


class DashboardPageUI(QWidget):

    # Signals
    search_requested = pyqtSignal(str)  # Emits search query
    clear_search_requested = pyqtSignal()  # Emits when clear is clicked
    edit_requested = pyqtSignal(int, str)  # Emits (student_id, student_name)
    delete_requested = pyqtSignal(int, str)  # Emits (student_id, student_name)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        #Create all UI elements
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header with search bar
        header_layout = self._create_header()
        layout.addLayout(header_layout)

        # Live counter label
        live_label = QLabel("● Live Enrollment Counter")
        live_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        live_label.setStyleSheet("color: #5DADE2;")
        layout.addWidget(live_label)

        # Stats cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)

        self.total_card = self._create_stat_card("Total Enrolled", "0", "students", "👥")
        self.available_card = self._create_stat_card("Available Slots", "0 / 500", "", "📢")

        stats_layout.addWidget(self.total_card)
        stats_layout.addWidget(self.available_card)

        layout.addLayout(stats_layout)

        # Enrollment by Strand card
        self.strand_card = self._create_strand_card()
        layout.addWidget(self.strand_card)

        # Recent Activity table
        self.activity_card = self._create_activity_table()
        layout.addWidget(self.activity_card)

        layout.addStretch()
        self.setLayout(layout)

    def _create_header(self) -> QHBoxLayout:
        #Create header with title, date, and search bar
        header_layout = QHBoxLayout()

        # Title section
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)

        self.title_label = QLabel("Overview")
        self.title_label.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #2C3E50;")

        self.date_label = QLabel(datetime.now().strftime("%A, %B %d, %Y"))
        self.date_label.setFont(QFont("Segoe UI", 11))
        self.date_label.setStyleSheet("color: #7F8C8D;")

        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.date_label)

        # Search bar
        search_widget = self._create_search_bar()

        header_layout.addWidget(title_widget)
        header_layout.addStretch()
        header_layout.addWidget(search_widget)

        return header_layout

    def _create_search_bar(self) -> QWidget:
        #Create search bar widget
        search_container = QWidget()
        search_container.setFixedWidth(400)
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(8)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, email, or strand...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #E8ECF1;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 13px;
                color: #2C3E50;
            }
            QLineEdit:focus {
                border: 2px solid #5DADE2;
            }
        """)
        self.search_input.returnPressed.connect(self._on_search_pressed)

        # Search button
        self.search_btn = QPushButton("Search")
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: #5DADE2;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4A9FD0;
            }
        """)

        self.advanced_search_btn = QPushButton("🔍 Advanced Search")
        self.advanced_search_btn.setStyleSheet("""
            QPushButton {
                background-color: #9B59B6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #8E44AD; }
        """)
        self.advanced_search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_layout.addWidget(self.advanced_search_btn)
        self.search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.search_btn.clicked.connect(self._on_search_pressed)

        # Clear button
        self.clear_search_btn = QPushButton("✕")
        self.clear_search_btn.setStyleSheet("""
            QPushButton {
                background-color: #E8ECF1;
                color: #7F8C8D;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #D5D9DD;
            }
        """)
        self.clear_search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_search_btn.setFixedWidth(40)
        self.clear_search_btn.clicked.connect(self._on_clear_pressed)
        self.clear_search_btn.setVisible(False)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.clear_search_btn)

        return search_container

    def _on_search_pressed(self):
        #Handle search button press
        query = self.search_input.text().strip()
        if query:
            self.search_requested.emit(query)
            self.clear_search_btn.setVisible(True)

    def _on_clear_pressed(self):
        #Handle clear button press
        self.search_input.clear()
        self.clear_search_btn.setVisible(False)
        self.clear_search_requested.emit()

    def _create_stat_card(self, title: str, value: str, suffix: str, icon: str) -> QFrame:
        #Create a statistics card
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E8ECF1;
                border-radius: 12px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)

        # Header with title and icon
        header = QHBoxLayout()

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 11))
        title_label.setStyleSheet("color: #7F8C8D; border: none;")

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI", 24))
        icon_label.setStyleSheet("""
            background-color: #E8F4F8;
            border-radius: 8px;
            padding: 8px;
            border: none;
        """)
        icon_label.setFixedSize(50, 50)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header.addWidget(title_label)
        header.addStretch()
        header.addWidget(icon_label)

        card_layout.addLayout(header)

        # Value
        value_layout = QHBoxLayout()

        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        value_label.setStyleSheet("color: #2C3E50; border: none;")
        value_label.setObjectName("value_label")

        suffix_label = QLabel(suffix)
        suffix_label.setFont(QFont("Segoe UI", 11))
        suffix_label.setStyleSheet("color: #7F8C8D; border: none;")

        value_layout.addWidget(value_label)
        if suffix:
            value_layout.addWidget(suffix_label)
        value_layout.addStretch()

        card_layout.addLayout(value_layout)

        return card

    def _create_strand_card(self) -> QFrame:
        #Create enrollment by strand card
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E8ECF1;
                border-radius: 12px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)

        title = QLabel("Enrollment by Strand")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2C3E50; border: none;")
        card_layout.addWidget(title)

        # Grid for strands
        self.strand_grid = QGridLayout()
        self.strand_grid.setSpacing(15)

        card_layout.addLayout(self.strand_grid)

        return card

    def _create_activity_table(self) -> QFrame:
        #Create recent activity table
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E8ECF1;
                border-radius: 12px;
            }
        """)
        card.setMinimumHeight(400)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)

        # Header
        header_layout = QHBoxLayout()

        self.activity_title = QLabel("Recent Enrollment Activity")
        self.activity_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.activity_title.setStyleSheet("color: #2C3E50; border: none;")

        self.activity_live_label = QLabel("● Live")
        self.activity_live_label.setFont(QFont("Segoe UI", 10))
        self.activity_live_label.setStyleSheet("color: #5DADE2; border: none;")

        header_layout.addWidget(self.activity_title)
        header_layout.addStretch()
        header_layout.addWidget(self.activity_live_label)

        card_layout.addLayout(header_layout)

        # Table with 4 columns (Name, Strand, Status, Actions) - Actions now has Edit + Delete
        self.activity_table = QTableWidget()
        self.activity_table.setColumnCount(4)
        self.activity_table.setHorizontalHeaderLabels(["Student Name", "Strand", "Status", "Actions"])

        # Set column resize modes
        self.activity_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.activity_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.activity_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.activity_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.activity_table.setColumnWidth(3, 180)  # Wider for Edit + Delete buttons

        self.activity_table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
                gridline-color: #F0F0F0;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #F0F0F0;
            }
            QHeaderView::section {
                background-color: #F8F9FA;
                padding: 10px;
                border: none;
                border-bottom: 1px solid #E0E0E0;
                font-weight: bold;
                color: #7F8C8D;
            }
        """)
        self.activity_table.verticalHeader().setVisible(False)
        self.activity_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.activity_table.setAlternatingRowColors(True)
        self.activity_table.setMinimumHeight(300)

        card_layout.addWidget(self.activity_table)

        return card

    def set_search_results_mode(self, count: int):
        #Switch to search results display mode
        self.activity_title.setText(f"Search Results ({count} found)")
        self.activity_live_label.setVisible(False)

    def set_recent_mode(self):
        #Switch back to recent enrollments mode
        self.activity_title.setText("Recent Enrollment Activity")
        self.activity_live_label.setVisible(True)