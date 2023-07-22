# LinkedIndek
This repository contains a simple Flask server that interacts with a PostgreSQL database to store and display LinkedIn URLs along with their corresponding names and years. Users can submit new LinkedIn URLs through a web form, and the server will validate the URL and add it to the database if it's valid and not already submitted.

# Requirements
To run this server, you need the following software and configurations:

1. Python 3.x: Make sure you have Python 3.x installed on your system.
2. PostgreSQL: You should have a PostgreSQL server running and configured with appropriate access credentials. The server should also have a database created to store the LinkedIn URL submissions.

# Installation
To install the server, follow these steps:

Clone the repository:
```
git clone https://github.com/koderik/linkedindek
```
Navigate to the repository directory:
```
cd linkedindek
```
Install the required Python packages:
```
pip install -r requirements.txt
```
Don't forget to set up a PostgreSQL server and database as mentioned in the Requirements section. Either locally or on a remote server. If you are unsure of this step, email me at erik@sandlov.com.

Set the following environment variables:
```
export POSTGRES_HOST="your_postgres_host"
export POSTGRES_USER="your_postgres_user"
export POSTGRES_PASSWORD="your_postgres_password"
export POSTGRES_DATABASE="your_postgres_database"
```
If you are loading the environment variables from a file, you need to uncomment some lines from the head of index.py

Run the server:
```
python api/index.py
```

Once the server is running, you can access it at http://localhost:5000.
