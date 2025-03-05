import re
import os
import pickle

from utils import *


extract_links = lambda x: (x[0], list(enumerate(dict.fromkeys(re.findall(r'href="/wiki/([^":]*)"', x[1])))))
extract_links_len = lambda x: (extract_links(x)[0], len(extract_links(x)[1]))



def create_rdd(spark):
    data = []
    to_process = os.listdir(RAW_PREFIX)[:MAX_TO_MAP]
    for name in to_process:
        with open(f"{RAW_PREFIX}{name}", "r") as f:
            data.append((name, f.read()))
        os.remove(f"{RAW_PREFIX}{name}")

    rdd = spark.sparkContext.parallelize(data)
    rdd1 = rdd.map(extract_links)
    rdd2 = rdd.map(extract_links_len)
    return rdd1

def collect(rdd):
    for name, li in rdd.collect():
        # with open(f"{EXTRACTED_PREFIX}{name}.debug", "w") as f:
        #     pass
        #     f.write("\n".join(list(map(lambda x: f"{x[0]}:{x[1]}", li))))
        with open(f"{EXTRACTED_PREFIX}{name}", "wb") as f:
            pickle.dump(li, f)

def extract(spark):
    collect(create_rdd(spark))