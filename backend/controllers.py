from flask import Flask ,session
from flask import current_app as app 
from flask import render_template
from flask import request,redirect
from backend.models import *
from backend.models import db
from flask import flash,url_for
from app import *


from sqlalchemy import or_
from datetime  import datetime 

@app.route('/')
def home_page():
    if 'costumer_id' not in session:
        return render_template("index.html")
    return render_template('index.html', csotumer=Costumer.query.get(session['costumer_id']))
@app.route('/contact_page')
def contact_page():
    return render_template('contact.html')
@app.route('/login')
def login():
    
    return render_template("/costumer/login.html")
@app.route('/costumer_dashboard')
def costumer_dashboard():
    service_requests = Service_request.query.filter_by(
        costumer_id=session['costumer_id']
    ).all()
    return render_template('/costumer/costumer_dashboard.html',service_requests=service_requests)

@app.route('/login',methods=["POST"])
def login_post():
    email = request.form.get('email')
    password = request.form.get("password")
    customer = Costumer.query.filter_by(email=email, password=password).first()
    
    if not customer:
        flash('Either password is wrong or user does not exist')
        return redirect(url_for('login'))
    if customer.is_blocked==True:
        flash("Your Account is Blocked ,please contact Admin")    
        return redirect(url_for('contact_page'))
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
    flash('User successfully Registered')
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
        
    session['professional_id'] = professional.id
    session['user_role'] = professional.role
    
    
    
   
    return redirect(url_for('professional_dashboard')) 

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
    #
    session.clear()
    flash('You have been logged out successfully')
    return redirect(url_for('home_page'))
    

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'costumer_id' not in session or session.get('user_role') != 0:
        flash('Unauthorized access')
        return redirect(url_for('login'))
    customers = Costumer.query.filter_by(role=1)
    professionals=Professional.query.filter_by(is_approved=False)
    services=Service.query.all()
    approved_professionals=Professional.query.filter_by(is_approved=True)
    service_requests=Service_request.query.all()
    return render_template('/admin/admin_dashboard.html', customers=customers,professionals=professionals,services=services,approved_professionals=approved_professionals,service_requests=service_requests)

@app.route('/admon_dashboard/view_professional/<int:prof_id>')
def view_professional(prof_id):
    if 'costumer_id' not in session or session.get('user_role') != 0:
        flash('Unauthorized access')
        return redirect(url_for('login'))
    professional=Professional.query.get(prof_id)
    return render_template('/admin/view_professional.html',professional=professional)
@app.route('/admin_dashboard/approve_professional/<int:prof_id>', methods=['POST'])
def approve_professional(prof_id):
    if 'costumer_id' not in session or session.get('user_role') != 0:
        flash('Unauthorized access')
        return redirect(url_for('login'))
    prof = Professional.query.get(prof_id)
    if prof:
        prof.is_approved = True
        prof.is_rejected = False
        db.session.commit()
        flash("Service Professional  approved")
    
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_dashboard/reject_professional/<int:prof_id>', methods=['POST'])
def reject_professional(prof_id):
    if 'costumer_id' not in session or session.get('user_role') != 0:
        flash('Unauthorized access')
        return redirect(url_for('login'))
    prof = Professional.query.get(prof_id)
    if prof:
        db.session.delete(prof)
        db.session.commit()
        flash("Service Professional rejected ")
    
    return redirect(url_for('admin_dashboard'))
@app.route('/admin_dashboard/block_professional/<int:prof_id>',methods=['POST'])
def block_professional(prof_id):
    if 'costumer_id' not in session or session.get('user_role') != 0:
        flash('Unauthorized access')
        return redirect(url_for('login'))
    professional=Professional.query.get(prof_id)
    if professional :
        professional.is_active=False
        db.session.commit()
        flash("prof Blocked Successfully")
    return redirect(url_for('admin_dashboard'))
