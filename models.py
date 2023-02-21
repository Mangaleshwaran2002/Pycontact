# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin,current_user
# from flask_admin.contrib.sqla import ModelView
# from flask_admin import AdminIndexView
# from flask import redirect,url_for,flash



# db=SQLAlchemy()
# class Contact(db.Model):
#     __tablename__ = "contact"
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
#     firstname=db.Column(db.String(),nullable=False)
#     lastname=db.Column(db.String(),nullable=True)
#     phonenumber=db.Column(db.String(15),nullable=False)
#     email=db.Column(db.String(),nullable=True)
#     gender=db.Column(db.String(1),nullable=False)
    





# class User(UserMixin,db.Model):
#     __tablename__ = "user"
#     id = db.Column(db.Integer, primary_key=True)
#     username=db.Column(db.String(50),unique=True)
#     email=db.Column(db.String(200),unique=True)
#     password=db.Column(db.Text,unique=True)
#     is_admin=db.Column(db.Boolean,default=False)
#     is_verified=db.Column(db.Boolean,default=False)

#     contacts = db.relationship(
#         Contact,
#         backref="user",
#         cascade="all, delete, delete-orphan",
#         single_parent=True,
#         # order_by="desc(contact.timestamp)",
#     )


# class MyModelView(ModelView):

#     def is_accessible(self):
#         return current_user.is_admin
#         # return True

# class MyAdminModelView(AdminIndexView):

#     def is_accessible(self):
#         return current_user.is_admin
#         # return True

#     def inaccessible_callback(self, name, **kwargs):
#         flash("you are not an admin.Admin page is only accessible to admins","error")
#         return redirect(url_for('views.contacts'))


# Made with ❤ By mangal

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask import redirect,url_for,flash
db=SQLAlchemy()




class User(UserMixin,db.Model):
    ___tablename__='user'

    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50),unique=True)
    email=db.Column(db.String(200),unique=True)
    password=db.Column(db.Text,unique=True)
    verified=db.Column(db.Boolean, default=False)
    is_admin=db.Column(db.Boolean, default=False)
    contacts = db.relationship('Contact', cascade="all,delete", backref='user')

    def is_active():
        return True

class Contact(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    id=db.Column(db.Integer, primary_key=True)
    firstname=db.Column(db.String(),nullable=False)
    lastname=db.Column(db.String(),nullable=True)
    phonenumber=db.Column(db.String(15),nullable=False)
    email=db.Column(db.String(),nullable=True)
    gender=db.Column(db.String(1),nullable=False)



class MyModelView(ModelView):

    def is_accessible(self):
        return current_user.is_admin
        # return True

class MyAdminModelView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_admin
        # return True

    def inaccessible_callback(self, name, **kwargs):
        flash("you are not an admin.Admin page is only accessible to admins","error")
        return redirect(url_for('views.contacts'))