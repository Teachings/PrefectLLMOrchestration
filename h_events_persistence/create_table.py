from models import Base, engine

# Create the flow_results table in the PostgreSQL database
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
