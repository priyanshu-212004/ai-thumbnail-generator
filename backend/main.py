import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import create_tables
from routes import router


# -----------------------
# LOGGING SETUP
# -----------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


# -----------------------
# LIFESPAN EVENT
# -----------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application... Creating tables if not exist.")
    create_tables()
    logger.info("Database ready.")
    yield
    logger.info("Shutting down application...")


# -----------------------
# FASTAPI APP
# -----------------------
app = FastAPI(
    title="YouTube Thumbnail Generator API",
    lifespan=lifespan,
)

# -----------------------
# CORS CONFIG
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------
# ROUTES
# -----------------------
app.include_router(router)