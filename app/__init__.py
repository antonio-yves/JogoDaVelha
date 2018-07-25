from flask import Flask
from os import urandom

app = Flask(__name__)

app.secret_key = urandom(24)

from app import views
