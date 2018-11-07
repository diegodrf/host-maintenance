from app.API.zabbixapi import Zabbix


api = Zabbix(server=Auth.server)
api.login(user=Auth.user, password=Auth.password)