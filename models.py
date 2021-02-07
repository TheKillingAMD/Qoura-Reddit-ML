# from manager import db, login_manager, app
# from flask_login import UserMixin
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


# class User(db.Document):
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(1000), nullable=False)
#     profile_pic = db.Column(db.String(100))
#     authenticity = db.Column(db.Boolean)

#     # def get_reset_token(self, expires_sec=600):
#     #     s = Serializer(app.config['SECRET_KEY'], expires_sec)
#     #     return s.dumps({'user_id': self.id}).decode('utf-8')

#     # @staticmethod
#     # def verify_reset_token(token):
#     #     s = Serializer(app.config['SECRET_KEY'])
#     #     try:
#     #         user_id = s.loads(token)['user_id']
#     #     except:
#     #         return None
#     #     return User.query.get(user_id)

#     # def __repr__(self):
#     #     return f"User('{self.username}','{self.email}')"


# class Question(db.Document):
#     site = db.Column(db.String(100),nullable=False)
#     username = db.Column(db.String(50), nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     image_file = db.Column(db.String(20), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     users = db.relationship(User)
    
#     def __repr__(self):
#         return f"Password('{self.id}','{self.site}','{self.username}','{self.password}','{self.image_file})"
