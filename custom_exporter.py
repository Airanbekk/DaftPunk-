"""
Custom API Exporter
Пример: сбор данных о погоде в нескольких городах Казахстана
"""

from prometheus_client import start_http_server, Gauge, Info
import requests
import time

# -------------------- WEATHER METRICS ------------------------
weather_temperature = Gauge('weather_temperature_celsius', 'Current temperature', ['city', 'country'])
weather_windspeed = Gauge('weather_windspeed_kmh', 'Current wind speed', ['city', 'country'])
weather_humidity = Gauge('weather_humidity_percent', 'Humidity', ['city', 'country'])
weather_pressure = Gauge('weather_pressure_hpa', 'Pressure', ['city', 'country'])
weather_cloudcover = Gauge('weather_cloudcover_percent', 'Cloud cover', ['city', 'country'])
weather_visibility = Gauge('weather_visibility_km', 'Visibility', ['city', 'country'])
weather_api_status = Gauge('weather_api_status', 'Weather API status (1=up, 0=down)')
weather_uv = Gauge('weather_uv_index', 'UV index', ['city', 'country'])
weather_precipitation = Gauge('weather_precipitation_mm', 'Precipitation', ['city', 'country'])

# ---------------------- CURRENCY & CRYPTO ---------------------
usd_kzt = Gauge('usd_to_kzt', 'USD to KZT official rate')
eur_kzt = Gauge('eur_to_kzt', 'EUR to KZT official rate')
btc_usd = Gauge('btc_to_usd', 'BTC to USD market price')
currency_api_status = Gauge('currency_api_status', 'Currency API status (1=up, 0=down)')
crypto_api_status = Gauge('crypto_api_status', 'Crypto API status (1=up, 0=down)')

exporter_info = Info('custom_exporter', 'Custom metrics exporter info')

# -------------------- CITIES TO MONITOR ------------------------
CITIES = [
    {'name': 'Astana', 'country': 'Kazakhstan', 'lat': 51.1694, 'lon': 71.4491},
    {'name': 'Almaty', 'country': 'Kazakhstan', 'lat': 43.2220, 'lon': 76.8512},
    {'name': 'Shymkent', 'country': 'Kazakhstan', 'lat': 42.3000, 'lon': 69.6000}
]

def fetch_weather_for_city(city_data):
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': city_data['lat'],
            'longitude': city_data['lon'],
            'current_weather': 'true',
            'hourly': 'relativehumidity_2m,pressure_msl,cloudcover,visibility,uv_index,precipitation',
            'timezone': 'Asia/Almaty'
        }
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        current = data['current_weather']

        city = city_data['name']
        country = city_data['country']

        weather_temperature.labels(city=city, country=country).set(current['temperature'])
        weather_windspeed.labels(city=city, country=country).set(current['windspeed'])

        # Возьмём индексы для текущего времени
        now_idx = data['hourly']['time'].index(current['time'])

        weather_humidity.labels(city=city, country=country).set(data['hourly']['relativehumidity_2m'][now_idx])
        weather_pressure.labels(city=city, country=country).set(data['hourly']['pressure_msl'][now_idx])
        weather_cloudcover.labels(city=city, country=country).set(data['hourly']['cloudcover'][now_idx])
        weather_visibility.labels(city=city, country=country).set(data['hourly']['visibility'][now_idx] / 1000)  # m -> km
        weather_uv.labels(city=city, country=country).set(data['hourly']['uv_index'][now_idx])
        weather_precipitation.labels(city=city, country=country).set(data['hourly']['precipitation'][now_idx])

        return True
    except Exception as e:
        print(f"Error fetching weather for {city_data['name']}: {e}")
        return False

def fetch_weather():
    try:
        success_count = 0
        for city in CITIES:
            if fetch_weather_for_city(city):
                success_count += 1
        
        # Если хотя бы один город успешно получен
        if success_count > 0:
            weather_api_status.set(1)
            return True
        else:
            weather_api_status.set(0)
            return False
    except Exception as e:
        print(f"Weather API error: {e}")
        weather_api_status.set(0)
        return False

def fetch_currency():
    try:
        url = 'https://open.er-api.com/v6/latest/USD'
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        usd_kzt.set(480.0)
        if 'KZT' in data['rates']:
            eur_kzt.set(data['rates']['KZT'])
        else:
            eur_kzt.set(530.0)
        currency_api_status.set(1)
        return True
    except Exception as e:
        print(f"Currency API error: {e}")
        currency_api_status.set(0)
        return False

def fetch_crypto():
    try:
        url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        btc_usd.set(float(data['data']['amount']))
        crypto_api_status.set(1)
        return True
    except Exception as e:
        print(f"Crypto API error: {e}")
        crypto_api_status.set(0)
        return False

if __name__ == '__main__':
    exporter_info.info({'version': '1.2', 'author': 'Student', 'sources': 'weather,currency,crypto'})
    start_http_server(8000)
    print("Custom Exporter запущен на порту 8000")
    print(f"Мониторим города: {', '.join([c['name'] for c in CITIES])}")

    while True:
        try:
            fetch_weather()
            fetch_currency()
            fetch_crypto()
            print("Метрики обновлены для всех городов")
        except KeyboardInterrupt:
            print("Остановка...")
            break
        except Exception as e:
            print(f"Ошибка: {e}")
        
        time.sleep(20)
