import re
import os
import pickle

from utils import *

    
extract_links = lambda x: (x[0], list(filter(lambda x: x[1] not in FALSE_LINKS, enumerate(dict.fromkeys(re.findall(r'href="/wiki/([^":]*)"', x[1]))))))
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
    for name, li in rdd1.collect():
        print(name, li)
    return rdd1

def collect(rdd):
    for name, li in rdd.collect():
        with open(f"{EXTRACTED_PREFIX}{name}", "wb") as f:
            pickle.dump(li, f)

def extract(spark):
    collect(create_rdd(spark))



def dijkstra(index):
    def find_min(matrix, found):
        ind, dist = (-1, 0)
        for i in range(len(matrix)):
            if not found[i] and matrix[i] != -1 and (matrix[i] < dist or ind == -1):
                ind = i
                dist = matrix[i]
        return ind

    global adjacency_matrix
    if adjacency_matrix is None:
        with open(f"{TARGET_PREFIX}adjacency_matrix", "rb") as f:
           adjacency_matrix = pickle.load(f)
    
    matrix = [-1 for _ in range(len(adjacency_matrix))]
    found = [False for _ in range(len(adjacency_matrix))]
    previous = [None for _ in range(len(adjacency_matrix))]

    matrix[index] = 0
    previous[index] = index

    ind = index
    while ind != -1:
        found[ind] = True
        for i in range(len(adjacency_matrix)):
            if found[i]:
                continue
            if adjacency_matrix[ind][i] == -1:
                continue
            if matrix[i] == -1 or matrix[ind] + adjacency_matrix[ind][i] < matrix[i]:
                matrix[i] = matrix[ind] + adjacency_matrix[ind][i]
                previous[i] = ind
        ind = find_min(matrix, found)
    return matrix, previous

def dijkstras(spark, n_max=None):
    global adjacency_matrix
    if adjacency_matrix is None:
        with open(f"{TARGET_PREFIX}adjacency_matrix", "rb") as f:
           adjacency_matrix = pickle.load(f)

    if n_max is None:
        n_max = len(adjacency_matrix)
    data = list(range(n_max))
    rdd = spark.sparkContext.parallelize(data)
    rdd1 = rdd.map(lambda i: (i, dijkstra(i)))

    return rdd1

def count_dists(spark, index):
    data, _ = dijkstra(index)
    df = spark.createDataFrame(enumerate(data), ["target", "dist"])
    counts = df.groupBy("dist").count().orderBy("dist", ascending=True)

    return counts

def max_distances(spark, n_max=None):
    global adjacency_matrix
    if adjacency_matrix is None:
        with open(f"{TARGET_PREFIX}adjacency_matrix", "rb") as f:
           adjacency_matrix = pickle.load(f)

    if n_max is None:
        n_max = len(adjacency_matrix)

    data = list(range(n_max))
    rdd = spark.sparkContext.parallelize(data)
    rdd1 = rdd.map(lambda i: (i, dijkstra(i)[0]))
    rdd2 = rdd1.map(lambda x: (x[0], max(x[1])))
    df = rdd2.toDF(["index", "max_distance"])
    return df

def max_distance(spark, n_max=None):
    df = max_distances(spark, n_max)
    return df.select("max_distance").agg({'max_distance': 'max'})

        
def path_from_previous(previous, start, end):
    if previous[end] is None:
        return None
    res = [end]
    while res[-1] != start:
        res.append(previous[res[-1]])
    return res[::-1]

