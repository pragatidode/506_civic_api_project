#!/usr/local/bin/python3

#import register as register
from flask import Flask, render_template, request, redirect,url_for,Blueprint
from flask_wtf import FlaskForm, form
#from login import generate_password_hash
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, InputRequired, length
from civic import find_elections, find_reps, validateAddress
from flask_login import current_user, login_user, login_required, logout_user, LoginManager
from models import db, login, UserModel




class loginForm(FlaskForm):

    email = StringField('Email', [InputRequired(), Length(min=6, max=50)])
    username = StringField('Username', [InputRequired(), Length(min=6, max=50)])
    password = PasswordField(label='Password',validators=[DataRequired(), Length(min=6, max=16)])
    submit = SubmitField(label='Login')

class RegisterForm(FlaskForm):

    email = StringField('Email', [InputRequired(), length(max=50)])
    username = StringField('Username', [InputRequired(), length(max=50)])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=16)])
    address = StringField('Address', [InputRequired()])
    submit = SubmitField(label='Register')

class ChangeAddressForm(FlaskForm):
    address = StringField('Address', [InputRequired()])
    submit = SubmitField(label='Update')

app=Flask(__name__)
app.secret_key='a secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)
login.login_view = 'login'




@app.before_first_request
def create_table():
    db.create_all()
    

@app.route('/')
def baseSite():
    return redirect("/login")

@app.route('/home')
def homepage():
    return render_template('home.html')
    
@app.route('/civic')
@login_required
def civic():
	address = current_user.address
	repdata=find_reps(address)
	officials = repdata["officials"]
	offices = repdata["offices"]
	return render_template('civic.html', address=address, election_data=find_elections(address), officials=officials, offices=offices)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/civic')
    form=RegisterForm()
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        pw = request.form["password"]
        address = request.form["address"]
        existinguser = UserModel.query.filter_by(username=username).first()
        if existinguser is None:
            response = validateAddress(address)
            validaddress = False
            for item in response['results']:
                if(item['geometry']['location_type']!= 'APPROXIMATE'):
                    user = UserModel(email, username, pw, address)
                    db.session.add(user)
                    db.session.commit()
                    validaddress = True
                    return redirect('/civic')
            if(not validaddress):
               return render_template('register.html', form=form)
        else:
            return render_template('login.html', form=form)
    else:
        return render_template('register.html', form=form)

            
@app.route('/login',methods=["POST", "GET"])
def login():
    print("TEST")
    if current_user.is_authenticated:
        return redirect('/civic')
    form=loginForm()

    if request.method == "POST":
        username=request.form["username"]
        pw=request.form["password"]
        user = UserModel.query.filter_by(username=username).first()
        print(user)
        if user is not None and user.check_password(pw):
            print("HEY I am good")
            login_user(user)
            return redirect('/civic')
        else:
            print("FAILED")
            return render_template('login.html',form=form)
    else:
        return render_template('login.html',form=form)

@app.route('/change_address', methods=['GET', 'POST'])
def change_address():
    if current_user.is_authenticated == False:
        return redirect('/login')
    form=ChangeAddressForm()
    if request.method == "POST":
        address = request.form["address"]
        response = validateAddress(address)
        validaddress = False
        for item in response['results']:
            if(item['geometry']['location_type']!= 'APPROXIMATE'):
                current_user.address = address
                db.session.commit()
                validaddress = True
                return redirect('/civic')
        if(not validaddress):
               return render_template('change_address.html', form=form)
    else:
        return render_template('change_address.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/home')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)




