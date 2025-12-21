"""
Payment Model - Handles payment transactions and tracking
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple
from datetime import datetime, date
from decimal import Decimal


@dataclass
class PaymentData:
    """Payment transaction data blueprint"""
    id: Optional[int] = None
    student_id: int = 0
    amount: Decimal = Decimal('0.00')
    payment_date: Optional[date] = None
    payment_method: str = "Cash"
    reference_number: Optional[str] = None
    receipt_number: Optional[str] = None
    academic_year_id: Optional[int] = None
    payment_type: str = "Tuition"
    notes: Optional[str] = None
    recorded_by: Optional[int] = None
    created_at: Optional[datetime] = None

    def is_valid(self) -> bool:
        """Validate payment data"""
        return bool(
            self.student_id and
            self.amount > 0 and
            self.payment_date
        )


class Payment:
    """Payment model - Database operations for payment transactions"""

    def __init__(self, db):
        self.db = db

    def add_payment(self, payment_data: PaymentData, user_id: int) -> Tuple[bool, str, Optional[int]]:
        """Add a new payment transaction"""
        try:
            if not payment_data.is_valid():
                return False, "Invalid payment data", None

            cursor = self.db.cursor()

            # Generate receipt number
            cursor.execute("SELECT COUNT(*) FROM payment_transactions")
            count = cursor.fetchone()[0]
            receipt_number = payment_data.receipt_number or f"REC-{datetime.now().strftime('%Y%m%d')}-{count + 1:04d}"

            # Insert payment
            query = """
                    INSERT INTO payment_transactions
                    (student_id, amount, payment_date, payment_method, reference_number,
                     receipt_number, academic_year_id, payment_type, notes, recorded_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
                    """
            values = (
                payment_data.student_id,
                float(payment_data.amount),
                payment_data.payment_date,
                payment_data.payment_method,
                payment_data.reference_number,
                receipt_number,
                payment_data.academic_year_id,
                payment_data.payment_type,
                payment_data.notes,
                user_id
            )
            cursor.execute(query, values)
            payment_id = cursor.lastrowid

            # Update student's payment totals
            cursor.execute("""
                           UPDATE students
                           SET amount_paid = amount_paid + %s,
                               balance     = total_fees - (amount_paid + %s)
                           WHERE id = %s
                           """, (float(payment_data.amount), float(payment_data.amount), payment_data.student_id))

            # Update payment status
            cursor.execute("""
                           SELECT total_fees, amount_paid + %s as new_paid
                           FROM students
                           WHERE id = %s
                           """, (float(payment_data.amount), payment_data.student_id))
            result = cursor.fetchone()

            if result:
                total_fees = result[0]
                new_paid = result[1]

                if new_paid >= total_fees:
                    new_status = 'Paid'
                elif new_paid > 0:
                    new_status = 'Partial'
                else:
                    new_status = 'Pending'

                cursor.execute("UPDATE students SET payment_status = %s WHERE id = %s",
                               (new_status, payment_data.student_id))

            self.db.commit()
            cursor.close()

            return True, f"Payment recorded successfully. Receipt: {receipt_number}", payment_id

        except Exception as e:
            print(f"Error adding payment: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Failed to record payment: {str(e)}", None

    def get_student_payments(self, student_id: int) -> List[dict]:
        """Get all payments for a student"""
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                    SELECT p.*, u.username as recorded_by_name, ay.year_name
                    FROM payment_transactions p
                             LEFT JOIN users u ON p.recorded_by = u.id
                             LEFT JOIN academic_years ay ON p.academic_year_id = ay.id
                    WHERE p.student_id = %s
                    ORDER BY p.payment_date DESC, p.created_at DESC \
                    """
            cursor.execute(query, (student_id,))
            payments = cursor.fetchall()
            cursor.close()
            return payments
        except Exception as e:
            print(f"Error getting student payments: {e}")
            return []

    def get_payment_summary(self, student_id: int) -> dict:
        """Get payment summary for a student"""
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                           SELECT total_fees,
                                  amount_paid,
                                  balance,
                                  payment_status
                           FROM students
                           WHERE id = %s
                           """, (student_id,))
            summary = cursor.fetchone()
            cursor.close()
            return summary or {
                'total_fees': 0,
                'amount_paid': 0,
                'balance': 0,
                'payment_status': 'Pending'
            }
        except Exception as e:
            print(f"Error getting payment summary: {e}")
            return {}

    def get_all_payments(self, date_from: date = None, date_to: date = None,
                         payment_status: str = None) -> List[dict]:
        """Get all payments with optional filters"""
        try:
            cursor = self.db.cursor(dictionary=True)

            query = """
                    SELECT p.*, s.full_name as student_name, s.strand, u.username as recorded_by_name
                    FROM payment_transactions p
                             INNER JOIN students s ON p.student_id = s.id
                             LEFT JOIN users u ON p.recorded_by = u.id
                    WHERE 1 = 1 \
                    """
            params = []

            if date_from:
                query += " AND p.payment_date >= %s"
                params.append(date_from)

            if date_to:
                query += " AND p.payment_date <= %s"
                params.append(date_to)

            if payment_status:
                query += " AND s.payment_status = %s"
                params.append(payment_status)

            query += " ORDER BY p.payment_date DESC, p.created_at DESC LIMIT 100"

            cursor.execute(query, params)
            payments = cursor.fetchall()
            cursor.close()
            return payments

        except Exception as e:
            print(f"Error getting all payments: {e}")
            return []

    def delete_payment(self, payment_id: int) -> Tuple[bool, str]:
        """Delete a payment transaction"""
        try:
            cursor = self.db.cursor()

            # Get payment details first
            cursor.execute("""
                           SELECT student_id, amount
                           FROM payment_transactions
                           WHERE id = %s
                           """, (payment_id,))
            payment = cursor.fetchone()

            if not payment:
                cursor.close()
                return False, "Payment not found"

            student_id, amount = payment

            # Delete payment
            cursor.execute("DELETE FROM payment_transactions WHERE id = %s", (payment_id,))

            # Update student totals
            cursor.execute("""
                           UPDATE students
                           SET amount_paid = amount_paid - %s,
                               balance     = total_fees - (amount_paid - %s)
                           WHERE id = %s
                           """, (float(amount), float(amount), student_id))

            # Update payment status
            cursor.execute("""
                           SELECT total_fees, amount_paid - %s as new_paid
                           FROM students
                           WHERE id = %s
                           """, (float(amount), student_id))
            result = cursor.fetchone()

            if result:
                total_fees = result[0]
                new_paid = result[1]

                if new_paid >= total_fees:
                    new_status = 'Paid'
                elif new_paid > 0:
                    new_status = 'Partial'
                else:
                    new_status = 'Pending'

                cursor.execute("UPDATE students SET payment_status = %s WHERE id = %s",
                               (new_status, student_id))

            self.db.commit()
            cursor.close()

            return True, "Payment deleted successfully"

        except Exception as e:
            print(f"Error deleting payment: {e}")
            return False, f"Failed to delete payment: {str(e)}"

    def get_payment_stats(self, academic_year_id: int = None) -> dict:
        """Get payment statistics"""
        try:
            cursor = self.db.cursor(dictionary=True)

            where_clause = ""
            params = []
            if academic_year_id:
                where_clause = "WHERE academic_year_id = %s"
                params = [academic_year_id]

            # Total collected
            cursor.execute(f"""
                SELECT SUM(amount) as total_collected, COUNT(*) as transaction_count
                FROM payment_transactions
                {where_clause}
            """, params)
            totals = cursor.fetchone()

            # By payment method
            cursor.execute(f"""
                SELECT payment_method, SUM(amount) as amount, COUNT(*) as count
                FROM payment_transactions
                {where_clause}
                GROUP BY payment_method
            """, params)
            by_method = cursor.fetchall()

            cursor.close()

            return {
                'total_collected': float(totals['total_collected'] or 0),
                'transaction_count': totals['transaction_count'],
                'by_method': by_method
            }

        except Exception as e:
            print(f"Error getting payment stats: {e}")
            return {}