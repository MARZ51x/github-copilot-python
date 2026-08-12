from flask import Flask

from routes.game import game_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(game_bp)

if __name__ == '__main__':
    app.run(debug=True)