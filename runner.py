from threading import Thread
from db import collection
from fetcher import fetch_page
from parser import parse_html
from saver import save_record

def worker(skip, limit):
    batch = collection.find({"status": "pending"}).skip(skip).limit(limit)
    for doc in batch:
        input_url = doc["url"]
        idd = doc["url_id"]

        html, html_path = fetch_page(input_url, idd, collection)
        if html:
            record = parse_html(html, idd, input_url, html_path)
            save_record(record, idd)

def run_scraper(total_threads=15, max_runs=10):
    run_count = 0
    while collection.count_documents({"status": "pending"}) > 0 and run_count < max_runs:
        total = collection.count_documents({"status": "pending"})
        batch_size = max(total // total_threads, 1)

        threads = [Thread(target=worker, args=(i, batch_size)) for i in range(0, total, batch_size)]
        [t.start() for t in threads]
        [t.join() for t in threads]

        run_count += 1
