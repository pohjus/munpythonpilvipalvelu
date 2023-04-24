import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("./secret.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'mydatabase-38cf0.appspot.com'})

bucket = storage.bucket()


# Upload a file to Firebase Storage
blob = bucket.blob('file.txt')
blob.upload_from_string('Hello, Firebase!', content_type='text/plain')

# Download a file from Firebase Storage
blob = bucket.blob('file.txt')
content = blob.download_as_string().decode('utf-8')
print(content)