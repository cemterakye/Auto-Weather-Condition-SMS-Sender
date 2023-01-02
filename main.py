import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import os

account_sid = "ur_account_sid"
auth_token = "your_auth_token"
twilio_phone_number = "the_phone_number_from_twilio"
to_telephone_number = "phone_number_you_wanna_send_message"

API_KEY = "b7adb7deaaf57c38b77481f33bab163a"
lat = 40.03
lon = 28.41
part = "hourly"
next_hour = 12


response = requests.get(url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API_KEY}")
data = response.json()
will_rain = False
for i in range(next_hour):
    weather_condition = int(data[i]["weather"][0]["id"])
    if weather_condition < 700:
        will_rain = True

if will_rain :
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {"https" : os.environ["http_proxy"]}

    client = Client(account_sid,auth_token,http_client= proxy_client )
    message = client.messages.create(body = "It is going to rain today. You better bring an umbrella"
                                     ,from_ = twilio_phone_number
                                     ,to = to_telephone_number)

    print(message.status)