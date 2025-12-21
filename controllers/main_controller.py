"""
Main Controller - Initializes MVC Architecture
Creates Database instance which initializes all Models,
then creates Controllers with Database reference
"""
import sys
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QMessageBox
from PyQt6.QtCore import QObject, Qt
from PyQt6.QtGui import QIcon

# Import centralized Database
from models.database import Database

# Import Controllers
from controllers.login_controller import LoginController
from controllers.sidebar_controller import SidebarController
from controllers.dashboard_controller import DashboardController
from controllers.enrollment_controller import EnrollmentController
from controllers.classrooms_controller import ClassroomsController
from controllers.reports_controller import ReportsController
from controllers.management_controller import ManagementController
from controllers.users_controller import UsersController


class MainController(QObject):

    def __init__(self):
        super().__init__()

        print("=" * 60)
        print("Initializing SmartEnroll - MVC Architecture")
        print("=" * 60)

        # ✨ STEP 1: Initialize centralized Database
        print("\n📦 Initializing Database...")
        self.database = Database()

        # Test connection
        if not self.database.test_connection():
            QMessageBox.critical(
                None,
                "Database Error",
                "Cannot connect to MySQL database!\n\n"
                "Please check:\n"
                "1. MySQL server is running\n"
                "2. Database credentials are correct"
            )
            sys.exit(1)

        print("✅ Database initialized successfully!")

        # Initialize tables
        print("\n🔧 Initializing database tables...")
        self.database.initialize_tables()

        # ✨ STEP 2: Create login controller (doesn't need database yet)
        print("\n🔐 Creating login controller...")
        self.login_controller = LoginController(self.database)
        self.login_controller.login_successful.connect(self.on_login_success)

        # Show login window
        print("📱 Showing login window...")
        self.login_controller.get_view().show()

        # Main window will be created after successful login
        self.main_window = None
        self.sidebar_controller = None
        self.dashboard_controller = None
        self.enrollment_controller = None
        self.reports_controller = None
        self.classrooms_controller = None
        self.management_controller = None
        self.users_controller = None
        self.current_user = None

    def on_login_success(self, user_info: dict):
        """Handle successful login"""
        print(f"\n✅ Login successful: {user_info['username']} (Role: {user_info['role']})")

        # Store current user
        self.current_user = user_info

        # Hide login window
        self.login_controller.get_view().hide()

        # Create main window with all controllers
        self.create_main_window(user_info)

    def create_main_window(self, user_info: dict):
        """Create main application window"""
        try:
            print("\n🏗️  Building main window UI...")

            # Create main window
            self.main_window = QMainWindow()
            self.main_window.setWindowTitle("SmartEnroll - Student Enrollment System")

            # Window setup
            from PyQt6.QtWidgets import QApplication
            screen = QApplication.primaryScreen().geometry()
            initial_width = int(screen.width() * 0.8)
            initial_height = int(screen.height() * 0.8)
            self.main_window.setMinimumSize(1000, 600)

            x = (screen.width() - initial_width) // 2
            y = (screen.height() - initial_height) // 2
            self.main_window.setGeometry(x, y, initial_width, initial_height)
            self.main_window.setStyleSheet("QMainWindow { background-color: #F5F7FA; }")

            # Create central widget
            central_widget = QWidget()
            self.main_window.setCentralWidget(central_widget)

            main_layout = QHBoxLayout(central_widget)
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.setSpacing(0)

            # ✨ STEP 3: Create sidebar controller
            print("📊 Creating sidebar...")
            self.sidebar_controller = SidebarController(user_info)
            self.sidebar_controller.page_changed.connect(self.change_page)
            self.sidebar_controller.sign_out_requested.connect(self.handle_logout)
            main_layout.addWidget(self.sidebar_controller.get_view())

            # ✨ STEP 4: Create stacked widget for pages
            print("📚 Creating page stack...")
            self.stacked_widget = QStackedWidget()

            # ✨ STEP 5: Create all page controllers with Database reference
            print("\n🎯 Creating page controllers with Database...")

            print("   → Dashboard controller...")
            self.dashboard_controller = DashboardController(self.database)

            print("   → Enrollment controller...")
            self.enrollment_controller = EnrollmentController(self.database)

            print("   → Reports controller...")
            self.reports_controller = ReportsController(self.database)

            print("   → Classrooms controller...")
            self.classrooms_controller = ClassroomsController(self.database)

            print("   → Management controller...")
            self.management_controller = ManagementController(self.database)

            # Connect enrollment signal to dashboard refresh
            self.enrollment_controller.student_enrolled.connect(
                self.dashboard_controller.refresh_data
            )

            # Add pages to stacked widget
            self.stacked_widget.addWidget(self.dashboard_controller.get_view())  # 0
            self.stacked_widget.addWidget(self.enrollment_controller.get_view())  # 1
            self.stacked_widget.addWidget(self.reports_controller.get_view())  # 2
            self.stacked_widget.addWidget(self.classrooms_controller.get_view())  # 3
            self.stacked_widget.addWidget(self.management_controller.get_view())  # 4

            # Create Users page ONLY for admins
            if user_info['role'].lower() == 'admin':
                print("   → Users controller (admin access)...")
                self.users_controller = UsersController(self.database)
                self.stacked_widget.addWidget(self.users_controller.get_view())  # 5
                print("   ✅ Users page added")

            # Set user role (show/hide admin features)
            self.sidebar_controller.set_user_role(user_info['role'])

            main_layout.addWidget(self.stacked_widget)

            # Show dashboard by default
            self.change_page("dashboard")

            # Show main window
            self.main_window.show()
            print("\n✅ Main window displayed successfully!")
            print("=" * 60)

        except Exception as e:
            print(f"❌ Error creating main window: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                None,
                "Error",
                f"Failed to create main window:\n{str(e)}"
            )

    def change_page(self, page_name: str):
        """Change the current displayed page"""
        try:
            page_map = {
                "dashboard": 0,
                "enrollment": 1,
                "reports": 2,
                "classrooms": 3,
                "management": 4,
                "users": 5
            }

            # Check access for users page
            if page_name == "users" and not self.users_controller:
                QMessageBox.warning(
                    self.main_window,
                    "Access Denied",
                    "You do not have permission to access the Users page."
                )
                return

            index = page_map.get(page_name, 0)
            self.stacked_widget.setCurrentIndex(index)

            # Refresh page data
            if page_name == "dashboard":
                self.dashboard_controller.refresh_data()
            elif page_name == "reports":
                self.reports_controller.refresh_data()
            elif page_name == "classrooms":
                self.classrooms_controller.refresh_classrooms()
            elif page_name == "management":
                self.management_controller.refresh_all_data()
            elif page_name == "users" and self.users_controller:
                self.users_controller.refresh_users()

        except Exception as e:
            print(f"❌ Error changing page: {e}")
            import traceback
            traceback.print_exc()

    def handle_logout(self):
        """Handle user logout"""
        try:
            reply = QMessageBox.question(
                self.main_window,
                "Sign Out",
                "Are you sure you want to sign out?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                print(f"\n🚪 User {self.current_user['username']} logging out...")

                # Close main window
                if self.main_window:
                    self.main_window.close()
                    self.main_window = None

                # Clear references
                self.sidebar_controller = None
                self.dashboard_controller = None
                self.enrollment_controller = None
                self.reports_controller = None
                self.classrooms_controller = None
                self.management_controller = None
                self.users_controller = None
                self.current_user = None

                # Show login window
                self.login_controller.get_view().clear_fields()
                self.login_controller.get_view().show()

                print("✅ Logged out successfully\n")

        except Exception as e:
            print(f"❌ Error during logout: {e}")
            import traceback
            traceback.print_exc()