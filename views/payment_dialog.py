"""
Payment Dialog - Record payments and manage payment history
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QLineEdit, QComboBox,
                             QScrollArea, QWidget, QMessageBox, QDateEdit,
                             QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont
from datetime import datetime
from decimal import Decimal


class PaymentDialog(QDialog):
    """Dialog for managing student payments"""

    payment_recorded = pyqtSignal(int, dict)  # student_id, payment_data

    def __init__(self, student_data: dict, payment_summary: dict, payment_history: list,
                 academic_years: list, current_user_id: int, parent=None):
        super().__init__(parent)
        self.student_data = student_data
        self.payment_summary = payment_summary
        self.payment_history = payment_history
        self.academic_years = academic_years
        self.current_user_id = current_user_id
        self.setup_ui()

    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle(f"Payment Management - {self.student_data.get('full_name', 'Unknown')}")
        self.setMinimumSize(1000, 750)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header = self._create_header()
        main_layout.addWidget(header)

        # Scrollable Content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #F5F7FA; }")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(25)

        # Payment Summary Card
        summary_card = self._create_payment_summary()
        content_layout.addWidget(summary_card)

        # Two-column layout: New Payment | Payment History
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(20)

        # Left: Record New Payment
        new_payment_card = self._create_new_payment_form()
        columns_layout.addWidget(new_payment_card, 1)

        # Right: Payment History
        history_card = self._create_payment_history()
        columns_layout.addWidget(history_card, 1)

        content_layout.addLayout(columns_layout)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # Action Buttons
        button_layout = self._create_button_layout()
        main_layout.addLayout(button_layout)

    def _create_header(self) -> QFrame:
        """Create header with student info"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #16A085, stop:1 #27AE60);
                border: none;
            }
        """)
        header.setFixedHeight(100)

        layout = QVBoxLayout(header)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(5)

        # Title row
        title_layout = QHBoxLayout()

        title = QLabel("💳 Payment Management")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")

        title_layout.addWidget(title)
        title_layout.addStretch()

        # Student info row
        info_layout = QHBoxLayout()

        student_name = QLabel(f"Student: {self.student_data.get('full_name', 'Unknown')}")
        student_name.setFont(QFont("Segoe UI", 12))
        student_name.setStyleSheet("color: white; background: transparent;")

        lrn_label = QLabel(f"LRN: {self.student_data.get('lrn', 'N/A')}")
        lrn_label.setFont(QFont("Segoe UI", 11))
        lrn_label.setStyleSheet("color: rgba(255,255,255,0.9); background: transparent;")

        strand_label = QLabel(
            f"{self.student_data.get('strand', 'N/A')} - Grade {self.student_data.get('grade_level', '11')}")
        strand_label.setFont(QFont("Segoe UI", 11))
        strand_label.setStyleSheet("color: rgba(255,255,255,0.9); background: transparent;")

        info_layout.addWidget(student_name)
        info_layout.addWidget(lrn_label)
        info_layout.addWidget(strand_label)
        info_layout.addStretch()

        layout.addLayout(title_layout)
        layout.addLayout(info_layout)

        return header

    def _create_payment_summary(self) -> QFrame:
        """Create payment summary card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E5E7EB;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("💰 Payment Summary")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2C3E50; border: none;")
        layout.addWidget(title)

        # Summary grid
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(20)

        # Total Fees
        total_fees = float(self.payment_summary.get('total_fees', 0))
        total_card = self._create_summary_item("Total Fees", f"₱{total_fees:,.2f}", "#3498DB")

        # Amount Paid
        amount_paid = float(self.payment_summary.get('amount_paid', 0))
        paid_card = self._create_summary_item("Amount Paid", f"₱{amount_paid:,.2f}", "#27AE60")

        # Balance
        balance = float(self.payment_summary.get('balance', 0))
        balance_color = "#E74C3C" if balance > 0 else "#27AE60"
        balance_card = self._create_summary_item("Balance", f"₱{balance:,.2f}", balance_color)

        # Payment Status
        status = self.payment_summary.get('payment_status', 'Pending')
        status_colors = {
            'Paid': '#27AE60',
            'Partial': '#F39C12',
            'Pending': '#E74C3C'
        }
        status_card = self._create_summary_item("Status", status, status_colors.get(status, '#7F8C8D'))

        summary_layout.addWidget(total_card)
        summary_layout.addWidget(paid_card)
        summary_layout.addWidget(balance_card)
        summary_layout.addWidget(status_card)

        layout.addLayout(summary_layout)

        return card

    def _create_summary_item(self, label: str, value: str, color: str) -> QFrame:
        """Create a summary item card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color}15;
                border-radius: 8px;
                border: 2px solid {color}40;
            }}
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        label_widget = QLabel(label)
        label_widget.setFont(QFont("Segoe UI", 10))
        label_widget.setStyleSheet(f"color: {color}; border: none; font-weight: bold;")

        value_widget = QLabel(value)
        value_widget.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        value_widget.setStyleSheet(f"color: {color}; border: none;")

        layout.addWidget(label_widget)
        layout.addWidget(value_widget)

        return card

    def _create_new_payment_form(self) -> QFrame:
        """Create form to record new payment"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E5E7EB;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title = QLabel("➕ Record New Payment")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet("color: #2C3E50; border: none;")
        layout.addWidget(title)

        # Amount
        amount_layout = self._create_field_layout("Amount (₱) *")
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount (e.g., 5000.00)")
        self.amount_input.setStyleSheet(self._input_style())
        self.amount_input.setMinimumHeight(40)
        amount_layout.addWidget(self.amount_input)
        layout.addLayout(amount_layout)

        # Payment Date
        date_layout = self._create_field_layout("Payment Date *")
        self.payment_date = QDateEdit()
        self.payment_date.setCalendarPopup(True)
        self.payment_date.setDate(QDate.currentDate())
        self.payment_date.setDisplayFormat("MMMM dd, yyyy")
        self.payment_date.setStyleSheet(self._combo_style())
        self.payment_date.setMinimumHeight(40)
        date_layout.addWidget(self.payment_date)
        layout.addLayout(date_layout)

        # Payment Method
        method_layout = self._create_field_layout("Payment Method *")
        self.payment_method = QComboBox()
        self.payment_method.addItems(["Cash", "Check", "Bank Transfer", "Online Payment", "Installment"])
        self.payment_method.setStyleSheet(self._combo_style())
        self.payment_method.setMinimumHeight(40)
        method_layout.addWidget(self.payment_method)
        layout.addLayout(method_layout)

        # Reference Number
        ref_layout = self._create_field_layout("Reference/Check Number")
        self.reference_input = QLineEdit()
        self.reference_input.setPlaceholderText("Optional - for checks/transfers")
        self.reference_input.setStyleSheet(self._input_style())
        self.reference_input.setMinimumHeight(40)
        ref_layout.addWidget(self.reference_input)
        layout.addLayout(ref_layout)

        # Payment Type
        type_layout = self._create_field_layout("Payment Type *")
        self.payment_type = QComboBox()
        self.payment_type.addItems(["Tuition", "Miscellaneous", "Other"])
        self.payment_type.setStyleSheet(self._combo_style())
        self.payment_type.setMinimumHeight(40)
        type_layout.addWidget(self.payment_type)
        layout.addLayout(type_layout)

        # Academic Year
        year_layout = self._create_field_layout("Academic Year")
        self.academic_year_combo = QComboBox()
        self.academic_year_combo.addItem("Current Academic Year", None)
        for year in self.academic_years:
            self.academic_year_combo.addItem(year['year_name'], year['id'])
        self.academic_year_combo.setStyleSheet(self._combo_style())
        self.academic_year_combo.setMinimumHeight(40)
        year_layout.addWidget(self.academic_year_combo)
        layout.addLayout(year_layout)

        # Notes
        notes_layout = self._create_field_layout("Notes")
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Optional notes...")
        self.notes_input.setStyleSheet(self._input_style())
        self.notes_input.setMaximumHeight(80)
        notes_layout.addWidget(self.notes_input)
        layout.addLayout(notes_layout)

        # Record Payment Button
        self.record_btn = QPushButton("💾 Record Payment")
        self.record_btn.setMinimumHeight(45)
        self.record_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.record_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #229954; }
        """)
        self.record_btn.clicked.connect(self.record_payment)
        layout.addWidget(self.record_btn)

        layout.addStretch()

        return card

    def _create_payment_history(self) -> QFrame:
        """Create payment history table"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E5E7EB;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Title
        title_layout = QHBoxLayout()
        title = QLabel("📜 Payment History")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet("color: #2C3E50; border: none;")

        count_label = QLabel(f"({len(self.payment_history)} transactions)")
        count_label.setStyleSheet("color: #7F8C8D; font-size: 11px; border: none;")

        title_layout.addWidget(title)
        title_layout.addWidget(count_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # Table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels([
            "Date", "Amount", "Method", "Receipt #", "Actions"
        ])

        # Set column widths
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.history_table.setColumnWidth(4, 100)

        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.history_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                gridline-color: #F0F0F0;
            }
            QHeaderView::section {
                background-color: #F8F9FA;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #E5E7EB;
                font-weight: bold;
                color: #2C3E50;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #F0F0F0;
            }
        """)

        # Populate history
        self._populate_history_table()

        layout.addWidget(self.history_table)

        return card

    def _populate_history_table(self):
        """Populate payment history table"""
        self.history_table.setRowCount(0)

        for row, payment in enumerate(self.payment_history):
            self.history_table.insertRow(row)

            # Date
            payment_date = payment.get('payment_date')
            if isinstance(payment_date, str):
                date_str = payment_date
            else:
                date_str = payment_date.strftime('%Y-%m-%d') if payment_date else 'N/A'
            self.history_table.setItem(row, 0, QTableWidgetItem(date_str))

            # Amount
            amount = float(payment.get('amount', 0))
            amount_item = QTableWidgetItem(f"₱{amount:,.2f}")
            amount_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.history_table.setItem(row, 1, amount_item)

            # Method
            self.history_table.setItem(row, 2, QTableWidgetItem(payment.get('payment_method', 'N/A')))

            # Receipt Number
            self.history_table.setItem(row, 3, QTableWidgetItem(payment.get('receipt_number', 'N/A')))

            # Actions - Print Receipt button
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 5, 5, 5)

            print_btn = QPushButton("🖨️")
            print_btn.setToolTip("Print Receipt")
            print_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            print_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498DB;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 4px;
                    font-size: 12px;
                }
                QPushButton:hover { background-color: #2980B9; }
            """)
            print_btn.clicked.connect(lambda checked, p=payment: self.print_receipt(p))

            action_layout.addWidget(print_btn)
            action_layout.addStretch()

            self.history_table.setCellWidget(row, 4, action_widget)
            self.history_table.setRowHeight(row, 45)

    def _create_field_layout(self, label_text: str) -> QVBoxLayout:
        """Create field layout with label"""
        layout = QVBoxLayout()
        layout.setSpacing(6)

        label = QLabel(label_text)
        label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        label.setStyleSheet("color: #374151; background: transparent;")
        layout.addWidget(label)

        return layout

    def _input_style(self) -> str:
        """Input field style"""
        return """
            QLineEdit, QTextEdit {
                background-color: white;
                border: 2px solid #E5E7EB;
                padding: 10px;
                border-radius: 6px;
                font-size: 13px;
                color: #1F2937;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #27AE60;
            }
        """

    def _combo_style(self) -> str:
        """Combobox style"""
        return """
            QComboBox, QDateEdit {
                background-color: white;
                border: 2px solid #E5E7EB;
                padding: 10px;
                border-radius: 6px;
                font-size: 13px;
                color: #1F2937;
            }
            QComboBox:focus, QDateEdit:focus {
                border: 2px solid #27AE60;
            }
        """

    def _create_button_layout(self) -> QHBoxLayout:
        """Create action buttons"""
        layout = QHBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)

        self.close_btn = QPushButton("Close")
        self.close_btn.setMinimumWidth(120)
        self.close_btn.setMinimumHeight(45)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #4B5563; }
        """)
        self.close_btn.clicked.connect(self.accept)

        layout.addWidget(self.close_btn)
        layout.addStretch()

        return layout

    def record_payment(self):
        """Record a new payment"""
        try:
            # Validate amount
            amount_text = self.amount_input.text().strip()
            if not amount_text:
                QMessageBox.warning(self, "Validation Error", "Please enter payment amount")
                return

            try:
                amount = Decimal(amount_text.replace(',', ''))
                if amount <= 0:
                    raise ValueError
            except:
                QMessageBox.warning(self, "Invalid Amount", "Please enter a valid positive amount")
                return

            # Build payment data
            payment_data = {
                'student_id': self.student_data.get('id'),
                'amount': amount,
                'payment_date': self.payment_date.date().toPyDate(),
                'payment_method': self.payment_method.currentText(),
                'reference_number': self.reference_input.text().strip() or None,
                'payment_type': self.payment_type.currentText(),
                'academic_year_id': self.academic_year_combo.currentData(),
                'notes': self.notes_input.toPlainText().strip() or None
            }

            # Confirm payment
            reply = QMessageBox.question(
                self,
                "Confirm Payment",
                f"Record payment of ₱{amount:,.2f}?\n\n"
                f"Method: {payment_data['payment_method']}\n"
                f"Date: {payment_data['payment_date']}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                # Emit signal
                self.payment_recorded.emit(self.student_data.get('id'), payment_data)

        except Exception as e:
            print(f"Error recording payment: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to record payment:\n{str(e)}")

    def print_receipt(self, payment_data: dict):
        """Print receipt for a payment"""
        try:
            from models.payment import PaymentData
            from utils.receipt_generator import generate_payment_receipt

            # Generate receipt PDF
            receipt_file = generate_payment_receipt(
                payment_data,
                self.student_data
            )

            if receipt_file:
                QMessageBox.information(
                    self,
                    "✅ Receipt Generated",
                    f"Receipt has been generated!\n\nFile: {receipt_file}"
                )

                # Try to open the PDF
                import os
                if os.name == 'nt':  # Windows
                    os.startfile(receipt_file)
                elif os.name == 'posix':  # macOS/Linux
                    import subprocess
                    subprocess.call(('open' if os.uname().sysname == 'Darwin' else 'xdg-open', receipt_file))

        except Exception as e:
            print(f"Error printing receipt: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to print receipt:\n{str(e)}")