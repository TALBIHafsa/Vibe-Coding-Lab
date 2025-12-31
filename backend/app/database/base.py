from sqlalchemy.orm import declarative_base

# All models (tables) inherit from this class so SQLAlchemy can track them.
Base = declarative_base()