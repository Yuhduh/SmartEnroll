
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
import os


class SidebarUI(QWidget):


    def __init__(self):
        super().__init__()
        self.setFixedWidth(250)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setup_ui()

    def setup_ui(self):
        #Create all UI elements
        self.setStyleSheet("""
            QWidget {
                background-color: #0c314b;
                color: white;
            }
            QPushButton {
                background-color: transparent;
                color: rgba(255, 255, 255, 0.7);
                border: none;
                padding: 12px 20px;
                text-align: left;
                font-size: 14px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgba(54, 84, 134, 0.5);
                color: white;
            }
            QPushButton[active="true"] {
                background-color: #365486;
                color: white;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header section
        header = self._create_header()
        layout.addWidget(header)

        # Navigation menu
        nav_widget = self._create_nav_menu()
        layout.addWidget(nav_widget)

        # Footer section
        layout.addStretch()
        footer = self._create_footer()
        layout.addWidget(footer)

        self.setLayout(layout)

    def _create_header(self) -> QWidget:
        #Create header with logo and title
        header = QWidget()
        header.setStyleSheet("border-bottom: 1px solid rgba(255, 255, 255, 0.1);")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 20, 20, 20)
        header_layout.setSpacing(10)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, "..", "school_logo.png")

        if not os.path.exists(logo_path):
            logo_path = os.path.join(script_dir, "school_logo.png")

        logo_label = QLabel()
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    80, 80,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                logo_label.setPixmap(scaled_pixmap)
                logo_label.setStyleSheet("""
                    border: none; 
                    background: transparent;
                    border-radius: 40px;
                """)
            else:
                self._set_fallback_logo(logo_label)
        else:
            self._set_fallback_logo(logo_label)

        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(logo_label)

        # Title
        title = QLabel("SmartEnroll")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white; border: none;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Enrollment System")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.7); border: none;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle)

        return header

    def _set_fallback_logo(self, logo_label):
        #Set fallback emoji if logo not found
        logo_label.setText("🎓")
        logo_label.setFont(QFont("Segoe UI", 40))
        logo_label.setStyleSheet("border: none; background: transparent; color: white;")

    def _create_nav_menu(self) -> QWidget:
        # Create navigation menu container
        nav_widget = QWidget()
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(15, 20, 15, 20)
        nav_layout.setSpacing(8)

        # Common button style
        button_style = """
            QPushButton {
                background-color: transparent;
                color: rgba(255, 255, 255, 0.7);
                border: none;
                padding: 12px 20px;
                text-align: left;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: rgba(54, 84, 134, 0.5);
                color: white;
            }
            QPushButton[active="true"] {
                background-color: #365486;
                color: white;
            }
        """

        # Main menu buttons
        self.dashboard_btn = QPushButton("Dashboard")
        self.dashboard_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dashboard_btn.setObjectName("dashboard_btn")
        self.dashboard_btn.setStyleSheet(button_style)

        self.enrollment_btn = QPushButton("Enrollment")
        self.enrollment_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.enrollment_btn.setObjectName("enrollment_btn")
        self.enrollment_btn.setStyleSheet(button_style)

        self.reports_btn = QPushButton("Reports")
        self.reports_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reports_btn.setObjectName("reports_btn")
        self.reports_btn.setStyleSheet(button_style)

        self.management_btn = QPushButton("Management")
        self.management_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.management_btn.setObjectName("management_btn")
        self.management_btn.setStyleSheet(button_style)

        self.classrooms_btn = QPushButton("Classrooms")
        self.classrooms_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.classrooms_btn.setObjectName("classrooms_btn")
        self.classrooms_btn.setStyleSheet(button_style)

        # Add main buttons to layout
        nav_layout.addWidget(self.dashboard_btn)
        nav_layout.addWidget(self.enrollment_btn)
        nav_layout.addWidget(self.reports_btn)
        nav_layout.addWidget(self.management_btn)
        nav_layout.addWidget(self.classrooms_btn)

        # Separator before admin section
        self.admin_separator = QWidget()
        self.admin_separator.setFixedHeight(1)
        self.admin_separator.setStyleSheet("background-color: rgba(255, 255, 255, 0.1);")
        self.admin_separator.setVisible(False)
        nav_layout.addWidget(self.admin_separator)

        # Admin section label
        self.admin_label = QLabel("ADMIN")
        self.admin_label.setStyleSheet(
            "color: rgba(255, 255, 255, 0.4); padding: 10px 20px; border: none; font-weight: bold;")
        self.admin_label.setVisible(False)
        nav_layout.addWidget(self.admin_label)

        # Users button - Admin only
        self.users_btn = QPushButton("Users")
        self.users_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.users_btn.setObjectName("users_btn")
        self.users_btn.setVisible(False)
        self.users_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: rgba(255, 255, 255, 0.7);
                border: none;
                padding: 12px 20px;
                text-align: left;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                border-left: 3px solid #E74C3C;
            }
            QPushButton:hover {
                background-color: rgba(54, 84, 134, 0.5);
                color: white;
            }
            QPushButton[active="true"] {
                background-color: #365486;
                color: white;
                border-left: 3px solid #E74C3C;
            }
        """)
        nav_layout.addWidget(self.users_btn)

        nav_layout.addStretch()
        return nav_widget

    def _create_footer(self) -> QWidget:
        #Create footer with user info
        footer = QWidget()
        footer.setStyleSheet("border-top: 1px solid rgba(255, 255, 255, 0.1);")
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(20, 15, 20, 15)
        footer_layout.setSpacing(10)

        # User info labels
        self.user_label = QLabel("👤 School Staff")
        self.user_label.setStyleSheet("color: white; border: none; font-size: 13px;")
        self.user_label.setWordWrap(True)
        self.user_label.setObjectName("user_label")
        footer_layout.addWidget(self.user_label)

        self.role_label = QLabel("Role: Staff")
        self.role_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); border: none; font-size: 10px;")
        self.role_label.setObjectName("role_label")
        footer_layout.addWidget(self.role_label)

        # Sign out button
        self.signout_btn = QPushButton("Sign Out")
        self.signout_btn.setStyleSheet("""
            QPushButton {
                color: rgba(255, 255, 255, 0.7);
                font-weight: bold;
                font-size: 11px;
                padding: 8px 10px;
                text-align: left;
                border-radius: 6px;
            }
            QPushButton:hover {
                color: white;
                background-color: rgba(220, 53, 69, 0.8);
            }
        """)
        self.signout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.signout_btn.setObjectName("signout_btn")
        footer_layout.addWidget(self.signout_btn)

        return footer

    def show_admin_features(self, show: bool = True):
        #Show or hide admin-only features
        self.users_btn.setVisible(show)
        self.admin_separator.setVisible(show)
        self.admin_label.setVisible(show)