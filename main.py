from flask import Flask, redirect
from sqlalchemy import create_engine, MetaData
from flask_login import UserMixin, LoginManager, login_user, logout_user
from flask_blogging import SQLAStorage, BloggingEngine

app = Flask(__name__)
app.config["SECRET_KEY"] = "SETIBagem"
app.config["BLOGGING_URL_PREFIX"] = "/"
app.config["BLOGGING_SITEURL"] = "http://localhost:8000"
app.config["BLOGGING_SITENAME"] = "megaBITES"
app.config["BLOGGING_KEYWORDS"] = ["blog", "food"]

engine = create_engine('sqlite:////tmp/blog.db')
meta = MetaData()
sql_storage = SQLAStorage(engine, metadata=meta)
blog_engine = BloggingEngine(app, sql_storage)
login_manager = LoginManager(app)
meta.create_all(bind=engine)

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
    def get_name(self):
        return "Ellie Stanton" # TODO: fetch from the database

@login_manager.user_loader
@blog_engine.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/login/")
def login():
    user = User("testuser") # TODO: login using password from the database
    login_user(user)
    return redirect("/")

@app.route("/logout/")
def logout():
    logout_user()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000, use_reloader=True)