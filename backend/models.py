from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()


class Costumer(db.Model):
    __tablename__="costumer"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,nullable=False,unique=True)
    full_name=db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)
    pincode=db.Column(db.String,nullable=False)
    Address=db.Column(db.String)
    role=db.Column(db.Integer,nullable=False,default=1)
    is_blocked = db.Column(db.Boolean, default=False)  
    Service_request=db.relationship("Service_request",backref="costumer",lazy=True)
  
class Professional(db.Model):
    __tablename__="professional"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,nullable=False,unique=True)
    full_name=db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)
    service=db.Column(db.String,nullable=False)
    experience=db.Column(db.String,nullable=False)
    pincode=db.Column(db.String,nullable=False)
    Description=db.Column(db.String,nullable=False)
    is_approved = db.Column(db.Boolean, default=False) 
    is_rejected= db.Column(db.Boolean, default=False) 
    role=db.Column(db.Integer,nullable=False,default=2)
 
      
    Service_request=db.relationship("Service_request",backref="professional",lazy=True)
    
class Service(db.Model):
    __tablename__="service"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    price=db.Column(db.String,nullable=False)
    time_required=db.Column(db.String,nullable=False)
    Description=db.Column(db.String)
    Service_request=db.relationship("Service_request",backref="service",lazy=True)
    
class Service_request(db.Model):
    __tablename__="service_request"
    id=db.Column(db.Integer,primary_key=True)
    service_id=db.Column(db.Integer,db.ForeignKey("service.id"),nullable=False)
    costumer_id=db.Column(db.Integer,db.ForeignKey("costumer.id"),nullable=False)
    professional_id=db.Column(db.Integer,db.ForeignKey("professional.id"),nullable=False)
    date_of_request=db.Column(db.Date,nullable=False)
    date_of_completion=db.Column(db.Date,nullable=False)
    status=db.Column(db.Integer,nullable=False,default='Requested')
    remarks=db.Column(db.String,nullable=False)
    Rating=db.Column(db.Integer)