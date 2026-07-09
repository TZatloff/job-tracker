from database import get_connection

def record_status_change(application_id: int, old_status: str, new_status: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """ INSERT INTO audit_log (application_id, action, old_status, new_status)
                    VALUES (%s, 'status_change', %s, %s);
                 """,
                (application_id, old_status, new_status)
            )
            conn.commit()
