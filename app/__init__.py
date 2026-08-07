from flask import Flask
from config import Config, mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)

    from app.routes.home import home_bp
    from app.routes.booking import booking_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(booking_bp)

    return app