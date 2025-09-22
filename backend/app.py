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
        from models import user, farmer, cooperative, buyer, produce, product

    # register blueprints
    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from routes.produce_routes import produce_bp
    app.register_blueprint(produce_bp, url_prefix="/produce")

    from routes.protected_routes import protected_bp
    app.register_blueprint(protected_bp, url_prefix="/protected")

    from routes.role_routes import role_bp
    app.register_blueprint(role_bp, url_prefix="/roles")

    from routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/admin")

    from routes.product import product_bp
    app.register_blueprint(product_bp, url_prefix="/products")

    @app.route("/")
    def home():
        return {"message": "Welcome to AgriConnect API 🚀"}
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
