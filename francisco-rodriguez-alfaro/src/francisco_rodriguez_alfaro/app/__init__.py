from flask import Flask
from .routes import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp)

