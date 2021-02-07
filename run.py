from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e6040f19d063c7ea55a33765df99277c'
app.config["MONGO_URI"] = "mongodb+srv://Ayush:mongodb@cluster0.0ngc1.mongodb.net/Qoura-ML"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
db_users = mongo.db.User
db_question = mongo.db.Question
db_answer = mongo.db.Answers

@app.route('/create')
def create():
    new_user = {'Name' : 'xyz', 'Age' : 20}
    db_users.insert_one(new_user)
    #print(user['Name'],'Created successfully')
    result = {'result' : 'Created successfully'}
    return result

if __name__ == "__main__":
    app.run(debug=True)
