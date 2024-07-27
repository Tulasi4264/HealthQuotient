from flask import Blueprint,render_template,request,flash,redirect,url_for,jsonify
from .models import User,Meal,Symptom,db,CombinedData
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user,current_user
from website import db
from mlxtend.frequent_patterns import fpgrowth,association_rules

auth=Blueprint('auth',__name__)





@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        joined_table_data = db.session.query(Meal.meal_name, Symptom.symptom_name) \
        .join(Symptom, Meal.user_id == Symptom.user_id).all()
        print(joined_table_data)
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in suucessfully',category='success')
                login_user(user,remember=True)
                return render_template('title.html')
            else:
                flash('incoorect password or email',category='error')
        
    return render_template("login.html")


@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        email=request.form.get('email')
        username=request.form.get('username')
        password=request.form.get('password')
        
        user=User.query.filter_by(email=email).first()
        if user:
            flash("user already exits",category='error')

        if len(email)<4:
            flash("email must be greater than 4 char",category='error')
        elif len(username)<2:
            flash("username must be greater than 2 char",category='error')

        elif len(password)<7:
            flash("security issue with ur pass",category='error')

        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user,remember=True)
            flash("account created",category='success')
            return redirect(url_for('views.home'))
            
    return render_template("signup.html")
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

        

