Overview
A networked database application that allows users to manage customer information through a client-server architecture. The server handles data validation, persistence, and business logic, while the client provides a user-friendly command-line interface.
Features

Customer Management: Add, find, update, and delete customer records
Input Validation:

Name: 1-10 characters
Age: 1-120 years
Address: Up to 20 characters
Phone: Format XXX-XXXX (area codes: 394, 426, 901, 514)


Persistent Storage: Records saved to data.txt
Error Handling: Comprehensive validation with detailed error messages
Database Reports: Generate formatted reports of all customers
Network Communication: TCP socket-based client-server model

Project Structure
├── server.py          # Server implementation with database logic
├── client.py          # Client with interactive menu interface
└── data.txt           # Database file (auto-created)
Prerequisites

Python 3.6 or higher
No external dependencies required (uses standard library only)

Installation & Setup

Clone or download the project files

bash   # Ensure server.py and client.py are in the same directory

Prepare the database file (optional)

Create data.txt in the same directory, or
Let the server create it automatically on first run



Usage
Starting the Server
bashpython server.py
The server will:

Load existing records from data.txt
Display any skipped records with error messages
Listen on 0.0.0.0:9999

Running the Client
bashpython client.py
```

The client will connect to `127.0.0.1:9999` and display the menu.

### Menu Options

1. **Find Customer** - Search for a customer by name
2. **Add Customer** - Create a new customer record
3. **Delete Customer** - Remove a customer from the database
4. **Update Customer Age** - Modify age field
5. **Update Customer Address** - Modify address field
6. **Update Customer Phone** - Modify phone field
7. **Print Report** - Display all customers sorted by name
8. **Exit** - Close the connection

### Data Format

**Database File (`data.txt`)**:
```
John|25|123 Main St|514-1234
Jane|30||426-5678
Fields are pipe-separated (|). Empty fields are allowed except for name and age.
Validation Rules
FieldRequiredFormat/ConstraintsNameYes1-10 characters, unique (case-insensitive)AgeYesInteger 1-120AddressNoMax 20 charactersPhoneNoXXX-XXXX where XXX ∈ {394, 426, 901, 514}
Error Handling
The system provides specific error messages for:

Invalid field formats
Duplicate records
Missing customers
Database read errors
Connection failures

Configuration
Server settings (in server.py):
pythonHOST = '0.0.0.0'      # Listen on all interfaces
PORT = 9999           # Server port
DB_FILE = 'data.txt'  # Database filename
Client settings (in client.py):
pythonSERVER_IP = '127.0.0.1'  # Server address
SERVER_PORT = 9999        # Server port
```

### Example Session
```
Python DB Menu

1. Find customer
2. Add customer
...
Select: 2

Customer Name: Alice
Customer Age: 28
Customer Address: 456 Oak Ave
Customer Phone: 514-9999

Server response: Alice|28|456 Oak Ave|514-9999 added to database
Technical Details

Protocol: TCP/IP with custom message format (command::param1::param2...)
Encoding: UTF-8
Buffer Size: 1024 bytes (client), 4096 bytes (server responses)
Concurrency: Single-threaded, sequential client handling
Data Structure: In-memory dictionary with case-insensitive keys

Troubleshooting
Connection Refused

Ensure server is running before starting client
Check firewall settings for port 9999
Verify server IP/port configuration

Database Not Loading

Check data.txt exists in server directory
Verify file format (pipe-separated fields)
Review server console for read errors

Author
Najlaa Achouhal
