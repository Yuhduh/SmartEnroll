"""
Record Payment Dialog - Records student payments and generates receipts
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QComboBox, QDateEdit,
                             QTextEdit, QMessageBox, QFrame, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont
from decimal import Decimal
from datetime import date


class RecordPaymentDialog(QDialog):
    """Dialog for recording student payments"""

    payment_recorded = pyqtSignal(int, dict)  # student_id, payment_data

    def __init__(self, student_data: dict, payment_summary: dict, parent=None):
        super().__init__(parent)
        self.student_data = student_data
        self.payment_summary = payment_summary
        self.setup_ui()
        self.populate_data()

    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle(f"Record Payment - {self.student_data.get('full_name', 'Student')}")
        self.setMinimumSize(700, 600)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = self._create_header()
        layout.addWidget(header)

        # Content
        content = QFrame()
        content.setStyleSheet("QFrame { background-color: #F5F7FA; }")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Student Info Summary
        content_layout.addWidget(self._create_student_summary())

        # Payment Balance Card
        content_layout.addWidget(self._create_balance_card())

        # Payment Details Section
        content_layout.addWidget(self._create_section_header("💰 Payment Details"))

        # Amount Row
        amount_layout = QHBoxLayout()
        amount_layout.setSpacing(15)

        amount_col = self._create_field_col("Amount to Pay *")
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        self.amount_input.setStyleSheet(self._input_style())
        self.amount_input.setMinimumHeight(45)
        amount_col.addWidget(self.amount_input)

        date_col = self._create_field_col("Payment Date *")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("MMMM dd, yyyy")
        self.date_input.setStyleSheet(self._input_style())
        self.date_input.setMinimumHeight(45)
        date_col.addWidget(self.date_input)

        amount_layout.addLayout(amount_col)
        amount_layout.addLayout(date_col)
        content_layout.addLayout(amount_layout)

        # Payment Method Row
        method_layout = QHBoxLayout()
        method_layout.setSpacing(15)

        method_col = self._create_field_col("Payment Method *")
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Cash", "Bank Transfer", "Online", "Check"])
        self.method_combo.setStyleSheet(self._combo_style())
        self.method_combo.setMinimumHeight(45)
        method_col.addWidget(self.method_combo)

        type_col = self._create_field_col("Payment Type *")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Tuition", "Miscellaneous", "Other Fees"])
        self.type_combo.setStyleSheet(self._combo_style())
        self.type_combo.setMinimumHeight(45)
        type_col.addWidget(self.type_combo)

        method_layout.addLayout(method_col)
        method_layout.addLayout(type_col)
        content_layout.addLayout(method_layout)

        # Reference Number
        ref_layout = self._create_field_col("Reference Number (Optional)")
        self.reference_input = QLineEdit()
        self.reference_input.setPlaceholderText("Transaction/Check number...")
        self.reference_input.setStyleSheet(self._input_style())
        self.reference_input.setMinimumHeight(45)
        ref_layout.addWidget(self.reference_input)
        content_layout.addLayout(ref_layout)

        # Notes
        notes_layout = self._create_field_col("Notes (Optional)")
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Additional notes about this payment...")
        self.notes_input.setStyleSheet(self._input_style())
        self.notes_input.setMinimumHeight(80)
        self.notes_input.setMaximumHeight(100)
        notes_layout.addWidget(self.notes_input)
        content_layout.addLayout(notes_layout)

        content_layout.addStretch()

        # Wrap content in scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #F5F7FA; }")

        layout.addWidget(scroll)

        # Buttons
        button_layout = self._create_button_layout()
        layout.addLayout(button_layout)

    def _create_header(self) -> QFrame:
        """Create dialog header"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #27AE60, stop:1 #229954);
                border: none;
            }
        """)
        header.setFixedHeight(80)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 20, 30, 20)

        title = QLabel("💳 Record Payment")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")

        layout.addWidget(title)
        layout.addStretch()

        return header

    def _create_student_summary(self) -> QFrame:
        """Create student info summary card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #E5E7EB;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)

        name = QLabel(f"👤 {self.student_data.get('full_name', 'N/A')}")
        name.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        name.setStyleSheet("color: #2C3E50; background: transparent; border: none;")

        details = QLabel(
            f"LRN: {self.student_data.get('lrn', 'N/A')} | "
            f"Strand: {self.student_data.get('strand', 'N/A')} | "
            f"Grade: {self.student_data.get('grade_level', 'N/A')}"
        )
        details.setStyleSheet("color: #6B7280; font-size: 12px; background: transparent; border: none;")

        layout.addWidget(name)
        layout.addWidget(details)

        return card

    def _create_balance_card(self) -> QFrame:
        """Create payment balance summary card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #E5E7EB;
            }
        """)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(30)

        # Total Fees
        total_col = QVBoxLayout()
        total_label = QLabel("Total Fees")
        total_label.setStyleSheet("color: #6B7280; font-size: 12px; background: transparent; border: none;")
        total_value = QLabel(f"₱ {self.payment_summary.get('total_fees', 0):,.2f}")
        total_value.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        total_value.setStyleSheet("color: #2C3E50; background: transparent; border: none;")
        total_col.addWidget(total_label)
        total_col.addWidget(total_value)

        # Amount Paid
        paid_col = QVBoxLayout()
        paid_label = QLabel("Amount Paid")
        paid_label.setStyleSheet("color: #6B7280; font-size: 12px; background: transparent; border: none;")
        paid_value = QLabel(f"₱ {self.payment_summary.get('amount_paid', 0):,.2f}")
        paid_value.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        paid_value.setStyleSheet("color: #27AE60; background: transparent; border: none;")
        paid_col.addWidget(paid_label)
        paid_col.addWidget(paid_value)

        # Balance
        balance_col = QVBoxLayout()
        balance_label = QLabel("Balance")
        balance_label.setStyleSheet("color: #6B7280; font-size: 12px; background: transparent; border: none;")
        balance = self.payment_summary.get('balance', 0)

        # Handle negative balance (overpayment)
        if balance < 0:
            balance_text = f"₱ {abs(balance):,.2f}"
            balance_color = "#27AE60"
            balance_label.setText("Overpaid")
        else:
            balance_text = f"₱ {balance:,.2f}"
            balance_color = "#E74C3C" if balance > 0 else "#27AE60"

        balance_value = QLabel(balance_text)
        balance_value.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        balance_value.setStyleSheet(
            f"color: {balance_color}; background: transparent; border: none;")
        balance_col.addWidget(balance_label)
        balance_col.addWidget(balance_value)

        layout.addLayout(total_col)
        layout.addLayout(paid_col)
        layout.addStretch()
        layout.addLayout(balance_col)

        return card

    def _create_section_header(self, text: str) -> QLabel:
        """Create section header"""
        label = QLabel(text)
        label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        label.setStyleSheet("""
            color: #2C3E50;
            background: transparent;
            border: none;
            padding: 10px 0px;
            border-bottom: 2px solid #E5E7EB;
        """)
        return label

    def _create_field_col(self, label_text: str) -> QVBoxLayout:
        """Create field column layout"""
        layout = QVBoxLayout()
        layout.setSpacing(8)

        label = QLabel(label_text)
        label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        label.setStyleSheet("color: #374151; background: transparent; border: none;")
        layout.addWidget(label)

        return layout

    def _input_style(self) -> str:
        return """
            QLineEdit, QTextEdit, QDateEdit {
                background-color: white;
                border: 2px solid #E5E7EB;
                padding: 10px;
                border-radius: 8px;
                font-size: 13px;
                color: #1F2937;
            }
            QLineEdit:focus, QTextEdit:focus, QDateEdit:focus {
                border: 2px solid #27AE60;
            }
        """

    def _combo_style(self) -> str:
        return """
            QComboBox {
                background-color: white;
                border: 2px solid #E5E7EB;
                padding: 10px;
                border-radius: 8px;
                font-size: 13px;
            }
            QComboBox:focus { border: 2px solid #27AE60; }
        """

    def _create_button_layout(self) -> QHBoxLayout:
        """Create action buttons"""
        layout = QHBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setMinimumWidth(120)
        self.cancel_btn.setMinimumHeight(45)
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cancel_btn.setStyleSheet("""
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
        self.cancel_btn.clicked.connect(self.reject)

        self.record_btn = QPushButton("💾 Record Payment & Generate Receipt")
        self.record_btn.setMinimumWidth(250)
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

        layout.addWidget(self.cancel_btn)
        layout.addStretch()
        layout.addWidget(self.record_btn)

        return layout

    def populate_data(self):
        """Pre-populate form with default values"""
        # Set amount to remaining balance
        balance = self.payment_summary.get('balance', 0)
        if balance > 0:
            self.amount_input.setText(f"{balance:.2f}")

    def record_payment(self):
        """Validate and record payment"""
        try:
            # Validate amount
            amount_text = self.amount_input.text().strip()
            if not amount_text:
                QMessageBox.warning(self, "Validation Error", "Please enter payment amount")
                return

            try:
                amount = Decimal(amount_text)
                if amount <= 0:
                    raise ValueError
            except:
                QMessageBox.warning(self, "Invalid Amount", "Please enter a valid positive amount")
                return

            # Build payment data
            payment_data = {
                'student_id': self.student_data.get('id'),
                'amount': amount,
                'payment_date': self.date_input.date().toPyDate(),
                'payment_method': self.method_combo.currentText(),
                'payment_type': self.type_combo.currentText(),
                'reference_number': self.reference_input.text().strip() or None,
                'notes': self.notes_input.toPlainText().strip() or None
            }

            # Emit signal
            self.payment_recorded.emit(self.student_data.get('id'), payment_data)
            self.accept()

        except Exception as e:
            print(f"Error recording payment: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to record payment:\n{str(e)}")