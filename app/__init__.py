from flask import Flask, Response
from config import Config, mail


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)

    from app.routes.home import home_bp
    from app.routes.booking import booking_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(booking_bp)

    @app.route("/sitemap.xml")
    def sitemap():
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://oluhleresorts.co.za/</loc>
    </url>
</urlset>
"""
        return Response(xml, mimetype="application/xml")

    return app