import os

def upload_file(
    file_bytes: bytes,
    file_name: str,
    folder: str,
    content_type: str = "image/png"
) -> str:

    save_dir = os.path.join("generated", folder)
    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, file_name)

    with open(file_path, "wb") as f:
        f.write(file_bytes)

    return file_path


def get_variants(base_url: str) -> dict:
    return {
        "youtube": base_url,
        "shorts": base_url,
        "square": base_url,
    }