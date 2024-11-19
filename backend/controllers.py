from flask import Flask ,session
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
    if 'costumer_id' not in session:
        return render_template("index.html")
    return render_template('index.html', csotumer=Costumer.query.get(session['costumer_id']))
@app.route('/login')
def login():
    
    return render_template("login.html")


@app.route('/login',methods=["POST"])
def login_post():
    email = request.form.get('email')
    password = request.form.get("password")
    customer = Costumer.query.filter_by(email=email, password=password).first()
    
    if not customer:
        flash('Either password is wrong or user does not exist')
        return redirect(url_for('login'))
        
   
    session['costumer_id'] = customer.id
    session['user_role'] = customer.role
    
    
    if customer.role == 0: 
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('home_page')) 
    
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

@app.route('/logout')
def logout():
    session.pop('costumer_id', None)
    
@app.route('/profile')
def profile():
    return render_template('profile.html')
@app.route('/admin_dashboard')
def admin_dashboard():
    customers = Costumer.query.filter_by(role=1)
    professionals=Professional.query.all()
    services=Service.query.all()
    return render_template('admin_dashboard.html', customers=customers,professionals=professionals,services=services)

    
    
@app.route('/admin_dashboard/add_service/')
def add_service():
    return render_template('service_form.html') 


    
@app.route('/admin_dashboard/add_service/',methods=['POST'])
def add_service_post():
    def add_service_post():
        if 'costumer_id' not in session or session.get('user_role') != 0:
            flash('Unauthorized access')
        return redirect(url_for('login'))
    
    
        
    name = request.form.get('category')
    description = request.form.get('description')
    price = request.form.get('price')
    time_required = request.form.get('time')
        
       
    if not ([name, price, time_required,description]):
        flash('All fields are required')
        return redirect(url_for('add_service'))
        
    else:
            new_service = Service(
            name=name,
            Description=description,
            price=price,
            time_required=time_required
        )
        
        
    db.session.add(new_service)
    db.session.commit()
        
    flash('Service added successfully')
    return redirect(url_for('admin_dashboard'))
        

     
@app.route('/admin_dashboard/edit_service/<int:service_id>', methods=['GET', 'POST'])
def edit_service(service_id):
    if 'costumer_id' not in session or session.get('user_role') != 0:
        flash('Unauthorized access')
        return redirect(url_for('login'))
    
    service = Service.query.get(service_id)
    
    if request.method == 'POST':
        service.name = request.form.get('category')
        service.Description = request.form.get('description')
        service.price = request.form.get('price')
        service.time_required = request.form.get('time')
        
        try:
            db.session.commit()
            flash('Service updated successfully')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating service')
            return redirect(url_for('admin_dashboard'))
    
    return render_template('edit_service.html', service=service)

@app.route('/admin_dashboard/delete_service/<int:service_id>', methods=['POST'])
def delete_service(service_id):
    if 'costumer_id' not in session or session.get('user_role') != 0:
        flash('Unauthorized access')
        return redirect(url_for('login'))
    
    service = Service.query.get(service_id)
    
    
    db.session.delete(service)
    db.session.commit()
    flash('Service deleted successfully')
    
    
    return redirect(url_for('admin_dashboard'))

