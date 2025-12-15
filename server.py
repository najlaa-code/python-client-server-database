import socketserver
import socket
import os

#configure the connection
HOST = '0.0.0.0'
PORT = 9999
DB_FILE = 'data.txt'

#Part 1: error checking functions
class Server:
	def __init__(self):
		# initialize server configuration
		self.host = HOST
		self.port = PORT
		self.db_file = DB_FILE
		self.customers={}
		self.load_database() #loads existing data from the file - write the method later

	#validation methods
	def valid_age(self, age):
		if not age:
			return False
		if not age.isdigit():
			return False
		age_int = int(age)
		return 1 <= age_int <= 120

	def valid_phone(self, phone):
		if not phone:   #if there is no phone number, it is still valid
			return True
		components = phone.split("-")
		if len(components) != 2:
			return False
		first3, last4 = components
		if first3 not in ['394', '426', '901','514']:
			return False
		if not first3.isdigit():
			return False
		if len(last4) != 4:
			return False
		if not last4.isdigit():
			return False
		return True

	def valid_name(self,name):
		return 0 < len(name) <= 10
	def valid_address(self, address):
		return len(address) <=20


	def load_database(self):
		skipped_elements = [] #this is a list of the records that couldn't be loaded
		# file reading
		#f = open("data.txt")
		try:
			f = open(self.db_file, 'r')
			lines = f.readlines()
			f.close()
			lineNbr = 0
			print("Loading database...")
			for line in lines:
				#lineNbr = nbr of customers so
				lineNbr += 1
				#remove extra spaces
				line = line.strip()
				#split based on |
				components = line.split('|')
				#because some of the lines have extra spaces like in the examples, clean them here
				cleaned_components = [] #list for the clean components
				for component in components:
					clean = component.strip()
					cleaned_components.append(clean) #append adds smtg at the end of the list

				#check 1: do we have 4 fields?
				if len(cleaned_components) != 4:
					skipped_elements.append(("[missing field(s)]:", line))
					continue
				#if we do have 4 fields, we can get the fields so we can check them
				name = cleaned_components[0]
				age = cleaned_components[1]
				address = cleaned_components[2]
				phone = cleaned_components[3]

				#check 2: is the name okay
				if not self.valid_name(name):
					skipped_elements.append(("DB read error: Record skipped [invalid name field]:", line))
					continue
				#check 3: is the age okay
				if not self.valid_age(age):
					skipped_elements.append(("DB read error: Record skipped [invalid age field]:", line))
					continue
				#check 4: is the address okay
				if not self.valid_address(address):
					skipped_elements.append(("DB read error: Record skipped [invalid address field]:", line))
					continue
				#check 5: is the phone okay
				if not self.valid_phone(phone):
					skipped_elements.append(("DB read error: Record skipped [invalid phone field]:", line))
					continue
				#check 6: does the name already exists
				#convert all names to lower case to compare
				lower_name = name.lower()
				if lower_name in self.customers:
					skipped_elements.append(("DB read error: Record skipped [key/record already exists]:", line))
					continue
				# every customer will be a dictionary , so we can access it by its key
				customer = {}
				customer['name'] = name
				#need to convert the age string to an int
				agenbr = int(age)
				customer['age'] = agenbr
				customer['address'] = address
				customer['phone'] = phone
				# add the customer to the database
				self.customers[lower_name]=customer

				#not sure yet if the records are printed when the server is created
				#print("Loading database...")
				#print(skipped_elements)
			if skipped_elements:
				for error_msg, skipped_line in skipped_elements:
					print(error_msg, skipped_line)
		except FileNotFoundError:
			print(f"{self.db_file} not found.")

	def find_customer(self, name):
		lower_case_name = name.lower()
		if lower_case_name in self.customers:
			found = self.customers[lower_case_name]
			return f"{found['name']}|{found['age']}|{found['address']}|{found['phone']}"
		return f"DB error: {name} not in the database"
	def add_customer(self, name, age, address, phone):
		if not self.valid_name(name):
			return f"DB add error: record contains invalid name [{name}]"
		if age and not self.valid_age(age):
			return f"DB add error: record contains invalid age [{age}]"
		if not self.valid_address(address):
			return f"DB add error: record contains invalid address [{address}]"
		if not self.valid_phone(phone):
			return f"DB add error: record contains invalid phone [{phone}]"
		lower_case_name = name.lower()
		if lower_case_name in self.customers:
			return f"[{name}] already stored in the database"
		self.customers[lower_case_name] = {
			'name': name,
			'age': age,
			'address': address,
			'phone': phone
		}
		return f"{name}|{age}|{address}|{phone} added to database"
	def delete_customer(self,name):
		lower_case_name = name.lower()
		if lower_case_name not in self.customers:
			return f"DB delete error: cannot delete {name}, as it is not in database"
		del self.customers[lower_case_name]
		return f"Customer {name} deleted from database"
	def update_age(self, name, age):
		lower_case_name = name.lower()
		if lower_case_name not in self.customers:
			return f"DB update error: attempt to update invalid age number {age}"
		if age and not self.valid_age(age):
			return "DB update error: attempt to update using an invalid age {age}"
		#self.customers[lower_case_name]['age'] = age
		self.customers[lower_case_name]['age'] = int(age) if age else ''
		return f"Customer [{name}] age updated"
	def update_address(self, name, address):
		lower_case_name = name.lower()
		if lower_case_name not in self.customers:
			return f"Error: Customer [{name}] does not exist"
		if not self.valid_address(address):
			return "Error: Invalid address field"
		self.customers[lower_case_name]['address'] = address
		return f"Customer [{name}] address updated"
	def update_phone(self, name, phone):
		lower_case_name = name.lower()
		if lower_case_name not in self.customers:
			return f"Error: Customer [{name}] does not exist"
		if not self.valid_phone(phone):
			return "Error: Invalid phone field"
		self.customers[lower_case_name]['phone'] = phone
		return f"Customer [{name}] phone updated"
	def print_report(self):
		#print("debugging print report ")
		if not self.customers:
			return "Error: No customers in database."
		# Help on built-in function sorted in module builtins:
	# sorted(iterable, /, *, key=None, reverse=False)
	#     Return a new list containing all items from the iterable in ascending order.
	#     A custom key function can be supplied to customize the sort order, and the
	#     reverse flag can be set to request the result in descending order.
		list_customers = sorted(self.customers.values(), key=lambda word: word['name'].lower())
		report = "\n++\n++ DB Report\n++\n"
		report += "Name\t\tAge\t\t\tAddress\t\t\t\tPhone\n"
		report += "----\t\t---\t\t\t-------\t\t\t\t-----\n"
		for customer in list_customers:
			name = customer['name'][:10]
			age = str(customer['age']) if customer['age'] else ''
			address = customer['address'][:20] if customer['address'] else ''
			phone = customer['phone'] if customer ['phone'] else ''
			report += f"{name}\t\t{age}\t\t{address}\t\t\t{phone}\n"
		return report

	#Part 2: start the server
	def start(self):
		print("Python DB server is now running...")
		# I obtained this part of the code from https://realpython.com/python-sockets/#:~:text=to%20the%20client.-,Echo%20Server,sendall(data)
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((self.host, self.port))
			s.listen()
			#print(f"DEBUGGING Server listening on {self.host}:{self.port}")
			while True:
				conn, addr = s.accept()
				print(f"Connected by {addr}")
				while True:
					try:
						data = conn.recv(1024).decode()
						if not data:
							print("Client disconnected")
							break
						print(f"Received request: {data}")
						response = self.handle_request(data)
						print(f"Sending response: {response[:50]}...")  # Print first 50 chars
						conn.sendall(response.encode())
						if data.strip().startswith("exit"):
							print("Exit command received, closing connection")
							break
					except Exception as e:
						print(f"Error handling request: {e}")
						break
				conn.close()
				print("Connection closed")

	def handle_request(self, request):
		requests = request.split("::")
		this_request = requests[0]
		if this_request=="find":
			return self.find_customer(requests[1])
		elif this_request=="add":
			return self.add_customer(requests[1],requests[2],requests[3],requests[4])
		elif this_request=="delete":
			return self.delete_customer(requests[1])
		elif this_request=="update_age":
			return self.update_age(requests[1], requests[2])
		elif this_request=="update_phone":
			return self.update_phone(requests[1], requests[2])
		elif this_request=="update_address":
			return self.update_address(requests[1], requests[2])
		elif this_request=="print_report":
			return self.print_report()
		elif this_request=="exit":
			return "Goodbye!:)"
		else:
			return "Invalid choice. Please select from a number from 1 to 8."

if __name__ == '__main__':
	s = Server()
	s.start()
