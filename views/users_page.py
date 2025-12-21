from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QPushButton, QTableWidget, QHeaderView,
                             QLineEdit, QComboBox, QScrollArea, QApplication, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class UsersPageUI(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Create all UI elements with FIXED consistent column sizing"""
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

        title_size = 18 if is_small_screen else 22
        title = QLabel("User Management")
        title.setFont(QFont("Segoe UI", title_size, QFont.Weight.Bold))
        title.setStyleSheet("color: #2C3E50;")

        admin_badge = QLabel("Admin Only")
        admin_badge.setStyleSheet("""
            background-color: white;
            color: #E74C3C;
            padding: 6px 12px;
            border-radius: 6px;
            border: 1px solid #E74C3C;
            font-size: 11px;
            font-weight: bold;
        """)
        admin_badge.setFixedHeight(30)

        self.user_count_label = QLabel("0 users")
        self.user_count_label.setStyleSheet("color: #7F8C8D; font-size: 14px;")

        header_layout.addWidget(title)
        header_layout.addWidget(admin_badge)
        header_layout.addStretch()
        header_layout.addWidget(self.user_count_label)

        layout.addLayout(header_layout)

        # Add New User Section
        add_user_frame = QFrame()
        add_user_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #E0E0E0;
            }
        """)
        add_layout = QVBoxLayout(add_user_frame)
        add_layout.setContentsMargins(20, 20, 20, 20)
        add_layout.setSpacing(15)

        add_title = QLabel("Add New User")
        add_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        add_title.setStyleSheet("color: #34495E; border: none;")
        add_layout.addWidget(add_title)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(15)

        self.new_username_input = QLineEdit()
        self.new_username_input.setPlaceholderText("Username")
        self.new_username_input.setStyleSheet(self._input_style(is_small_screen))

        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText("Password (min 6 characters)")
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password_input.setStyleSheet(self._input_style(is_small_screen))

        self.new_role_combo = QComboBox()
        self.new_role_combo.addItems(["staff", "admin"])
        self.new_role_combo.setStyleSheet(self._combo_style(is_small_screen))

        self.add_user_btn = QPushButton("Add User")
        self.add_user_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_user_btn.setStyleSheet(self._button_style("#27AE60", is_small_screen))

        input_layout.addWidget(self.new_username_input, 2)
        input_layout.addWidget(self.new_password_input, 2)
        input_layout.addWidget(self.new_role_combo, 1)
        input_layout.addWidget(self.add_user_btn, 1)

        add_layout.addLayout(input_layout)
        layout.addWidget(add_user_frame)

        # Users Table - FIXED: Consistent column sizing
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(5)
        self.users_table.setHorizontalHeaderLabels(
            ["ID", "Username", "Role", "Created At", "Actions"])

        # FIXED: Proper proportional column sizing
        header = self.users_table.horizontalHeader()

        # Column 0: ID - Fixed 80px
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.users_table.setColumnWidth(0, 80)

        # Column 1: Username - Fixed 250px (was stretching too much)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.users_table.setColumnWidth(1, 250)

        # Column 2: Role - Fixed 150px
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.users_table.setColumnWidth(2, 150)

        # Column 3: Created At - Stretch (takes remaining space)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        # Column 4: Actions - Fixed 120px
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.users_table.setColumnWidth(4, 120)

        self.users_table.verticalHeader().setVisible(False)
        self.users_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.users_table.setAlternatingRowColors(True)
        self.users_table.setShowGrid(False)
        self.users_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
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
        """)

        layout.addWidget(self.users_table)

        # Set the scroll area widget
        scroll.setWidget(container)

        # Main layout for the class
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)

    def _input_style(self, is_small_screen: bool) -> str:
        """Return input field stylesheet"""
        font_size = 12 if is_small_screen else 13
        padding = 8 if is_small_screen else 12

        return f"""
            QLineEdit {{
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                padding: {padding}px;
                border-radius: 6px;
                font-size: {font_size}px;
            }}
            QLineEdit:focus {{
                background-color: white;
                border: 1px solid #365486;
            }}
        """

    def _combo_style(self, is_small_screen: bool) -> str:
        """Return combobox stylesheet"""
        font_size = 12 if is_small_screen else 13
        padding = 8 if is_small_screen else 12

        return f"""
            QComboBox {{
                background-color: #F5F5F5;
                border: 1px solid #E0E0E0;
                padding: {padding}px;
                border-radius: 6px;
                font-size: {font_size}px;
            }}
            QComboBox:focus {{
                background-color: white;
                border: 1px solid #365486;
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