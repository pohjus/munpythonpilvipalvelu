import os

import dropbox
from flask import Flask, request, jsonify, json
import requests

app = Flask(__name__)

access_token = os.getenv("avain")

dbx = dropbox.Dropbox(access_token)


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTH_URL = 'https://www.dropbox.com/oauth2/authorize'
TOKEN_URL = 'https://api.dropbox.com/oauth2/token'
REDIRECT_URI = 'http://localhost:5000/auth'

auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, 'token')

# Location in Dropbox to store the access token file
ACCESS_TOKEN_FILE_PATH = '/access_token.txt'

@app.route('/auth')
def auth():
    # Get the authorization code from the URL query parameters
    code = request.args.get('code')

    # Use the authorization code to obtain a new access token
    try:
        access_token, user_id = auth_flow.finish(code)

        # Store the new access token securely in an environment variable
        os.environ['DROPBOX_ACCESS_TOKEN'] = access_token

        return redirect(url_for('get_customers'))
    except dropbox.exceptions.AuthError as e:
        return jsonify({'error': str(e)})


@app.route('/auth/start')
def start_auth():
    auth_url = auth_flow.start()
    return redirect(auth_url)


def load_access_token():
    # Download the access token file from Dropbox
    try:
        metadata, res = dbx.files_download(ACCESS_TOKEN_FILE_PATH)
        access_token = res.content.decode('utf-8').strip()
        return access_token
    except dropbox.exceptions.ApiError as e:
        print('Error downloading access token file:', e)
        raise e


@app.route('/customers', methods=['GET'])
def get_customers():
    # Load the access token from the environment variable
    access_token = os.getenv('DROPBOX_ACCESS_TOKEN')

    dbx = dropbox.Dropbox(access_token)



    metadata, res = dbx.files_download('/highscores.json')
    data = json.loads(res.content.decode("utf-8"))
    return jsonify(data)

@app.route('/customers', methods=['POST'])
def add_customer():
    # Load the access token from the environment variable
    access_token = os.getenv('DROPBOX_ACCESS_TOKEN')

    dbx = dropbox.Dropbox(access_token)

    customer = request.get_json()
    customer_json = json.dumps(customer)

    dbx.files_upload(customer_json.encode("utf-8"), '/highscores.json',  mode=dropbox.files.WriteMode("overwrite"))
    return jsonify({'message': 'Customer added successfully!'})



if __name__ == '__main__':
    app.run()