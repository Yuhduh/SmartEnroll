"""
Users Controller - Uses User Model directly
"""
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget, QMessageBox, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from views.users_page import UsersPageUI


class UsersController(QObject):

    def __init__(self, database):
        super().__init__()

        # Store database reference
        self.db = database

        # Create VIEW
        self.view = UsersPageUI()

        # Connect signals
        self._connect_signals()

        # Load initial data
        self.refresh_users()

    def _connect_signals(self):
        """Connect UI signals to controller methods"""
        self.view.add_user_btn.clicked.connect(self.add_user)
        self.view.new_username_input.returnPressed.connect(self.add_user)
        self.view.new_password_input.returnPressed.connect(self.add_user)

    def get_view(self) -> QWidget:
        """Return the view widget"""
        return self.view

    def refresh_users(self):
        """Refresh the users table using User Model"""
        try:
            # Get all users from User Model
            users = self.db.users.get_all_users()

            # Update user count
            self.view.user_count_label.setText(f"{len(users)} users")

            # Clear table
            self.view.users_table.setRowCount(0)

            # Populate table
            for row, user in enumerate(users):
                self.view.users_table.insertRow(row)

                # Column 0: ID
                self.view.users_table.setItem(row, 0, self._create_table_item(str(user['id'])))

                # Column 1: Username
                self.view.users_table.setItem(row, 1, self._create_table_item(user['username']))

                # Column 2: Role with badge
                role_widget = self._create_role_badge(user['role'])
                self.view.users_table.setCellWidget(row, 2, role_widget)

                # Column 3: Created date
                self.view.users_table.setItem(row, 3, self._create_table_item(user['created_at']))

                # Column 4: Actions (Delete button)
                actions_widget = self._create_actions_widget(user['id'], user['username'])
                self.view.users_table.setCellWidget(row, 4, actions_widget)

                # Set row height
                self.view.users_table.setRowHeight(row, 60)

        except Exception as e:
            print(f"Error refreshing users: {e}")
            import traceback
            traceback.print_exc()

    def _create_table_item(self, text: str):
        """Create a table item"""
        from PyQt6.QtWidgets import QTableWidgetItem
        item = QTableWidgetItem(text)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        return item

    def _create_role_badge(self, role: str) -> QWidget:
        """Create role badge widget"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)

        badge = QLabel(role.upper())

        if role == "admin":
            badge.setStyleSheet("""
                background-color: white;
                color: #E74C3C;
                border: 1px solid #E74C3C;
                padding: 6px 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
            """)
        else:
            badge.setStyleSheet("""
                background-color: white;
                color: #3498DB;
                border: 1px solid #3498DB;
                padding: 6px 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
            """)

        layout.addWidget(badge)
        layout.addStretch()

        return widget

    def _create_actions_widget(self, user_id: int, username: str) -> QWidget:
        """Create actions widget with delete button"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)

        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.clicked.connect(lambda: self.delete_user(user_id, username))

        layout.addWidget(delete_btn)
        layout.addStretch()

        return widget

    def add_user(self):
        """Add a new user using User Model"""
        try:
            # Get form data
            username = self.view.new_username_input.text().strip()
            password = self.view.new_password_input.text().strip()
            role = self.view.new_role_combo.currentText()

            # Validate inputs
            if not username:
                QMessageBox.warning(self.view, "Invalid Input", "Please enter a username")
                return

            if not password:
                QMessageBox.warning(self.view, "Invalid Input", "Please enter a password")
                return

            if len(password) < 6:
                QMessageBox.warning(
                    self.view,
                    "Invalid Input",
                    "Password must be at least 6 characters long for security"
                )
                return

            # Add user using User Model
            success, message = self.db.users.add_user(username, password, role)

            if success:
                QMessageBox.information(
                    self.view,
                    "✅ Success",
                    f"User '{username}' added successfully!\n\n"
                    f"🔒 Password has been securely hashed and stored."
                )

                # Clear form
                self.view.new_username_input.clear()
                self.view.new_password_input.clear()
                self.view.new_role_combo.setCurrentIndex(0)

                # Refresh table
                self.refresh_users()
            else:
                QMessageBox.critical(self.view, "Error", message)

        except Exception as e:
            print(f"Error adding user: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.view, "Error", f"Failed to add user: {str(e)}")

    def delete_user(self, user_id: int, username: str):
        """Delete a user using User Model"""
        try:
            # Confirm deletion
            reply = QMessageBox.question(
                self.view,
                "Confirm Deletion",
                f"Are you sure you want to delete user '{username}'?\n\n"
                f"This action cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Delete using User Model
                success, message = self.db.users.delete_user(user_id)

                if success:
                    QMessageBox.information(
                        self.view,
                        "✅ Success",
                        f"User '{username}' deleted successfully!"
                    )
                    self.refresh_users()
                else:
                    QMessageBox.critical(self.view, "Error", message)

        except Exception as e:
            print(f"Error deleting user: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.view, "Error", f"Failed to delete user: {str(e)}")