import firebase_admin
from firebase_admin import credentials, firestore, auth

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

import bcrypt

def register_user(email, password, username):
    try:
        # Hash password before storing
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Save to Firestore
        user = auth.create_user(email=email, password=password, display_name=username)
        uid = user.uid

        db.collection("users").document(uid).set({
            "username": username,
            "email": email,
            "password": hashed_password  # Store hashed password securely
        })

        return {"message": "User registered successfully", "user_id": uid}
    
    except Exception as e:
        return {"error": str(e)}



def verify_user_exists(uid):
    try:
        # Try to get the document from Firestore
        user_doc = db.collection("users").document(uid).get()

        # Check if the document exists
        if user_doc.exists:
            return {
                "message": "User exists",
                "user_data": user_doc.to_dict()  # Return user data as a dictionary
            }
        else:
            return {
                "message": "User does not exist"
            }
    
    except Exception as e:
        return {
            "error": str(e)
        }





       