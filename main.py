import begin
import mapper
import crawler
from utils import *


from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[1]").appName("WikiGameBreaker").getOrCreate() 

begin.create_base()
mapper.extract(spark)
for i in range(N_ROUNDS):
    print(f"Round {i+1}")
    crawler.crawl_pages()
    mapper.extract(spark)
