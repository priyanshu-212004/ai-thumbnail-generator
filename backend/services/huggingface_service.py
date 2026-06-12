import requests
from urllib.parse import quote


async def generate_thumbnail(
    prompt: str,
    style_prompt: str,
    headshot_url: str = None,
) -> bytes:

    full_prompt = f"{prompt}. {style_prompt}"

    url = (
        "https://image.pollinations.ai/prompt/"
        + quote(full_prompt)
    )

    response = requests.get(url, timeout=120)

    if response.status_code != 200:
        raise Exception(
            f"Pollinations Error: {response.text}"
        )

    return response.content