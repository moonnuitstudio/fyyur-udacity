import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:2098@localhost:5432/fyyur_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False