from functools import wraps
import jwt
from flask import request,jsonify,current_app
from models import User
from werkzeug.security import check_password_hash
import datetime

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token=None
        if 'token' in request.args:
            token=request.args.get('token')
            print("token",token)
            try:
                data=jwt.decode(token,current_app.config['SECRET_KEY'])
                # print("data :",data)
                # print("username :",data['user'])
                current_user=User.query.filter_by(username=data['user']).first()
                # print("current_user:",current_user.username)
            except:
                return jsonify({'message':'token is  invalid'}),403
            # return f(current_user,*args, **kwargs)
            return f(current_user,*args, **kwargs)
        else:
            return jsonify({'message':'Token is missing'}),403

        
    return decorated





def login_user(Account):
    if request.method == 'POST':
        if( (Account.get('password') != None) and (Account.get('email') != None)):
            user=User.query.filter_by(email=Account.get('email')).first()
            if not user:
                    return jsonify({
                    "status":"error",
                    "message":"email is not exists"}),401
            else:
                if check_password_hash(pwhash=user.password,password=Account.get('password')):
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
                     return jsonify({
            "status":"error",
            "message":"incorrect password"}),401   
        else:
            return jsonify({
            "status":"error",
            "message":"email/password is missing"
        }),401
    else:
        return jsonify({
            "status":"error",
            "message":"Method is not allowed"
        })