from flask import Flask, render_template
from models import db
from routes import app as routes_app
from config import Config
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize Flask-Migrate
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()  # This can be omitted if using migrations

    app.register_blueprint(routes_app)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
