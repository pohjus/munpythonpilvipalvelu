import os
from flask import Flask, request, jsonify, json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import tempfile

app = Flask(__name__)

# luetaan firebase ympäristömuuttuja
# tee render.comiin uusi muuttuja nimeltä firebase jonka
# sisältö on json tiedosto jonka saat firebaselta
json_str = os.environ.get('firebase')

# tallennetaan ympäristömuuttujan sisältö väliaikaiseen tiedostoon
with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    f.write(json_str)
    temp_path = f.name

# luetaan tiedostosta json filu
cred = credentials.Certificate(temp_path)

# tee render.comiin ympäristömuuttuja bucket, jonka sisältö
# esim: mydatabase-38cf0.appspot.com
firebase_admin.initialize_app(cred, {
    'storageBucket': os.environ.get('bucket')
})

bucket = storage.bucket()

@app.route('/customers', methods=['GET'])
def get_customers():
    # Load the contents of the highscores file from Firebase Storage
    blob = bucket.blob('highscores.json')
    content = blob.download_as_string().decode('utf-8')
    data = json.loads(content)

    return jsonify(data)

@app.route('/customers', methods=['POST'])
def add_customer():
    # Load the customer data from the request
    customer = request.get_json()
    customer_json = json.dumps(customer)

    # Upload the updated highscores file to Firebase Storage
    blob = bucket.blob('highscores.json')
    blob.upload_from_string(customer_json, content_type='text/plain')

    return jsonify({'message': 'Customer added successfully!'})

if __name__ == '__main__':
    app.run