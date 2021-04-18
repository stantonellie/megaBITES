import sys

from sqlalchemy import Column, ForeignKey, Integer, String, MetaData, Table, ForeignKeyConstraint, DateTime, \
    text

from sqlalchemy.schema import ForeignKeyConstraint

from sqlalchemy.dialects.mysql import \
        BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
        DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
        LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
        NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
        TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR, insert

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

Base = declarative_base()
meta = MetaData()


class Blog (Base):
    __tablename__ = 'Blog'

    post_id = Column(Integer, primary_key=True)
    blog_author = Column(String, nullable=False)
    blog_title = Column(String, nullable=False)
    post_date = Column(DateTime, nullable=False)
    content = Column(String, nullable=False)
    comments = Column(Integer, nullable=False)
    likes = Column(Integer, nullable=False)

# creates a create_engine instance - insert our password and team
engine = create_engine("mysql://admin1:@GitPa$$w0rd#@54.74.234.11/team_404?charset=utf8mb4")


Base.metadata.create_all(engine)