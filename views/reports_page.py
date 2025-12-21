from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QFrame, QPushButton, QComboBox, QGridLayout, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ReportsPageUI(QWidget):
    def __init__(self):
        super().__init__()
        self.report_buttons = []
        self.setup_ui()

    def setup_ui(self):
        # 1. Main Page Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # 2. Header Section
        title = QLabel("Reports")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet("color: #2C3E50; border: none;")
        subtitle = QLabel("Select a report type and date range to view enrollment data.")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setStyleSheet("color: #7F8C8D; border: none;")
        self.main_layout.addWidget(title)
        self.main_layout.addWidget(subtitle)

        # 3. Report Selection (Buttons)
        type_grid = QGridLayout()
        type_grid.setSpacing(12)
        reports = [
            ("Total Enrollment Summary", "total"),
            ("Enrollment by Strand", "strand"),
            ("Recent Enrollment Activity", "recent")]

        self.report_buttons = []
        for idx, (label, report_type) in enumerate(reports):
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setProperty("report_type", report_type)
            btn.setStyleSheet(self._report_button_style(False))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(45)
            btn.setMinimumWidth(220)
            type_grid.addWidget(btn, 0, idx)
            self.report_buttons.append(btn)

        self.main_layout.addLayout(type_grid)

        # 4. Filter & Action Row (Date Range + Action Buttons)
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)
        self.date_range_badge = QLabel("All Time")
        self.date_range_badge.setStyleSheet("""
                    color: #365486; 
                    background-color: #E8F4F8;
                    padding: 8px 15px; 
                    border-radius: 6px;
                    border: 1px solid #7FC7D9; 
                    font-weight: bold;
                """)
        action_layout.addWidget(self.date_range_badge)

        date_label = QLabel("Date Range:")
        date_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        date_label.setStyleSheet("color: #2C3E50; border: none;")
        action_layout.addWidget(date_label)
        self.date_combo = QComboBox()
        self.date_combo.addItems(["All Time", "Last 30 Days", "Last 7 Days", "Today"])
        self.date_combo.setStyleSheet(self._combo_style())
        action_layout.addWidget(self.date_combo)

        action_layout.addStretch()

        self.generate_btn = QPushButton("Generate Report")
        self.generate_btn.setStyleSheet(self._button_style("#365486"))
        self.generate_btn.setMinimumWidth(150)
        self.generate_btn.setEnabled(False)
        action_layout.addWidget(self.generate_btn)

        self.export_btn = QPushButton("Export to PDF")
        self.export_btn.setStyleSheet(self._button_style("#E74C3C"))
        self.export_btn.setMinimumWidth(150)
        self.export_btn.setEnabled(False)
        action_layout.addWidget(self.export_btn)
        self.main_layout.addLayout(action_layout)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        # 5. Report Display Card
        self.report_card = QFrame()
        self.report_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E8ECF1;
            }
        """)
        self.report_layout = QVBoxLayout(self.report_card)
        self.report_layout.setContentsMargins(15, 15, 15, 15)
        self.placeholder = self._create_placeholder()
        self.report_layout.addWidget(self.placeholder)
        self.scroll.setWidget(self.report_card)
        self.main_layout.addWidget(self.scroll, stretch=1)


    def _create_placeholder(self) -> QWidget:
        placeholder = QWidget()
        layout = QVBoxLayout(placeholder)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        txt = QLabel("No Report Generated")
        txt.setFont(QFont("Segoe UI", 14))
        txt.setStyleSheet("color: #7F8C8D; border: none;")
        layout.addWidget(txt)
        return placeholder

    def _report_button_style(self, selected: bool) -> str:
        border_color = "#365486" if selected else "#E8ECF1"
        bg_color = "#DCF2F1" if selected else "white"
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: #2C3E50;
                border: 2px solid {border_color};
                padding: 10px;
                border-radius: 8px;
            }}
            QPushButton:hover {{ border-color: #7FC7D9; }}
        """

    def _combo_style(self) -> str:
        return """
            QComboBox {
                background-color: #F8F9FA;
                border: 1px solid #D1D5DB;
                padding: 8px;
                border-radius: 6px;
                min-width: 140px;
            }
        """

    def _button_style(self, bg: str) -> str:
        return f"""
            QPushButton {{
                background-color: {bg};
                color: white;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }}
            QPushButton:disabled {{ background-color: #D1D5DB; color: #9CA3AF; }}
        """

#fixed