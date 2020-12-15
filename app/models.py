from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))
    idea = db.relationship('Comments', backref='author', lazy='dynamic')
    
    def __repr__(self):
        return f'User {self.username}'
   
    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute')
    
    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)
    
    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)
   
    def __repr__(self):
        return f'User {self.username}'



class Blog(UserMixin,db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key = True)
    blog_name = db.Column(db.String(255),index = True)
    # blog_email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    description = db.Column(db.String(255), index=True)
    idea_title = db.Column(db.String(255), index=True)
    # bio = db.Column(db.String(255))
    # profile_pic_path = db.Column(db.String())
    # blog_pass_secure = db.Column(db.String(255))
    
    # @property
    # def password(self):
    #     raise AttributeError('You cannot read the password attribute')

    # @password.setter
    # def password(self, password):
    #     self.blog_pass_secure = generate_password_hash(password)


    # def verify_password(self,password):
    #     return check_password_hash(self.blog_pass_secure,password)
    
    def __repr__(self):
        return f'User {self.username}'
    


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")
    
    def __repr__(self):
        return f'User {self.name}'
    
class Comments(db.Model):
    
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(255))
    idea_id = db.Column(db.Integer, db.ForeignKey("idea.id"))
    date = db.Column(db.DateTime(250), default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comment(cls,id):
        comments = Comments.query.filter_by(idea_id=id).all()
        
        return comments
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def __repr__(self):
        return f"Comments('{self.comment}', '{self.date}')"
    
class Idea(db.Model):
    __tablename__= 'idea'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    idea = db.Column(db.String(255))
    date = db.Column(db.DateTime(250), default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship('Comments', backref='title', lazy='dynamic')

    def save_idea(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_idea(cls,cate):
        idea = idea.query.filter_by(category=cate).all()
        return idea
    
    @classmethod
    def get_all_idea(cls):
        idea = Idea.query.order_by('-id').all()
        return idea

    def __repr__(self):
        return f'Posts {self._title}'