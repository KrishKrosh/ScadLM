import base64
import os


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_last_generated_iteration(generation_id: str):
    iteration = 0
    while os.path.exists(f"generated/{generation_id}/{iteration}"):
        iteration += 1
    return iteration - 1


def get_last_generated_scad(generation_id: str):
    iteration = get_last_generated_iteration(generation_id)
    # get code from last iteration file
    with open(f"generated/{generation_id}/{iteration}/output.scad", "r") as file:
        code = file.read()
    return code


# uses openscad to render the code.
# creates .scad, .png, and .stl files
# places them in /generated/{generation_id}/{iteration}/output.{filetype}
def render_scad(code: str, generation_id: str, iteration: int) -> bool:
    os.system(f"mkdir -p generated/{generation_id}/{iteration}")
    os.system(f"echo '{code}' > generated/{generation_id}/{iteration}/output.scad")
    png_command = f"openscad -o generated/{generation_id}/{iteration}/output.png generated/{generation_id}/{iteration}/output.scad"
    stl_command = f"openscad -o generated/{generation_id}/{iteration}/output.stl generated/{generation_id}/{iteration}/output.scad"
    png_success = os.system(png_command) == 0
    stl_success = os.system(stl_command) == 0
    return png_success and stl_success
