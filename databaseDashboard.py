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

# Data yang ingin dimasukkan
# murid_1 = {'Nama':'Evan', 'Jurusan':'Teknologi Sains Data', 'IPK': 4}
# murid_2 = {'Nama':'Ryan', 'Jurusan':'Teknologi Sains Data', 'IPK': 4}
# murid_3 = {'Nama':'Oki', 'Jurusan':'Teknologi Sains Data', 'IPK': 4}

# isi = collections.find()
# for i in isi:
#     print(i)

def store_data(data):
    hasil = collections.insert_one(data)
    return hasil.inserted_id

def get_data():
    get_result = collections.find()
    return get_result

@app.route('/sensor1', methods = ['POST'])
def save_sensor_data():
    if request.method == "POST":
        body = request.get_json()
        temperature = body['temperature']
        humidity = body['humidity']
        timestamp = body['timestamp']

        data_sensor = {
            'temperature':temperature,
            'humidity':humidity,
            'timestamp':timestamp,
        }

        store_data(data_sensor)
        return {
            'message':"Berhasil Menyimpan Data!"
        }
if __name__ == '__main__':
    app.run(debug=True)