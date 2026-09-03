import json
import os
import re
import sys
import requests

def sanitize_filename(name):
    """Remove spaces and all special characters from the name."""
    return re.sub(r"[^a-zA-Z0-9]", "", name)


def download_images(json_file, OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(json_file, "r", encoding="utf-8") as f:
        items = json.load(f)

    for item in items:
        name = item.get("name")
        image_url = item.get("image")

        if not name or not image_url:
            print(f"Skipping invalid item: {item}")
            continue

        filename = sanitize_filename(name)

        if not filename:
            print(f"Skipping '{name}': invalid filename")
            continue

        # Try to preserve the image extension from the URL
        extension = os.path.splitext(image_url.split("?")[0])[1]
        if not extension:
            extension = ".jpg"

        output_path = os.path.join(OUTPUT_DIR, filename + extension)

        # Skip download if the file already exists
        if os.path.isfile(output_path):
            print(f"Already exists, skipping: {output_path}")
            continue

        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                f.write(response.content)

            print(f"Downloaded: {name} -> {output_path}")

        except requests.RequestException as e:
            print(f"Failed to download '{name}': {e}")


if __name__ == "__main__":
    for mediaType in ["books", "movies"]:
        print(f"Processing {mediaType}")
        print(os.path.join(os.getcwd(), mediaType+".json"))
        print(os.path.join(os.getcwd(), "media", mediaType))
        download_images(os.path.join(os.getcwd(), mediaType+".json"),os.path.join(os.getcwd(), "media", mediaType))