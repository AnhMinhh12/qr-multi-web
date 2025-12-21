from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from pyzbar.pyzbar import decode

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    image_bytes = file.read()

    # Chuyển bytes → OpenCV image
    npimg = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"error": "Invalid image"}), 400

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    qr_codes = decode(gray)

    results = []
    for qr in qr_codes:
        results.append(qr.data.decode("utf-8"))

    return jsonify({
        "count": len(results),
        "data": results
    })

if __name__ == "__main__":
    app.run(debug=True)
