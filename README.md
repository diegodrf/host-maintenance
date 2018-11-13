## Projeto para criar hosts em manutenção no Zabbix utilizando uma conta com permissão de usuário

Para criar a imagem.
```
docker build -t diegodrf/flask:1 .
```

Para rodar o container utilizando os arquivos locais para desenvolvimento.
```
docker container run --name flask \
-p 8000:80 \
-e ZABBIX_SERVER="IP do Servidor" \
-e ZABBIX_USER="Usuário do Zabbix" \
-e ZABBIX_PASSWORD="Senha do Zabbix" \
-e TZ="America/Sao_Paulo" \
-v "$(pwd)/app:/app/app" diegodrf/flask:1
```

* A variável de ambiente TZ é importante, pois tive problemas de envio de hora errado por causa disso e levei um bom tempo até descobrir que apenas setando ela já poderia resolver.

