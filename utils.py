DEBUG = False

BASE_URL = "https://nrm.wikipedia.org/wiki/"
RANDOM_ENDPOINT = "Sp%C3%A9cial:Page_au_hasard"
LANGUAGE = "norman"

RAW_PREFIX = "target/raw/"
EXTRACTED_PREFIX = "target/extracted/"
CRAWLED_PREFIX = "target/crawled/"


MAX_TO_CRAWL = 1
MAX_TO_DOWNLOAD_PER_PAGE = 100000
MAX_TO_MAP = 1000
N_ROUNDS = 10000
N_START = 10

# N_TOTAL_PAGES = 6_962_454 # From https://en.wikipedia.org/wiki/Wikipedia:Size_of_Wikipedia#Annual_growth_rate_for_the_English_Wikipedia
N_TOTAL_PAGES = 5_031 # From https://nrm.wikipedia.org/wiki/Sp%C3%A9cial:Statistiques



import requests
import os



def debug_print(s):
    if DEBUG:
        print(s)



def download_page(url):
    if url in os.listdir(RAW_PREFIX) or url in os.listdir(EXTRACTED_PREFIX) or url in os.listdir(CRAWLED_PREFIX):
        debug_print(f"[+] The page {url} was already downloaded")
        return
    r = requests.get(f"{BASE_URL}{url}")
    debug_print(r.url)
    if r.status_code != 200:
        debug_print(f"[!] There was a problem recovering {url} (at {r.url}), status code was {r.status_code}")
        return
    with open(f"target/raw/{r.url.split('/')[-1]}", "wb") as f:
        f.write(r.content)