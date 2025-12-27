from app import app, db
from app.models import Staff, Task, Manager


with app.app_context():
    db.create_all()
    print('Database tables created.')

    user = Manager(staffname='admin', password='chungTanphat@2001')
    if Manager.query.filter_by(staffname='admin').first():
        print('This admin is used')
    else:
        db.session.add(user)
        db.session.commit()
        print('User is just added')