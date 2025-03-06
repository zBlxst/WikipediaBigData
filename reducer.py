from pyspark.sql import SparkSession
import os
import pickle
from utils import *

def process_pickle_files():
    spark = SparkSession.builder.appName("WikiLinks").getOrCreate()

    data = []
    for filename in os.listdir(CRAWLED_PREFIX):
        file_path = os.path.join(CRAWLED_PREFIX, filename)
        if os.path.isfile(file_path):
            data.extend(pickle.load(open(file_path, "rb")))

    df = spark.createDataFrame(data, ["id", "term"])

    return df

def main():
    df = process_pickle_files()
    term_counts = df.groupBy("term").count().orderBy("count", ascending=False)

    output_path = "output.parquet"
    term_counts.write.parquet(output_path, mode="overwrite")

    term_counts.show(10)

if __name__ == "__main__":
    main()
