from flask import Flask, send_from_directory, abort
from flask import jsonify
from flask_cors import CORS, cross_origin
from flask import request
from generate import generate_scad
import os

from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@cross_origin()
@app.route("/cad", methods=["GET"])
def cad():
    query = request.args.get("query")
    generation_id, iteration = generate_scad(query)
    serve_stl(generation_id, iteration)


@cross_origin()
@app.route("/models/generated/<generation_id>/<iteration>/output.stl")
def serve_stl(generation_id, iteration):
    # Construct the file path
    file_path = os.path.join("generated", generation_id, iteration, "output.stl")

    # Check if the file exists
    if not os.path.exists(file_path):
        abort(404, description="Resource not found")

    # Serve the file
    return send_from_directory(os.path.dirname(file_path), "output.stl")


@cross_origin()
@app.route("/models/generated/<generation_id>/<iteration>/output.png")
def serve_png(generation_id, iteration):
    # Construct the file path
    file_path = os.path.join("generated", generation_id, iteration, "output.png")

    # Check if the file exists
    if not os.path.exists(file_path):
        abort(404, description="Resource not found")

    # Serve the file
    return send_from_directory(os.path.dirname(file_path), "output.png")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
