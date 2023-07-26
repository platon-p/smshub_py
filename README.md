# Python SmsHub API package

Community python module for [SmsHub API](https://www.smshub.org/ru/info)

- Python typing
- Understandable docstrings
- Asynchronous way available
- Easy to use

## Useful links

- [List of services](https://www.smshub.org/ru/info#getServices)
- [List of countries and operators](https://www.smshub.org/ru/info#getCountries)

## Install

```shell
pip install ./
```

# Examples
- [Classic example](#classic-example)
    - [Activation](#activation)
    - [Balance and other actions through wrapper](#balance-and-other-actions-through-wrapper)
- [Asynchronous example](#async-example)
    - [Activation](#activation-1)
    - [Balance and other actions through wrapper](#balance-and-other-actions-through-wrapper-1)
- [Useful utils](#some-useful-utils)

## Classic example

#### Activation

```python
from smshub_py import SmsActivation

a = SmsActivation('YOUR_API_KEY', 'SERVICE_CODE')
print(f"Phone number is +{a.phone}")
# ...
# Do something to send code by SMS
# ...
a.sms_sent()
a.wait_for_sms()
print(f"Code is {a.code}")
# Receive another SMS if expected
a.retry()
a.wait_for_sms()
print(f"Code is {a.code}")
# ...
# Use this code as you want
# ...
# Finish activation if all is OK
a.finish()
```

#### Balance and other actions through wrapper
```python
from smshub_py import SmsHubWrapper

w = SmsHubWrapper('YOUR_API_KEY')
print(f"Balance is {w.get_balance()}")
print(w.get_prices()) # Get all prices
```

## Async example

#### Activation

```python
from smshub_py.asyncio import AsyncSmsActivation
import asyncio


async def main():
    with AsyncSmsActivation('YOUR_API_KEY', 'SERVICE_CODE') as a:
        print(f"Phone number is +{a.phone}")
        # ...
        # Do something to send code by SMS
        # ...
        await a.sms_sent()
        await a.wait_for_sms()
        print(f"Code is {a.code}")
        # Receive another SMS if expected
        await a.retry()
        await a.wait_for_sms()
        print(f"Code is {a.code}")
        # ...
        # Use this code as you want
        # ...
        # Finish activation if all is OK
        await a.finish()


asyncio.run(main())
```

#### Balance and other actions through wrapper

```python
from smshub_py.asyncio import AsyncSmsHubWrapper
import asyncio


async def main():
    async with AsyncSmsHubWrapper('YOUR_API_KEY') as w:
        print(f"Balance is {await w.get_balance()}")
        print(await w.get_prices())  # Get all prices


asyncio.run(main())
```

## Some useful utils

```python
from smshub_py.utils import find_min_prices, country_to_id, id_to_country

# Minimal 100 prices of specified service
find_min_prices(wrapper, 'SERVICE_CODE', count=100)

# Convert Alpha-2 country code to SmsHub Country ID
country_to_id('US') # -> 12

# And back
id_to_country(12) # -> 'US'
```