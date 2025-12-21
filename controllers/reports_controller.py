from datetime import datetime, timedelta
from PyQt6.QtCore import QObject, QSize
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel,
                             QFrame, QTableWidget, QTableWidgetItem,
                             QHeaderView, QGridLayout, QFileDialog, QMessageBox, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from views.reports_page import ReportsPageUI

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class ReportsController(QObject):

    def __init__(self, database):
        super().__init__()

        # Store database reference
        self.db = database

        # Create view
        self.view = ReportsPageUI()

        # Controller state
        self.selected_report = None
        self.report_generated = False
        self.current_report_data = None
        self.current_date_range = "All Time"

        # Connect signals
        self._connect_signals()
        self._apply_responsive_settings()

    def _apply_responsive_settings(self):
        self.view.setMinimumSize(QSize(950, 600))

    def _connect_signals(self):
        for btn in self.view.report_buttons:
            btn.clicked.connect(lambda checked, b=btn: self.select_report_type(b))

        self.view.generate_btn.clicked.connect(self.generate_report)
        self.view.export_btn.clicked.connect(self.export_to_pdf)
        self.view.date_combo.currentTextChanged.connect(self.on_date_range_changed)

    def get_view(self) -> QWidget:
        return self.view

    def select_report_type(self, button):
        for btn in self.view.report_buttons:
            btn.setChecked(False)
            btn.setStyleSheet(self.view._report_button_style(False))

        button.setChecked(True)
        button.setStyleSheet(self.view._report_button_style(True))

        self.selected_report = button.property("report_type")
        self.view.generate_btn.setEnabled(True)
        self.view.export_btn.setEnabled(False)
        self.report_generated = False
        self.current_report_data = None

    def on_date_range_changed(self, date_range: str):
        """Handle date range change - FIXED"""
        print(f"DEBUG: Date range changed to: {date_range}")
        self.current_date_range = date_range
        if self.report_generated and self.selected_report:
            print("DEBUG: Auto-regenerating report with new date range")
            self.generate_report()

    def generate_report(self):
        """Generate report using Student Model - FIXED date filtering"""
        if not self.selected_report:
            return

        try:
            self.current_date_range = self.view.date_combo.currentText()
            print(f"DEBUG: Generating report for date range: {self.current_date_range}")
            self.view.date_range_badge.setText(f"{self.current_date_range}")

            self._clear_report_display()

            if self.selected_report == "total":
                self._generate_total_report()
            elif self.selected_report == "strand":
                self._generate_strand_report()
            elif self.selected_report == "recent":
                self._generate_recent_report()

            self.report_generated = True
            self.view.export_btn.setEnabled(True)

        except Exception as e:
            print(f"Error generating report: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.view,
                "Error",
                f"Failed to generate report:\n{str(e)}"
            )

    def _clear_report_display(self):
        while self.view.report_layout.count() > 0:
            item = self.view.report_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

    def _clear_layout(self, layout):
        while layout.count() > 0:
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

    def _get_date_filter(self):
        """Get date filter for queries - FIXED"""
        today = datetime.now()

        if self.current_date_range == "Today":
            start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
            print(f"DEBUG: Date filter - Today: {start_date}")
            return start_date
        elif self.current_date_range == "Last 7 Days":
            start_date = today - timedelta(days=7)
            print(f"DEBUG: Date filter - Last 7 Days: {start_date}")
            return start_date
        elif self.current_date_range == "Last 30 Days":
            start_date = today - timedelta(days=30)
            print(f"DEBUG: Date filter - Last 30 Days: {start_date}")
            return start_date
        else:  # All Time
            print("DEBUG: Date filter - All Time (None)")
            return None

    def _generate_total_report(self):
        """Generate total enrollment report - FIXED"""
        print("DEBUG: Generating total report...")
        date_filter = self._get_date_filter()
        stats = self.db.students.get_enrollment_stats(date_filter=date_filter)
        print(f"DEBUG: Stats retrieved: {stats}")
        self.current_report_data = stats

        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)

        total_card = self._create_stat_card("Total Enrolled", str(stats['total_enrolled']))
        slots_card = self._create_stat_card("Total Slots", str(stats['total_slots']))
        available_card = self._create_stat_card("Available Slots", str(stats['available_slots']))

        total_card.setMinimumWidth(120)
        slots_card.setMinimumWidth(120)
        available_card.setMinimumWidth(120)

        stats_grid.addWidget(total_card, 1, 0)
        stats_grid.addWidget(slots_card, 1, 1)
        stats_grid.addWidget(available_card, 1, 2)

        self.view.report_layout.addLayout(stats_grid)

        breakdown_label = QLabel(f"Breakdown by Strand ({self.current_date_range})")
        breakdown_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        breakdown_label.setStyleSheet("color: #2C3E50; border: none; margin-top: 15px;")
        self.view.report_layout.addWidget(breakdown_label)

        table = self._create_strand_table(stats['by_strand'])
        self.view.report_layout.addWidget(table)

    def _generate_strand_report(self):
        """Generate strand report - FIXED"""
        print("DEBUG: Generating strand report...")
        date_filter = self._get_date_filter()
        stats = self.db.students.get_enrollment_stats(date_filter=date_filter)
        print(f"DEBUG: Stats retrieved: {stats}")
        self.current_report_data = stats['by_strand']

        info_label = QLabel(f"Showing data for: {self.current_date_range}")
        info_label.setStyleSheet("color: #7F8C8D; font-size: 12px; border: none; margin-bottom: 10px;")
        self.view.report_layout.addWidget(info_label)

        table = self._create_strand_table(stats['by_strand'], show_total=True)
        self.view.report_layout.addWidget(table)

    def _generate_recent_report(self):
        """Generate recent enrollments report - FIXED"""
        print("DEBUG: Generating recent report...")
        date_filter = self._get_date_filter()

        if date_filter:
            print(f"DEBUG: Fetching enrollments since: {date_filter}")
            enrollments = self.db.students.get_enrollments_by_date(date_filter, limit=50)
        else:
            print("DEBUG: Fetching recent enrollments (no date filter)")
            enrollments = self.db.students.get_recent_enrollments(50)

        print(f"DEBUG: Found {len(enrollments)} enrollments")
        self.current_report_data = enrollments

        count_label = QLabel(f"Showing {len(enrollments)} enrollments ({self.current_date_range})")
        count_label.setStyleSheet("color: #7F8C8D; font-size: 12px; border: none;")
        self.view.report_layout.addWidget(count_label)

        if len(enrollments) == 0:
            no_data_label = QLabel(f"No enrollments found for {self.current_date_range}")
            no_data_label.setStyleSheet("""
                color: #E74C3C;
                font-size: 14px;
                border: 2px dashed #E8ECF1;
                padding: 40px;
                border-radius: 8px;
                text-align: center;
            """)
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.view.report_layout.addWidget(no_data_label)
            return

        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Student Name", "Strand", "Date Enrolled", "Status"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setStyleSheet(self._table_style())
        table.verticalHeader().setVisible(False)

        table.setRowCount(len(enrollments))
        for row, enrollment in enumerate(enrollments):
            table.setItem(row, 0, QTableWidgetItem(enrollment['full_name']))
            table.setItem(row, 1, QTableWidgetItem(enrollment['strand']))

            # Parse date properly
            date_str = enrollment['date']
            try:
                if isinstance(date_str, str):
                    # Try parsing with seconds first
                    try:
                        dt_object = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        # Fallback for data missing seconds
                        try:
                            dt_object = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                        except ValueError:
                            # Fallback for date only
                            dt_object = datetime.strptime(date_str, "%Y-%m-%d")

                    formatted_date = dt_object.strftime("%b %d, %Y")
                else:
                    formatted_date = str(date_str)
            except Exception as e:
                print(f"DEBUG: Date parsing error: {e}")
                formatted_date = str(date_str)

            table.setItem(row, 2, QTableWidgetItem(formatted_date))
            table.setItem(row, 3, QTableWidgetItem(enrollment['status']))

        self.view.report_layout.addWidget(table)

    def _create_stat_card(self, title: str, value: str) -> QFrame:
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #DCF2F1;
                border-radius: 8px;
                padding: 15px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #365486; border: none;")

        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        value_label.setStyleSheet("color: #0F1035; border: none;")

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        return card

    def _create_strand_table(self, strand_data: list, show_total: bool = False) -> QTableWidget:
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Strand", "Enrolled", "Total Slots", "Available", "Fill Rate"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setStyleSheet(self._table_style())
        table.verticalHeader().setVisible(False)

        rows = len(strand_data)
        if show_total:
            rows += 1

        table.setRowCount(rows)

        total_enrolled = 0
        total_slots = 0

        for row, strand in enumerate(strand_data):
            enrolled = strand['enrolled']
            slots = strand['total_slots']
            available = slots - enrolled
            fill_rate = (enrolled / slots * 100) if slots > 0 else 0

            table.setItem(row, 0, QTableWidgetItem(strand['name']))
            table.setItem(row, 1, QTableWidgetItem(str(enrolled)))
            table.setItem(row, 2, QTableWidgetItem(str(slots)))
            table.setItem(row, 3, QTableWidgetItem(str(available)))
            table.setItem(row, 4, QTableWidgetItem(f"{fill_rate:.1f}%"))

            total_enrolled += enrolled
            total_slots += slots

        if show_total:
            total_available = total_slots - total_enrolled
            total_fill_rate = (total_enrolled / total_slots * 100) if total_slots > 0 else 0

            table.setItem(rows - 1, 0, QTableWidgetItem("TOTAL"))
            table.setItem(rows - 1, 1, QTableWidgetItem(str(total_enrolled)))
            table.setItem(rows - 1, 2, QTableWidgetItem(str(total_slots)))
            table.setItem(rows - 1, 3, QTableWidgetItem(str(total_available)))
            table.setItem(rows - 1, 4, QTableWidgetItem(f"{total_fill_rate:.1f}%"))

            for col in range(5):
                item = table.item(rows - 1, col)
                if item:
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)

        return table

    def _table_style(self) -> str:
        return """
            QTableWidget {
                border: 1px solid #E8ECF1;
                background-color: white;
                gridline-color: #F0F0F0;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #F0F0F0;
            }
            QHeaderView::section {
                background-color: #365486;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """

    def refresh_data(self):
        """Refresh current report - FIXED"""
        if self.report_generated and self.selected_report:
            print("DEBUG: Refreshing report data...")
            self.generate_report()

    def export_to_pdf(self):
        if not self.report_generated or not self.current_report_data:
            QMessageBox.warning(
                self.view,
                "No Data",
                "Please generate a report first before exporting."
            )
            return

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"SmartEnroll_{self.selected_report}_{self.current_date_range.replace(' ', '_')}_{timestamp}.pdf"

            file_path, _ = QFileDialog.getSaveFileName(
                self.view,
                "Export Report to PDF",
                default_filename,
                "PDF Files (*.pdf);;All Files (*)"
            )

            if not file_path:
                return

            if self.selected_report == "total":
                self._export_total_pdf(file_path)
            elif self.selected_report == "strand":
                self._export_strand_pdf(file_path)
            elif self.selected_report == "recent":
                self._export_recent_pdf(file_path)

            QMessageBox.information(
                self.view,
                "Export Successful",
                f"Report exported successfully to:\n{file_path}"
            )

            print(f"✅ PDF exported to: {file_path}")

        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Export Failed",
                f"Failed to export PDF report:\n{str(e)}"
            )
            print(f"❌ Error exporting PDF: {e}")
            import traceback
            traceback.print_exc()

    def _create_pdf_header(self, story, styles, title: str, subtitle: str = None):
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#365486'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#7F8C8D'),
            spaceAfter=12,
            alignment=TA_CENTER
        )

        date_style = ParagraphStyle(
            'DateRange',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#365486'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        story.append(Paragraph("SmartEnroll System", title_style))
        story.append(Paragraph("Student Enrollment Management System", subtitle_style))
        story.append(Paragraph(f"📅 Date Range: {self.current_date_range}", date_style))
        story.append(Spacer(1, 0.2 * inch))

        story.append(Paragraph(title, title_style))
        if subtitle:
            story.append(Paragraph(subtitle, subtitle_style))
        story.append(Spacer(1, 0.3 * inch))

    def _create_pdf_footer(self, story, styles):
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#7F8C8D'),
            alignment=TA_CENTER
        )

        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph("_" * 100, footer_style))
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph(
            f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M:%S %p')}",
            footer_style
        ))
        story.append(Paragraph("© 2025 SmartEnroll System. All rights reserved.", footer_style))

    def _export_total_pdf(self, file_path: str):
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        self._create_pdf_header(story, styles, "TOTAL ENROLLMENT SUMMARY REPORT",
                                f"Complete System Overview")

        heading_style = ParagraphStyle(
            'Heading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#365486'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )

        story.append(Paragraph("ENROLLMENT STATISTICS", heading_style))

        summary_data = [
            ['Metric', 'Value'],
            ['Total Students Enrolled', str(self.current_report_data['total_enrolled'])],
            ['Total Available Slots', str(self.current_report_data['total_slots'])],
            ['Remaining Slots', str(self.current_report_data['available_slots'])],
            ['Fill Rate',
             f"{(self.current_report_data['total_enrolled'] / self.current_report_data['total_slots'] * 100):.1f}%"],
        ]

        summary_table = Table(summary_data, colWidths=[3 * inch, 3 * inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#365486')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E8ECF1')),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F7FA')]),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
        ]))

        story.append(summary_table)
        story.append(Spacer(1, 0.3 * inch))

        story.append(Paragraph(f"ENROLLMENT BY STRAND ({self.current_date_range})", heading_style))

        strand_data = [['Strand', 'Enrolled', 'Total Slots', 'Available', 'Fill Rate']]

        for strand in self.current_report_data['by_strand']:
            available = strand['total_slots'] - strand['enrolled']
            fill_rate = (strand['enrolled'] / strand['total_slots'] * 100) if strand['total_slots'] > 0 else 0
            strand_data.append([
                strand['name'],
                str(strand['enrolled']),
                str(strand['total_slots']),
                str(available),
                f"{fill_rate:.1f}%"
            ])

        strand_table = Table(strand_data, colWidths=[1.5 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch])
        strand_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#365486')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E8ECF1')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F7FA')]),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))

        story.append(strand_table)

        self._create_pdf_footer(story, styles)

        doc.build(story)

    def _export_strand_pdf(self, file_path: str):
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        self._create_pdf_header(story, styles, "ENROLLMENT BY STRAND REPORT",
                                f"Detailed Strand Analysis - {self.current_date_range}")

        strand_data = [['Strand', 'Enrolled', 'Total Slots', 'Available', 'Fill Rate (%)']]

        total_enrolled = 0
        total_slots = 0

        for strand in self.current_report_data:
            enrolled = strand['enrolled']
            slots = strand['total_slots']
            available = slots - enrolled
            fill_rate = (enrolled / slots * 100) if slots > 0 else 0

            strand_data.append([
                strand['name'],
                str(enrolled),
                str(slots),
                str(available),
                f"{fill_rate:.1f}%"
            ])

            total_enrolled += enrolled
            total_slots += slots

        total_fill_rate = (total_enrolled / total_slots * 100) if total_slots > 0 else 0
        strand_data.append([
            'TOTAL',
            str(total_enrolled),
            str(total_slots),
            str(total_slots - total_enrolled),
            f"{total_fill_rate:.1f}%"
        ])

        strand_table = Table(strand_data, colWidths=[1.5 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch, 1.5 * inch])
        strand_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#365486')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#F5F7FA')]),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#DCF2F1')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E8ECF1')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
        ]))

        story.append(strand_table)
        self._create_pdf_footer(story, styles)

        doc.build(story)

    def _export_recent_pdf(self, file_path: str):
        doc = SimpleDocTemplate(file_path, pagesize=landscape(letter))
        story = []
        styles = getSampleStyleSheet()

        self._create_pdf_header(story, styles, "RECENT ENROLLMENT ACTIVITY REPORT",
                                f"Last {len(self.current_report_data)} Enrollments - {self.current_date_range}")

        if len(self.current_report_data) == 0:
            no_data_style = ParagraphStyle(
                'NoData',
                parent=styles['Normal'],
                fontSize=14,
                textColor=colors.HexColor('#E74C3C'),
                spaceAfter=20,
                alignment=TA_CENTER
            )
            story.append(Paragraph(f"⚠️ No enrollments found for {self.current_date_range}", no_data_style))
        else:
            enrollment_data = [['#', 'Student Name', 'Strand', 'Enrollment Date', 'Status']]

            for idx, enrollment in enumerate(self.current_report_data, 1):
                enrollment_data.append([
                    str(idx),
                    enrollment['full_name'],
                    enrollment['strand'],
                    enrollment['date'],
                    enrollment['status']
                ])

            enrollment_table = Table(enrollment_data,
                                     colWidths=[0.5 * inch, 2.5 * inch, 1.5 * inch, 2 * inch, 1.2 * inch])
            enrollment_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#365486')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F7FA')]),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E8ECF1')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ]))

            story.append(enrollment_table)

        self._create_pdf_footer(story, styles)

        doc.build(story)