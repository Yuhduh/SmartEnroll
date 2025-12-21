from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QIcon, QColor
import os


class LoginViewUI(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.set_window_icon()

    def setup_ui(self):
        """Create modern login UI with horizontal branding"""
        self.setWindowTitle("SmartEnroll - Login")
        self.setFixedWidth(750)

        # Background
        self.setStyleSheet("""
            QWidget {
                background-color: #1a2b4b;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 40, 50, 40)
        main_layout.setSpacing(20)

        # ===== HORIZONTAL BRANDING SECTION =====
        branding_container = QWidget()
        branding_container.setStyleSheet("background: transparent;")
        branding_layout = QHBoxLayout(branding_container)
        branding_layout.setContentsMargins(0, 0, 0, 0)
        branding_layout.setSpacing(12)  # Tight spacing between text and logo

        # Left side: Text branding
        text_container = QWidget()
        text_container.setStyleSheet("background: transparent;")
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(8)
        text_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        title_label = QLabel("SmartEnroll")
        title_label.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white; background: transparent;")
        text_layout.addWidget(title_label)

        subtitle_label = QLabel("SHS Student Enrollment System")
        subtitle_label.setFont(QFont("Segoe UI", 13))
        subtitle_label.setStyleSheet("color: #aebcd1; background: transparent;")
        text_layout.addWidget(subtitle_label)

        # Right side: Logo
        logo_label = self._create_logo_widget()

        # Add to branding layout - no stretch for tighter spacing
        branding_layout.addWidget(text_container)
        branding_layout.addWidget(logo_label)
        branding_layout.addStretch()  # Push everything to the left

        main_layout.addWidget(branding_container)
        main_layout.addSpacing(20)  # Reduced spacing

        # Login card
        login_card = self._create_login_card()
        main_layout.addWidget(login_card)

        main_layout.addStretch()

        # Footer
        # footer_label = QLabel(
        #     "Authorized personnel only. All access is logged.\n"
        #     "© 2025 SmartEnroll. All rights reserved."
        # )
        # footer_label.setFont(QFont("Segoe UI", 8))
        # footer_label.setStyleSheet("color: #aebcd1; background: transparent;")
        # footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # main_layout.addWidget(footer_label)

        self.setLayout(main_layout)

    def set_window_icon(self):
        """Set custom window icon (taskbar and title bar)"""
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Try multiple possible locations for the logo
        possible_paths = [
            os.path.join(script_dir, "..", "school_logo.png"),
            os.path.join(script_dir, "school_logo.png"),
            "school_logo.png"
        ]

        icon_set = False
        for logo_path in possible_paths:
            if os.path.exists(logo_path):
                print(f"✅ Setting window icon from: {logo_path}")
                icon = QIcon(logo_path)
                self.setWindowIcon(icon)
                icon_set = True
                break

        if not icon_set:
            print("⚠️ Window icon not found. Using default icon.")
            print("💡 Place 'school_logo.png' in project root to set custom icon")

    def _create_logo_widget(self) -> QLabel:
        """Create logo widget with circular background"""
        # Get the correct path to logo
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, "..", "school_logo.png")

        if not os.path.exists(logo_path):
            logo_path = os.path.join(script_dir, "school_logo.png")

        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setFixedSize(100, 100)  # Logo size without background padding

        if os.path.exists(logo_path):
            print(f"✅ Login logo found at: {logo_path}")
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                # Scale logo to fit nicely
                scaled_pixmap = pixmap.scaled(
                    100, 100,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                logo_label.setPixmap(scaled_pixmap)

                # No background - just the logo, clean and simple
                logo_label.setStyleSheet("""
                    QLabel {
                        background: transparent;
                        border: none;
                    }
                """)

            else:
                print("❌ Failed to load login logo image")
                self._set_fallback_logo(logo_label)
        else:
            print(f"❌ Login logo not found at: {logo_path}")
            print("💡 Please save your logo as 'school_logo.png' in the project root")
            print(f"💡 Current working directory: {os.getcwd()}")
            print(f"💡 Script directory: {script_dir}")
            self._set_fallback_logo(logo_label)

        return logo_label

    def _set_fallback_logo(self, logo_label):
        """Set fallback - hide if no logo found"""
        # Just hide the logo label if image not found
        logo_label.setVisible(False)

    def _create_login_card(self) -> QFrame:
        """Create modern login card"""
        login_card = QFrame()
        login_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
            }
        """)

        # Add shadow to card
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 80))
        login_card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(login_card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)

        # Card title
        card_title = QLabel("Login")
        card_title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        card_title.setStyleSheet("color: #1a2b4b; background: transparent;")
        card_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(card_title)

        card_subtitle = QLabel("Enter your credentials to access the system")
        card_subtitle.setFont(QFont("Segoe UI", 11))
        card_subtitle.setStyleSheet("color: #6B7280; background: transparent;")
        card_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(card_subtitle)

        card_layout.addSpacing(15)

        # Username field
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        username_label.setStyleSheet("color: #374151; background: transparent;")
        card_layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet(self._input_style())
        self.username_input.setFixedHeight(48)
        self.username_input.setObjectName("username_input")
        card_layout.addWidget(self.username_input)

        # Password field
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        password_label.setStyleSheet("color: #374151; background: transparent;")
        card_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(self._input_style())
        self.password_input.setFixedHeight(48)
        self.password_input.setObjectName("password_input")
        card_layout.addWidget(self.password_input)

        card_layout.addSpacing(15)

        # Login button
        self.login_btn = QPushButton("Log In")
        self.login_btn.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_btn.setFixedHeight(48)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2c5282, stop:1 #1a365d);
                color: white;
                border: none;
                padding: 12px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a365d, stop:1 #15293d);
            }
            QPushButton:pressed {
                background: #0f1e2e;
            }
        """)
        self.login_btn.setObjectName("login_btn")
        card_layout.addWidget(self.login_btn)

        return login_card

    def _input_style(self) -> str:
        """Return modern input field stylesheet"""
        return """
            QLineEdit {
                background-color: #F9FAFB;
                border: 2px solid #E5E7EB;
                padding: 12px 16px;
                border-radius: 10px;
                font-size: 13px;
                color: #1F2937;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus {
                background-color: #FFFFFF;
                border: 2px solid #2c5282;
                outline: none;
            }
            QLineEdit:hover {
                border: 2px solid #D1D5DB;
            }
        """

    def clear_fields(self):
        """Clear input fields"""
        self.username_input.clear()
        self.password_input.clear()
        self.username_input.setFocus()