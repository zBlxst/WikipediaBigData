import os
from utils import *
import pickle
import time

def weight(index, total):
    return 1

def translate():
    all_files = os.listdir(CRAWLED_PREFIX)
    num_to_name = {}
    name_to_num = {}


    for i, name in enumerate(all_files):
        num_to_name[i] = name
        name_to_num[name] = i

    with open(f"{TARGET_PREFIX}number_to_name", "wb") as f:
        pickle.dump(num_to_name, f)
    with open(f"{TARGET_PREFIX}name_to_number", "wb") as f:
        pickle.dump(name_to_num, f)
    return num_to_name, name_to_num

def create_matrix():
    global adjacency_matrix
    all_files = os.listdir(CRAWLED_PREFIX)
    adjacency_matrix = [[-1 for _ in range(len(all_files))] for __ in range(len(all_files))]
    
    _, name_to_num = translate()
    for i, name in enumerate(all_files):
        with open(f"{CRAWLED_PREFIX}{name}", "rb") as f:
            li = pickle.load(f)
            length = len(li)
            for index, name_ref in li:
                if name_ref == name:
                    adjacency_matrix[i][i] = 0
                else:
                    adjacency_matrix[i][name_to_num[name_ref]] = weight(index, length)


    with open(f"{TARGET_PREFIX}adjacency_matrix", "wb") as f:
        pickle.dump(adjacency_matrix, f)
