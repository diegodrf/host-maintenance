from flask import Flask, redirect, render_template, url_for, request, sessions

#TODO: Corrigir o problema de importar a classe logando automaticamente.
#from app import models

app = Flask(__name__)
app.secret_key = 'Rn5!c3cU@a5t'

@app.route('/')
def index():
    return redirect('login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/authentication', methods=['POST',])
def authentication():
    # Apenas testando o login
    user = request.form['user']
    if user == 'diego':
        return redirect('http://g1.globo.com')
    else:
        return redirect('http://google.com')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
