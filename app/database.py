from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# eta amder database er url
# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"
# ekhne real value gula dia dite hbe
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:duke123@localhost/fastapi"


# ekta engine banate hbe , engine ta amader sqlAlchemy take postgress er sathe connect korabe

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the database session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
