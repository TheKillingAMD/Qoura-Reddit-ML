from flask import Flask, request, session, redirect, url_for
from flask_pymongo import PyMongo, ObjectId
from flask.json import JSONEncoder
from bson import ObjectId
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


@app.route("/")
@app.route("/home")
def home():
    questions = {}
    count = 1
    for question in db_question.find():
        user_id = str(question["user_id"])
        user = db_users.find_one({"_id": ObjectId(user_id)})
        qid = str(question["_id"])
        answer = db_answer.find_one({"question_id": qid})
        if (answer == None):
            questions[ int(count) ] = {'Question_Id': str(question["_id"]),
                                 'Question': question["Question"],
                                 'User': user["Username"],
                                 'Answer': "No Answer Available"
                                 }
        else:
            questions[ int(count) ] = {'Question_Id': str(question["_id"]),
                                    'Question': question["Question"],
                                    'User': user["Username"],
                                    'Answer': answer["answer"]
                                    }
        count = count + 1
    return questions


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
    else:
        return redirect(url_for('login'))


@app.route('/update_question/<qid>', methods=['GET', 'POST'])
def update_question(qid):
    if 'user_id' in session and session['user_id'] is not None:
        if request.method == 'GET':
            return {'result': 'Question Update Page'}
        if request.method == 'POST':

            question_id = qid
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

            db_question.update_one({'_id': ObjectId(str(qid))}, {
                                   "$set": {'Question': question}})
            return {'result': 'Question Updated Succesfully'}
    else:
        return redirect(url_for('login'))


@app.route('/add_answer/<qid>', methods=['GET', 'POST'])
def add_answer(qid):
    if 'user_id' in session and session['user_id'] is not None:
        if request.method == 'GET':
            question = db_question.find_one({"_id": ObjectId(qid)})
            print(question)
            quest = {'Question': question["Question"]}
            return quest

        if request.method == 'POST':
            question_id = qid
            user_id = session['user_id']
            answer = request.form.get('answer')

            # This is when Front End is made and we can upload pictures
            # profile_picture = request.files['img']
            # if img.filename != '':
            #     filename = secure_filename(img.filename)
            #     img.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            #     img_url = upload_to_cloudinary(current_app.config['UPLOAD_FOLDER']+filename)
            # else:
            # img_url = 'https://res.cloudinary.com/thekillingamd/image/upload/v1612692376/Profile%20Pictures/hide-facebook-profile-picture-notification_q15wp8.jpg'

            data = {
                "question_id": question_id,
                "user_id": user_id,
                "answer": answer,
            }
            db_answer.insert_one(data)
            return {'result': 'Answer Added successfully'}
    else:
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
