import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()


from backend.infrastructure.logging.logging_middleware import log_requests
from backend.infrastructure.api.routes import api_router

app = FastAPI(title="Crew Rostering Backend", version="0.1.0")
app.middleware("http")(log_requests)

# Allow CORS for local frontend dev
origins = [
    "http://localhost:5173",  # Vite default
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

# Import and include API routers
app.include_router(api_router)
