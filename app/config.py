# Configuration for environment variables can go in here.

import os
from dotenv import load_dotenv

# Required to load .flaskenv, .env.
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

SITE_NAME = "Gaazonify"

# sqlite db path.
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")

# flask, flask-login, wtforms requirement.
# SECRET_KEY = os.urandom(32)
SECRET_KEY = "SECRET_KEY_01"  # use above after development.

# Run Debug Toolbar
RUN_DEBUG_TOOLBAR = False

# Debug toolbar setting
DEBUG_TB_INTERCEPT_REDIRECTS = False

# See generated SQL queries in toolbar.
SQLALCHEMY_RECORD_QUERIES = True
