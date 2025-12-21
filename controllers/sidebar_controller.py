from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton
from views.sidebar import SidebarUI

class SidebarController(QObject):

    # Signals
    page_changed = pyqtSignal(str)  # Emits page name when navigation button clicked
    sign_out_requested = pyqtSignal()  # Emits when user clicks sign out

    def __init__(self, user_info: dict = None):
        super().__init__()

        # Create VIEW
        self.view = SidebarUI()

        # Store user info
        self.user_info = user_info or {'username': 'School Staff', 'role': 'staff'}
        self.current_page = "dashboard"

        # Update user display
        self._update_user_display()

        # Connect signals
        self._connect_signals()

        # Set initial active button
        self.set_active_button(self.view.dashboard_btn)

    def _connect_signals(self):
        """Connect UI signals to controller methods"""
        self.view.dashboard_btn.clicked.connect(
            lambda: self.on_menu_click("dashboard", self.view.dashboard_btn)
        )
        self.view.enrollment_btn.clicked.connect(
            lambda: self.on_menu_click("enrollment", self.view.enrollment_btn)
        )
        self.view.classrooms_btn.clicked.connect(
            lambda: self.on_menu_click("classrooms", self.view.classrooms_btn)
        )
        self.view.management_btn.clicked.connect(
            lambda: self.on_menu_click("management", self.view.management_btn)
        )
        self.view.reports_btn.clicked.connect(
            lambda: self.on_menu_click("reports", self.view.reports_btn)
        )
        self.view.users_btn.clicked.connect(
            lambda: self.on_menu_click("users", self.view.users_btn)
        )
        self.view.signout_btn.clicked.connect(self.on_sign_out)

    def get_view(self) -> QWidget:
        """Return the view widget"""
        return self.view

    def on_menu_click(self, page_name: str, button: QPushButton):
        """Handle menu button click"""
        print(f"Menu clicked: {page_name}")
        self.current_page = page_name
        self.set_active_button(button)
        self.page_changed.emit(page_name)

    def set_active_button(self, active_button: QPushButton):
        """Set the active state for menu buttons - FIXED: Include management button"""
        # FIXED: Include ALL navigation buttons including management
        all_buttons = [
            self.view.dashboard_btn,
            self.view.enrollment_btn,
            self.view.reports_btn,
            self.view.classrooms_btn,
            self.view.management_btn,  # FIXED: Added management button
            self.view.users_btn
        ]

        # Deactivate all buttons
        for btn in all_buttons:
            btn.setProperty("active", "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        # Activate clicked button
        active_button.setProperty("active", "true")
        active_button.style().unpolish(active_button)
        active_button.style().polish(active_button)

    def on_sign_out(self):
        """Handle sign out button click"""
        self.sign_out_requested.emit()

    def _update_user_display(self):
        """Update user information display"""
        username = self.user_info.get('username', 'User')
        role = self.user_info.get('role', 'staff')

        # Update username with icon based on role
        if role.lower() == 'admin':
            self.view.user_label.setText(f"👤 {username}")
        else:
            self.view.user_label.setText(f"👤 {username}")

        # Update role with styling
        role_display = role.title()
        if role.lower() == 'admin':
            self.view.role_label.setText(f"Role: {role_display} ⭐")
            self.view.role_label.setStyleSheet(
                "color: rgba(231, 76, 60, 0.9); border: none; font-size: 10px; font-weight: bold;"
            )
        else:
            self.view.role_label.setText(f"Role: {role_display}")
            self.view.role_label.setStyleSheet(
                "color: rgba(255, 255, 255, 0.6); border: none; font-size: 10px;"
            )

    def update_user_info(self, user_info: dict):
        """Update user information"""
        self.user_info = user_info
        self._update_user_display()

    def set_user_role(self, role: str):
        """Show/hide features based on user role"""
        is_admin = (role.lower() == "admin")

        print("\n" + "=" * 60)
        print("SETTING USER ROLE")
        print("=" * 60)
        print(f"   Role: {role}")
        print(f"   Is Admin: {is_admin}")
        print(f"   Username: {self.user_info['username']}")
        print("\nCHECKING VIEW COMPONENTS:")
        print(f"   ✓ View exists: {self.view is not None}")
        print(f"   ✓ Users button exists: {hasattr(self.view, 'users_btn')}")
        print(f"   ✓ Admin separator exists: {hasattr(self.view, 'admin_separator')}")
        print(f"   ✓ Admin label exists: {hasattr(self.view, 'admin_label')}")
        print("\nVISIBILITY BEFORE:")
        print(f"   Users button visible: {self.view.users_btn.isVisible()}")
        print(f"   Admin separator visible: {self.view.admin_separator.isVisible()}")
        print(f"   Admin label visible: {self.view.admin_label.isVisible()}")

        # Call the view method to show/hide admin features
        print("\nCALLING show_admin_features()...")
        self.view.show_admin_features(is_admin)

        print("\nVISIBILITY AFTER:")
        print(f"   Users button visible: {self.view.users_btn.isVisible()}")
        print(f"   Admin separator visible: {self.view.admin_separator.isVisible()}")
        print(f"   Admin label visible: {self.view.admin_label.isVisible()}")

        if is_admin:
            print("\n✅ ADMIN FEATURES ENABLED")
            print(f"   User: {self.user_info['username']}")
            print(f"   Available pages: Dashboard, Enrollment, Reports, Classrooms, Management, Users")
            if not self.view.users_btn.isVisible():
                print("\n⚠️ WARNING: Users button should be visible but it's not!")
        else:
            print("\n👤 STANDARD USER ACCESS")
            print(f"   User: {self.user_info['username']}")
            print(f"   Available pages: Dashboard, Enrollment, Reports, Classrooms, Management")

        print("=" * 60 + "\n")