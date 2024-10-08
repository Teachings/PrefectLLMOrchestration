from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class FlowResult(Base):
    __tablename__ = 'flow_results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    flow_run_id = Column(String, unique=True, nullable=False)
    flow_name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    result = Column(JSON, nullable=False)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime)

# Set up the PostgreSQL connection
DATABASE_URL = "postgresql://prefect_user:prefect_pass@localhost:5432/prefect_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
