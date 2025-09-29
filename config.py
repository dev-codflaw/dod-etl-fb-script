import os
from urllib.parse import quote_plus

# === MongoDB ===
USERNAME = os.getenv("MONGO_USER", "your_username")
PASSWORD = quote_plus(os.getenv("MONGO_PASS", "your_password"))
CLUSTER  = os.getenv("MONGO_CLUSTER", "cluster1.c4idkzi.mongodb.net")
DB_NAME  = os.getenv("MONGO_DB", "test")


MONGO_URI = f"mongodb+srv://{USERNAME}:{PASSWORD}@{CLUSTER}/"


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
