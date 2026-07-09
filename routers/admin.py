from fastapi import APIRouter, Depends
from database import get_connection
from auth import verify_token

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["Admin"],
    dependencies=[Depends(verify_token)]
)


@router.get("/stats")
def stats():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """ SELECT status, COUNT(*) FROM applications GROUP BY status;
                 """
            )
            rows = cur.fetchall()
    return {status: count for status, count in rows}


@router.get("/audit")
def audit_log(limit: int = 20):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """ SELECT id, application_id, action, old_status, new_status, created_at
                    FROM audit_log
                    ORDER BY created_at DESC
                    LIMIT %s;
                 """,
                (limit,)

            )

            rows = cur.fetchall()
    return [
        {
            "id": row[0],
            "application_id": row[1],
            "action": row[2],
            "old_status": row[3],
            "new_status": row[4],
            "created_at": row[5]
        }
        for row in rows
    ]
