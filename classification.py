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

#reference string TAACGTA
def recurse_search_matrix(node, target_string):
	"""returns coordinates if true, else returns -1"""
	# print(node.coordinates)
	# print(node.get_data())
	# print(target_string)
	if (node == []):
		return -1
	elif (node.get_data() == target_string): #looping here
		return node.coordinates
	elif len(node.next) == 1:
		if (node.coordinates[1] > node.next[0].coordinates[1]):
			recurse_search_matrix(node.next[0], target_string)
		else:
			return -1
	#this is a cycle
	else:
		for child in node.next:
			temp = recurse_search_matrix(child, target_string)
			if temp != -1:
				return temp
		return -1

#reference string TAACGTA
def search_matrix(node_matrix, input_node):
	"""returns matching node index (if found data matches) or -1 if not
	 found. remember that because it is called everytime, the cardinality
	 of each node should be preserved.
	 this run time is gonna be absolute trash"""
	 #memoize by having an index of checked?
	inpt = input_node.get_data()
	for i in range(0, len(node_matrix)):
		#at this point i'm iterating through columns, then into rows
		if (type(node_matrix[i][0]) == Node):
			#check the path of the node
			if (node_matrix[i][0].next == None):
				if (node_matrix[i][0].get_data() == inpt):
					return node_matrix[i][0].coordinates
				else:
					return -1
			else:
				check = recurse_search_matrix(node_matrix[i][0], inpt)
				if (check != -1):
					return check
	return -1

#reference string TAACGTA
def classify(RNA_arr, scan_length, node_matrix):
	"""lmao i have no idea what i am doing"""
	for i in range(len(RNA_arr) - 1): #iterate by rows
		tr = RNA_arr[i] 
		if (i == 0):
			j = 0
			while (j < len(tr)):
				if (len(tr[j:j+scan_length])) == scan_length:
					new_node = Node(tr[j:j+scan_length], None, [i, j])
					if (j == 0):
						head = new_node
						curr = head
						curr.root = head #do i need this?
						node_matrix[i][j] = curr
						j += 1
					else:
						if (search_matrix(node_matrix, new_node) == -1):
							curr.root = head #extra??
							curr.set_next(new_node)
							curr = curr.get_next(0)
							node_matrix[i][j] = curr
							j += 1
						else:
							curr.root = head #extra??
							print(search_matrix(node_matrix, curr))
							i_coord = search_matrix(node_matrix, curr)[0]
							j_coord = search_matrix(node_matrix, curr)[1]
							curr.set_next(node_matrix[i_coord][j_coord])					
		else:
			for j in range(0, len(tr)): # don't forget to reset j
				if (len(tr[j:j+scan_length])) == scan_length: #check i'm still valid
					check = node_matrix[i][j]
					new_node = Node(tr[j:j+scan_length], None, [i, j])
					if (type(check) == Node): #check my current path is a node
					#now i have to iterate through the whole freaking matrix, 
					#TODO: memoize my current largest index?
						if (search_matrix(node_matrix, check) != -1):

						else: 
					


classify(RNA_arr, scan_length, node_matrix)


