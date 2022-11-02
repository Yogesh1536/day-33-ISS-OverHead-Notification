import requests
from datetime import datetime
import ssl
import smtplib
import time

# enter Your mail id
my_email = 'yogeshs15101999@gmail.com'
# account->settings->privacy->app password-> select others(type "python")-> click generate
password = "****************"

MY_LAT = 9.925201
MY_LON = 78.119774

context = ssl.create_default_context()


def at_current_pos():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    data = response.json()
    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])

    if longitude - 5 <= MY_LON <= longitude + 5 and latitude - 5 <= MY_LAT <= latitude + 5:
        return True


def is_dark():
    parameter = {
        "lat": MY_LAT,
        "lng": MY_LON,
        "formatted": 0
    }
    resp = requests.get(url="https://api.sunrise-sunset.org/json", params=parameter)
    resp.raise_for_status()
    sun_data = resp.json()
    sunrise = int(sun_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(sun_data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    hour = time_now.hour
    if hour >= sunset or hour <= sunrise:
        return True


while True:
    time.sleep(60)
    if at_current_pos() and is_dark():
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as connection:
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=f"Subject:Look Up!\n\nThe ISS is above you in the way"
            )
