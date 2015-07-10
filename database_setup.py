import os
#sys module provide munctions and variables which can be used
#to manipulate different parts of the Python runtime environment
import sys 

#necessary for mapper code

from sqlalchemy import Column, ForeignKey, Integer, String

#used in configuration and class code
from sqlalchemy.ext.declarative import declarative_base

#used for writing mapper
from sqlalchemy.orm import relationship

#used for configuration code at the end of the file
from sqlalchemy import create_engine

#helps in setting up the class code
#lets our classes know that they are special
#SQLAlchemy classes that correspond to tables
#in the database
Base = declarative_base()

class Restaurant(Base):
	__tablename__ = 'restaurant'
	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key = True)

class MenuItem(Base):
	__tablename__ = 'menu_item'
	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key = True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

class Employee(Base):
	__tablename__ = 'employee'
	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)

class Address(Base):
	__tablename__ = 'address'
	street = Column(String(80), nullable=False)
	zip_code = Column(String(5), primary_key=True)
	employee_id = Column(Integer, ForeignKey('employee.id'))
	employee = relationship(Employee)

#instance of create_engine class and point to the database
engine = create_engine('sqlite:///restaurantmenu.db')

#adds the classes we will create as a table in the database
Base.metadata.create_all(engine)
