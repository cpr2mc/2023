from flask import Flask

def create_app():
    app = Flask(__name__)
    # Configuration, Blueprints, Database Initialization, etc.

    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    
    return app
