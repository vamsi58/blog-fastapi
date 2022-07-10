import urllib.parse

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://root:{urllib.parse.quote_plus('V@msi58c')}@localhost:3306" \
#                          f"/blog_db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./blog_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://nwslttcpscvmnl:d31ddd044d4e41f74d16a2de0351fb420cfb70d2cba906324f25381e1c78e7ef@ec2-3-223-169-166.compute-1.amazonaws.com:5432/dtjavg2ck5351"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
