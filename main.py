from flask import Flask, render_template
from routes import routes

app = Flask(__name__)
app.register_blueprint(routes, url_prefix="")

if __name__ == "__main__":
    app.run(debug=True)
