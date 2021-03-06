from ZabbixAPI_py import Zabbix
from app.API.auth import Auth


class Maintenance:
    def __init__(self, name, active_since, active_till, description, maintenance_type=0):
        self.name = name
        self.active_since = active_since
        self.active_till = active_till
        self.maintenance_type = maintenance_type
        self.description = description


class OneTimeOnly(Maintenance):
    def __init__(self, name, active_since, active_till, description, maintenance_type, start_date, period):
        super().__init__(name, active_since, active_till, description, maintenance_type)
        self.start_date = start_date
        self.period = period

    def create(self, ids, groupids=False):

        # Realiza o login após o método ser chamado.
        api = Zabbix(server=Auth.zabbixServer)
        api.login(user=Auth.zabbixUser, password=Auth.zabbixPassword)

        # Se o groupids for False, o id será reconhecido como um id de host. Se não, será um id de Grupo
        if groupids is False:
            target = 'hostids'
        else:
            target = 'groupids'

        action = api.maintenance('create', {'name': self.name,
                                            'active_since': self.active_since,
                                            'active_till': self.active_till,
                                            'maintenance_type': self.maintenance_type,
                                            'description': self.description,
                                            target: ids,
                                            'timeperiods': [{'timeperiod_type': 0,
                                                             'start_date': self.start_date,
                                                             'period': self.period}]
                                            })
        return action


# Função isolada para pegar todas as manutenções.
# Se id for vazio, lista todas as manutenções.
# Se passado o id, retorna apenas a manutenção solicitada.
def get_maintenance(id=None):
    # Realiza o login após o método ser chamado.
    api = Zabbix(server=Auth.zabbixServer)
    api.login(user=Auth.zabbixUser, password=Auth.zabbixPassword)

    if id is None:
        maintenances = api.maintenance('get', {'output': 'extend',
                                               'selectGroups': ['name'],
                                               'selectHosts': ['name'],
                                               'sortfield': ['maintenanceid'],
                                               'sortorder': ['DESC']})
        return maintenances

    else:
        maintenance = api.maintenance('get', {'output': 'extend',
                                               'selectGroups': ['name'],
                                               'selectHosts': ['name'],
                                               'filter': {'maintenanceid': id}
                                               })
        return maintenance[0]
