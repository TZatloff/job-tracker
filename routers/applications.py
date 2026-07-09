import psycopg2
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from fastapi import Depends

from auth import verify_token
from database import get_connection
from schemas import ApplicationCreate, StatusUpdate
from services.audit import record_status_change

router = APIRouter(
    prefix="/api/v1/applications",
    tags=["Applications"]
)


@router.post("", status_code=201)
def create_application(app_in: ApplicationCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    """ INSERT INTO public.applications(company_id, position, notes)
                        VALUES (%s, %s, %s)
                        RETURNING id, company_id, position, status, applied_date, notes;
                     """, (app_in.company_id, app_in.position, app_in.notes)
                )
                row = cur.fetchone()
            except psycopg2.errors.ForeignKeyViolation:
                conn.rollback()
                raise HTTPException(status_code=404,
                                    detail="Company not found")
            conn.commit()
    return {
        "id": row[0],
        "company_id": row[1],
        "position": row[2],
        "status": row[3],
        "applied_date": row[4],
        "notes": row[5]
    }


@router.get("")
def list_applications():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
             SELECT a.id, a.company_id, a.position, a.status, a.applied_date, a.notes
              FROM applications a
               JOIN companies c ON a.company_id = c.id 
                ORDER BY a.applied_date DESC;
                """)
            rows = cur.fetchall()
            return [
                {
                    "id": row[0],
                    "company_id": row[1],
                    "position": row[2],
                    "status": row[3],
                    "applied_date": row[4],
                    "notes": row[5]
                }
                for row in rows
            ]


@router.patch("/{app_id}/status", dependencies=[Depends(verify_token)])
def update_status(app_id: int, upd: StatusUpdate, background_tasks: BackgroundTasks):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """ SELECT status FROM public.applications WHERE id = %s; """, (app_id,)
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Application not found")
            old_status = row[0]

            cur.execute(
                """ UPDATE public.applications
                    SET status = %s
                    WHERE id = %s
                    RETURNING id;
                 """, (upd.status, app_id)
            )
        conn.commit()

    background_tasks.add_task(record_status_change, app_id, old_status, upd.status)

    return {
        "id": app_id,
        "old_status": old_status,
        "new_status": upd.status
    }
