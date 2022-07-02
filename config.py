import bcrypt
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


# Inisiasi object Flask
app = Flask(__name__)

# inisiasi tempat sqlite file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# inisiasi object sql alchemy
db = SQLAlchemy(app)

# Inisiasi object flask restful
api = Api(app)

# Inisiasi object flask cors
cors = CORS(app)
