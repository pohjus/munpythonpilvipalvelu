import os

import dropbox
from flask import Flask, request, jsonify, json

# hae renderistä access token
access_token = os.getenv("avain")

dbx = dropbox.Dropbox(access_token)

app = Flask(__name__)

@app.route('/customers', methods=['GET'])
def get_customers():
    metadata, res = dbx.files_download('/highscore.json')
    data = json.loads(res.content.decode("utf-8"))
    return jsonify(data)

@app.route('/customers', methods=['POST'])
def add_customer():
    customer = request.get_json()
    customer_json = json.dumps(customer)

    dbx.files_upload(customer_json.encode("utf-8"), '/highscores.json',  mode=dropbox.files.WriteMode("overwrite"))
    return jsonify({'message': 'Customer added successfully!'})



if __name__ == '__main__':
    app.run()