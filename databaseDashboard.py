from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
uri = "mongodb+srv://primarizkiahmadh:HaloOki222@cluster-uni437.wqp2b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-UNI437"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Database
db = client['Database1']
collections = db['DataSiswa']

# Fungsi Menyimpan Data di Database
def store_data(data):
    hasil = collections.insert_one(data)
    return hasil.inserted_id

# Fungsi Mengambil Data dari Database
def get_data():
    get_result = collections.find()
    return get_result

# API untuk Menyimpan data ke Database 
@app.route('/sensor1', methods = ['POST'])
def save_sensor_data():
    if request.method == "POST":
        body = request.get_json()
        temperature = body['temperature']
        humidity = body['humidity']
        timestamp = body['timestamp']
        motion = body['motion']

        data_sensor = {
            'temperature':temperature,
            'humidity':humidity,
            'timestamp':timestamp,
            "motion":motion
        }

        store_data(data_sensor)
        return {
            'message':"Berhasil Menyimpan Data!"
        }
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)