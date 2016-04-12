import numpy as np
#node class
class Node:
	def __init__(self, initdata, root, coordinates):
		self.data = initdata
		self.next = []
		self.root = root
		self.coordinates = coordinates

	def get_data(self):
		return self.data

	def set_next(self, new_next):
		self.next.append(new_next)

	def get_next(self, node):
		return self.next[node]

	def insert(self, data):
		new_node = Node(data)
		new_node.set_next(self.head)
		self.head = new_node

	def print(self):
		current = self
		while (current):
			print(current.get_data())
			current = current.next

	def search(self, data):
	    current = self.head
	    found = False
	    while current and found is False:
	        if current.get_data() == data:
	            found = True
	        else:
	            current = current.get_next(0)            
	    if current is None:
	        raise ValueError("Data not in list")
	    return current

#test arrays
RNA_arr = ["AAACGAA", "TAACGTA"]
RNA_arr = sorted(RNA_arr, key = len)
RNA_arr = RNA_arr[::-1]
#tempvariables
scan_length = 3

#Node has to exist somewhere in memory right? right.
#main structure (2d matrix), where valid entries are nodes, null/invalid entries are random floats
row = len(RNA_arr)
column = len(RNA_arr[0]) - scan_length + 1
node_matrix = np.ndarray(shape=(row, column), dtype=Node)

#def search_matrix(node_matrix, target_node, input_node):


def classify(RNA_arr, scan_length, node_matrix):
	"""lmao i have no idea what i am doing"""
	for i in range(len(RNA_arr)): #iterate by rows
		tr = RNA_arr[i] 
		if (i == 0):
			for j in range(0, len(tr)): # don't forget to reset j
				if (len(tr[j:j+scan_length])) == scan_length:
					new_node = Node(tr[j:j+scan_length], None, [i, j])
					if (j == 0):
						head = new_node
						curr = head
						curr.root = head #do i need this?
						node_matrix[i][j] = curr
					else:
						curr.root = head #extra??
						curr.set_next(new_node)
						curr = curr.get_next(0)
						node_matrix[i][j] = curr
		# else:
		# 	for j in range(0, len(tr)): # don't forget to reset j
		# 		if (len(tr[j:j+scan_length])) == scan_length: #check i'm still valid
		# 			check = node_matrix[i][j]
		# 			new_node = Node(tr[j:j+scan_length], None, [i, j])
		# 			if (type(check) == Node): #check my current path is a node
		# 			#now i have to iterate through the whole freaking matrix, 
		# 			#TODO: memoize my current largest index?
		# 				for i1, j1 in 
		# 					if (check.get_data() == new_node.get_data()):
		# 						node_matrix[i][j] = None

		# 					else:


classify(RNA_arr, scan_length, node_matrix)


