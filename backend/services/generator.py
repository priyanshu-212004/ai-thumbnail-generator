import asyncio
import logging

from sqlmodel import Session, select

from database import engine
from models import Job, Thumbnail
from services.huggingface_service import generate_thumbnail
from services.imagekit_service import upload_file

logger = logging.getLogger(__name__)

STYLE_ORDER = [
    "bold_dramatic",
    "clean_minimal",
    "vibrant_energetic",
]
STYLES = {
    "bold_dramatic": (
        "Create a bold, dramatic YouTube thumbnail with high contrast, "
        "cinematic lighting, dark moody background, and powerful composition. "
        "The person's face should be prominent with a dramatic expression."
    ),
    "clean_minimal": (
        "Create a clean, minimal YouTube thumbnail with bright lighting, "
        "light background, modern professional aesthetic, and sharp composition. "
        "The person should look approachable and professional."
    ),
    "vibrant_energetic": (
        "Create a vibrant, energetic YouTube thumbnail with colorful gradients, "
        "dynamic angles, and eye-catching composition. The person should look excited."
    ),
}

DEFAULT_STYLE = STYLES["bold_dramatic"]


# ---------------------------
# SINGLE THUMBNAIL GENERATION
# ---------------------------
async def generate_single_thumbnail(thumbnail: Thumbnail, prompt: str, headshot_url: str):
    thumbnail_id = thumbnail.id
    job_id = thumbnail.job_id
    style_name = thumbnail.style_name

    style_prompt = STYLES.get(style_name, DEFAULT_STYLE)

    # STEP 1: Mark generating
    with Session(engine) as session:
        db_thumb = session.get(Thumbnail, thumbnail_id)
        if not db_thumb:
            logger.error(f"Thumbnail {thumbnail_id} not found")
            return

        db_thumb.status = "generating"
        session.add(db_thumb)
        session.commit()

    try:
        # STEP 2: Generate image
        image_bytes = await generate_thumbnail(
            prompt,
            style_prompt,
            headshot_url,
        )

        # STEP 3: Upload to ImageKit
        file_name = f"{thumbnail_id}.png"
        folder = f"thumbnails/{job_id}/"

        url = upload_file(
            file_bytes=image_bytes,
            file_name=file_name,
            folder=folder,
        )

        # STEP 4: Save success
        with Session(engine) as session:
            db_thumb = session.get(Thumbnail, thumbnail_id)
            if not db_thumb:
                return

            db_thumb.imagekit_url = url
            db_thumb.status = "uploaded"

            session.add(db_thumb)
            session.commit()

        logger.info(
            f"Thumbnail {thumbnail_id} uploaded successfully for job {job_id}"
        )

    except Exception as e:
        logger.exception(f"Thumbnail {thumbnail_id} failed")

        with Session(engine) as session:
            db_thumb = session.get(Thumbnail, thumbnail_id)
            if db_thumb:
                db_thumb.status = "failed"
                db_thumb.error_message = str(e)[:500]

                session.add(db_thumb)
                session.commit()


# ---------------------------
# JOB PROCESSING
# ---------------------------
async def process_job(job_id: str):
    with Session(engine) as session:
        job = session.get(Job, job_id)

        if not job:
            raise ValueError(f"Job {job_id} not found")

        job.status = "processing"
        session.add(job)
        session.commit()

        prompt = job.prompt
        headshot_url = job.headshot_url

        thumbnails = session.exec(
            select(Thumbnail).where(Thumbnail.job_id == job_id)
        ).all()

    if not thumbnails:
        logger.error(f"No thumbnails found for job {job_id}")
        return

    # Run all thumbnails in parallel
    tasks = [
        generate_single_thumbnail(t, prompt, headshot_url)
        for t in thumbnails
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Log exceptions (important fix)
    for r in results:
        if isinstance(r, Exception):
            logger.error(f"Task error: {r}")

    # ---------------------------
    # FINAL JOB STATUS UPDATE
    # ---------------------------
    with Session(engine) as session:
        thumbnails = session.exec(
            select(Thumbnail).where(Thumbnail.job_id == job_id)
        ).all()

        success_count = sum(
            1 for t in thumbnails if t.status == "uploaded"
        )
        fail_count = sum(
            1 for t in thumbnails if t.status == "failed"
        )

        job = session.get(Job, job_id)
        if not job:
            raise ValueError(f"Job {job_id} not found")

        if success_count == len(thumbnails):
            job.status = "completed"
        elif success_count > 0:
            job.status = "partial_success"
        else:
            job.status = "failed"

        session.add(job)
        session.commit()

    logger.info(
        f"Job {job_id} finished | success={success_count} fail={fail_count}"
    )