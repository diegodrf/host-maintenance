import os


class Auth:
    # Variáveis de ambiente para Docker
    zabbixServer = 'http://docker.westus2.cloudapp.azure.com' #os.getenv('ZABBIX_SERVER', 'http://0.0.0.0')
    zabbixUser = os.getenv('ZABBIX_USER', 'Admin')
    zabbixPassword = os.getenv('ZABBIX_PASSWORD', 'zabbix')
