from app import application, bcrypt, db, login_required
from flask import render_template, request, flash, redirect, url_for
from app.models import User

@application.route("/register/<int:id>", methods=["GET", "POST"])
@application.route("/register", methods=["GET", "POST"])
@login_required
def register(id=None):
    
    if id:
        usuario = User.query.get_or_404(id)
    else:
        usuario = None        
    if request.method == 'POST':        
        if usuario:         
            usuario.name = request.form['usuario']
            usuario.email = request.form['email']
            usuario.password =  bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            usuario.role =  request.form['role']
            action = "editar"
        else:         
            username = request.form['usuario']
            password = request.form['password']
            email = request.form['email']
            role = request.form['role']            
            hashPassword = bcrypt.generate_password_hash(password).decode('utf-8')
            newUser = User(name=username, email=email, password=hashPassword, role=role)            
            db.session.add(newUser)
            action = "adicionar"
        try:
            db.session.commit()
            flash('Conta criada com sucesso!', 'success')
            return redirect(url_for('listUsers'))
        except:
            return f"Houve um erro ao {action} o usuário."        
    return render_template('register.html', usuario=usuario)

@application.route('/listUsers', methods=['GET'])
@login_required
def listUsers():
    page = request.args.get('page', 1, type=int)  
    per_page = 9  
    users = User.query.paginate(page=page, per_page=per_page, error_out=False) 
    return render_template('users.html', users=users)

@application.route('/register/d/<int:id>')
@login_required
def  userDelete(id: None):
    if id:
        usuario = User.query.get_or_404(id)        
        try:
            db.session.delete(usuario)
            db.session.commit()
        except:
            return "Erro ao excluir o usuário."       
    return redirect(url_for('listUsers'))
