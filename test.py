RNA_simple = ["AAACGAA", "TAACGTA", ]

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
		current = self.head
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