@app.route('/admin_dashboard/unblock_professional/<int:prof_id>',methods=['POST'])
def unblock_professional(prof_id):
    if 'costumer_id' not in session or session.get('user_role') != 0:
        flash('Unauthorized access')
        return redirect(url_for('login'))
    professional=Professional.query.get(prof_id)
    if professional:
        professional.is_active=True
        db.session.commit()
        flash("prof unblocked Successfully")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_dashboard/block_costumer/<int:costumer_id>',methods=['POST'])
def block_costumer(costumer_id):
    if 'costumer_id' not in session or session.get('user_role') != 0:
        flash('Unauthorized access')
        return redirect(url_for('login'))
    costumer=Costumer.query.get(costumer_id)
    if costumer :
        costumer.is_blocked=True
        db.session.commit()
        flash("Costumer Blocked Successfully")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_dashboard/unblock_costumer/<int:costumer_id>',methods=['POST'])
def unblock_costumer(costumer_id):
    if 'costumer_id' not in session or session.get('user_role') != 0:
        flash('Unauthorized access')
        return redirect(url_for('login'))
    costumer=Costumer.query.get(costumer_id)
    if costumer:
        costumer.is_blocked=False
        db.session.commit()
        flash("Costumer UNBlocked Successfully")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_dashboard/add_service/')
def add_service():
    if 'costumer_id' not in session or session.get('user_role') != 0:
        flash('Unauthorized access')
        return redirect(url_for('login'))
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
        db.session.commit()
        flash('Service updated successfully')
        return redirect(url_for('admin_dashboard'))
        
        
       
        
    
    return render_template('/admin/edit_service.html', service=service)

@app.route('/admin_dashboard/delete_service/<int:service_id>', methods=['POST'])
def delete_service(service_id):
    if 'costumer_id' not in session or session.get('user_role') != 0:
        flash('Unauthorized access')
        return redirect(url_for('login'))
    
    service = Service.query.get(service_id)
    Service_request.query.filter_by(service_id=service_id).delete()
    
    db.session.delete(service)
    db.session.commit()
    flash('Service deleted successfully')
    
    
    return redirect(url_for('admin_dashboard'))




@app.route('/costumer_dashboard/ac_repair')
def ac_repair():
    ac_repair_services = Service.query.filter_by(name='AC repair').all() 
    available_professionals = Professional.query.filter_by(
        service='AC repair',
        is_approved=True,
        is_active=True
    ).first()
    
    if not available_professionals:
        flash('No service professionals are currently available for AC repair at this moment. Please try again later.')
        return redirect(url_for('costumer_dashboard'))
        
    return render_template('/costumer/ac_repair.html', services=ac_repair_services)

    
@app.route('/costumer_dashboard/cleaning')
def cleannig():
    cleaning_services=Service.query.filter_by(name='Cleaning').all()
    available_professionals = Professional.query.filter_by(
        service='Cleaning',
        is_approved=True,
        is_active=True
    ).first()
    
    if not available_professionals:
        flash('No service professionals are currently available for Cleaning Service at this moment. Please try again later.')
        return redirect(url_for('costumer_dashboard'))
    return render_template('/costumer/cleaning.html',services=cleaning_services)
@app.route('/costumer_dashboard/plumbing')
def plumbing():
    
      
    plumbing_service=Service.query.filter_by(name='plumbing')
    available_professionals = Professional.query.filter_by(
        service='plumbing',
        is_approved=True,
        is_active=True
    ).first()
    
    if not available_professionals:
        flash('No service professionals are currently available for Plumbing Service at this moment. Please try again later.')
        return redirect(url_for('costumer_dashboard'))
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
    new_request = Service_request(service_id=service_id,costumer_id=session['costumer_id'],professional_id=professional_id,date_of_request=date_of_request,status='Requested',remarks=remarks)
    
    db.session.add(new_request)
    db.session.commit()
    flash('Service request submitted successfully')
    return redirect(url_for('costumer_dashboard'))
    

    

   
