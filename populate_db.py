from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String, MetaData, Table, ForeignKeyConstraint, DateTime, \
    text

from sqlalchemy.schema import ForeignKeyConstraint

from sqlalchemy.dialects.mysql import \
        BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
        DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
        LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
        NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
        TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR, insert

from database_setup import Base, Blog

# bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
engine = create_engine( "mysql://admin1:@GitPa$$w0rd#@54.74.234.11/team_404?charset=utf8mb4" )

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object.
session = DBSession()

# Create



Post_one = Blog ( Author="Kaz", Title="Vegan Bolognese", Contents="How to make vegan bologenese" )
session.add(Post_one)
session.commit()

# Read

session.query(Blog).all()
session.query(Blog).first()

# Update
#editedBook = session.query(Book).filter_by(id=1).one()
#editedBook.author = "Alexander McCall Smith"
#session.add(editedBook)
#session.commit()

# Delete

#bookToDelete = session.query(Book).filter_by(title="The No. 1 Ladies' Detective Agency").one()
#ession.delete(bookToDelete)
#ßsession.commit()
