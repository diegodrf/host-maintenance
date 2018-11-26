from flask import Flask, redirect, render_template, url_for, request
import app.epoch as epoch
from ZabbixAPI_py import Zabbix
from app import models
from app.API.auth import Auth
import time


app = Flask(__name__, static_folder='../static', template_folder='../templates')


@app.template_filter('strftime')
def _jinja2_filter_datetime(date):
    return time.strftime('%d/%m/%Y - %H:%M', time.localtime(int(date)))


@app.route('/')
def index():
    return redirect(url_for('maintenance'))


@app.route('/maintenance', methods=['GET', 'POST'])
def maintenance():
    if request.method == 'GET':
        # Faz um get para listar os hosts para o usuário. Só será retornado o que o usuário tiver permissão para ver.
        api = Zabbix(server=Auth.zabbixServer)
        api.login(user=Auth.zabbixUser, password=Auth.zabbixPassword)
        hosts = [host for host in api.host('get', {'output': ['hostid', 'name']})]

        return render_template('maintenance.html', hosts=hosts)

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
    maintenance_created = models.get_maintenance(message['maintenanceids'][0])

    return render_template('maintenance_created.html', maintenance=maintenance_created)


@app.route('/maintenance_list')
def maintenance_list():

    maintenances = models.get_maintenance()
    return render_template('maintenance_list.html', maintenances=maintenances)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
