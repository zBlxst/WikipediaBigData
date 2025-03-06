import pickle
from utils import *
import os

import begin
import mapper


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

def crawl_everything(spark):
    if len(os.listdir(CRAWLED_PREFIX)) > N_TOTAL_PAGES:
        return
    begin.create_base()
    mapper.extract(spark)
    for i in range(N_ROUNDS):
        print(f"Beginning of round {i+1}")
        crawl_pages()
        mapper.extract(spark)

        extracted = len(os.listdir(EXTRACTED_PREFIX))
        crawled = len(os.listdir(CRAWLED_PREFIX))
        print(f"Ending of round {i+1}\nPercentage of {LANGUAGE} wikipedia covered : {(extracted + crawled)*100 / N_TOTAL_PAGES:.04f}%")
        print(f"{extracted} extracted")
        print(f"{crawled} crawled")
        print(f"Total  : {extracted + crawled}/{N_TOTAL_PAGES}\n\n")
        if extracted == 0:
            print("No more page to crawl")
            exit()
