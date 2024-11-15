from flask import Flask 
from flask import current_app as app 
from flask import render_template
from flask import request,redirect
from backend.models import *
from backend.models import db
from flask import flash,url_for,blueprints,Blueprint
from app import *
from functools import wraps

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")
@app.route('/login', methods=['POST'])
def login_post():
    email=request.form.get('email')
    password=request.form.get("password")
    costumer=Costumer.query.filter_by(email=email,password=password).first()
    
    if not costumer:
        flash('User does not exist')
        return redirect(url_for('login'))
  
    return "hello"
@app.route('/register')
def register():
    return render_template("register.html")
@app.route('/register',methods=['POST'])
def register_post():
    email=request.form.get('email')
    password=request.form.get('password')
    full_name=request.form.get('full_name')
    pincode=request.form.get('pincode')
    address=request.form.get('add')
    if email=='' or password=='':
        flash("Email or password cannot be empty")
        return redirect(url_for('register'))
    if Costumer.query.filter_by(email=email).first():
        flash('User already Exist')
        return redirect(url_for('register'))
    costumer=Costumer(email=email,password=password,full_name=full_name,Address=address,pincode=pincode)
    db.session.add(costumer)
    
    db.session.commit()
    flash('User Successfully Registered')
    return redirect(url_for('login'))