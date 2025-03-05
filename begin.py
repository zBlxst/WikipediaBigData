from utils import *

url = "Special:Random"

def create_base():
    for _ in range(N_START):
        download_page(url)

