from machine import Pin
import time
import dht
import network
import urequests as requests

# ID dan Token UBIDOTS
DEVICE_ID = "ESP32"
TOKEN = "BBUS-n6mEItXZ0ail8ZuynYpjHGH4v6OCHb"

# Pin ESP32
dht_sensor = dht.DHT11(Pin(21))
led = Pin(18, Pin.OUT)
pir_sensor = Pin(4, Pin.IN)

# Fungsi Mendapatkan Timestamp
def get_timestamp():
    timestamp = time.localtime() 
    timestamp_str = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
        timestamp[0], timestamp[1], timestamp[2], timestamp[3], timestamp[4], timestamp[5])
    return timestamp_str

# Fungsi Connect ke Wi-Fi
def do_connect():
    import network
    sta_if = network.WLAN(network.WLAN.IF_STA)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('AgusGIA3', '123456Ag')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ipconfig('addr4'))

# Fungsi Membaca Hasil PIR Sensor
def baca_pir():
    baca = pir_sensor.value()
    if baca == 1:
        return "Terdeteksi Gerakan"
    elif baca == 0:
        return "Tidak Terdeteksi Gerakan"

# Fungsi Mengirim Data ke API Flask 
def send_data_server(temp, humi):
    url = "http://192.168.0.200:5000/sensor1"
    headers = {'Content-Type': 'application/json'}
    timestamp = get_timestamp()
    payload = {
        "temperature": temp,
        "humidity": humi,
        "timestamp": timestamp,
        "motion": baca_pir()
        }
    try:
        response = requests.post(url, json=payload, headers=headers)
        print("Response from API:", response.text)
    except Exception as e:
        print("Error sending data:", e)

# Fungsi Mengirim Data ke Ubidots
def send_data_ubidots(temperature, humidity):
    url = "http://industrial.api.ubidots.com/api/v1.6/devices/" + DEVICE_ID
    headers = {"Content-Type": "application/json", "X-Auth-Token": TOKEN}
    data = {
        "temp": temperature,
        "humidity": humidity,
        "motion": baca_pir(),
        "led": led.value()
    }
    response = requests.post(url, json=data, headers=headers)
    print("Done Sending Data!")
    print("Response:", response.text)
    
# Menjalankan Fungsi Connect ke Wi-Fi
do_connect()

while True:
    dht_sensor.measure()
    temp = dht_sensor.temperature()
    humi = dht_sensor.humidity()
    timestamp = get_timestamp()
    pir = pir_sensor.value()
    data = {
        "temp": temp,
        "humidity": humi,
        "timestamp": timestamp,
        "motion": baca_pir()
    }
    print(data)
    if pir == 1:
        led.value(1)
        print("Motion Detected")
    else:
        led.value(0)
        print("Motion Not Detected")
    
    send_data_server(temp, humi)
    send_data_ubidots(temp, humi)
    time.sleep(20)
    
    
    