from flask import Flask, request, jsonify
from dotenv import load_dotenv

from sqlalchemy.exc import IntegrityError

from models import db, User

import os

load_dotenv()

app = Flask(__name__)

# Fetch MySQL root password from docker secret file
with open(os.environ["MYSQL_ROOT_PASSWORD_FILE"]) as f:
    MYSQL_ROOT_PASSWORD = f.read().splitlines()[0]

# Initialize MySQL
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql://root:{MYSQL_ROOT_PASSWORD}@db:3306/{os.environ['MYSQL_DATABASE']}"
)

with app.app_context():
    db.init_app(app)
    db.create_all()


@app.route("/")
def home():
    """Test function for default flask route"""
    return "Flask is working fine!"


@app.route("/create_user", methods=["POST"])
def create_user():
    """Create a new user in the database consisting of user id and user name

    User is created when a post request to the following URL is made (Assuming NGINX is running on port 80):
    localhost:80/create_user?userid=<UserID>&username=<Username>"

    Will complain to sender if <UserID> already exists in database
    """
    userid = request.args.get("userid", None)
    username = request.args.get("username", None)

    if not userid or not username:
        return jsonify(
            {
                "message": f"Please provide userid and username. Got {userid} and {username}"
            }
        )

    try:
        user = User(userid=userid, username=username)
        db.session.add(user)
        db.session.commit()

        return jsonify(
            {
                "message": "User creation successful!",
                "user": {
                    "userid": userid,
                    "username": username,
                },
            }
        )
    except IntegrityError:
        # TODO: Do not return HTTP 200 code
        return jsonify({"message": "User already exists!"})


@app.route("/get_user", methods=["GET"])
def get_user():
    """Return the information about a user by its ID

    User is queried when a get request to the following URL is made (Assuming NGINX is running on port 80):
    localhost:80/get_user?userid=<UserID>"
    """
    userid = request.args.get("userid", None)

    user = User.query.get_or_404(userid)
    return jsonify(
        {
            "user": {
                "userid": user.userid,
                "username": user.username,
            }
        }
    )
