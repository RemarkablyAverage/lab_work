import numpy as np
import random
import math
import re
import itertools

"""The following is the set up hash function and data structures
for the classification of the RNA sequence(s) passed in from an array"""
def hash_4(base_string):
    my_dict = {"A" : "00", "T" : "01", "C" : "10", "G" : "11"}
    ret = "1"
    for i in range(len(base_string)):
        ret += my_dict[base_string[i]]
    return int(ret, 2)

class Node:
    def __init__(self, initdata, size, k):
        self.data = initdata
        self.list = np.zeros((size,), dtype = int)
        self.update_list(k)

    def update_list(self, k):
        self.list[k] = 1

class rna_graph:
    def __init__(self):
        self.nodes_dict = {} #takes in a hash key and maps to a node, inside of the node goes to a list of transciprts

    def add_node(self, Node):
        str_add = Node.data
        self.nodes_dict[hash_4(str_add)] = Node

    #unncessary
    def search(self, target_str):
        for k in self.nodes_dict:
            search_node = self.nodes_dict[k]
            if (search_node.data == target_str):
                return search_node
            else:
                return -1

    def debug(self):
        for k in self.nodes_dict:
            print("key", k)
            print("node value", self.nodes_dict[k])
            print("node present in transcripts", self.nodes_dict[k].list)

def classify(RNA_list, scan_length, RNA_op_graph):
    RNA_list = sorted(RNA_list, key = len)
    RNA_list = RNA_list[::-1]
    size = len(RNA_list)
    for transcript_index in range(len(RNA_list)):
        #unnecessary?
        RNA_list[transcript_index] = RNA_list[transcript_index].upper()
        transcript = RNA_list[transcript_index]
        i = 0
        while (i < len(transcript) - scan_length + 1):
            substring = transcript[i:i+scan_length]
            #print(substring)
            i += 1
            hash_check = hash_4(substring)
            if hash_check in RNA_op_graph.nodes_dict:
                op_node = RNA_op_graph.nodes_dict[hash_check]
                op_node.update_list(transcript_index)
            else: 
                RNA_op_graph.add_node(Node(substring, size, transcript_index))
        #print("new transcript")

""""The following is the random RNA_sequence generation 
and the generation of base pairs in accordance to a 
rayleigh distribution"""

def generate_string(length):
    alphabet = list('ATGC')
    rna = [random.choice(alphabet) for i in range(length)]
    rna = ''.join(rna)
    return rna

def rayleigh_distribution(x, fit):
    """this returns the y given an x for a distrubtion"""
    if (fit):
        sigma = 7
        return (x / (sigma**2) * math.e**(-x**2/(2*sigma**2)))
    else:
        sigma = 11
        return (x / (sigma**2) * math.e**(-x**2/(2*sigma**2)))

def transcript_pr_matrix(RNA_list):
    RNA_list = sorted(RNA_list, key = len)
    RNA_list = RNA_list[::-1]
    return np.zeros((len(RNA_list[0]), len(RNA_list)), dtype = float)

def populate_pr_matrix(RNA_list, tr_matrix, scan_length, fit=False):
    RNA_list = sorted(RNA_list, key = len)
    RNA_list = RNA_list[::-1]
    for col in range(len(RNA_list)):
        for i in range(len(RNA_list[col]) - scan_length + 1):
            tr_matrix[i, col] = rayleigh_distribution(i + 1, fit)
        tr_matrix[:,col] = tr_matrix[:,col] / sum(tr_matrix[:,col])

def power_set(n):
    lst = list(itertools.product([0, 1], repeat=n))
    lst = [list(tp) for tp in lst]
    return lst[1:]

def lists(graph):
    for x in graph.nodes_dict:
        print(graph.nodes_dict[x].list)

def create_row(lst, pr):
    for x in range(len(lst)):
        if lst[x] == 1:
            lst[x] = pr
        else:
            lst[x] = 0
    return lst

def eq_class_matrix(RNA_op_graph, tr_matrix, RNA_list, scan_length):
    #sort entry list
    RNA_list = sorted(RNA_list, key = len)
    RNA_list = RNA_list[::-1]
    #obtain powerset
    powerset = power_set(len(RNA_list))
    #set up parameters for matrix
    dict_nodes = RNA_op_graph.nodes_dict
    col_count = len(list(dict_nodes.values())[0].list)
    eq_pr_matrix = np.zeros((0, col_count), dtype = float)
    keys = list(RNA_op_graph.nodes_dict.keys())
    pr = 0.0
    for subset in powerset:
        for node_key in range(len(keys)):
            node = dict_nodes[keys[node_key]]
            if np.array_equal(node.list, subset):
                print(node.list)
                for i in range(len(node.list)):
                    if node.list[i] == 1:
                        start_indexes = [m.start() for m in re.finditer(node.data, RNA_list[i])]
                        for index in start_indexes:
                            for _ in range(index, index + scan_length):
                                print("individual pr", tr_matrix[_,i])
                                pr += tr_matrix[_, i]
        #deep copy                              
        append_row = create_row(subset, pr)
        eq_pr_matrix = np.vstack([eq_pr_matrix, append_row])
        pr = 0.0
    #normalize
    for col in range(len(eq_pr_matrix[0,:])):
        eq_pr_matrix[:,col] = eq_pr_matrix[:,col] / sum(eq_pr_matrix[:,col])
    return eq_pr_matrix

#test arrays
RNA_arr = ["AAACGAA", "TAACGTA"] #[generate_string(50), generate_string(40), generate_string(45)]#
#tempvariables
scan_length = 3

#test calls
RNA_graph = rna_graph()
scan_length = 3
classify(RNA_arr, scan_length, RNA_graph)
#end classification

#start probability matrix construction
tr_matrix = transcript_pr_matrix(RNA_arr)
populate_pr_matrix(RNA_arr, tr_matrix, scan_length)
pr_matrix = eq_class_matrix(RNA_graph, tr_matrix, RNA_arr, scan_length)






