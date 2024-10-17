from app import application, db, login_required
from flask import render_template, request, flash, redirect, url_for
from app.models import RegisterNF
from datetime import datetime

@application.route("/registerNF/<int:id>", methods=["GET", "POST"])
@application.route("/registerNF", methods=['GET', 'POST'])
@login_required
def ControllerRegisterNF(id=None):
    
    if id:
        nf = RegisterNF.query.get_or_404(id)
    else:
        nf = None    
    if request.method == 'POST':        
        if nf:
            nf.NFId = request.form['NFId']
            nf.NFValue = request.form['NFValue']
            nf.NFDate = datetime.strptime(request.form['NFDate'], "%Y-%m-%d")
            action = "editar"
        else:
            NFId = request.form['NFId']
            NFValue = request.form['NFValue']
            NFDate = datetime.strptime(request.form['NFDate'], "%Y-%m-%d")            
            newNF = RegisterNF(NFId=NFId, NFValue=NFValue, NFDate=NFDate)
            db.session.add(newNF)            
            action = "adicionar"
        try:
            db.session.commit()
            flash(message='Dados Salvos Com Sucesso')
            return redirect(url_for('ControllerListNF'))
        except:
            return f"Houve um erro ao {action} o usuário."            
    return render_template('registerNF.html', nf=nf)

@application.route('/listNF')
@login_required
def ControllerListNF():
    page = request.args.get('page', 1, type=int)
    per_page = 9 
    nfs = RegisterNF.query.paginate(page=page, per_page=per_page, error_out=False)    
    return render_template('listNF.html', nfs=nfs)

@application.route('/registerNF/d/<int:id>')
@login_required
def  nfDelete(id: None):
    if id:
        nf = RegisterNF.query.get_or_404(id)        
        try:
            db.session.delete(nf)
            db.session.commit()
        except:
            return "Erro ao excluir a Nota Fiscal."        
    return redirect(url_for('ControllerListNF'))
