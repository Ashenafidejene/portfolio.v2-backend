from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import routers
from src.config.firebase import init_firebase
from src.utils.logger import logger
from src.core.rate_limiter import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from src.config.setting import settings

# Initialize Firebase
init_firebase()

# Create FastAPI app
app = FastAPI(
    title="AI Portfolio Backend",
    description="Backend for AI-powered developer portfolio",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add exception handlers
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include all routers
for router in routers:
    app.include_router(router)

# Apply rate limiting middleware
app.state.limiter = limiter

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down")

@app.get("/health", include_in_schema=False)
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
