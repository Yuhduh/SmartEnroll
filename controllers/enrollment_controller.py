from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMessageBox
from views.enrollment_page import EnrollmentPageUI
from models.student import StudentData
from models.section import SectionData
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os


class EnrollmentController(QObject):
    student_enrolled = pyqtSignal()

    def __init__(self, database):
        super().__init__()

        # Store database reference
        self.db = database

        # Create view
        self.view = EnrollmentPageUI()

        # Last enrolled student
        self.last_enrolled_student = None

        # Connect signals
        self._connect_signals()

        # Update display
        self.update_limits_display()

    def get_view(self):
        return self.view

    def _connect_signals(self):
        """Connect view signals to controller methods"""
        self.view.enroll_btn.clicked.connect(self.enroll_student)
        self.view.clear_btn.clicked.connect(self.clear_form)
        self.view.print_btn.clicked.connect(self.print_registration_form)

    def update_limits_display(self):
        """Update enrollment limits display using Model data"""
        try:
            # Get stats from Student model
            stats = self.db.students.get_enrollment_stats()

            total_enrolled = stats['total_enrolled']
            total_slots = 500
            available = total_slots - total_enrolled

            # Update view with processed data
            self.view.limits_text.setText(
                f"<b>Enrollment Status:</b> {total_enrolled}/{total_slots} students enrolled | "
                f"<span style='color: {'#E74C3C' if available < 50 else '#27AE60'};'>"
                f"{available} slots remaining</span>"
            )
        except Exception as e:
            print(f"Error updating limits: {e}")
            self.view.limits_text.setText("<b>Enrollment Status:</b> Unable to load data")

    def enroll_student(self):
        """
        Handle student enrollment with ALL required fields
        """
        try:
            # 1. GET DATA FROM VIEW
            lrn = self.view.lrn_input.text().strip()
            first_name = self.view.fname_input.text().strip()
            middle_name = self.view.mname_input.text().strip()
            last_name = self.view.lname_input.text().strip()
            gender = self.view.gender_combo.currentText()
            date_of_birth = self.view.dob_input.date().toString("yyyy-MM-dd")
            address = self.view.address_input.text().strip()
            contact = self.view.contact_input.text().strip()
            email = self.view.email_input.text().strip()
            guardian_name = self.view.guardian_name_input.text().strip()
            guardian_contact = self.view.guardian_contact_input.text().strip()
            last_school = self.view.last_school_input.text().strip()
            strand = self.view.strand_combo.currentText()
            grade_level = self.view.grade_combo.currentText()
            payment_mode = self.view.payment_combo.currentText()

            # Build full name
            if middle_name:
                full_name = f"{first_name} {middle_name} {last_name}"
            else:
                full_name = f"{first_name} {last_name}"

            # 2. CREATE MODEL OBJECT with ALL fields
            student_data = StudentData(
                lrn=lrn,
                full_name=full_name,
                first_name=first_name,
                last_name=last_name,
                email=email if email else f"{lrn}@student.edu",
                contact_number=contact if contact else "N/A",
                gender=gender,
                date_of_birth=date_of_birth,
                address=address if address else "N/A",
                guardian_name=guardian_name if guardian_name else None,
                guardian_contact=guardian_contact if guardian_contact else None,
                strand=strand,
                track='Academic' if strand in ['STEM', 'ABM', 'HUMSS', 'GAS'] else 'TVL',
                payment_status=payment_mode,
                payment_mode=payment_mode
            )

            # 3. VALIDATE USING MODEL METHOD
            if not student_data.is_valid():
                self._show_validation_errors(student_data)
                return

            # Additional validation
            if not address:
                QMessageBox.warning(
                    self.view,
                    "Validation Error",
                    "<b>Address is required</b><br><br>• Please enter the student's complete address"
                )
                return

            if not contact or len(contact) != 11:
                QMessageBox.warning(
                    self.view,
                    "Validation Error",
                    "<b>Invalid contact number</b><br><br>• Contact number must be exactly 11 digits<br>• Format: 09XXXXXXXXX"
                )
                return

            # 4. BUSINESS LOGIC: Find available section
            section = self.db.sections.find_available_section(strand)

            if not section:
                QMessageBox.warning(
                    self.view,
                    "No Available Section",
                    f"Sorry, there are no available sections for {strand} strand.\n\n"
                    "All sections are full or no sections have been created."
                )
                return

            # Assign section to student
            student_data.section_id = section.id
            student_data.section_name = section.section_name

            # 5. SAVE USING MODEL
            success, message = self.db.students.add_student(student_data)

            # 6. UPDATE VIEW WITH RESULT
            if success:
                # Success - show confirmation
                QMessageBox.information(
                    self.view,
                    "✅ Enrollment Successful",
                    f"<b>Student enrolled successfully!</b><br><br>"
                    f"<b>Name:</b> {student_data.full_name}<br>"
                    f"<b>LRN:</b> {lrn}<br>"
                    f"<b>Gender:</b> {gender}<br>"
                    f"<b>Grade Level:</b> {grade_level}<br>"
                    f"<b>Strand:</b> {strand}<br>"
                    f"<b>Section:</b> {section.section_name}<br>"
                    f"<b>Room:</b> {section.room_number or 'TBA'}<br>"
                    f"<b>Available Slots:</b> {section.available_slots - 1}/{section.capacity}"
                )

                # Store for printing
                self.last_enrolled_student = student_data

                # Emit signal
                self.student_enrolled.emit()

                # Update limits
                self.update_limits_display()

                # Clear form
                self.clear_form()

                # Enable print button
                self.view.print_btn.setEnabled(True)
            else:
                # Error
                QMessageBox.critical(
                    self.view,
                    "Enrollment Failed",
                    f"<b>Unable to enroll student:</b><br><br>{message}"
                )

        except Exception as e:
            print(f"Error during enrollment: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.view,
                "System Error",
                f"An unexpected error occurred:\n\n{str(e)}"
            )

    def _show_validation_errors(self, student: StudentData):
        """Show specific validation errors"""
        errors = []

        if not student.lrn or len(student.lrn) != 12:
            errors.append("• LRN must be exactly 12 digits")

        if not student.first_name:
            errors.append("• First name is required")

        if not student.last_name:
            errors.append("• Last name is required")

        if not student.email or '@' not in student.email:
            errors.append("• Valid email address is required")

        if not student.strand:
            errors.append("• Please select a strand")

        QMessageBox.warning(
            self.view,
            "Validation Error",
            "<b>Please fix the following errors:</b><br><br>" + "<br>".join(errors)
        )

    def clear_form(self):
        """Clear all form fields"""
        self.view.lrn_input.clear()
        self.view.fname_input.clear()
        self.view.mname_input.clear()
        self.view.lname_input.clear()
        self.view.gender_combo.setCurrentIndex(0)
        from PyQt6.QtCore import QDate
        self.view.dob_input.setDate(QDate.currentDate().addYears(-16))
        self.view.address_input.clear()
        self.view.contact_input.clear()
        self.view.email_input.clear()
        self.view.guardian_name_input.clear()
        self.view.guardian_contact_input.clear()
        self.view.last_school_input.clear()
        self.view.strand_combo.setCurrentIndex(0)
        self.view.grade_combo.setCurrentIndex(0)
        self.view.payment_combo.setCurrentIndex(0)
        self.view.lrn_input.setFocus()
        self.view.print_btn.setEnabled(False)

    def print_registration_form(self):
        """Generate PDF registration form"""
        if not self.last_enrolled_student:
            QMessageBox.warning(
                self.view,
                "No Data",
                "No enrollment data available to print."
            )
            return

        try:
            # Generate filename
            lrn = self.last_enrolled_student.lrn
            filename = f"Registration_{lrn}.pdf"

            # Create PDF
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []

            # Title
            title_style = styles['Title']
            title_style.textColor = colors.HexColor('#2C3E50')
            story.append(Paragraph("STUDENT ENROLLMENT FORM", title_style))
            story.append(Spacer(1, 12))

            # School info
            subtitle_style = styles['Normal']
            subtitle_style.alignment = 1  # Center
            story.append(Paragraph("SmartEnroll System", subtitle_style))
            story.append(Paragraph("Student Enrollment Management", subtitle_style))
            story.append(Spacer(1, 20))

            # Student information table
            data = [
                ['Field', 'Information'],
                ['LRN', self.last_enrolled_student.lrn],
                ['Full Name', self.last_enrolled_student.full_name],
                ['Gender', self.last_enrolled_student.gender],
                ['Date of Birth', str(self.last_enrolled_student.date_of_birth)],
                ['Address', self.last_enrolled_student.address],
                ['Contact Number', self.last_enrolled_student.contact_number],
                ['Email Address', self.last_enrolled_student.email],
                ['Guardian Name', self.last_enrolled_student.guardian_name or 'N/A'],
                ['Guardian Contact', self.last_enrolled_student.guardian_contact or 'N/A'],
                ['Strand', self.last_enrolled_student.strand],
                ['Section', self.last_enrolled_student.section_name or 'TBA'],
                ['Payment Mode', self.last_enrolled_student.payment_mode],
            ]

            # Create table
            table = Table(data, colWidths=[150, 350])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#365486')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ]))

            story.append(table)
            story.append(Spacer(1, 30))

            # Footer
            story.append(Paragraph("This is an official enrollment document.", styles['Normal']))
            story.append(Spacer(1, 10))

            from datetime import datetime
            date_str = datetime.now().strftime("%B %d, %Y at %I:%M:%S %p")
            story.append(Paragraph(f"Generated on: {date_str}", styles['Normal']))

            # Build PDF
            doc.build(story)

            # Success message
            QMessageBox.information(
                self.view,
                "✅ PDF Generated",
                f"Registration form saved successfully!\n\nFile: {filename}"
            )

            # Try to open the PDF
            if os.name == 'nt':  # Windows
                os.startfile(filename)
            elif os.name == 'posix':  # macOS/Linux
                import subprocess
                subprocess.call(('open' if os.uname().sysname == 'Darwin' else 'xdg-open', filename))

        except Exception as e:
            print(f"Error printing registration: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self.view,
                "Print Error",
                f"Failed to generate PDF:\n\n{str(e)}"
            )