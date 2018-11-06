from flask import Flask, redirect, render_template, url_for, request
from app import models

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
    # Verifica se o usuário possui uma conta válida no Zabbix para poder logar.
    user = request.form['user']
    password = request.form['password']
    try:
        zabbix = models.Zabbix(server='http://0.0.0.0')
        zabbix.login(user=user, password=password)
        return redirect(url_for('maintenance'))
    except:
        # Caso não seja possível logar, retorna para a tela de login.
        return redirect(url_for('login'))


@app.route('/maintenance')
def maintenance():
    return render_template('maintenance.html')



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
