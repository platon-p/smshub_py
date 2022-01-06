# SMSHUB API

Библиотека для автоматизации получения sms (а еще тут есть подсказки типов)

### Основные методы
```python
from smshub_py import Client

client = Client(YOUR_TOKEN)

balance = client.get_balance()
vk_numbers = client.get_number_status(0)['vk']
order_id, number = client.get_number('vk')
if ACTIVATED:
    client.set_status(order_id, 1)
print(client.get_status(order_id))
prices = client.get_prices('vk', 0)
```
### Утилиты
```python

from smshub_py import Utils, Client

client = Client(YOUR_TOKEN)
utils = Utils(client)

utils.find_min_prices('tg', 4)
```