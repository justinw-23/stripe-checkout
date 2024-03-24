import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

# Get directory of current file
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Create sqlite path
connection_str = 'sqlite:////' + os.path.join(BASE_DIR, 'site.sqlite3')
print(connection_str)

# Create postgres path
# connection_str = 'postgresql://postgres:7NPT48!cni3j@127.0.0.1:5432/handshakedb'

engine = create_engine(connection_str)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        
db_dependency = Annotated[Session, Depends(get_session)]