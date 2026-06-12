import os
from dotenv import load_dotenv

load_dotenv()


# -----------------------
# HUGGING FACE (ONLY AI YOU USE)
# -----------------------
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")


if not HUGGINGFACE_API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY is missing in environment variables")


# -----------------------
# IMAGEKIT
# -----------------------
IMAGEKIT_PRIVATE_KEY = os.getenv("IMAGEKIT_PRIVATE_KEY")
IMAGEKIT_PUBLIC_KEY = os.getenv("IMAGEKIT_PUBLIC_KEY")
IMAGEKIT_URL_ENDPOINT = os.getenv("IMAGEKIT_URL_ENDPOINT")

# if not IMAGEKIT_PRIVATE_KEY:
#     raise ValueError("IMAGEKIT_PRIVATE_KEY is missing")

# if not IMAGEKIT_PUBLIC_KEY:
#     raise ValueError("IMAGEKIT_PUBLIC_KEY is missing")

# if not IMAGEKIT_URL_ENDPOINT:
#     raise ValueError("IMAGEKIT_URL_ENDPOINT is missing")


# -----------------------
# DATABASE
# -----------------------
DATABASE_URL = "sqlite:///./thumbnailbuilder.db"