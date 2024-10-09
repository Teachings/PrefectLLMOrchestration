import psycopg2
from psycopg2 import sql
from sqlalchemy.exc import OperationalError
from models import Base, engine

# Database connection parameters
db_name = "prefect_db"
db_user = "prefect_user"
db_password = "prefect_pass"
db_host = "localhost"
db_port = "5432"

# Connect to the default database (postgres) to check if the target database exists
def create_database_if_not_exists():
    try:
        # Connect to the default database 'postgres' as an admin user
        conn = psycopg2.connect(dbname="postgres", user=db_user, password=db_password, host=db_host, port=db_port)
        conn.autocommit = True
        cursor = conn.cursor()

        # Check if the database exists
        cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [db_name])
        exists = cursor.fetchone()

        if not exists:
            # Create the database if it doesn't exist
            cursor.execute(sql.SQL(f"CREATE DATABASE {db_name}"))
            print(f"Database '{db_name}' created successfully!")
        else:
            print(f"Database '{db_name}' already exists.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")
        raise

# Call the function to create the database if it doesn't exist
create_database_if_not_exists()

# Now, create the tables in the database
try:
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
except OperationalError as e:
    print(f"Error: {e}")