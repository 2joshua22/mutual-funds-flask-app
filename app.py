from flask import Flask,render_template,jsonify,url_for,redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import requests
import confidential

app=Flask(__name__)
app.config['SECRET_KEY']=confidential.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI']=confidential.SQLALCHEMY_DATABASE_URI

db=SQLAlchemy(app)
app.app_context().push()

class User(db.Model):
    __tablename__="userdb"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    phone=db.Column(db.Integer)
    email=db.Column(db.String)
    password=db.Column(db.String)

class Mutual(db.Model):
    __tabelname__="mutualdb"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    code=db.Column(db.String)
    nav=db.Column(db.Integer)
    units=db.Column(db.Integer)
    total=db.Column(db.String)

url=confidential.api_url
response=requests.get(url)
list_data=response.json()

users=User.query.order_by(User.id)
mutuals=Mutual.query.order_by(Mutual.id)

class UserForm(FlaskForm):
    name=StringField("Full Name: ",validators=[DataRequired()])
    phone=IntegerField("Phone Number: ",validators=[DataRequired()])
    email=StringField("Email ID: ",validators=[DataRequired()])
    password=PasswordField("Password: ",validators=[DataRequired()])
    submit=SubmitField("SIGN IN")

class MfForm(FlaskForm):
    mname=StringField("Full Name: ",validators=[DataRequired()])
    code=StringField("Scheme Code: ",validators=[DataRequired()])
    nav=IntegerField("Nav: ",validators=[DataRequired()])
    units=IntegerField("Units: ",validators=[DataRequired()])
    submit=SubmitField("ADD")

@app.route('/',methods=['POST','GET'])
def index():
    form1=UserForm()
    if form1.validate_on_submit():
        name=form1.name.data
        phone=form1.phone.data
        email=form1.email.data
        password=form1.password.data
        user=User(name=name,email=email,phone=phone,password=password)
        db.session.add(user)
        db.session.commit()
    
    form2=MfForm()
    if form2.validate_on_submit():
        mname=form2.mname.data
        code=form2.code.data
        nav=form2.nav.data
        units=form2.units.data
        total=float(nav)*int(units)
        mutual=Mutual(name=mname,code=code,nav=nav,units=units,total=total)
        db.session.add(mutual)
        db.session.commit()
    
    return render_template('index.html',Form1=form1,Form2=form2,Users=users,Mutuals=mutuals,L=list_data)

@app.route('/userdel/<i>')
def userdel(i):
    temp=db.session.execute(db.select(User).filter_by(id=i)).scalar_one()
    db.session.delete(temp)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/mutualdel/<i>')
def mutualdel(i):
    temp=db.session.execute(db.select(Mutual).filter_by(id=i)).scalar_one()
    db.session.delete(temp)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/useredit/<i>',methods=['POST','GET'])
def useredit(i):
    temp=db.session.execute(db.select(User).filter_by(id=i)).scalar_one()
    UserForm.submit=SubmitField("Update")
    form=UserForm()
    if form.validate_on_submit():
        temp.name=form.name.data
        temp.phone=form.phone.data
        temp.email=form.email.data
        temp.password=form.password.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('uedit.html',Form=form,L=list_data)

@app.route('/mutualedit/<i>',methods=['POST','GET'])
def mutualedit(i):
    temp=db.session.execute(db.select(Mutual).filter_by(id=i)).scalar_one()
    MfForm.submit=SubmitField("Update")
    form3=MfForm()
    if form3.validate_on_submit():
        temp.name=form3.mname.data
        temp.code=form3.code.data
        temp.nav=form3.nav.data
        temp.units=form3.units.data
        temp.total=float(temp.nav)*int(temp.units)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('medit.html',Form3=form3,L=list_data)

if __name__=='__main__':
    app.run(debug=True)