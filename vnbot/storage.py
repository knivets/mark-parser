from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
 
class Place(Base):
  __tablename__ = 'places'
  id = Column(Integer, primary_key=True)
  title_ru = Column(String(500), nullable=False)
  title_ua = Column(String(500), nullable=False)
  phone = Column(String(500))
  address = Column(String(150))
  website = Column(String(150))

engine = create_engine('sqlite:///store.db') 
Base.metadata.create_all(engine)

def get_session():
  Base.metadata.bind = engine
  return sessionmaker(bind=engine)()
