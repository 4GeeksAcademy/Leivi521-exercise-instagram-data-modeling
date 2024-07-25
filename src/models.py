import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Enum, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from enum import Enum as PyEnum

Base = declarative_base()

follower = Table(
    "follower",
    Base.metadata,
    Column("user_from_id", Integer, ForeignKey("users.id")),
    Column("user_to_id", Integer, ForeignKey("users.id")),
)

class User(Base):
    __tablename__ = 'users'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    posts = relationship('Post', back_populates = 'user')
    comments = relationship('Comment', back_populates = 'user')
    following = relationship('User', secondary = follower, primaryjoin = id == follower.c.user_from_id, secondaryjoin = id == follower.c.user_to_id, backref = 'followers')
    



class Post(Base):
    __tablename__ = 'posts'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    image_url = Column(String, nullable = False)
    caption = Column(Text)

    user = relationship('User', back_populates = 'posts')
    comments = relationship('Comment', back_populates  = 'post')
    media = relationship('Media', back_populates = 'post')


class Mediatype(PyEnum):
    IMAGE = 'image'
    VIDEO = 'video'

class  Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum(Mediatype), nullable = False)
    url = Column(String(250), nullable = False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable = False)
    post = relationship('Post', back_populates = 'media')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable = True)
    author_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable = False)
    user = relationship('User', back_populates = 'comments')
    post = relationship('Post', back_populates = 'comments')







    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
