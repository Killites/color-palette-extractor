from flask import  Flask, render_template, request
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def get_colors(image_path, k=10):
    image = Image.open(image_path)
    image = image.resize((200, 200))

    data = np.array(image)
    data = data.reshape((-1, 3))

    kmeans = KMeans(n_clusters=k)
    kmeans.fit(data)

    colors = kmeans.cluster_centers_
    return colors.astype(int)

def rgb_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])

@app.route("/", methods=["GET", "POST"])
def index():
    colors = []

    if request.method == "POST":
        file = request.files["image"]
        path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(path)

        extracted_colors = get_colors(path)
        colors = [rgb_to_hex(c) for c in extracted_colors]

    return render_template("index.html", colors=colors)

if __name__ == "__main__":
    app.run(debug=True)



