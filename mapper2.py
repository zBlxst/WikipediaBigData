import os
import requests
from itertools import islice

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, ArrayType

from utils import *

FRED_WORKING_DIR = "Big_Data/WikipediaBigData"

def get_wikipedia_links(article):
    print(f"{article}")

    url = f"https://fr.wikipedia.org/w/api.php?action=query&titles={article}&prop=links&pllimit=max&format=json"
    try:
        response = requests.get(url)
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        
        cited_articles = []
        for page_id, page_data in pages.items():
            if "links" in page_data:
                cited_articles = [link["title"] for link in page_data["links"] if link["ns"] == 0]  # Filtrer uniquement les articles
        
        return cited_articles
    except Exception as e:
        print(f"Erreur lors de la récupération de {article}: {e}")
        return []
    
spark = SparkSession.builder \
    .appName("WikipediaCitedArticles") \
    .config("spark.sql.parquet.compression.codec", "snappy") \
    .getOrCreate()

schema = StructType([
    StructField("article", StringType(), True),
    StructField("cited_articles", ArrayType(StringType()), True)
])

def process_articles(input_file, output_file):

    with open(input_file, "r", encoding="utf-8") as f:
        articles = [line.strip() for line in f.readlines()]

        articles = list(set(articles))
        articles = [article for article in articles if not (article[0] == "(") and len(article) > 1]

    data = [(article, get_wikipedia_links(article)) for article in islice(articles, 50000)]

    
    df = spark.createDataFrame(data, schema=schema)
    df.write.mode("overwrite").parquet(output_file, compression="zstd")

    print(f"Données enregistrées dans {output_file}")

if __name__ == "__main__":
    process_articles(os.path.join(FRED_WORKING_DIR, "frwiki-latest-all-titles-in-ns0"), os.path.join(FRED_WORKING_DIR, "data.parquet"))