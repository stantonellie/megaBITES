from flask import Flask, render_template, redirect, url_for, make_response
from flask import request
from sqlalchemy import create_engine
import sqlalchemy.orm
from database_setup import Base, Blog, Subscriber, User
from datetime import datetime

app = Flask(__name__)

engine = create_engine("mysql://admin1:@GitPa$$w0rd#@54.74.234.11/team_404?charset=utf8mb4")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin1:@GitPa$$w0rd#@54.74.234.11/team_404'
Base.metadata.bind = engine

DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def home():
    return render_template("home.html", posts=session.query(Blog).limit(5).all())


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/post/<post>')
def post(post):
    return render_template("post.html", post=session.query(Blog).filter_by(post_id=post).first())


@app.route('/post/create', methods=['GET', 'POST'])
def create_post():
    if request.cookies['admin'] != 'yes':
        return redirect('/')
    if request.method == 'GET':
        return render_template("create_post.html")
    else:
        blog = Blog(
            blog_author=request.cookies['email'],
            blog_title=request.form['title'],
            blog_subtitle=request.form['subtitle'],
            post_date=datetime.now(),
            content=request.form['content'],
            comments=0,
            likes=0
        )

        session.add(blog)
        session.commit()

        return redirect('/')


@app.route('/post/<post>/edit', methods=['GET', 'POST'])
def edit_post(post):
    if request.cookies['admin'] != 'yes':
        return redirect('/')
    if request.method == 'GET':
        return render_template("create_post.html", post=session.query(Blog).filter_by(post_id=post).first())
    else:
        blog = session.query(Blog).filter_by(post_id=post).first()
        blog.blog_title = request.form['title']
        blog.blog_subtitle = request.form['subtitle']
        blog.content = request.form['content']
        session.commit()
        return redirect('/post/' + post)


@app.route('/post/<post>/delete')
def delete_post(post):
    if request.cookies['admin'] != 'yes':
        return redirect('/post/' + post)
    it = session.query(Blog).filter_by(post_id=post).first()
    session.delete(it)
    session.commit()
    return redirect('/')


@app.route('/post/<post>/like')
def like_post(post):
    # 1. Fetch the post
    # 2. increase like by 1
    # 3. commit to the session
    return redirect('/post/' + post)


@app.route('/post/<post>/comment')
def comment_post(post):
    # 1. Fetch the post
    # 2. create a comment from the request.form
    # 3. set the author of the comment to the user id of login user
    # 4. set the date of the comment to now
    # 5. commit to the session
    return redirect('/post/' + post)


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


@app.route('/login', methods=['POST'])
def login():
    return try_login(request.form['email'], request.form['password'])


def try_login(email, password):
    user = session.query(User) \
        .filter_by(email=email) \
        .first()
    if user.password == password:
        response = make_response(redirect(url_for('home')))
        response.set_cookie('email', user.email)
        response.set_cookie('admin', user.is_admin)
        return response
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('home')))
    response.delete_cookie('email')
    response.delete_cookie('admin')
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("registration.html")
    else:
        user = User(
            email=request.form['email'],
            password=request.form['password'],
            is_admin="no"
        )
        session.add(user)
        session.commit()
        return try_login(request.form['email'], request.form['password'])


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5555)
