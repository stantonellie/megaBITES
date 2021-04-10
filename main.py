from flask import Flask, render_template_string
from sqlalchemy import create_engine, MetaData

app = Flask(__name__)
app.config["SECRET_KEY"] = "SETIBagem"
app.config["BLOGGING_SITEURL"] = "http://localhost:8000"
app.config["BLOGGING_SITENAME"] = "megaBITES"
app.config["BLOGGING_KEYWORDS"] = ["blog", "food"]

engine = create_engine('sqlite:////tmp/blog.db')
meta = MetaData()


@app.route("/")
def index():
    return render_template_string(
        """
        <!DOCTYPE html>
        <html>
            <head></head>
            <body>
                <h1>megaBITES</h1>
            </body>
        </html>
        """
    )


if __name__ == "__main__":
    app.run(debug=True, port=8000, use_reloader=True)
