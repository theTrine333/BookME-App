import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyA9JR4urLfePcB04VHRBN4n7Kgq-Fbbqto",
    "authDomain": "bookme-1703626309990.firebaseapp.com",
    "databaseURL": "https://bookme-1703626309990-default-rtdb.firebaseio.com",
    "projectId": "bookme-1703626309990",
    "storageBucket": "bookme-1703626309990.appspot.com",
    "messagingSenderId": "402315590026",
    "appId": "1:402315590026:web:f6007b648ffc547f77f073",
    "measurementId": "G-S648RNPT3X"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()