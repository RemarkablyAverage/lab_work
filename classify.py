#execute statement:
#ipython -i classify.py --pylab
import numpy as np
import random
import math
import re
import itertools
import matplotlib.pyplot as plt

def prefixes(s):
    prefixes = [0]*len(s)
    j = 0
    # X = 2*i-j
    for i in range(1, len(s)):
        while j > 0 and s[i] != s[j]:
            # j > prefixes[j-1]
            j = prefixes[j-1]
            # X = X + (j - prefixes[j-1]), which is larger
        
        if s[i] == s[j]:
            j += 1
            prefixes[i] = j
            # X = X + 1 /*from i*/ - 1 /*from j*/, no change
        else :
            prefixes[i] = j
            # X = X + 1 /*from i*/
        # thus X increasing
    # at the end, X is at most 2*len(s), and non-monotonicities must
    # happen at most len(s) times since i strictly increasing.  so
    # creating the table is O(len(s)).
    return prefixes

def is_substr(s1, s2):
    ps = prefixes(s1)
    j = 0
    # X = 2*i-j
    for i in range(0, len(s2)):
        if j >= len(s1):
            return True
        while j > 0 and s2[i] != s1[j]:
            j = ps[j-1]
            # X = X + (j - prefixes[j-1])
        if s2[i] == s1[j]:
            j += 1
            # X = X - 1
        # X = X + 1
        # (so X = X or X = X + 1)
        # (X = X can only happen at most len(s2) times)
    return False

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
        sigma = 20
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

def tset(RNA_graph):
    ret_set = set(tuple(node.list) for node in RNA_graph.nodes_dict.values())
    return [list(subset) for subset in ret_set]

def lists(graph):
    for x in graph.nodes_dict:
        print(graph.nodes_dict[x].list, graph.nodes_dict[x].data)

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
    #obtain sets
    tsets = tset(RNA_op_graph)
    #set up parameters for matrix
    dict_nodes = RNA_op_graph.nodes_dict
    col_count = len(list(dict_nodes.values())[0].list)
    eq_pr_matrix = np.zeros((0, col_count), dtype = float)
    keys = list(RNA_op_graph.nodes_dict.keys())
    for subset in tsets:
        pr = 0.0
        for node_key in range(len(keys)):
            node = dict_nodes[keys[node_key]]
            if np.array_equal(node.list, subset):
                for i in range(len(node.list)):
                    start_indexes = [m.start() for m in re.finditer(node.data, RNA_list[i])]
                    for index in start_indexes:
                        pr += node.list[i] * np.sum(tr_matrix[index:index+scan_length, i])
        #deep copy                              
        append_row = create_row(subset, pr)
        eq_pr_matrix = np.vstack([eq_pr_matrix, append_row])
    #normalize
    for col in range(len(eq_pr_matrix[0,:])):
        eq_pr_matrix[:,col] = eq_pr_matrix[:,col] / sum(eq_pr_matrix[:,col])
    return eq_pr_matrix

#test array
RNA_arr = [generate_string(100), generate_string(150), generate_string(80)]#, generate_string(100), 
            #generate_string(120), generate_string(120)]    
                        #generate_string(5000)]#["AAACGAA", "TAACGTA"]

#test calls
RNA_graph = rna_graph()
scan_length = 3
classify(RNA_arr, scan_length, RNA_graph)
#end classification

#start probability matrix construction
tr_matrix = transcript_pr_matrix(RNA_arr)
populate_pr_matrix(RNA_arr, tr_matrix, scan_length)
pr_matrix = eq_class_matrix(RNA_graph, tr_matrix, RNA_arr, scan_length)

"""plotting stuff"""

def find_eq_classes(pr_m):
    eq_classes = []
    for i in range(len(pr_m[:,0])):
        print(i)
        eq_class = []
        for j in range(len(pr_m[0,:])):
            if (pr_m[i,j] != 0):
                eq_class.append(1)
            else:
                eq_class.append(0)
        eq_classes.append(eq_class)
    return eq_classes


def plot(RNA_graph, RNA_list, tr_m, pr_m, scan_length, tr_number):
    #plot naive distribution
    RNA_list = sorted(RNA_list, key = len)
    RNA_list = RNA_list[::-1]
    x = np.arange(len(RNA_list[tr_number]))
    y = tr_m[:,tr_number]
    y = [value for value in tr_m[:, tr_number] if value != 0]
    for _ in range(scan_length - 1):
        y.append(0)
    plt.plot(x, y)
    #determine equivalence class plots / transcript reconstruction
    for i in range(len(pr_m[:, tr_number])):
        #determine what kind of eq class it is (to lat)
        if (pr_m[i, tr_number] != 0.0):
            #determine the normalizing factor (reads)
            counter = 0
            # for key in RNA_graph.nodes_dict:
            #     if (np.array_equal(check_vector, RNA_graph.node_dict[key].list)):
            #         counter += 1
            #find all instances of matching substring


plot(RNA_graph, RNA_arr, tr_matrix, pr_matrix, scan_length, 1) 













