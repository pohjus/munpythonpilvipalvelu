import os

import dropbox
from flask import Flask, request, jsonify, json
import requests

# hae renderistä access token
access_token = os.getenv("avain")

dbx = dropbox.Dropbox(access_token)

app = Flask(__name__)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "https://mun-super-palvelu-jee-jee.onrender.com/callback"
TOKEN_URL = "https://api.dropboxapi.com/oauth2/token"

@app.route('/callback', methods=['GET'])
def callback():
    code = request.args.get('code')

    if code:
        payload = {
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI
        }
        
        response = requests.post(TOKEN_URL, data=payload)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data['access_token']
            refresh_token = token_data['refresh_token']
            
            # Save the access token and refresh token securely (e.g. in a database or encrypted file)
            # Use the access token to make API requests and refresh it when it expires

            return f"Access token: {access_token}, Refresh token: {refresh_token}"
        else:
            return f"Error: {response.text}"
    else:
        error = request.args.get('error', 'No error information provided')
        return f"Error during authorization: {error}"

@app.route('/customers', methods=['GET'])
def get_customers():
    metadata, res = dbx.files_download('/highscores.json')
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