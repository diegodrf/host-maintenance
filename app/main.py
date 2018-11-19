from flask import Flask, redirect, render_template, url_for, request, session
import app.epoch as epoch
from ZabbixAPI_py import Zabbix
from app import models
from app.API.auth import Auth
from time import time, sleep

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.secret_key = 'Rn5!c3cU@a5t'

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/maintenance/<user>')
def maintenance(user):

    # Verifica se o usuário está logado a mais de 10 minutos. Se sim, da timeout e desloga, se não, permite o acesso
    # e renova o timestamp
    if round(time() - session[user]['timestamp'], 0) > 600.0:
        session.pop(user, None)
        return redirect(url_for('login'))
    else:
        session[user]['timestamp'] = time()

        # Faz um get para listar os hosts para o usuário. Só será retornado o que o usuário tiver permissão para ver.
        api = Zabbix(server=Auth.zabbixServer)
        api.login(user=session[user]['user'], password=session[user]['password'])
        hosts = [host for host in api.host('get', {'output': ['hostid', 'name']})]

        return render_template('maintenance.html', hosts=hosts)

@app.route('/manitenanceToZabbix', methods=['POST'])
def maintenanceToZabbix():

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
    # Comentado pois por enquanto não trataremos a manutenção nesta granularidade
    # if request.form['target'] == '0':
    #     message = maintenanceZabbix.create(ids=host_list, groupids=False)
    # else:
    #     message = maintenanceZabbix.create(ids=host_list, groupids=True)

    message = maintenanceZabbix.create(ids=host_list, groupids=False)
    print(message)
    print(message['maintenanceids'][0])
    maintenance_created = models.get_maintenance(message['maintenanceids'][0])

    return render_template('maintenance_created.html', maintenance=maintenance_created)


@app.route('/maintenance_list')
def maintenance_list():
    try:
        maintenances = models.get_maintenance()
        return render_template('maintenance_list.html', maintenances=maintenances)
    except:
        return redirect('login')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/auth', methods=['POST'])
def auth():
    user = request.form['user']
    password = request.form['password']
    timestamp = time()
    server = Auth.zabbixServer

    # Verifica se o usuário já possui sessão ativa, se tiver, permite a entrada e renova seu timestamp,
    # se não, verifica no zabbix a existência do usuário.
    if user in session:
        session[user]['timestamp'] = time()
        return redirect(url_for('maintenance', user=user))
    else:
        api = Zabbix(server=server)
        token = api.login(user=user, password=password)
        if len(token) == 32:
            session[user] = {'user': user, 'password': password, 'timestamp': timestamp}
            return redirect(url_for('maintenance', user=user))
        else:
            return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
