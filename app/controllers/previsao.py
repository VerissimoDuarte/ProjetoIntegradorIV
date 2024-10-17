from app import application, projeto, login_required
from flask import request

@application.route('/previsao', methods=['POST'])
@login_required
def previsao():    
    meses = request.get_json()['meses']
    data = request.get_json()['valor']
    previsao = projeto.getPrevision(data, meses)
    return previsao