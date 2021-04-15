from flask import Flask, render_template_string
from sqlalchemy import create_engine

app = Flask(__name__)

engine = create_engine( "mysql://admin1:@GitPa$$w0rd#@54.74.234.11/team_404?charset=utf8mb4" )
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin1:@GitPa$$w0rd#@54.74.234.11/team_404'

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
