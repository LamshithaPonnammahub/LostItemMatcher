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
import os

# Try to import utils (which depends on heavier ML packages). If the import
# fails (for example, because dependencies are not installed), provide
# lightweight stub implementations so the Flask server can still start and
# respond to basic endpoints during development.
try:
    from utils import find_item, save_notification, save_confirmation
    _UTILS_AVAILABLE = True
except Exception as _e:
    print("Warning: could not import utils module; using stubs:", _e)
    _UTILS_AVAILABLE = False

    def find_item(user_item):
        # Return empty list so frontend receives "Item Not Found." flow
        print("Stub: find_item called with:", user_item)
        return []

    def save_notification(email, description, status="pending"):
        print(f"Stub: save_notification -> {email}, {description}, {status}")

    def save_confirmation(email, filename, description, status="claimed"):
        print(f"Stub: save_confirmation -> {email}, {filename}, {description}, {status}")

app = Flask(__name__)
# 
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}})


# Folder where images are stored
UPLOAD_FOLDER = os.path.join(os.getcwd(), "dataset", "images")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Serve images
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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


# Metrics endpoint: return accuracy curve and sample counts
@app.route("/metrics/accuracy", methods=["GET"])
def metrics_accuracy():
    # If utils provide a compute_accuracy_curve function, use it.
    try:
        if _UTILS_AVAILABLE and hasattr(__import__('utils'), 'compute_accuracy_curve'):
            from utils import compute_accuracy_curve
            metrics = compute_accuracy_curve()
            return jsonify(metrics), 200
        else:
            # Fallback demo data so frontend can still show a meaningful chart
            demo = {
                "accuracy": [55, 62, 70, 78, 83, 86, 90],
                "labels": ["Ep1","Ep2","Ep3","Ep4","Ep5","Ep6","Ep7"],
                "train_counts": [30, 60, 90, 120, 150, 180, 210],
                "test_counts": [270, 240, 210, 180, 150, 120, 90],
                "note": "Demo data (utils not available or compute disabled)."
            }
            return jsonify(demo), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
