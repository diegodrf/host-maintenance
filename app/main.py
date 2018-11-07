from flask import Flask, redirect, render_template, url_for, request
import app.epoch as epoch
from app.API.zabbixapi import Zabbix
from app import models

app = Flask(__name__)
app.secret_key = 'Rn5!c3cU@a5t'


@app.route('/')
def index():
    return redirect('maintenance')


@app.route('/maintenance')
def maintenance():

    # Faz um get para listar os hosts para o usuário.
    api = Zabbix(server='http://10.241.0.4/zabbix')
    api.login('API', 'APIzabbix')
    hosts = [host for host in api.host('get', {'output': ['hostid', 'name'], 'groupids': '83'})]

    return render_template('maintenance.html', hosts=hosts)

@app.route('/print', methods=['POST'])
def manitenanceToZabbix():

    # Recebe os campos do POST
    name = request.form['name']
    description = request.form['description']
    maintenance_type = request.form['maintenance_type']
    starttime = epoch.humanToEpoch(request.form['starttime'])
    endtime = epoch.humanToEpoch(request.form['endtime'])
    start_date = starttime
    period = endtime - starttime
    # Recebe os hosts selecionados em forma de array
    host_list = request.form.getlist('host_list')

    # Instancia a Classe necessária
    maintenanceZabbix = models.OneTimeOnly(name=name,
                                           active_since=starttime,
                                           active_till=endtime,
                                           description=description,
                                           maintenance_type=maintenance_type,
                                           start_date=start_date,
                                           period=period)

    # Chama o método nos padrões necessários de acordo com a opção do usuário.
    if request.form['target'] == '0':
        message = maintenanceZabbix.create(ids=host_list, groupids=False)
    else:
        message = maintenanceZabbix.create(ids=host_list, groupids=True)

    #TODO: Criar uma tela amigavel para a validação da ação.
    return str(message)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
