from flask import Blueprint,render_template,request,redirect,url_for,flash
from models import Contact,db
from flask_login import login_required,current_user

views=Blueprint('views',__name__)



@views.route('/')
@login_required
def contacts():
        contacts=Contact.query.filter_by(user_id =current_user.id).order_by("firstname").all()
        mode = request.cookies.get('mode')
        # print(contacts)
        return render_template('contacts.html',contacts=contacts,mode=mode)


@views.route('/savecontact',methods=['GET', 'POST'])
@login_required
def savecontact():
    mode = request.cookies.get('mode')
    if request.method == 'POST':
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        phonenumber=request.form.get('phonenumber')
        
        email=request.form.get('email')
        gender=request.form.get('gender')
        print("gender:",gender)
        if (gender == 'm'):
            if( len(firstname)>3 and len(phonenumber)==10 ):
            # phonenumber='+91'+phonenumber
                contact=Contact(user_id=current_user.id,firstname=str(firstname),lastname=str(lastname),phonenumber=phonenumber,email=email,gender=True)
                db.session.add(contact)
                db.session.commit()
                return redirect(url_for('views.contacts'))
            else:
                flash('please provide a valid inputs and phone number must contains 10 digit number only','error')
                return redirect(url_for('views.savecontact'))
        else:
            if( len(firstname)>3 and len(phonenumber)==10 ):
            # phonenumber='+91'+phonenumber
                contact=Contact(user_id=current_user.id,firstname=str(firstname),lastname=str(lastname),phonenumber=phonenumber,email=email,gender=False)
                db.session.add(contact)
                db.session.commit()
                return redirect(url_for('views.contacts'))
            else:
                flash('please provide a valid inputs and phone number must contains 10 digit number only','error')
                return redirect(url_for('views.savecontact'))
        
    return render_template('savecontact.html',mode=mode)

@views.route('/delete/<int:id>')
def deletecontact(id):
    contact=Contact.query.filter_by(id=id).first()
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('views.contacts'))


@views.route('/updatecontact/<int:id>',methods=['GET','POST'])
def updatecontact(id):
    mode = request.cookies.get('mode')
    contact=Contact.query.filter_by(id=id).first()
    if request.method == 'POST':
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        phonenumber=request.form.get('phonenumber')
        email=request.form.get('email')
        gender=request.form.get('gender')
        print("gender:",gender)
        if (gender == 'm'):
            if( len(firstname)>3 and len(phonenumber)==10):
                contact.firstname=firstname
                contact.lastname=lastname
                contact.phonenumber=phonenumber
                contact.email=email
                contact.gender=True
                db.session.add(contact)
                db.session.commit()
                return redirect(url_for('views.contacts'))
            else:
                flash('please provide a valid inputs and phone number must contains 10 digit number only','error')
                return redirect(url_for('views.updatecontact',id=id))
        elif (gender == 'f'):
            if(len(firstname)>3 and len(phonenumber)==10):
                contact.firstname=firstname
                contact.lastname=lastname
                contact.phonenumber=phonenumber
                contact.email=email
                contact.gender=False
                db.session.add(contact)
                db.session.commit()
                return redirect(url_for('views.contacts'))
            else:
                flash('please provide a valid inputs and phone number must contains 10 digit number only','error')
                return redirect(url_for('views.updatecontact',id=id))
        else:
            pass
    return render_template('updatecontact.html',contact=contact,mode=mode)




# Made with ❤ By mangal