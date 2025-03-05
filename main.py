import begin
import mapper
import crawler
from utils import *
import os

from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[1]").appName("WikiGameBreaker").getOrCreate() 

begin.create_base()
mapper.extract(spark)
for i in range(N_ROUNDS):
    print(f"Beginning of round {i+1}")
    crawler.crawl_pages()
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

