from app import application, login_required, MachineLearn
from flask import render_template, request, jsonify
from app.models import RegisterNF
from datetime import datetime
from collectionpy.chart.apexcharts import Chart, CND_SRC



@application.route('/previsao', methods=['GET', 'POST'])
@login_required
def previsao():
        
    if request.method == 'POST':
        ml = MachineLearn()
        
        if 'amostras' not in request.form:
            dataI = request.form['DateI1']
            dataF = request.form['DateF1']
            periodo = request.form['period1']     
            start_date = datetime.strptime(dataI, '%Y-%m-%d')
            end_date = datetime.strptime(dataF, '%Y-%m-%d')
            results = RegisterNF.query.with_entities(RegisterNF.NFDate, RegisterNF.NFValue).filter(RegisterNF.NFDate.between(start_date, end_date)).all()
            df = ml.convertQueryToDateframe(results, ['NFDate', 'NFValue'], periodo )
            x, y = ml.get_eixos(df, 'Date', 'Valor')
            chart1 = Chart(x, y)
            chart_data = {
                "x_data": chart1.x,    
                "y_data": chart1.y,   
                "options": chart1.options() 
            }
            return jsonify(chart_data)
            
            
        else:
            dataI = request.form['DateI2']
            dataF = request.form['DateF2']
            periodo = request.form['period2']
            amostras = request.form['amostras']
            quantPrevisao = request.form['QuantPrevisao']           
            start_date = datetime.strptime(dataI, '%Y-%m-%d')
            end_date = datetime.strptime(dataF, '%Y-%m-%d')
            results = RegisterNF.query.with_entities(RegisterNF.NFDate, RegisterNF.NFValue).filter(RegisterNF.NFDate.between(start_date, end_date)).all()        
            x, y = ml.getPrevision(results, ['NFDate', 'NFValue'], periodo, int(amostras), int(quantPrevisao) )
            chart2 = Chart(x, y)            
            chart_data = {
                "x_data": chart2.x,   
                "y_data": chart2.y,   
                "options": chart2.options()  
            }          
            return jsonify(chart_data)        
    return render_template('estimativa.html', cnd=CND_SRC)