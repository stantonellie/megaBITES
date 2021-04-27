from flask import Flask, render_template, redirect, url_for, make_response
from flask import request
from flask_mail import Mail, Message
from sqlalchemy import create_engine
import sqlalchemy.orm
from database_setup import Base, Blog, Subscriber, User, Comment
from datetime import datetime
from forms import ContactForm
from forms import SearchForm

app = Flask(__name__)
app.secret_key = 'development key'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'megabites.blogger@gmail.com'
app.config["MAIL_PASSWORD"] = 'jwwfyzvrxobbeykh'

mail = Mail()
mail.init_app(app)

engine = create_engine("mysql://admin1:@GitPa$$w0rd#@54.74.234.11/team_404?charset=utf8mb4")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin1:@GitPa$$w0rd#@54.74.234.11/team_404'
Base.metadata.bind = engine

DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def home():
    return render_template("home.html", posts=session.query(Blog).all())


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/post/<post_id>')
def post(post_id):
    print(len(session.query(Comment).all()))
    return render_template(
        "post.html",
        post=session.query(Blog).filter_by(post_id=post_id).first(),
        comments=session.query(Comment).filter_by(post_id=post_id).all()
    )


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
            likes=0,
            masthead=request.form['masthead']
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
        blog.masthead = request.form['masthead']
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


@app.route('/post/<id>/like')
def like_post(id):
    post = session.query(Blog).filter_by(post_id=id).first()
    post.likes += 1
    session.commit()
    return redirect('/post/' + id)


@app.route('/post/<id>/comment', methods=['POST'])
def comment_post(id):
    if request.cookies['is_logged_in'] != 'yes':
        return redirect('/')

    comment = Comment(
        post_id=id,
        author=request.cookies['name'],
        message=request.form['message'],
        date=datetime.now(),
        likes=0
    )

    session.add(comment)
    session.commit()
    return redirect('/post/' + id)


@app.route('/post/<id>/comment', methods=['GET'])
def get_comments():
    return session.query.filter_by(post_id=post.id).order_by(Comment.date.desc())


@app.route('/recipes/')
def recipes():
    return render_template("recipes.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        msg = Message(form.subject.data, sender=form.email.data, recipients=['megabites.blogger@gmail.com'])
        msg.body = """
              From: %s <%s>
              %s
              """ % (form.name.data, form.email.data, form.message.data)
        mail.send(msg)
        return redirect('/')

    elif request.method == 'GET':
        return render_template('contact.html', form=form)


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
    return try_login(request.form['email'], request.form['password'], redirect(url_for('home')))


def try_login(email, password, then):
    user = session.query(User) \
        .filter_by(email=email) \
        .first()
    if user.password == password:
        response = make_response(then)
        response.set_cookie('email', user.email)
        response.set_cookie('admin', user.is_admin)
        response.set_cookie('name', user.name or user.email)
        response.set_cookie('is_logged_in', 'yes')
        return response
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('home')))
    response.delete_cookie('email')
    response.delete_cookie('admin')
    response.delete_cookie('is_logged_in')
    response.delete_cookie('name')
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("registration.html")
    else:
        try:
            user = User(
                name=request.form['name'],
                email=request.form['email'],
                password=request.form['password'],
                is_admin="no"
            )
            session.add(user)
            return try_login(
                request.form['email'],
                request.form['password'],
                render_template("thank_you_for_registering.html")
            )
        except:
            session.rollback()
            return render_template("error.html", email=request.form['email'], error="uh oh... There was a problem registering!")


@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search']
    posts = session.query(Blog).filter(Blog.content.contains(search_term)).all()
    return render_template('search.html', posts=posts, search=search_term)


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5555)
