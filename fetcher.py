import os, requests
from config import PROXY_URL, HTML_SAVE_PATH
from utils import get_useragent

def fetch_page(input_url, idd, collection):
    headers = {
        "User-Agent": get_useragent(),
        "accept": "text/html,application/xhtml+xml",
    }
    proxies = {"http": PROXY_URL, "https": PROXY_URL}

    html_file_path = os.path.join(HTML_SAVE_PATH, f"{idd}.html")
    os.makedirs(HTML_SAVE_PATH, exist_ok=True)

    if os.path.exists(html_file_path):
        with open(html_file_path, "r", encoding="utf-8") as f:
            return f.read(), html_file_path

    resp = requests.get(input_url, headers=headers, proxies=proxies, verify=False)
    if resp.status_code == 200:
        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(resp.text)
        collection.update_one({"url_id": idd}, {"$set": {"status": "page_saved"}})
        return resp.text, html_file_path
    else:
        collection.update_one({"url_id": idd}, {"$set": {"status": f"error_{resp.status_code}"}})
        return None, None
