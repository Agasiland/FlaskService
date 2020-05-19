from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/FlaskDB"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70))
    email = db.Column(db.String(120))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def home():
    return "This is home page"


@app.route('/users', methods=['POST', 'GET'])
def handle_users():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_user = User(username=data['username'], email=data['email'])
            db.session.add(new_user)
            db.session.commit()
            return {"message": f"new user {new_user.username} added"}
        else:
            return {"error": "the request is not json format"}
    elif request.method == 'GET':
        users = User.query.all()
        results = [
            {
                "username": user.username,
                "email": user.email
            } for user in users]
        return {"count": len(results), "users": results}


@app.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id):
    user_by_id = User.query.get_or_404(user_id)
    if request.method == "GET":
        response = {
            "username": user_by_id.username,
            "email": user_by_id.email
        }
        return {"message": "success", "user": response}
    elif request.method == "PUT":
        data = request.get_json()
        user_by_id.username = data['username']
        user_by_id.email = data['email']
        db.session.add(user_by_id)
        db.session.commit()
        return {"message": f"User {user_by_id.username} successfully updated."}
    elif request.method == "DELETE":
        db.session.delete(user_by_id)
        db.session.commit()
        return {"message": f"User {user_by_id.username} successfully deleted."}


if __name__ == "__main__":
    app.run(port=4996)
