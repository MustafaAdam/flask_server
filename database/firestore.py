from firebase_admin import firestore, initialize_app, credentials

cred = credentials.Certificate("key.json")
default_app = initialize_app(cred)
db = firestore.client()
