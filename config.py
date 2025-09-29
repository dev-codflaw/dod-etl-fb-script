import os
from urllib.parse import quote_plus

# === MongoDB ===

DB_NAME  = os.getenv("MONGO_DB", "test")


DB_NAME = os.getenv("MONGO_DB", "test")

def _build_uri_from_credentials() -> str:
    """Fallback connection string derived from discrete credentials."""

    username = os.getenv("MONGO_USER", "your_username")
    password = quote_plus(os.getenv("MONGO_PASS", "your_password"))
    cluster = os.getenv("MONGO_CLUSTER", "cluster1.c4idkzi.mongodb.net")

    return f"mongodb+srv://{username}:{quote_plus(password)}@cluster1.c4idkzi.mongodb.net/"


MONGO_URI = os.getenv("MONGO_URI") or _build_uri_from_credentials()


INPUT_COLLECTION  = "batch_aa"
OUTPUT_COLLECTION = "output_batch_aa"

# === Paths ===
HTML_SAVE_PATH = os.getenv("HTML_PATH", "./Facebook_pages/output_batch_aa/")

# === Proxy ===
SCRAPEDO_TOKEN = os.getenv("SCRAPEDO_TOKEN", "")
PROXY_URL = f"http://{SCRAPEDO_TOKEN}:geoCode=us@proxy.scrape.do:8080"

# === Concurrency ===
THREADS = 15
MAX_RUNS = 10
