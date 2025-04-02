from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  # Import CORS
import os
import cv2

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Define folders for uploaded and processed images
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def process_image(image_path):
    """Converts an image to grayscale and saves it"""
    img = cv2.imread(image_path)
    if img is None:
        return None  # Return None if the image couldn't be loaded

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed_path = os.path.join(PROCESSED_FOLDER, "processed.png")
    cv2.imwrite(processed_path, gray)
    
    return processed_path

@app.route("/process", methods=["POST"])
def process():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    img_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(img_path)

    # Process the image
    processed_path = process_image(img_path)
    if processed_path is None:
        return jsonify({"error": "Invalid image format"}), 400

    return jsonify({
        "original": f"https://egg-counter-github-io.onrender.com/uploads/{file.filename}",
        "processed": f"https://egg-counter-github-io.onrender.com/processed/processed.png"
    })

@app.route("/uploads/<filename>")
def get_uploaded_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename))

@app.route("/processed/<filename>")
def get_processed_file(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Use port 10000 for Render
