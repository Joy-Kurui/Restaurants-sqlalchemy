
from sqlalchemy import create_engine
from faker import Faker
from sqlalchemy.orm import sessionmaker
from models import Base, Restaurant, Customer, Review

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

for _ in range(5):
    restaurant = Restaurant(name=fake.company(), price=fake.random_int(1, 5))

   
    customer = Customer(first_name=fake.first_name(), last_name=fake.last_name())
    review = Review(star_rating=fake.random_int(1, 5))

   
    restaurant.reviews.append(review)
    customer.reviews.append(review)
    restaurant.customers.append(customer)

    session.add_all([restaurant, customer])

print("Seed data added successfully.")
