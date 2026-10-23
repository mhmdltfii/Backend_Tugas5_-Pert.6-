from flask import Flask


def create_app():
    app = Flask(__name__)

    from app.routes.v1.category_routes import categories_bp_v1
    from app.routes.v1.item_routes import items_bp_v1

    app.register_blueprint(items_bp_v1)
    app.register_blueprint(categories_bp_v1)

    return app