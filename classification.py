#test arrays
RNA_simple = ["AAACGAA", "TAACGTA", ]

#node class
class Node:
	def __init__(self, initdata, next_node):
		self.data = initdata
		self.next = next_node

	def get_data(self):
		return self.data

	def get_next(self):
		return self.next_node

	def set_next(self, new_next):
		self.next_node = new_next

	def insert(self, data):
		new_node = Node(data)
		new_node.set_next(self.head)
		self.head = new_node

	def search(self, data):
	    current = self.head
	    found = False
	    while current and found is False:
	        if current.get_data() == data:
	            found = True
	        else:
	            current = current.get_next()
	    if current is None:
	        raise ValueError("Data not in list")
	    return current


#todo, function to get nodes -> probability matrix

#classification algorithm 
#place RNA sequences into correct equivalent classes 
#naive implementation
def classify(RNA_arr, scan_length):
	#starter node/RNA line
	starter_rna = RNA_arr[0]
	head = Node(starter_rna[0:scan_length], None)
	curr = head
	for i in range(1, len(starter_rna)):
		new_node = Node(starter_rna[i:i+scan_length])

	# for i in range(1, len(RNA_arr)):
	# 	for 







