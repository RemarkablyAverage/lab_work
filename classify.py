import numpy as np
import random

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
            print(substring)
            i += 1
            hash_check = hash_4(substring)
            if hash_check in RNA_op_graph.nodes_dict:
                op_node = RNA_op_graph.nodes_dict[hash_check]
                op_node.update_list(transcript_index)
            else: 
                RNA_op_graph.add_node(Node(substring, size, transcript_index))
        print("new transcript")

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
    return np.zeros((len(RNA_list[0]), len(RNA_list)), dtype = float)

def populate_pr_matrix(RNA_list, tr_matrix, fit=False):
    for col in range(len(tr_matrix[0])):
        for i in range(len(tr_matrix)):
            tr_matrix[i, col] = rayleigh_distribution(i + 1, fit)
        tr[:,col] = tr[:,col] / sum(tr[:,col])

def eq_class_matrix(RNA_op_graph, tr_matrix):
    nodes = RNA_op_graph.nodes_dict.iteritems()
    for key, node in nodes:



#test arrays
RNA_arr = ["AAACGAA", "TAACGTA"]
#tempvariables
scan_length = 3

#test calls
RNA_graph = rna_graph()
scan_length = 3
classify(RNA_arr, scan_length, RNA_graph)
#end classification

#start probability matrix construction
transcript_probability = transcript_pr_matrix(RNA_arr)
populate_pr_matrix(RNA_arr, tr_matrix)











