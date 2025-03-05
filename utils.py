DEBUG = False


RAW_PREFIX = "target/raw/"
EXTRACTED_PREFIX = "target/extracted/"
CRAWLED_PREFIX = "target/crawled/"
MAX_TO_CRAWL = 10
MAX_TO_DOWNLOAD_PER_PAGE = 10
MAX_TO_MAP = 1000
N_ROUNDS = 5
N_START = 10



import requests
import os

base_url = "https://en.wikipedia.org/wiki/"

def debug_print(s):
    if DEBUG:
        print(s)



def download_page(url):
    if url in os.listdir(RAW_PREFIX) or url in os.listdir(EXTRACTED_PREFIX) or url in os.listdir(CRAWLED_PREFIX):
        debug_print(f"[+] The page {url} was already downloaded")
        return
    r = requests.get(f"{base_url}{url}")
    debug_print(r.url)
    if r.status_code != 200:
        debug_print(f"[!] There was a problem recovering {url} (at {r.url}), status code was {r.status_code}")
        return
    with open(f"target/raw/{r.url.split('/')[-1]}", "wb") as f:
        f.write(r.content)