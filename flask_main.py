from flask import Flask, render_template, url_for, request, make_response, session, send_file
import os, sys
import datetime
from warehousingLogic import addDeposit, fetchDeposit


app = Flask(__name__)
app.config['SECRET_KEY']='089bcc9bf633533dd60b6f19402d1634'


@app.route('/deposit')
def depositInitiate():
    return render_template('deposit.html')


@app.route('/Deposited', methods=['GET','POST'])
def deposit():
    params = (request.form).to_dict()
    str = addDeposit(params)
    data = str
    return render_template('deposit.html',data=data)
    
    
@app.route('/reciept')
def RecieptInitiate():
    html = fetchDeposit(type = 'unprocessed')
    return render_template('Reciept.html', data=html)
    
    
    

@app.route('/download/<filePath>', methods=['GET', 'POST'])
def download_results(filePath):
    return send_file(
        filePath,
        mimetype='text/csv',
        as_attachment=True
    )
    
if __name__=='__main__':
    import pandas as pd
    app.run(debug=True, host='127.0.0.1', port=5000)