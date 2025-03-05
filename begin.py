from utils import *
import requests

def create_base():
    for i in range(N_START):
        debug_print(i)
        r = requests.get(f"{BASE_URL}{RANDOM_ENDPOINT}")
        download_page(r.url.split("/")[-1])

