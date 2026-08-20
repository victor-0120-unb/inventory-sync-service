import os
import mysql.connector
from mysql.connector import Error


def get_connection():
    """
    Create a connection to the Solstice Events MySQL database.
    """

    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "Vack0120."),
        database=os.getenv("DB_NAME", "solstice_checkin")
    )


def get_attendee_by_qr(qr_code):
    """
    Find an attendee using their QR code.
    """

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT attendee_id, qr_code, full_name, status, checked_in_at
        FROM attendees
        WHERE qr_code = %s
        """,
        (qr_code,)
    )

    attendee = cursor.fetchone()

    cursor.close()
    connection.close()

    return attendee


def create_print_job(job_id, attendee_id):
    """
    Create one pending print job for an attendee.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO print_jobs
            (job_id, attendee_id, status)
            VALUES (%s, %s, 'PENDING')
            """,
            (job_id, attendee_id)
        )

        connection.commit()

        return True

    except Error:
        connection.rollback()
        return False

    finally:
        cursor.close()
        connection.close()


def complete_print_job(job_id):
    """
    Mark a print job as completed and check the attendee in.

    The job must still be pending. This prevents a duplicate
    webhook from changing the same job more than once.
    """

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        connection.start_transaction()

        cursor.execute(
            """
            SELECT attendee_id, status
            FROM print_jobs
            WHERE job_id = %s
            FOR UPDATE
            """,
            (job_id,)
        )

        job = cursor.fetchone()

        if job is None:
            connection.rollback()
            return {
                "success": False,
                "message": "Print job not found"
            }

        # Ignore duplicate webhook confirmations.
        if job["status"] == "COMPLETED":
            connection.rollback()
            return {
                "success": True,
                "message": "Print job was already completed"
            }

        cursor.execute(
            """
            UPDATE print_jobs
            SET status = 'COMPLETED',
                completed_at = CURRENT_TIMESTAMP
            WHERE job_id = %s
            """,
            (job_id,)
        )

        cursor.execute(
            """
            UPDATE attendees
            SET status = 'CHECKED_IN',
                checked_in_at = CURRENT_TIMESTAMP
            WHERE attendee_id = %s
              AND status = 'PENDING'
            """,
            (job["attendee_id"],)
        )

        connection.commit()

        return {
            "success": True,
            "message": "Print job completed and attendee checked in"
        }

    except Error as error:
        connection.rollback()

        return {
            "success": False,
            "message": str(error)
        }

    finally:
        cursor.close()
        connection.close()