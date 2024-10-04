from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from . import config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_object=config):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_object)

    # initialize
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # blueprints
    from .routes import main

    app.register_blueprint(main)

    # Create db + tables
    # Must appear after db init and blueprint registration.
    with app.app_context():
        db.create_all()

    # error handlers
    @app.errorhandler(401)
    def internal_error(error):
        return render_template("errors/401.html", title="Unauthorized Access"), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html", title="Page not found"), 404

    @app.errorhandler(405)
    def page_not_found(error):
        return render_template("errors/405.html", title="Method Not Allowed"), 405

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("errors/500.html", title="Internal Server Error"), 500

    return app
