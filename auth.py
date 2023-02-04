from flask import Blueprint,render_template,redirect,url_for,request,flash
from models import User,db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager,login_user,current_user,logout_user,login_required


login_manager=LoginManager()
login_manager.login_view="auth.login"
login_manager.login_message="Please log in to access this page. "
login_manager.login_message_category="error"



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# @login_manager.unauthorized_handler
# def handle_needs_login():
#     #instead of using request.path to prevent Open Redirect Vulnerability 
#      next=url_for(request.endpoint)
#      print('next_path:',next)
#      return redirect(url_for('auth.login', next=next))



Auth=Blueprint('auth',__name__)

@Auth.route('/')
@login_required
def auth():
    # return redirect(url_for('auth.login'))
    return str(current_user.username)+":"+str(current_user.id)


@Auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        passwd=request.form.get('passwd')
        confirmed_passwd=request.form.get('confirmed_passwd')
        if((email!='') and (passwd!='') and (confirmed_passwd!='')):
            user=User.query.filter_by(email=email).first()
            if user:
                
                    if(check_password_hash(pwhash=user.password,password=passwd)):
                        login_user(user,remember=True)
                        return redirect(url_for('views.contacts'))
                    else:
                        flash('password is incorrect', 'error')
                        return redirect(url_for('auth.auth'))
                
            else:
                flash('Please create an account.','error')
                return redirect(url_for('auth.signup'))
        else:
            flash('please fill all the fields', 'error')
            return redirect(url_for('auth.login'))
    mode = request.cookies.get('mode')
    return render_template('login.html',mode=mode)

@Auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username=request.form.get('username')
        email=request.form.get('email')
        passwd=request.form.get('passwd')
        confirmed_passwd=request.form.get('confirmed_passwd')
        if((username!='') and (email!='') and (passwd!='') and (confirmed_passwd!='')):
            user=User.query.filter_by(email=email).first()
            if (user==None):
                if(passwd == confirmed_passwd):
                    user=User(username=username,email=email,password=generate_password_hash(passwd))
                    db.session.add(user)
                    db.session.commit()
                    flash('account created successfully.','success')
                    login_user(user=user)
                    return redirect(url_for('views.contacts'))
                else:
                    flash('password and confirmed password is miss matching', 'error')
                    return redirect(url_for('auth.signup'))
            else:
                flash('email address is already signuped', 'error')
                return redirect(url_for('auth.signup'))
                
        else:
            flash('please fill all the fields', 'error')
            return redirect(url_for('auth.signup'))

    mode = request.cookies.get('mode')
    return render_template('signup.html',mode=mode)

@Auth.route('/user',methods=['GET','POST'])
@login_required
def edit_user():
    mode = request.cookies.get('mode')
    if request.method == 'POST':
        user=User.query.filter_by(id=current_user.id).first()
        user.username=request.form.get('username')
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('views.contacts'))
    # return redirect(url_for('auth.login'))
    return render_template('editUser.html',mode=mode)

@Auth.route('/del_user',methods=['GET','POST'])
@login_required
def delete_user():
    user=User.query.filter_by(id=current_user.id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('auth.logout'))


@Auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.auth'))



# Made with ❤ By mangal