from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import RequestValidationError
from api.config import get_settings, SupabaseManager
from api.routers import mortgage_deeds
from api.routers import housing_cooperative
from api.routers import signing
from api.routers import statistics
from api.routers import audit_logs
from fastapi.responses import JSONResponse
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Set logging levels for specific loggers
logging.getLogger("uvicorn").setLevel(logging.INFO)
logging.getLogger("fastapi").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

# Define API tags metadata
tags_metadata = [
    {
        "name": "mortgage-deeds",
        "description": "Operations with mortgage deeds including creation, updates, deletion, and retrieval.",
    },
    {
        "name": "housing-cooperatives",
        "description": "Endpoints for managing housing cooperative information and details.",
    },
    {
        "name": "signing",
        "description": "Manage the signing workflow for mortgage deeds including status transitions and notifications.",
    },
    {
        "name": "statistics",
        "description": "Analytics and statistical information about mortgage deeds and system usage.",
    },
    {
        "name": "audit-logs",
        "description": "Access and manage audit logs for tracking all system actions and changes.",
    },
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up FastAPI application...")
    settings = get_settings()
    print("kjhkjhkjhjk", settings.BACKEND_CORS_ORIGINS)
    print(f"Loaded settings - Supabase URL: {settings.SUPABASE_URL}")
    print(f"Supabase key type: {'service_role' if len(settings.SUPABASE_KEY) > 100 else 'anon'}")
    await SupabaseManager.get_client()  # Initialize the client
    yield
    # Shutdown
    await SupabaseManager.cleanup()

app = FastAPI(
    title="Mortgage Deed Management API",
    description="""
    The Mortgage Deed Management API provides a comprehensive solution for managing digital mortgage deeds.
    
    ## Key Features
    
    * **Mortgage Deed Management**: Create, read, update, and delete mortgage deeds
    * **Housing Cooperative Integration**: Fetch and manage housing cooperative details
    * **Digital Signing Workflow**: Manage the complete signing process with status tracking
    * **Analytics**: Access statistical data about mortgage deeds and system usage
    
    ## Authentication
    
    This API uses Supabase Auth for authentication. Include your JWT token in the Authorization header:
    
    `Authorization: Bearer your-jwt-token`
    """,
    lifespan=lifespan
)

# Get settings for CORS configuration
settings = get_settings()
# Add CORS middleware BEFORE including routers!
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://test-frontend-production-61e5.up.railway.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Now include routers
app.include_router(mortgage_deeds.router, prefix="/api/mortgage-deeds", tags=["mortgage-deeds"])
app.include_router(housing_cooperative.router, prefix="/api/housing-cooperatives", tags=["housing-cooperatives"])
app.include_router(signing.router, prefix="/api/mortgage-deeds", tags=["signing"])
app.include_router(statistics.router, prefix="/api/statistics", tags=["statistics"])
app.include_router(audit_logs.router, prefix="/api", tags=["audit-logs"])