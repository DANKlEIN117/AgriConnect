from flask import Flask
from config import Config
from extensions import db, migrate, jwt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # import models so migrations can detect them
    with app.app_context():
        from models import user, farmer, cooperative, buyer, produce

    # register blueprints
    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    @app.route("/")
    def home():
        return {"message": "Welcome to AgriConnect API 🚀"}
    
    from routes.produce_routes import produce_bp
    app.register_blueprint(produce_bp)

    




    return app

    


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
