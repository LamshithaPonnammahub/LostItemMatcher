# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from utils import find_item, save_notification, save_confirmation
# import os

# app = Flask(__name__)
# CORS(app)  # Allow requests from frontend
# @app.route('/')
# def home():
#     return jsonify({"message": "Backend is running!"})


# # Folder where uploaded or dataset images are stored
# UPLOAD_FOLDER = os.path.join(os.getcwd(), "dataset", "images")
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Serve uploaded images
# @app.route('/images/<path:filename>')
# def serve_image(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# @app.route("/find-item", methods=["POST"])
# def find_item_endpoint():
#     """
#     Expects JSON input:
#     {
#         "type": "bottle",
#         "color": "blue",
#         "description": "Plastic bottle with sports cap",
#         "email": "user@example.com"  # optional
#     }
#     """
#     user_item = request.get_json()

#     # Find matched items using Naive Bayes
#     matched_items = find_item(user_item)

#     # Save notifications if email is provided
#     if "email" in user_item and user_item["email"]:
#         if matched_items:
#             for item in matched_items:
#                 save_notification(user_item["email"], item["description"], status="pending")
#         else:
#             save_notification(user_item["email"], user_item["description"], status="pending")

#     # Update image_path for frontend
#     for item in matched_items:
#         filename_only = os.path.basename(item.get('image_path', item['filename']))
#         item['image_path'] = f"images/{filename_only}"  # Matches the /images/<filename> route

#     return jsonify(matched_items)


# @app.route("/confirm-item", methods=["POST"])
# def confirm_item_endpoint():
#     """
#     Expects JSON input:
#     {
#         "email": "user@example.com",
#         "filename": "blue_bottle.jpg",
#         "description": "Plastic bottle with sports cap",
#         "status": "claimed"   # or "ignored"
#     }
#     """
#     data = request.get_json()
#     save_confirmation(
#         data.get("email"),
#         data.get("filename"),
#         data.get("description"),
#         data.get("status", "claimed")
#     )
#     return jsonify({"message": "Confirmation saved successfully."})


# @app.route("/add-notification", methods=["POST"])
# def add_notification_endpoint():
#     """
#     Expects JSON input:
#     {
#         "email": "user@example.com",
#         "description": "Plastic bottle with sports cap"
#     }
#     """
#     data = request.get_json()
#     save_notification(data.get("email"), data.get("description"), status="pending")
#     return jsonify({"message": "Notification added successfully."})


# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# from utils import find_item, save_notification, save_confirmation
# import os

# app = Flask(__name__)
# CORS(app)

# # Folder where images are stored
# UPLOAD_FOLDER = os.path.join(os.getcwd(), "dataset", "images")
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Serve images
# @app.route('/images/<path:filename>')
# def serve_image(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# # Find item
# @app.route("/find-item", methods=["POST"])
# def find_item_endpoint():
#     user_item = request.get_json()
#     matched_items = find_item(user_item)

#     # Save notifications if email is provided
#     email = user_item.get("email")
#     if email:
#         if matched_items:
#             for item in matched_items:
#                 save_notification(email, item["description"], status="pending")
#         else:
#             save_notification(email, user_item.get("description", ""), status="pending")

#     # Update image path for frontend
#     for item in matched_items:
#         filename_only = os.path.basename(item['image_path'])
#         item['image_path'] = f"images/{filename_only}"

#     return jsonify(matched_items)

# # Confirm item
# @app.route("/confirm-item", methods=["POST"])
# def confirm_item_endpoint():
#     data = request.get_json()
#     save_confirmation(
#         data.get("email"),
#         data.get("filename"),
#         data.get("description"),
#         data.get("status", "claimed")
#     )
#     return jsonify({"message": "Confirmation saved successfully."})

# # Add notification
# @app.route("/add-notification", methods=["POST"])
# def add_notification_endpoint():
#     data = request.get_json()
#     save_notification(data.get("email"), data.get("description"), status="pending")
#     return jsonify({"message": "Notification added successfully."})

# if __name__ == "__main__":
#     app.run(debug=True)













from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from utils import find_item, save_notification, save_confirmation
import os

app = Flask(__name__)
CORS(app)

# Folder where images are stored
UPLOAD_FOLDER = os.path.join(os.getcwd(), "dataset", "images")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Serve images
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Find item
@app.route("/find-item", methods=["POST"])
def find_item_endpoint():
    user_item = request.get_json()
    matched_items = find_item(user_item)

    # Save notifications if email is provided
    email = user_item.get("email")
    if email:
        if matched_items:
            for item in matched_items:
                save_notification(email, item["description"], status="pending")
        else:
            save_notification(email, user_item.get("description", ""), status="pending")

    # If no match found → return “Item Not Found.”
    if not matched_items:
        return jsonify({"message": "Item Not Found."}), 200

    # Update image path for frontend
    for item in matched_items:
        filename_only = os.path.basename(item['image_path'])
        item['image_path'] = f"/images/{filename_only}"

    return jsonify(matched_items), 200

# Confirm item
@app.route("/confirm-item", methods=["POST"])
def confirm_item_endpoint():
    data = request.get_json()
    save_confirmation(
        data.get("email"),
        data.get("filename"),
        data.get("description"),
        data.get("status", "claimed")
    )
    return jsonify({"message": "Confirmation saved successfully."})

# Add notification
@app.route("/add-notification", methods=["POST"])
def add_notification_endpoint():
    data = request.get_json()
    save_notification(data.get("email"), data.get("description"), status="pending")
    return jsonify({"message": "Notification added successfully."})

if __name__ == "__main__":
    app.run(debug=True)
