import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

firebase_config = {
  "apiKey": "AIzaSyBVZOFJqZqG2b-s2ypBOIHRn-b2cKG3WbQ",
  "authDomain": "escript-72796.firebaseapp.com",
  "projectId": "escript-72796",
  "storageBucket": "escript-72796.firebasestorage.app",
  "messagingSenderId": "209248647382",
  "appId": "1:209248647382:web:adee42acb7106e4d093177",
  "measurementId": "G-MZT7DZZBTP",
  "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)
firebase_auth = firebase.auth()
