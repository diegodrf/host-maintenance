import os


class Auth:
    # Variáveis de ambiente para Docker
    zabbixServer = 'http://10.241.0.4/zabbix' #os.getenv('ZABBIX_SERVER', 'http://0.0.0.0')
    zabbixUser = 'diego.rodrigues' #os.getenv('ZABBIX_USER', 'Admin')
    zabbixPassword = 'Curumim982150*' #os.getenv('ZABBIX_PASSWORD', 'zabbix')
