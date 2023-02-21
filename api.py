from models import User,db,Contact
from schema import users_schema,contacts_schema,contact_schema
from apiauth import token_required
from flask import jsonify,request,current_app
from werkzeug.security import generate_password_hash
import jwt
import datetime
from connexion import NoContent

############################ user section #############################

def create_user(UserAccount):
    if request.method == 'POST':
        if((UserAccount.get('username') != None) and (UserAccount.get('email') != None) and (UserAccount.get('password') != None) ):
            username=UserAccount.get('username')
            email=UserAccount.get('email')
            passwd=UserAccount.get('password')
            user=User.query.filter_by(email=email).first()
            if (user == None):
                user=User(username=username,email=email,password=generate_password_hash(passwd))
                db.session.add(user)
                db.session.commit()
                token=jwt.encode({"user":user.username,'exp': datetime.datetime.utcnow() +datetime.timedelta(minutes=3)},current_app.config['SECRET_KEY'])
                return jsonify({
                        "status":"success",
                        "message":{
                        "username":user.username,
                        "email":user.email,
                        "admin":user.is_admin,
                        "token":token.decode('UTF-8')
                        }
                        })
            else:
                return jsonify({"status":"error",
                                "message":"Account is created"}),400 
        else:
            return jsonify({"status":"error",
                            "message":"fill all the fields to create a account"}),400
    else:
        return jsonify({"status":"error",
                        "message":"method is not allowed"}),400






@token_required
def read_all_users(current_user):
    if current_user.is_admin:
        users = User.query.all()
        return users_schema.dump(users)
    else:
        return jsonify({"status":"error",
                        "message":"Error you are not an Admin.So Access denied"}),400



@token_required
def delete_user(current_user,userId):
    if current_user.id == userId:
        user = User.query.filter_by(id=userId).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"status":"success","message":f"Successfully deleted the user {user.username}"}),200
        else:
            return jsonify({"status":"error",
                            "message":"error user is not found"}),400
    else:
        if current_user.is_admin:
            user = User.query.filter_by(id=userId).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                return jsonify({"status":"success","message":f"Successfully deleted the user {user.username}"}),200
            else:
                return jsonify({"status":"error",
                                "message":"error user is not found"}),400
        else:
            return jsonify({"status":"error",
                            "message":"Access denied. Your not an admin"}),400

###################### contact section ################################


@token_required
def get_contact(current_user):
    contacts=Contact.query.filter_by(user_id =current_user.id).all()
    return contacts_schema.dump(contacts)

@token_required
def create_contact(current_user,Phonebook):
    if request.method == 'POST':
        firstname=Phonebook.get('firstname')
        lastname=Phonebook.get('lastname')
        phonenumber=Phonebook.get('phonenumber')
        email=Phonebook.get('email')
        gender=Phonebook.get('gender')
        if(len(str(phonenumber)) == 10):
            contact=Contact(user_id=current_user.id,firstname=str(firstname),lastname=str(lastname),phonenumber=phonenumber,email=str(email),gender=gender)
            db.session.add(contact)
            db.session.commit()
            return contact_schema.dump(contact)
        else:
            return jsonify({"status":"error","message":"Enter a valid phone number"})
    else:
        return jsonify({"status":"error","message":"method is not allowed"})

@token_required
def edit_contact(current_user,Phonebook,contactId):
    if request.method == 'PUT':
        firstname=Phonebook.get('firstname')
        lastname=Phonebook.get('lastname')
        phonenumber=Phonebook.get('phonenumber')
        email=Phonebook.get('email')
        gender=Phonebook.get('gender')
        if(len(str(phonenumber)) == 10):
            contact=Contact.query.filter_by(id=contactId).first()
            if( contact.user_id == current_user.id):
                contact.firstname=firstname
                contact.lastname=lastname
                contact.phonenumber=phonenumber
                contact.email=email
                contact.gender=gender
                db.session.add(contact)
                db.session.commit()
                return contact_schema.dump(contact)
            else:
                return jsonify({"status":"error","message":"You are not a autherized user to edit this"})
        else:
            return jsonify({"status":"error","message":"Enter a valid phone number"})
    else:
        return jsonify({"status":"error","message":"method is not allowed"})



@token_required
def del_contact(current_user,contactId):
    contact =Contact.query.filter_by(id=contactId).first()
    if contact:
        if current_user.is_admin:
            db.session.delete(contact)
            db.session.commit()
            return contact_schema.dump(contact),204
        else:
            if contact.user_id == current_user.id:
                db.session.delete(contact)
                db.session.commit()
                return contact_schema.dump(contact),204
            else:
                return jsonify({"status":"error","message":"Access denied. youare not a authorized user or admin to delete this data"}),400
    else:
        return jsonify({"status":"error","message":"contact is not found"}),400
    # return contacts_schema.dump(contacts)