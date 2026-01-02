from flask import Flask
from app.core.server import core_bp
from app.usecases.usecase import usecase_bp

def create_app():

    app = Flask(__name__)

    @app.route("/", methods=["GET", "HEAD"])
    def health():
        return {"status": "ok"}, 200
    
    app.register_blueprint(
        core_bp,
        url_prefix="/notification-handler"
    )
    app.register_blueprint(
        usecase_bp,
        url_prefix="/notification-handler"
    )

    return app
