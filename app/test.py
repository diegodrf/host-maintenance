# from app import models
#
# manutencao = models.OneTimeOnly(name='UM DIA',
#                                 active_since=1540717963,
#                                 active_till=1540727963,
#                                 description='Testando',
#                                 maintenance_type=0,
#                                 start_date=1540717963,
#                                 period=60)
# print(manutencao.create([4], True))

from app.models import get_maintenance

print(get_maintenance())