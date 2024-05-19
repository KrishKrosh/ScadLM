from flask import Flask, send_from_directory, abort, jsonify
from flask_cors import CORS, cross_origin
from flask import request
from generate import generate_scad
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


def serve_file(generation_id, iteration, file_name):
    file_path = os.path.join("generated", str(generation_id), str(iteration), file_name)
    if not os.path.exists(file_path):
        abort(404, description="Resource not found")
    return send_from_directory(os.path.dirname(file_path), file_name)


@cross_origin()
@app.route("/cad", methods=["GET"])
def cad():
    query = request.args.get("query")
    generation_id, iteration = generate_scad(query)
    return {"id": generation_id, "iteration": iteration, "shapes": []}


@cross_origin()
@app.route("/models/generated/<generation_id>", methods=["GET"])
def get_iterations(generation_id):
    directory = os.path.join("generated", str(generation_id))
    if not os.path.exists(directory):
        abort(404, description="Resource not found")
    iterations = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    return jsonify(iterations)

@cross_origin()
@app.route("/models/generated/<generation_id>/<iteration>/output.stl")
def serve_stl(generation_id, iteration):
    return serve_file(generation_id, iteration, "output.stl")


@cross_origin()
@app.route("/models/generated/<generation_id>/<iteration>/output.png")
def serve_png(generation_id, iteration):
    return serve_file(generation_id, iteration, "output.png")


@cross_origin()
@app.route("/models/generated/<generation_id>/<iteration>/output.scad")
def serve_scad(generation_id, iteration):
    return serve_file(generation_id, iteration, "output.scad")


@cross_origin()
@app.route("/files/<generation_id>/<iteration>", methods=["GET"])
def get_files(generation_id, iteration):
    directory = os.path.join("generated", str(generation_id), str(iteration))
    if not os.path.exists(directory):
        abort(404, description="Resource not found")
    files = os.listdir(directory)
    return jsonify(files)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    debug = os.getenv("DEBUG", "True").lower() in ["true", "1", "t"]
    app.run(debug=debug, port=port)
