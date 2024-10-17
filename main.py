from app import application, db, User, bcrypt


def create_tables():
    db.create_all()
    if not User.query.filter_by(name="admin").first():  
        newUser = User(name='admin', email='admin@admin.com', role='admin', password=bcrypt.generate_password_hash('admin').decode('utf-8'))
        db.session.add(newUser)  
        db.session.commit()

if __name__ == "__main__":
    with application.app_context():
        create_tables()
    application.run(debug=True)