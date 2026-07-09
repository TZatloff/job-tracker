import psycopg2.errors
from fastapi import APIRouter, HTTPException, status
from database import get_connection
from schemas import CompanyCreate, CompanyOut

router = APIRouter(
    prefix="/api/v1/companies",
    tags=["Companies"]
)


@router.post("", status_code=201)
def create_company(company: CompanyCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""INSERT INTO public.companies(name, website)
                            VALUES (%s, %s)
                            RETURNING id, name, website, created_at; 
                             """, (company.name, company.website)
                            )
                row = cur.fetchone()
            except psycopg2.errors.UniqueViolation:
                conn.rollback()
                raise HTTPException(status_code=409,
                                    detail="Company already exists")
            conn.commit()
            return {
                "id": row[0],
                "name": row[1],
                "website": row[2],
                "created_at": row[3]
            }


@router.get("")
def list_companies():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, website, created_at FROM public.companies ORDER BY created_at DESC;")
            rows = cur.fetchall()
            return [
                {
                    "id": row[0],
                    "name": row[1],
                    "website": row[2],
                    "created_at": row[3]
                }
                for row in rows
            ]
