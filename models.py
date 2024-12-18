from flask_pymongo import PyMongo
from bson import ObjectId

mongo = PyMongo()

class Fuse:
    def __init__(self, name, price, types, ratings=None, comments=None):
        self.name = name
        self.price = price
        self.types = types
        self.ratings = ratings if ratings else []
        self.comments = comments if comments else []

    def to_db_data(self):
        return {
            'name': self.name,
            'price': self.price,
            'types': self.types,
            'ratings': self.ratings,
            'comments': self.comments
        }

    @classmethod
    def from_db_data(cls, data):
        return cls(
            name=data['name'],
            price=data['price'],
            types=data['types'],
            ratings=data['ratings'],
            comments=data['comments']
        )

    def add_rating(self, rating):
        self.ratings.append(rating)

    def add_comment(self, comment):
        self.comments.append(comment)
