import requests
import pickle
from utils import *
import os


def crawl_page(name):
    print(f"Starting to crawl {BASE_URL}{name}")
    with open(f"{EXTRACTED_PREFIX}{name}", "rb") as f:
        li = pickle.load(f)
        for no, reference in li[:MAX_TO_DOWNLOAD_PER_PAGE]:
            download_page(reference)
    os.rename(f"{EXTRACTED_PREFIX}{name}", f"{CRAWLED_PREFIX}{name}")
        

def crawl_pages():
    names = list(filter(lambda x: not x.endswith(".debug"), os.listdir(EXTRACTED_PREFIX)))[:MAX_TO_CRAWL] 
    for name in names:
        crawl_page(name)