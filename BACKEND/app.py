from flask import Flask , request , jsonify
from auth_service import register_user, verify_user_exists , auth,db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/register", methods= ["POST"])
def register():
    data = request.json
    if not data or "email" not in data or "password" not in data or "username" not in data:
        return jsonify(
            {
                "error" : "required values missing"
            }
        ), 405
    
    return jsonify(register_user(data["email"], data["password"],  data["username"]))

@app.route("/check_user", methods=["POST"])
def check_user():
    data = request.json
    if not data or "email" not in data :
        return jsonify({
            "error": "Email is required"
        }), 400
    
    # Verify if the user exists
    user_exists = verify_user_exists(data["email"])
    if user_exists:
        return jsonify({
            "message": "User exists"
        }), 200
    else:
        return jsonify({
            "message": "User does not exist"
        }), 404


def verify_user_exists(email):
    try:
        # Check in Firebase Authentication if the user exists
        user = auth.get_user_by_email(email)
        return True
    except auth.UserNotFoundError:
        # If the user is not found in Firebase Auth, check Firestore
        user_ref = db.collection("user").where("email", "==", email).limit(1).get()
        if user_ref:
            return True
        return False





import bcrypt

@app.route("/verify_password", methods=["POST"])
def verify_password():
    data = request.json
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        user = auth.get_user_by_email(data["email"])  # Check Firebase Authentication
        user_doc = db.collection("users").document(user.uid).get()

        if user_doc.exists:
            stored_password_hash = user_doc.to_dict()["password"]  # Retrieve hashed password

            # Check if hash format is valid
            if not stored_password_hash.startswith("$2b$"):
                return jsonify({"error": "Invalid hash format detected"}), 500

            # Validate password against stored hash
            if bcrypt.checkpw(data["password"].encode('utf-8'), stored_password_hash.encode('utf-8')):
                return jsonify({"valid": True}), 200
            else:
                return jsonify({"valid": False, "message": "Incorrect password"}), 401
        else:
            return jsonify({"message": "User does not exist"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)