import socket
import os

def menu():
    os.system("cls") #debugging maybe later used clear() not work
    print("Python DB Menu\n")
    print("1. Find customer")
    print("2. Add customer")
    print("3. Delete customer")
    print("4. Update customer age")
    print("5. Update customer address")
    print("6. Update customer phone")
    print("7. Print report")
    print("8. Exit\n")
    #print("Select: ")
    choice = input("Select: ")
    return choice

def find_customer(sock):
    name = input("Customer name: ")
    request = "find::" + name
    response = send_request(sock, request)
    print("\nServer response: " + response)
    #print("Press any key to continue...")
    input("\nPress any key to continue...")
def add_customer(sock):
    name = input("Customer Name: ")
    age = input("Customer Age: ")
    address = input("Customer Address: ")
    phone = input("Customer Phone: ")
    request = "add::" + name + "::" + age + "::" + address + "::" + phone
    response = send_request(sock, request)
    print("\nServer response: " + response)
    # print("Press any key to continue...")
    input("\nPress any key to continue...")
def delete_customer(sock):
    name = input("Customer Name: ")
    request = "delete::" + name
    response = send_request(sock,request)
    print("\nServer response: "+ response)
    input("\nPress any key to continue...")
def update_customer_age(sock):
    name = input("Customer Name: ")
    age = input("Customer age to update: ")
    request = "update_age::" + name + "::" + age
    response = send_request(sock, request)
    print("\nServer response: " + response)
    input("\nPress any key to continue...")
def update_customer_address(sock):
    name = input("Customer Name: ")
    address = input("Customer address to update: ")
    request = "update_address::" + name + "::" + address
    response = send_request(sock, request)
    print("\nServer response: " + response)
    input("\nPress any key to continue...")
def update_customer_phone(sock):
    name = input("Customer Name: ")
    phone = input("Customer phone to update: ")
    request = "update_phone::" + name + "::" + phone
    response = send_request(sock, request)
    print("\nServer response: " + response)
    input("\nPress any key to continue...")
def print_report(sock):
    response = send_request(sock, "print_report")
    print("\nServer response: " + response)
    input("\nPress any key to continue...")
def exit_server(sock):
    response = send_request(sock,"exit")
    print("\nSever Response: ")
def send_request(sock, message):
    sock.sendall(message.encode()) #send to server
    response = sock.recv(4096).decode() #response of the server
    return response
def main():
    #print("DEBUGGING STARTING CLIENT")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #found on socket (https://realpython.com/python-sockets/#:~:text=to%20the%20client.-,Echo%20Server,sendall(data))
    #try to connect to the server
    try:
        sock.connect(('127.0.0.1', 9999))
    except ConnectionRefusedError:
        print("Unsuccessful connection to the server.")
        sock.close()
        return
    while True:
        selection = menu()
        if selection == '1':
            find_customer(sock)
        elif selection == '2':
            add_customer(sock)
        elif selection == '3':
            delete_customer(sock)
        elif selection == '4':
            update_customer_age(sock)
        elif selection == '5':
            update_customer_address(sock)
        elif selection == '6':
            update_customer_phone(sock)
        elif selection == '7':
            print_report(sock)
        elif selection == '8':
            response = send_request(sock, "exit")
            print("\nServer Response: " + response)
            break
        else:
            print("Invalid selection. Please try again.")
            input("\nPress any key to continue...")
    sock.close()
if __name__ == '__main__':
    main()
