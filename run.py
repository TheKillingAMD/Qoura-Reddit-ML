from flask import Flask, request
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
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
    return r['url'].replace('http:','https:')

@app.route('/login', methods=['GET','POST'])    
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            user = db_users.find_one({'Email': email})
            correct_pass = user["Password"]
            if bcrypt.check_password_hash(correct_pass, password):
                return {'result' : 'Login Successfully'}  
            else:
                return {'result' : 'Wrong Password'}         
        except:
            return {'result' : 'No Such User Found'}               

@app.route('/register', methods=['GET','POST'])
def register():
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
            "Username" : username,
            "Email" : email,
            "Password" : password,
            "Profile Picture" : img_url,
            "Authenticity" : 0
        }
        db_users.insert_one(data)
        return {'result' : 'Created successfully'}

if __name__ == "__main__":
    app.run(debug=True)
