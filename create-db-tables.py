from sqlalchemy import create_engine, Column, Integer, String, Text, Numeric, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from flask_sqlalchemy import SQLAlchemy

# Database URL (replace with your actual credentials)
DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"

# Create a new SQLAlchemy engine instance
engine = create_engine(DATABASE_URL, echo=True)

# Base class for declarative models
Base = declarative_base()


# Initialize SQLAlchemy
db = SQLAlchemy()

# Define the Restaurant model
class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    phone_number = Column(String(15), nullable=True)
    email = Column(String(255), nullable=True)
    
    # Relationship to Menu
    menus = relationship('Menu', back_populates='restaurant')

    def __repr__(self):
        return f'<Restaurant(name={self.name}, address={self.address})>'

# Define the Menu model
class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    description = Column(Text, nullable=True)
    available = Column(Boolean, default=True, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'), nullable=False)
    
    # Relationship to Restaurant
    restaurant = relationship('Restaurant', back_populates='menus')

    def __repr__(self):
        return f'<Menu(name={self.name}, price={self.price})>'

# Create all tables
def create_tables():
    Base.metadata.create_all(engine)
    print("Tables created")

# Insert sample data
def insert_data():
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Create restaurants
    r1 = Restaurant(name="Italian Bistro", address="123 Pasta St", phone_number="555-1234", email="contact@italianbistro.com")
    r2 = Restaurant(name="Sushi Haven", address="456 Sushi Ave", phone_number="555-5678", email="info@sushihaven.com")
    
    # Add restaurants to the session
    session.add_all([r1, r2])
    session.commit()

    # Create menus
    m1 = Menu(name="Spaghetti Carbonara", price=12.99, description="Classic Italian pasta with cream and bacon", restaurant=r1)
    m2 = Menu(name="Margherita Pizza", price=9.99, description="Simple pizza with tomato, mozzarella, and basil", restaurant=r1)
    m3 = Menu(name="California Roll", price=8.99, description="Roll with crab, avocado, and cucumber", restaurant=r2)
    m4 = Menu(name="Tempura Udon", price=11.99, description="Udon noodles with crispy tempura", restaurant=r2)
    
    # Add menus to the session
    session.add_all([m1, m2, m3, m4])
    session.commit()

    print("Data inserted")

if __name__ == '__main__':
    create_tables()
    insert_data()
