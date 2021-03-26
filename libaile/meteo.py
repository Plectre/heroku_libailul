import requests
import json
import time


with open('./libailul/libaile/datas/secret.json', 'r') as secret_file:
    secret = json.load(secret_file)
    URL = secret['url_weather_map']
print(URL)
#url = "https://api.openweathermap.org/data/2.5/weather?q=Bordeaux&lang=fr&appid=73f0cb8d52b1212107a574bf5fc5370e&units=metric"

def fetchApi():
	try:
		respons = requests.get(URL)
	except:
		return False
	if respons.status_code == 200:
			weather = respons.json()
			temp = round(weather["main"]["temp"])
			wind_speed = round(weather["wind"]["speed"]*3.6)
			wind_dir = weather["wind"]["deg"]
			sunset = weather["sys"]["sunset"]
			sunrise = weather["sys"]["sunrise"]
			cloud_desc = weather["weather"][0]["description"]
			pressure = weather["main"]["pressure"]
			sunset_format = time.strftime("%Hh%M", time.gmtime(sunset))
			wind_speed = round(wind_speed*1.9438)
			print(sunset_format)
			meteo = [{
					'temp': temp,
					'wind_speed' : wind_speed,
					'wind_dir' : wind_dir,
					'sunset' : sunset_format,
					'sunrise': sunrise,
					'cloud_desc': cloud_desc,
					'pressure': pressure
					}]
			return meteo
	else:
		return 'meteo'