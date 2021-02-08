from flask import Flask, request, session
from flask_pymongo import PyMongo, ObjectId
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import os
import cloudinary
import cloudinary.uploader as up
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e6040f19d063c7ea55a33765df99277c'
app.config["MONGO_URI"] = "mongodb+srv://Ayush:mongodb@cluster0.0ngc1.mongodb.net/Qoura-ML"
app.config['UPLOAD_FOLDER'] = 'static/images/'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
db_users = mongo.db.User
db_question = mongo.db.Question
db_answer = mongo.db.Answers


def upload_to_cloudinary(file):
    cloudinary.config(api_key="375383943137763",
                      api_secret="LRxVIl_5DuDgMc-3twcxHxYNkfs",
                      cloud_name="thekillingamd")
    r = up.upload(file)
    return r['url'].replace('http:', 'https:')

# class User:
#     def __init__(self, username):
#         self.username = username

#     @staticmethod
#     def is_authenticated():
#         return True

#     @staticmethod
#     def is_active():
#         return True

#     @staticmethod
#     def is_anonymous():
#         return False

#     def get_id(self):
#         return self.username

#     @staticmethod
#     def check_password(password_hash, password):
#         return check_password_hash(password_hash, password)


#     @login.user_loader
#     def load_user(username):
#         u = mongo.db.Users.find_one({"Name": username})
#         if not u:
#             return None
#         return User(username=u['Name'])

@app.route("/")
@app.route("/home")
def home():
    if 'user_id' in session and session['user_id'] is not None:
        questions = {}
        for question in db_question.find():
            user_id = question["user_id"]
            user = db_users.find_one({"_id": ObjectId(user_id)})
            questions['question'] = {'Question': question["Question"],
                                    'User': user["Username"]
                                    }
        return questions
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return {'result': 'Login Page'}
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            user = db_users.find_one({'Email': email})
            correct_pass = user["Password"]
            if bcrypt.check_password_hash(correct_pass, password):
                session['user_id'] = str(user["_id"])
                return {'result': 'Login Successfully'}
            else:
                return {'result': 'Wrong Password'}
        except:
            return {'result': 'No Such User Found'}


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return {'result': 'Registration Page'}
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        password = bcrypt.generate_password_hash(password).decode('utf-8')

        # This is when Front End is made and we can upload pictures
        # profile_picture = request.files['img']
        # if img.filename != '':
        #     filename = secure_filename(img.filename)
        #     img.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        #     img_url = upload_to_cloudinary(current_app.config['UPLOAD_FOLDER']+filename)
        # else:
        img_url = 'https://res.cloudinary.com/thekillingamd/image/upload/v1612692376/Profile%20Pictures/hide-facebook-profile-picture-notification_q15wp8.jpg'
        authenticity = 0
        data = {
            "Username": username,
            "Email": email,
            "Password": password,
            "Profile Picture": img_url,
            "Authenticity": 0
        }
        db_users.insert_one(data)
        return {'result': 'Created successfully'}


@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if 'user_id' in session and session['user_id'] is not None:
        if request.method == 'GET':
            return {'result': 'Question Adding Page'}
        if request.method == 'POST':
            user_id = session['user_id']
            question = request.form.get("question")

            # This is when Front End is made and we can upload pictures
            # profile_picture = request.files['img']
            # if img.filename != '':
            #     filename = secure_filename(img.filename)
            #     img.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            #     img_url = upload_to_cloudinary(current_app.config['UPLOAD_FOLDER']+filename)
            # else:
            # img_url = 'https://res.cloudinary.com/thekillingamd/image/upload/v1612692376/Profile%20Pictures/hide-facebook-profile-picture-notification_q15wp8.jpg'

            data = {
                "user_id": user_id,
                "Question": question,
            }
            db_question.insert_one(data)
            return {'result': 'Question Added successfully'}


if __name__ == "__main__":
    app.run(debug=True)
