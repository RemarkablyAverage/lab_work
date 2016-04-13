import numpy as np

"""Test Variables"""
#test arrays
RNA_arr = ["AAACGAA", "TAACGTA"]
RNA_arr = sorted(RNA_arr, key = len)
RNA_arr = RNA_arr[::-1]
#tempvariables
scan_length = 3

class Node:
	def __init__(self, initdata, size):
		self.data = initdata
		self.list = np.zeros((size,), dtype = int)

	def update_list(self, k):
		self.list[k] = 1

class rna_graph:
	def __init__(self):
		self.nodes_dict = {} #takes in a hash key and maps to a node, inside of the node goes to a list of transciprts

	def add_node(self, Node):
		str_add = Node.data
		self.nodes_dict[hash(str_add)] = Node

	def update_transcript(self, transcript):
		edit_node = self.nodes_dict[hash]
		edit_node.update_list(Node, transcript)

	def debug(self):
		for k in self.nodes_dict:
			print("key", k)
			print("node value", self.nodes_dict[k])
			print("node present in transcripts", self.nodes_dict[k].list)


test = rna_graph()
test_node = Node("AAA", 2)



