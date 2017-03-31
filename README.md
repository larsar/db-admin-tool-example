# db-admin-tool-example
Administration tool example for managing data in a PostgreSQL database 
using Python a command line script.

# Database
This example is written to support local development using PostgreSQL 
running in docker and instances on Heroku for other stages.

# Python installation (Mac)
brew install python3
pip3 install psycopg2
pip3 install tabulate

# Make
For simplicity, you can use make to run commands.

Make target  | Comment
------------ | -------------
up           | Create and start database
migrate      | Create schema and tables
seed         | Populate tables with data
run          | Run the admin script
ps           | Check running processes
down         | Destroy database
run          | Start script using local database
schema       | Dump database schema
stop         | Stop database
start        | Start database
restart      | Restart database
logs         | Show database logs

