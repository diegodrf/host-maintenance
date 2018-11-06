from app.API.zabbixapi import Zabbix
from app.API.auth import Auth

api = Zabbix(server=Auth.server)
api.login(user=Auth.user, password=Auth.password)

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
        if groupids is False:
            target = 'hostids'
        else:
            target = 'groupids'

        action = api.maintenance('create', {'name': self.name,
                                            'active_since': self.active_since,
                                            'active_till': self.active_till,
                                            'maintenance_type': self.maintenance_type,
                                            target: ids,
                                            'timeperiods': [{'timeperiod_type': 0,
                                                             'start_date': self.start_date,
                                                             'period': self.period}]
                                            })
        return action

