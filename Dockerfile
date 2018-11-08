FROM tiangolo/uwsgi-nginx-flask:python3.7
COPY . /app

ENV ZABBIX_SERVER "http://127.0.0.1/zabbix"
ENV ZABBIX_USER "Admin"
ENV ZABBIX_PASSWORD "zabbix"

RUN pip install -r /app/requirements.txt
