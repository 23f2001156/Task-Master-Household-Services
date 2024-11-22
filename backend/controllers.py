from flask import Flask ,session
from flask import current_app as app 
from flask import render_template
from flask import request,redirect
from backend.models import *
from backend.models import db
from flask import flash,url_for,blueprints,Blueprint
from app import *
from functools import wraps


from datetime  import datetime ,timedelta

@app.route('/')
def home_page():
    if 'costumer_id' not in session:
        return render_template("index.html")
    return render_template('index.html', csotumer=Costumer.query.get(session['costumer_id']))
@app.route('/login')
def login():
    
    return render_template("/costumer/login.html")
@app.route('/costumer_dashboard')
def costumer_dashboard():
   
    return render_template('/costumer/costumer_dashboard.html')

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
    return redirect(url_for('costumer_dashboard')) 
    
@app.route('/register')
def register():
    return render_template("/costumer/register.html")
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
@app.route('/professional_login')
def professional_login():
    return render_template('/professional/professional_login.html')


@app.route('/professional_login',methods=["POST"])
def professional_login_post():
    email = request.form.get('email')
    password = request.form.get("password")
    professional = Professional.query.filter_by(email=email, password=password).first()
    
    if not professional:
        flash('Either password is wrong or user does not exist')
        return redirect(url_for('professional_login'))
        
   
    
    
    
   
    return redirect(url_for('home_page')) 
@app.route('/professional_signup')
def professional_signup():
    return render_template("/professional/professional_signup.html")
@app.route('/professional_signup',methods=['POST'])
def professional_signup_post():
    email=request.form.get('email')
    password=request.form.get('password')
    full_name=request.form.get('full_name')
    pincode=request.form.get('pincode')
    Description=request.form.get('Description')
    service_name=request.form.get('service_name')
    experience=request.form.get('experience')
    if email=='' or password=='':
        flash("Email or password cannot be empty")
        return redirect(url_for('professional_signup'))
    if Professional.query.filter_by(email=email).first():
        flash('User already Exist')
        return redirect(url_for('professional_signup'))
    professional=Professional(email=email,password=password,full_name=full_name,pincode=pincode, Description= Description,service=service_name,experience=experience)
    db.session.add(professional)
    
    db.session.commit()
    flash('Service Professional Successfully Registered')
    return redirect(url_for('professional_login'))

@app.route('/logout')
def logout():
    session.pop('costumer_id', None)
    

@app.route('/admin_dashboard')
def admin_dashboard():
    customers = Costumer.query.filter_by(role=1)
    professionals=Professional.query.filter_by(is_approved=False)
    services=Service.query.all()
    approved_professionals=Professional.query.filter_by(is_approved=True)
    return render_template('/admin/admin_dashboard.html', customers=customers,professionals=professionals,services=services,approved_professionals=approved_professionals)

    
@app.route('/admin_dashboard/approve_professional/<int:prof_id>', methods=['POST'])
def approve_professional(prof_id):
    prof = Professional.query.get(prof_id)
    if prof:
        prof.is_approved = True
        prof.is_rejected = False
        db.session.commit()
        flash("Service Professional  approved")
    
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_dashboard/reject_professional/<int:prof_id>', methods=['POST'])
def reject_professional(prof_id):
    prof = Professional.query.get(prof_id)
    if prof:
        db.session.delete(prof)
        db.session.commit()
        flash("Service Professional rejected ")
    
    return redirect(url_for('admin_dashboard'))
@app.route('/admin_dashboard/block_professional/<int:prof_id>',methods=['POST'])
def block_professional(prof_id):
    professional=Professional.query.get(prof_id)
    if professional :
        professional.is_active=False
        db.session.commit()
        flash("prof Blocked Successfully")
    return redirect(url_for('admin_dashboard'))
@app.route('/admin_dashboard/unblock_professional/<int:prof_id>',methods=['POST'])
def unblock_professional(prof_id):
    professional=Professional.query.get(prof_id)
    if professional:
        professional.is_active=True
        db.session.commit()
        flash("prof unblocked Successfully")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_dashboard/block_costumer/<int:costumer_id>',methods=['POST'])
def block_costumer(costumer_id):
    costumer=Costumer.query.get(costumer_id)
    if costumer :
        costumer.is_blocked=True
        db.session.commit()
        flash("Costumer Blocked Successfully")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_dashboard/unblock_costumer/<int:costumer_id>',methods=['POST'])
def unblock_costumer(costumer_id):
    costumer=Costumer.query.get(costumer_id)
    if costumer:
        costumer.is_blocked=False
        db.session.commit()
        flash("Costumer UNBlocked Successfully")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_dashboard/add_service/')
def add_service():
    return render_template('/admin/service_form.html') 


    
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
    
    return render_template('/admin/edit_service.html', service=service)

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




@app.route('/costumer_dashboard/ac_repair')
def ac_repair():
    ac_repair_services = Service.query.filter_by(name='AC_repair').all()
    return render_template('/costumer/ac_repair.html',services=ac_repair_services)
@app.route('/costumer_dashboard/cleaning')
def cleannig():
    cleaning_services=Service.query.filter_by(name='Cleaning').all()
    return render_template('/costumer/cleaning.html',services=cleaning_services)
@app.route('/costumer_dashboard/plumbing')
def plumbing():
    plumbing_service=Service.query.filter_by(name='plumbering')
    return render_template('/costumer/plumbing.html',services=plumbing_service)

@app.route('/costumer_dashboard/book_service/<int:service_id>')
def book_service(service_id):
    if 'costumer_id' not in session:
        flash('Please login first')
        return redirect(url_for('login'))
    
    service = Service.query.get(service_id)
   
    professionals = Professional.query.filter_by(service=service.name, is_approved=True, is_active=True).all()
    
    return render_template('/costumer/book_service.html', service=service, professionals=professionals)

@app.route('/book_service_post', methods=['POST'])
def book_service_post():
    if 'costumer_id' not in session:
        flash('Please login first')
        return redirect(url_for('login'))
    
    service_id = request.form.get('service_id')
    professional_id = request.form.get('professional_id')
    remarks = request.form.get('remarks')
    date_of_request = datetime.now().date()
    
  
    
    new_request = Service_request(
        service_id=service_id,
        costumer_id=session['costumer_id'],
        professional_id=professional_id,
        date_of_request=date_of_request,
        
        status='Requested',
        remarks=remarks
    )
    
    db.session.add(new_request)
    db.session.commit()
    
    flash('Service request submitted successfully')
    return redirect(url_for('costumer_dashboard'))
