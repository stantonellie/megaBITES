from sqlalchemy import Column, Integer, String, MetaData, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

Base = declarative_base()
meta = MetaData()


class Blog(Base):
    __tablename__ = 'Blog'

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    blog_author = Column(String, nullable=False)
    blog_title = Column(String, nullable=False)
    blog_subtitle = Column(String, nullable=False)
    post_date = Column(DateTime, nullable=False)
    content = Column(Text, nullable=False)
    comments = Column(Integer, nullable=False)
    likes = Column(Integer, nullable=False)
    masthead = Column(String, nullable=False)


class Subscriber(Base):
    __tablename__ = 'Subscribers'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(String, nullable=False)
    name = Column(String, nullable=False)

class Comment(Base):
        __tablename__ = 'Comment'
        id = Column(Integer, primary_key=True)
        post_id = Column(Integer, nullable=False)
        author = Column(String, nullable=False)
        date = Column(DateTime, nullable=False)
        likes = Column(String, nullable=False)
        message = Column(String, nullable=False)


# creates a create_engine instance - insert our password and team
engine = create_engine("mysql://admin1:@GitPa$$w0rd#@54.74.234.11/team_404?charset=utf8mb4")

Base.metadata.create_all(engine)
