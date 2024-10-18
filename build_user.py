from app import application, db, bcrypt
from app.models import User 


def create_admin():
    with application.app_context():
        if not User.query.filter_by(name="admin").first():  
            newUser = User(name='admin', email='admin@admin.com', role='admin', password=bcrypt.generate_password_hash('admin').decode('utf-8'))
            db.session.add(newUser)  
            db.session.commit()

if __name__ == "__main__":
    create_admin()
