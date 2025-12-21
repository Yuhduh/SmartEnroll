"""
Advanced Search Dialog - Filter students by multiple criteria
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class AdvancedSearchDialog(QDialog):
    """Dialog for advanced student search"""

    search_requested = pyqtSignal(dict)  # Emits search filters

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle("Advanced Student Search")
        self.setMinimumSize(600, 500)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("🔍 Advanced Search Filters")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #2C3E50;")
        layout.addWidget(title)

        # Search by name/LRN/email
        name_layout = QVBoxLayout()
        name_label = QLabel("Search by Name, LRN, or Email:")
        name_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter name, LRN, or email...")
        self.name_input.setStyleSheet(self._input_style())
        self.name_input.setMinimumHeight(40)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Filters row 1: Strand, Grade, Status
        filters1 = QHBoxLayout()
        filters1.setSpacing(15)

        # Strand filter
        strand_layout = QVBoxLayout()
        strand_label = QLabel("Strand:")
        strand_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.strand_combo = QComboBox()
        self.strand_combo.addItems(["All", "STEM", "ABM", "HUMSS", "GAS", "TVL"])
        self.strand_combo.setStyleSheet(self._combo_style())
        self.strand_combo.setMinimumHeight(40)
        strand_layout.addWidget(strand_label)
        strand_layout.addWidget(self.strand_combo)

        # Grade filter
        grade_layout = QVBoxLayout()
        grade_label = QLabel("Grade Level:")
        grade_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.grade_combo = QComboBox()
        self.grade_combo.addItems(["All", "11", "12"])
        self.grade_combo.setStyleSheet(self._combo_style())
        self.grade_combo.setMinimumHeight(40)
        grade_layout.addWidget(grade_label)
        grade_layout.addWidget(self.grade_combo)

        # Status filter
        status_layout = QVBoxLayout()
        status_label = QLabel("Status:")
        status_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["All", "Enrolled", "Pending", "Dropped", "Transferred", "Graduated"])
        self.status_combo.setStyleSheet(self._combo_style())
        self.status_combo.setMinimumHeight(40)
        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_combo)

        filters1.addLayout(strand_layout)
        filters1.addLayout(grade_layout)
        filters1.addLayout(status_layout)
        layout.addLayout(filters1)

        # Filters row 2: Payment Status, Gender
        filters2 = QHBoxLayout()
        filters2.setSpacing(15)

        # Payment Status
        payment_layout = QVBoxLayout()
        payment_label = QLabel("Payment Status:")
        payment_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.payment_combo = QComboBox()
        self.payment_combo.addItems(["All", "Pending", "Partial", "Paid"])
        self.payment_combo.setStyleSheet(self._combo_style())
        self.payment_combo.setMinimumHeight(40)
        payment_layout.addWidget(payment_label)
        payment_layout.addWidget(self.payment_combo)

        # Gender
        gender_layout = QVBoxLayout()
        gender_label = QLabel("Gender:")
        gender_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["All", "Male", "Female"])
        self.gender_combo.setStyleSheet(self._combo_style())
        self.gender_combo.setMinimumHeight(40)
        gender_layout.addWidget(gender_label)
        gender_layout.addWidget(self.gender_combo)

        filters2.addLayout(payment_layout)
        filters2.addLayout(gender_layout)
        layout.addLayout(filters2)

        # Buttons
        button_layout = QHBoxLayout()

        self.clear_btn = QPushButton("Clear Filters")
        self.clear_btn.setMinimumHeight(45)
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.setStyleSheet("""
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
        self.clear_btn.clicked.connect(self.clear_filters)

        self.search_btn = QPushButton("🔍 Search")
        self.search_btn.setMinimumHeight(45)
        self.search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.search_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2563EB; }
        """)
        self.search_btn.clicked.connect(self.perform_search)

        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.search_btn)
        layout.addLayout(button_layout)

        layout.addStretch()

    def _input_style(self):
        return """
            QLineEdit {
                background-color: white;
                border: 2px solid #E5E7EB;
                padding: 10px;
                border-radius: 8px;
                font-size: 13px;
            }
            QLineEdit:focus { border: 2px solid #3B82F6; }
        """

    def _combo_style(self):
        return """
            QComboBox {
                background-color: white;
                border: 2px solid #E5E7EB;
                padding: 10px;
                border-radius: 8px;
                font-size: 13px;
            }
            QComboBox:focus { border: 2px solid #3B82F6; }
        """

    def clear_filters(self):
        """Clear all filter selections"""
        self.name_input.clear()
        self.strand_combo.setCurrentIndex(0)
        self.grade_combo.setCurrentIndex(0)
        self.status_combo.setCurrentIndex(0)
        self.payment_combo.setCurrentIndex(0)
        self.gender_combo.setCurrentIndex(0)

    def perform_search(self):
        """Emit search filters"""
        filters = {
            'name': self.name_input.text().strip(),
            'strand': self.strand_combo.currentText() if self.strand_combo.currentText() != "All" else None,
            'grade_level': self.grade_combo.currentText() if self.grade_combo.currentText() != "All" else None,
            'status': self.status_combo.currentText() if self.status_combo.currentText() != "All" else None,
            'payment_status': self.payment_combo.currentText() if self.payment_combo.currentText() != "All" else None,
            'gender': self.gender_combo.currentText() if self.gender_combo.currentText() != "All" else None
        }
        self.search_requested.emit(filters)
        self.accept()