"""
Login Controller - Handles login logic using User Model
"""
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication
from views.login_view import LoginViewUI


class LoginController(QObject):
    # Signal emitted when login is successful
    login_successful = pyqtSignal(dict)  # Emits user info dict

    def __init__(self, database):
        super().__init__()

        # Store database reference
        self.db = database

        # Create VIEW
        self.view = LoginViewUI()

        # Connect signals
        self._connect_signals()

        # Center the login window on screen AFTER view is fully created
        self.view.show()
        self.center_window()

    def center_window(self):
        """Position the login window at the top-center of the screen"""
        def position_window():
            screen = QApplication.primaryScreen().geometry()
            x = (screen.width() - self.view.width()) // 2
            y = 50
            self.view.move(x, y)

        # Delay positioning slightly to ensure window is rendered
        QTimer.singleShot(10, position_window)

    def _connect_signals(self):
        """Connect UI signals to controller methods"""
        self.view.login_btn.clicked.connect(self.handle_login)
        self.view.password_input.returnPressed.connect(self.handle_login)

    def get_view(self) -> QWidget:
        """Return the view widget"""
        return self.view

    def handle_login(self):
        """Handle login attempt"""
        username = self.view.username_input.text().strip()
        password = self.view.password_input.text().strip()

        # Basic validation
        if not username or not password:
            self._show_error("Login Error", "Please enter both username and password")
            return

        # Use User Model to validate credentials
        user_info = self.db.users.validate_user(username, password)

        if user_info:
            # SUCCESS - Emit signal with user info
            self.login_successful.emit(user_info)
        else:
            # FAILED - Show error
            self._show_error(
                "Login Failed",
                "Invalid username or password.\n\nPlease try again."
            )

            # Clear password and focus
            self.view.password_input.clear()
            self.view.password_input.setFocus()

    def _show_error(self, title: str, message: str):
        """Show error message dialog"""
        msg = QMessageBox(self.view)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()