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