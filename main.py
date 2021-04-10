from flask import Flask, render_template_string
from sqlalchemy import create_engine

app = Flask(__name__)

engine = create_engine('sqlite:////tmp/blog.db')


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
