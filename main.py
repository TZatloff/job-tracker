from fastapi import FastAPI
from routers import companies, applications, admin
import auth
import time
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Job Tracker API")

app.include_router(companies.router)
app.include_router(applications.router)
app.include_router(admin.router)
app.include_router(auth.router)

@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}


@app.middleware("http")
async def log_and_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.method} {request.url} completed in {process_time:.2f} seconds")
    return response


origins = [
    "http://localhost:3000",
    "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
