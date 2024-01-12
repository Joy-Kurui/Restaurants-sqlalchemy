# models.py

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine('sqlite:///restaurants.db')
Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    reviews = relationship('Review', back_populates='restaurant')
    customers = relationship('Customer', secondary='reviews', back_populates='restaurants')

    @classmethod
    def fanciest(cls):
        return max(cls.query.all(), key=lambda restaurant: restaurant.price, default=None)

    def all_reviews(self):
        return [review.full_review() for review in self.reviews]

    def __repr__(self):
        return f"<Restaurant(id={self.id}, name='{self.name}', price={self.price})>"

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    reviews = relationship('Review', back_populates='customer')
    restaurants = relationship('Restaurant', secondary='reviews', back_populates='customers')

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        highest_rating = max([review.star_rating for review in self.reviews], default=0)
        return next((review.restaurant for review in self.reviews if review.star_rating == highest_rating), None)

    def add_review(self, restaurant, rating):
        new_review = Review(restaurant=restaurant, customer=self, star_rating=rating)
        self.reviews.append(new_review)

    def delete_reviews(self, restaurant):
        self.reviews = [review for review in self.reviews if review.restaurant != restaurant]

    def __repr__(self):
        return f"<Customer(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}')>"

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."

    def __repr__(self):
        return f"<Review(id={self.id}, star_rating={self.star_rating}, restaurant_id={self.restaurant_id}, customer_id={self.customer_id})>"
