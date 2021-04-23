from flask import Flask, render_template, redirect, url_for, make_response
from flask import request
from sqlalchemy import create_engine
import sqlalchemy.orm
from database_setup import Base, Blog, Subscriber

app = Flask(__name__)

engine = create_engine("mysql://admin1:@GitPa$$w0rd#@54.74.234.11/team_404?charset=utf8mb4")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin1:@GitPa$$w0rd#@54.74.234.11/team_404'
Base.metadata.bind = engine

DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def home():
    return render_template("home.html", posts=session.query(Blog).limit(5).all())


@app.route('/post/<post>')
def post(post):
    return render_template("post.html", post=session.query(Blog).filter_by(post_id=post).first())


@app.route('/recipes/')
def recipes():
    return render_template("recipes.html")


@app.route('/contact/')
def contact():
    return render_template("contact.html")


@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    try:
        session.add(Subscriber(email=email))
        session.commit()
        return render_template("thank_you_for_subscribing.html")
    except:
        session.rollback()
        return render_template("error.html", email=email, error="uh oh... This email is already registered!")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            response = make_response(redirect(url_for('login')))
            response.set_cookie('mBuID', '9268d0b2d17670598c70045b0c7abf38')
            return response
    return render_template('login.html', error=error)

@app.route('/logout', methods=['POST'])
def logout():
    response = make_response(redirect(url_for('home')))
    response.delete_cookie('mBuID')
    return response

@app.route( '/posts/new/', methods=['GET', 'POST'])
def newPost():
    if request.method == 'POST':
         newPost = Post(title=request.form['name'], author=request.form['author'], post_date=request.form['post_date'])
         session.add( newPost )
         session.commit()
         return redirect(url_for('showPosts'))
    else:
         return render_template('createpost.html')

# @app.route( '/' )
# @app.route( '/blog' )
# def showBooks():
#     books = session.query( Book ).all()
#     return render_template( "books.html", books=books )
#
#
# # This will let us Create a new book and save it in our database
# @app.route( '/books/new/', methods=['GET', 'POST'] )
# def newBook():
#     if request.method == 'POST':
#         newBook = Book( title=request.form['name'], author=request.form['author'], genre=request.form['genre'] )
#         session.add( newBook )
#         session.commit()
#         return redirect( url_for( 'showBooks' ) )
#     else:
#         return render_template( 'createbook.html' )
#
#
# # This will let us Update our books and save it in our database
# @app.route( "/books/<int:book_id>/edit/", methods=['GET', 'POST'] )
# def editBook(book_id):
#     editedBook = session.query( Book ).filter_by( id=book_id ).one()
#     if request.method == 'POST':
#         if request.form['name']:
#             editedBook.title = request.form['name']
#             return redirect( url_for( 'showBooks' ) )
#     else:
#         return render_template( 'editBook.html', book=editedBook )
#
#
# # This will let us Delete our book
# @app.route( '/books/<int:book_id>/delete/', methods=['GET', 'POST'] )
# def deleteBook(book_id):
#     bookToDelete = session.query( Book ).filter_by( id=book_id ).one()
#     if request.method == 'POST':
#         session.delete( bookToDelete )
#         session.commit()
#         return redirect( url_for( 'showBooks', book_id=book_id ) )
#     else:
#         return render_template( 'deleteBook.html', book=bookToDelete )
#

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5555)
