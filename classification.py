#test arrays
RNA_arr = ["AAACGAA", "TAACGTA", ]
#Node has to exist somewhere in memory right?

#node class
class Node:
	def __init__(self, initdata, next_node):
		self.data = initdata
		self.next = next_node

	def get_data(self):
		return self.data

	def set_next(self, new_next):
		self.next_node = new_next

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
	            current = current.get_next()
	    if current is None:
	        raise ValueError("Data not in list")
	    return current


#tempvariables
scan_length = 3

#classification algorithm 
#place RNA sequences into correct equivalent classes 
#naive implementation
#returns a probability matrix 
#def classify(RNA_arr, scan_length):
	#starter node/RNA line
starter_rna = RNA_arr[0]
for i in range(0, len(starter_rna)):
	if len(starter_rna[i:i+scan_length]) == scan_length:
		new_node = Node(starter_rna[i:i+scan_length], None)
		if (i == 0):
			head = new_node
			curr = head
		curr.next = new_node
		curr = curr.next


