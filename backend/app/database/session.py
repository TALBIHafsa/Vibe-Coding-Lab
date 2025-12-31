from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Define the SQLite URL
# The 'sqlite:///' prefix indicates a local file database.
SQLALCHEMY_DATABASE_URL = "sqlite:///./agri.db"

# 2. Create the Engine
# 'check_same_thread': False is strictly required for SQLite with FastAPI/Uvicorn
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# 3. Create the Session Factory
# This 'SessionLocal' will be used to create a database session for each request.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Dependency Injection
# This function is used by your routers (Depends(get_db)) to access the DB.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()