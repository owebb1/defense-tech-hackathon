


from flask import Flask

app = Flask(__name__)
from app import views

# Import views at the end to avoid circular imports