@app.route('/costumer_dashboard/edit_request/<int:request_id>', methods=['GET', 'POST'])
def edit_request(request_id):  
    service_request = Service_request.query.get(request_id)
    if request.method == 'POST':
        
        service_request.professional_id = request.form.get('professional_id')
        service_request.remarks = request.form.get('remarks')
        db.session.commit()
        flash('Service request updated successfully')
        return redirect(url_for('costumer_dashboard'))
    professionals = Professional.query.filter_by(service=service_request.service.name, is_approved=True, is_active=True).all()
    
    return render_template('/costumer/edit_service_request.html', service_request=service_request, professionals=professionals)

  
    
    
    

@app.route('/costumer_dashboard/delete_request/<int:request_id>',methods=['POST'])
def delete_request(request_id):
    request=Service_request.query.get(request_id)
    
    if request.status=='Requested':
            db.session.delete(request)
            db.session.commit()
            flash('Service Request Successfully Deleted')

    return redirect(url_for('costumer_dashboard'))
@app.route('/rate_service/<int:request_id>',methods=['GET'])
def rate_service(request_id):
    request = Service_request.query.get(request_id)
    professional = Professional.query.get(request.professional_id)
    return render_template('/costumer/review.html',request=request,professional=professional)
    
@app.route('/rate_service/<int:request_id>',methods=['POST'])
def rate_service_post(request_id):
    service_request = Service_request.query.get(request_id)
    
   
    review = request.form.get('review')
    rating = request.form.get('rating')
 
    service_request.rating = rating
    service_request.review = review
    db.session.commit()
    
    flash("Review submitted successfully")
    return redirect(url_for('costumer_dashboard'))
@app.route('/professional_dashboard')
def professional_dashboard():
    if 'professional_id' not in session:
        flash('Please login first')
        return redirect(url_for('professional_login'))
        
    
    service_requests = Service_request.query.filter_by(
        professional_id=session['professional_id']
    ).all()
    
    return render_template('/professional/professional_dashboard.html', service_requests=service_requests)

@app.route('/accept_service_request/<int:request_id>', methods=['POST'])
def accept_service_request(request_id):
   
        
    service_request = Service_request.query.get(request_id)
    if service_request and service_request.professional_id == session['professional_id']:
        service_request.status = 'Accepted'
        db.session.commit()
        flash('Service request accepted')
   
    
    return redirect(url_for('professional_dashboard'))

@app.route('/reject_service_request/<int:request_id>', methods=['POST'])
def reject_service_request(request_id):
  
        
    service_request = Service_request.query.get(request_id)
    if service_request and service_request.professional_id == session['professional_id']:
        service_request.status = 'Rejected'
        db.session.commit()
        flash('Service request Rejected')
    
    
    return redirect(url_for('professional_dashboard'))

@app.route('/complete_service_request/<int:request_id>', methods=['POST'])
def complete_service_request(request_id):
   
        
    service_request = Service_request.query.get(request_id)
    if service_request and service_request.costumer_id == session['costumer_id']:
        service_request.status = 'Completed'
        service_request.date_of_completion = datetime.now().date()
        db.session.commit()
        flash('Service request marked as complete')
    else:
        flash('Invalid request')
    
    return redirect(url_for('costumer_dashboard'))


@app.route('/search')
def search():
    
    is_admin = 'costumer_id' in session and session.get('user_role') == 0
    query = request.args.get('query')
    search_by = request.args.get('search_by', 'all')  
 
    
    services = []
    professionals = []
    
    if search_by == 'all' or search_by == 'services':
        services = Service.query.filter(
            or_(Service.name.ilike(f'%{query}%'),Service.Description.ilike(f'%{query}%'),Service.price.ilike(f'%{query}%')
            )
        ).all()
    
    if search_by == 'all' or search_by == 'professionals':
        if is_admin:
           
            professionals = Professional.query.filter(
                or_(Professional.full_name.ilike(f'%{query}%'),
                    Professional.service.ilike(f'%{query}%'),
                    Professional.Description.ilike(f'%{query}%'),
                    Professional.experience.ilike(f'%{query}%'),
                    Professional.pincode.ilike(f'%{query}%')
                )
            ).all()
        else:
           
            professionals = Professional.query.filter(
                or_(
                    Professional.full_name.ilike(f'%{query}%'),
                    Professional.service.ilike(f'%{query}%'),
                    Professional.Description.ilike(f'%{query}%'),
                    Professional.experience.ilike(f'%{query}%'),
                    Professional.pincode.ilike(f'%{query}%')
                )
            ).filter_by(is_approved=True,is_active=True).all()
    
    elif search_by == 'location':
       
        professionals = Professional.query.filter(
            Professional.pincode.ilike(f'%{query}%')
        ).filter_by(is_approved=True,is_active=True).all()
        
        
        
    
   
       
    
    return render_template('search.html',services=services,professionals=professionals,query=query,search_by=search_by)
    
    
