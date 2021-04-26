from flask import Flask, request, session, redirect, url_for
from flask_pymongo import PyMongo, ObjectId
from flask.json import JSONEncoder
from bson import ObjectId
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_cors import CORS
from functools import wraps
from werkzeug.utils import secure_filename
from PIL import Image
import os
import cloudinary
import cloudinary.uploader as up
import json
import jwt
from datetime import date, timedelta, datetime
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (
    create_refresh_token, create_access_token, jwt_required, get_jwt_identity, get_jwt)
from final import get_result
import random


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'e6040f19d063c7ea55a33765df99277c'
app.config["MONGO_URI"] = "mongodb+srv://Ayush:mongodb@cluster0.0ngc1.mongodb.net/Qoura-ML"
app.config['JWT_ALGORITHM'] = 'HS512'
app.config['UPLOAD_FOLDER'] = 'static/images/'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
test_jwt = JWTManager(app)
app.json_encoder = JSONEncoder
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
db_users = mongo.db.User
db_question = mongo.db.Question
db_answer = mongo.db.Answers


def upload_to_cloudinary(file):
    cloudinary.config(api_key="375383943137763",
                      api_secret="LRxVIl_5DuDgMc-3twcxHxYNkfs",
                      cloud_name="thekillingamd")
    r = up.upload(file)
    return r['url'].replace('http:', 'https:')


def ml_file_maker(question, answer):
    f = open("question.txt", 'w')
    f.write(question)
    f = open("answer.txt", 'w')
    f.write(answer)


@app.route("/")
@app.route("/home")
def home():
    questions = list()
    for question in db_question.find():
        user_id = str(question["user_id"])
        user = db_users.find_one({"_id": ObjectId(user_id)})
        qid = str(question["_id"])
        # answer = db_answer.find_one({"question_id": qid})
        # if (answer == None):
        #     questions.append({'Question_Id': str(question["_id"]),
        #                       'Question': question["Question"],
        #                       'User': user["Username"]
        #                     #   'Answer': "No Answer Available"
        #                       })
        # else:
        questions.append({'Question_Id': str(question["_id"]),
                          'Question': question["Question"],
                          'User': user["Username"]
                          #   'Answer': answer["answer"]
                          })
    random.shuffle(questions)
    return {'questions': questions}


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return {'result': 'Login Page'}
    if request.method == 'POST':
        email = request.json.get("email")
        password = request.json.get("password")
        try:
            user = db_users.find_one({'Email': email})
            correct_pass = user["Password"]
            if bcrypt.check_password_hash(correct_pass, password):
                userId = str(user['_id'])
                accessToken = create_access_token(
                    identity=email, expires_delta=None, additional_claims={'user': userId})
                print({'result': 'Login Successfully',
                       'accessToken': accessToken, "email": email})
                return {'result': 'Login Successfully', "accessToken": accessToken, "email": email, "avatarURL": user["Profile Picture"], "name": user['Username']}
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
        print(request.files)

        # This is when Front End is made and we can upload pictures
        image = request.files['image']
        if image.filename != '':
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            foo = Image.open(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))
            foo = foo.resize((100, 100), Image.ANTIALIAS)
            foo.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename), quality=95)
            img_url = upload_to_cloudinary(
                app.config['UPLOAD_FOLDER']+filename)
        else:
            img_url = 'https://res.cloudinary.com/thekillingamd/image/upload/v1612692376/Profile%20Pictures/hide-facebook-profile-picture-notification_q15wp8.jpg'
        authenticity = 0
        print(img_url)
        data = {
            "Username": username,
            "Email": email,
            "Password": password,
            "Profile Picture": img_url,
            "Authenticity": 0
        }
        result = db_users.insert_one(data)
        accessToken = create_access_token(
            identity=email, expires_delta=None, additional_claims={'user': str(result.inserted_id)})
        return {'result': 'Created successfully', "accessToken": accessToken, "email": email, "avatarURL": img_url, "name": username}


@app.route('/add_question', methods=['GET', 'POST'])
@jwt_required()
def add_question():
    if request.method == 'GET':
        return {'result': 'Question Adding Page'}
    if request.method == 'POST':
        question = request.json.get("question")
        user_id = get_jwt()['user']

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


# @token_required
@app.route('/add_answer/<qid>', methods=['GET', 'POST'])
@jwt_required()
def add_answer(qid):
    # if 'user_id' in session and session['user_id'] is not None:
    if request.method == 'GET':
        question = db_question.find_one({"_id": ObjectId(qid)})
        print(question)
        quest = {'Question': question["Question"]}
        return quest

    if request.method == 'POST':
        question_id = qid
        user_id = get_jwt()['user']
        answer = request.form.get('answer')

        if db_answer.find_one({'user_id': user_id, 'question_id': qid}) != None:
            return {'Error': 'User Already Added Answer'}

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
# else:
#     return redirect(url_for('login'))


@app.route("/question/<qid>")
def question(qid):
    answers = list()
    questions = ""
    users = []
    answers = []
    ans_ml = []
    scores = []
    if db_answer.find({"question_id": qid}) != None:
        for answer in db_answer.find({"question_id": qid}):
            question = db_question.find_one({"_id": ObjectId(qid)})
            q_user = db_users.find_one({"_id": ObjectId(question['user_id'])})
            question = [question["Question"], q_user['Username']]
            user_id = answer["user_id"]
            user = db_users.find_one({"_id": ObjectId(user_id)})
            userAvatarURL = user["Profile Picture"]
            user = user["Username"]
            ans = answer["answer"]
            # answer = db_answer.find_one({"question_id": qid})
            # if (answer == None):
            #     questions.append({'Question_Id': str(question["_id"]),
            #                       'Question': question["Question"],
            #                       'User': user["Username"]
            #                     #   'Answer': "No Answer Available"
            #                       })
            # else:
            # questions.append(question)
            users.append([user, userAvatarURL])
            ans_ml.append(ans)
        value = get_result(question[0], ans_ml)
        for score in value:
            scores.append(str(score[0]))
        final = list(sorted(zip(scores, users, ans_ml)))
        print(final)

        # print(list(zipped))
        return {'Question': question, 'Answer': final}
    else:
        return {'Answer':  "No Answer"}


if __name__ == "__main__":
    app.run(debug=True)
