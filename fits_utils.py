
import requests
from io import BytesIO
from astropy.io import fits

REPOSITORY = "FrancescoZ04/FITS"
FOLDER = "FITS"
BRANCH = "main"

API_URL = (
    f"https://api.github.com/repos/{REPOSITORY}"
    f"/contents/{FOLDER}?ref={BRANCH}"
)


def get_fits_files(session):
    response = session.get(API_URL, timeout=30)
    response.raise_for_status()

    return sorted(
        [
            item for item in response.json()
            if item["type"] == "file"
            and item["name"].lower().endswith((".fits", ".fts"))
        ],
        key=lambda item: item["name"]
    )


def open_fits_file(session, url):
    response = session.get(url, timeout=60)
    response.raise_for_status()

    return fits.open(BytesIO(response.content))
