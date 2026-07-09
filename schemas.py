from pydantic import BaseModel
from typing import Literal


class CompanyCreate(BaseModel):
    name: str
    website: str | None = None


class CompanyOut(BaseModel):
    id: int
    name: str
    website: str | None


class ApplicationCreate(BaseModel):
    company_id: int
    position: str
    notes: str | None = None


class StatusUpdate(BaseModel):
    status: Literal["applied", "screening", "interview", "offer", "rejected"]
