import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, count

WORKING_DIR = ""

spark = SparkSession.builder.appName("WikipediaReducer").getOrCreate()


df = spark.read.parquet(os.path.join(WORKING_DIR, "data.parquet"))
df_exploded = df.withColumn("cited_article", explode(col("cited_articles")))


df_count = df_exploded.groupBy("cited_article").agg(count("*").alias("citation_count"))
df_sorted = df_count.orderBy(col("citation_count").desc())

df_sorted.write.mode("overwrite").csv("ranking.csv", header=True)

print("Classement des articles cités enregistré en Parquet et CSV.")
df_sorted.show(10)
