from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "Logged in successfully"}), 200

    return jsonify({"message": "Invalid username or password"}), 400

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201

    return jsonify({"message": "Invalid username or password"}), 400

@app.route("/user/<int:user_id>", methods=["GET"])
def read_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"username": user.username}), 200
    
    return jsonify({"message": "User not found"}), 404

@app.route("/user/<int:user_id>", methods=["PUT"])
@login_required
def update_user(user_id):
    data = request.get_json()
    new_password = data.get("password")
    user = User.query.get(user_id)
    if user and new_password and current_user.id == user_id:
        user.password = new_password
        db.session.commit()
        return jsonify({"message": f"User {user_id} updated successfully"}), 200
    
    return jsonify({"message": "User not found"}), 404

@app.route("/user/<int:user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)

    if current_user.id != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User {user_id} deleted successfully"}), 200
    
    return jsonify({"message": "User not found"}), 404

@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)