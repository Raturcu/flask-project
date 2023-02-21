from flask import Blueprint
from flask import render_template,request,redirect,url_for
from flask import flash
from .models import User
from werkzeug.security import check_password_hash,generate_password_hash
from devapp import db

auth = Blueprint('auth', __name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        
        user=User.query.filter_by(username=username).first()
        
        if user:
            if check_password_hash(user.password,password):
                flash('Welcome,'+" "+username+'!' ,category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorect password',category="error")
        else:
            flash("Username does not exist",category='error')
    
    
    if request.method == 'POST' and 'register_form' in request.form:
        return redirect(url_for('auth.register'))         
    
    return render_template('login.html')
        
    
    

@auth.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form.get('username')
        email=request.form.get('email')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        
        user=User.query.filter_by(username=username).first()
        if user:
            flash(username +"already exist",category='error')
        elif len(str(username)) < 3:
            flash("Username must contains at least 4 characters!",category='error')
        elif len(str(email)) < 5:
            flash("Email adress must contains at least 5 characters!",category='error')
        elif password1 != password2:
            flash("Password don't match",category='error')
        elif len(str(password1))< 8:
            flash("Password must be at least 8 characters",category='error')
        else:
            new_user=User(username=username,email=email,password=generate_password_hash(password1,method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created!',category='success')
            return redirect(url_for("auth.home"))
            
    return render_template('register.html')