@app.route('/admin_dashboard/summary')
def admin_summary():
    if 'costumer_id' not in session or session.get('user_role') != 0:
        flash('Unauthorized access')
        return redirect(url_for('login'))
    customer_stats = {
        'total': Costumer.query.filter_by(role=1).count(),
        'active': Costumer.query.filter_by(role=1, is_blocked=False).count(),
        'blocked': Costumer.query.filter_by(role=1, is_blocked=True).count()
    }
    
    professional_stats = {
        'total': Professional.query.count(),
        'active': Professional.query.filter_by(is_approved=True, is_active=True).count(),
        'blocked': Professional.query.filter_by(is_active=False).count(),
        'pending': Professional.query.filter_by(is_approved=False, is_rejected=False).count(),
        
    }
    
    service_stats = {
        'total': Service_request.query.count(),
        'pending': Service_request.query.filter_by(status='Requested').count(),
        'accepted': Service_request.query.filter_by(status='Accepted').count(),
        'completed': Service_request.query.filter_by(status='Completed').count(),
        'rejected': Service_request.query.filter_by(status='Rejected').count()
    }
    
   
    
   
    return render_template('/admin/admin_summary.html',customer_stats=customer_stats,professional_stats=professional_stats,service_stats=service_stats)
@app.route('/professional_dashboard/professional_summary')
def professional_summary():
    service_requests = Service_request.query.filter_by(
        professional_id=session['professional_id']
    ).all()
    request_summary = {
        'total': Service_request.query.filter_by(professional_id=session['professional_id']).count(),
        'pending': Service_request.query.filter_by(professional_id=session['professional_id'], status='Accepted').count(),
        
        'completed': Service_request.query.filter_by(professional_id=session['professional_id'], status='Completed').count(),
        'rejected': Service_request.query.filter_by(professional_id=session['professional_id'], status='Rejected').count()
    }
    return render_template('/professional/professional_summary.html',service_requests=service_requests,request_summary=request_summary)



@app.route('/edit_profile',methods=['GET','POST'])
def edit_profile():
    if 'costumer_id'in session:
        user = Costumer.query.get(session['costumer_id'])
        template = '/costumer/edit_profile.html'
        user_type = 'costumer'
    elif 'professional_id' in session:
       
        user = Professional.query.get(session['professional_id'])
        template = '/professional/edit_profile.html'
        user_type = 'professional'
    else:
        flash('Login to continue')
        return redirect(url_for('login'))
    if request.method == 'POST' and user_type=='costumer':
       
        user.full_name = request.form.get('full_name')
        user.email = request.form.get('email')
        user.pincode = request.form.get('pincode')
        user.Address = request.form.get('address')
        new_password = request.form.get('new_password')
        if new_password:
            user.password = new_password
        
        db.session.commit()
        flash('Profile updated successfully')
    elif  request.method == 'POST' and user_type=='professional':
        user.full_name = request.form.get('full_name')
        user.email = request.form.get('email')
        user.pincode = request.form.get('pincode')
        user.service = request.form.get('service')
        user.experience = request.form.get('experience')
        user.Description = request.form.get('description')
        new_password = request.form.get('new_password')
        if new_password:
            user.password = new_password
        
        db.session.commit()
        flash('Profile updated successfully')
        return redirect(url_for('costumer_dashboard') if user_type == 'costumer' else 'professional_dashboard')
    
    return render_template(template, user=user)