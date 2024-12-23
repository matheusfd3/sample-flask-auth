from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud"

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
        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)
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
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password, role="user")
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201

    return jsonify({"message": "Invalid username or password"}), 400

@app.route("/user/<int:user_id>", methods=["GET"])
@login_required
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

    if current_user.id != user_id and current_user.role == "user":
        return jsonify({"message": "Unauthorized"}), 403

    if user and new_password:
        hashed_password = bcrypt.hashpw(str.encode(new_password), bcrypt.gensalt())
        user.password = hashed_password
        db.session.commit()
        return jsonify({"message": f"User {user_id} updated successfully"}), 200
    
    return jsonify({"message": "User not found"}), 404

@app.route("/user/<int:user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)

    if current_user.role != "admin":
        return jsonify({"message": "Unauthorized"}), 403

    if current_user.id != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User {user_id} deleted successfully"}), 200
    
    return jsonify({"message": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)