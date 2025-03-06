import mapper
import crawler
import translator

from utils import *
import pickle
from urllib.parse import unquote
import random



def shortest_path(s, e):
    start = name_to_num[s]
    end = name_to_num[e]
    _, prev = mapper.dijkstra(start)
    path = mapper.path_from_previous(prev, start, end)
    if path is None:
        print(f"No path from {unquote(s)} to {unquote(e)}")
        return
    print(len(path), list(map(lambda x: unquote(num_to_name[x]), path)))

def print_dists(spark, name):
    print(f"Distances from {unquote(name)}")
    df = mapper.count_dists(spark, name_to_num[name])
    df.show()  

def print_max_distances(spark, n_max=None):
    df = mapper.max_distances(spark, n_max)
    df.show()

def print_max_distance(spark, n_max=None):
    mapper.max_distance(spark, n_max).show()    

def map_dijkstra(spark, n_max=None):
    rdd = mapper.dijkstras(spark, n_max)
    for i, d in rdd.collect():
        with open(f"{RES_PREFIX}{num_to_name[i]}", "wb") as f:
            pickle.dump(d, f)



with open(f"{TARGET_PREFIX}number_to_name", "rb") as f:
    num_to_name = pickle.load(f)

with open(f"{TARGET_PREFIX}name_to_number", "rb") as f:
    name_to_num = pickle.load(f)


if __name__ == "__main__":
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.master("local[1]").appName("WikiGameBreaker").getOrCreate() 
    spark._sc.setLogLevel("FATAL")
    print()
    print()

    crawler.crawl_everything(spark)
    translator.create_matrix()

    # for i in range(5):
    #     shortest_path(num_to_name[random.randrange(N_TOTAL_PAGES)], num_to_name[random.randrange(N_TOTAL_PAGES)])

    # for i in range(3):
    #     print_dists(spark, num_to_name[i])
    
    print_max_distances(spark, n_max=10)
