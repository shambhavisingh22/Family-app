from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from flask import Flask
import lib.log as log
import logging
from config import config, APP_NAME
from flask import jsonify
from lib.flask_email import *

Logger = logging.getLogger(APP_NAME)

db = SQLAlchemy()
mail= Mail()

def initialize_db(app):
    db.init_app(app)
    import models
    import family.finfo.members.models_members  #Importing all the models
    import family.meminfo.models_meminfo
    migrate = Migrate(app, db)


def create_app(config_name):
    app = Flask(__name__)
    CORS(app,resources={r"":{"origins":""}})
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    log.setup_logging(config[config_name])

    initialize_db(app)
    mail.init_app(app)



    return app
