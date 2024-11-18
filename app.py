from flask import Flask
from backend.models import *

import os

app=None


def init_app():
    Services_app=Flask(__name__)
    Services_app.debug=True
    Services_app.secret_key = 'my_secret_key'
    Services_app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///Services.sqlite3"
    Services_app.app_context().push()
    
    db.init_app(Services_app)
    with Services_app.app_context():
        db.create_all()
        
        admin = Costumer.query.filter_by(role=0).first()
        if not admin:
            admin = Costumer(
                email='admin@gmail.com',
                password='123',
                full_name='admin',
                pincode='283203',
                Address='Firozabad',
                role=0
            )
            db.session.add(admin)
            db.session.commit()
    print("A To Z Household Services application Started ")
    return Services_app

   
app=init_app()
from backend.controllers import *




if __name__=="__main__":
    app.run()
    