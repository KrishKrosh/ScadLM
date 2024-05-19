system_msg = "You are an assistant that helps with generating OpenSCAD code."

openscad_cheatsheet = """
Here is a cheatsheet for OpenSCAD to help you generate code:

Syntax
var = value;
var = cond ? value_if_true : value_if_false;
var = function (x) x + x;
module name(…) { … }
name();
function name(…) = …
name();
include <….scad>
use <….scad>
Constants
undef
undefined value
PI
mathematical constant π (~3.14159)
Operators
n + m
Addition
n - m
Subtraction
n * m
Multiplication
n / m
Division
n % m
Modulo
n ^ m
Exponentiation
n < m
Less Than
n <= m
Less or Equal
b == c
Equal
b != c
Not Equal
n >= m
Greater or Equal
n > m
Greater Than
b && c
Logical And
b || c
Logical Or
!b
Negation
Special variables
$fa
minimum angle
$fs
minimum size
$fn
number of fragments
$t
animation step
$vpr
viewport rotation angles in degrees
$vpt
viewport translation
$vpd
viewport camera distance
$vpf
viewport camera field of view
$children
 number of module children
$preview
 true in F5 preview, false for F6
Modifier Characters
*
disable
!
show only
#
highlight / debug
%
transparent / background
2D
circle(radius | d=diameter)
square(size,center)
square([width,height],center)
polygon([points])
polygon([points],[paths])
text(t, size, font,
     halign, valign, spacing,
     direction, language, script)
import("….ext", convexity)
projection(cut)
3D
sphere(radius | d=diameter)
cube(size, center)
cube([width,depth,height], center)
cylinder(h,r|d,center)
cylinder(h,r1|d1,r2|d2,center)
polyhedron(points, faces, convexity)
import("….ext", convexity)
linear_extrude(height,center,convexity,twist,slices)
rotate_extrude(angle,convexity)
surface(file = "….ext",center,convexity)
Transformations
translate([x,y,z])
rotate([x,y,z])
rotate(a, [x,y,z])
scale([x,y,z])
resize([x,y,z],auto,convexity)
mirror([x,y,z])
multmatrix(m)
color("colorname",alpha)
color("#hexvalue")
color([r,g,b,a])
offset(r|delta,chamfer)
hull()
minkowski(convexity)
Lists
list = […, …, …];
  create a list
var = list[2];
  index a list (from 0)
var = list.z;
  dot notation indexing (x/y/z)
Boolean operations
union()
difference()
intersection()
List Comprehensions
Generate [ for (i = range|list) i ]
Generate [ for (init;condition;next) i ]
Flatten [ each i ]
Conditions [ for (i = …) if (condition(i)) i ]
Conditions [ for (i = …) if (condition(i)) x else y ]
Assignments [ for (i = …) let (assignments) a ]
Flow Control
for (i = [start:end]) { … }
for (i = [start:step:end]) { … }
for (i = […,…,…]) { … }
for (i = …, j = …, …) { … }
intersection_for(i = [start:end]) { … }
intersection_for(i = [start:step:end]) { … }
intersection_for(i = […,…,…]) { … }
if (…) { … }
let (…) { … }
Type test functions
is_undef
is_bool
is_num
is_string
is_list
is_function
Other
echo(…)
render(convexity)
children([idx])
assert(condition, message)
assign (…) { … }
Functions
concat
lookup
str
chr
ord
search
version
version_num
parent_module(idx)
Mathematical
abs
sign
sin
cos
tan
acos
asin
atan
atan2
floor
round
ceil
ln
len
let
log
pow
sqrt
exp
rands
min
max
norm
cross
"""

code_prefix_prompt = """"""

work_harder_prompt = "Do not be lazy. Give your full best effort. Work at your highest potential. Do not 'give a basic example'"

pre_prompt = (
    "Generate openscad code to create a 3D model with the following details. "
    + work_harder_prompt
    + code_prefix_prompt
)

feedback_prompt = (
    """
This is the rendering of the code you provided. Does it look correct?

If yes, respond YES.

If no, respond NO, identify what is wrong with the current model, then generate new code that addresses these issues. Be as specific as possible. Among other things, check if it looks like parts align correctly, and that they are connected properly."""
    + work_harder_prompt
    + code_prefix_prompt
)

no_compile_prompt = (
    "The code you provided does not compile. Identify what is wrong then generate new code that addresses these issues."
    + work_harder_prompt
    + code_prefix_prompt
)

update_prompt = (
    """
Take the above openscad code that you generated and add the following details to it. 
"""
    + work_harder_prompt
    + code_prefix_prompt
)
<<<<<<< HEAD:backend/prompts.py
=======


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
    # Ensure the output directory exists
    output_dir = f"generated/{generation_id}/{iteration}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Write the SCAD code to a file
    scad_file = f"{output_dir}/output.scad"
    with open(scad_file, 'w') as file:
        file.write(code)
    
    # Generate STL file
    stl_command = f"openscad -o {output_dir}/output.stl {scad_file}"
    stl_success = os.system(stl_command) == 0
    
    # Call the bash script to generate images
    bash_script = "./scad2image.sh"
    bash_command = f"{bash_script} {scad_file}"
    png_success = os.system(bash_command) == 0

    # Check if the final combined image is created
    final_image_path = f"{output_dir}/renders/final_image.png"
    if png_success and os.path.exists(final_image_path):
        # Move the final image to the output directory
        os.rename(final_image_path, f"{output_dir}/output.png")
        return stl_success
    else:
        return False


# Generates OpenSCAD code given an initial prompt
def generate_scad(input_prompt: str, old_generation_id: str = ""):
    iteration = 0
    if old_generation_id == "":
        prompt = f"{pre_prompt}\n\n{input_prompt}\n\n{openscad_cheatsheet}"
    else:
        prompt = f"{get_last_generated_scad(old_generation_id)}\n\n{update_prompt}"
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt},
    ]
    response = ""

    # make the generation id the current time
    generation_id = datetime.now().strftime("%Y%m%d%H%M%S")

    while iteration < ITERATION_LIMIT:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview", messages=messages
        )

        print("response", response)

        # get output from last message
        output = response.choices[0].message.content

        # append output to messages
        messages.append({"role": "assistant", "content": output})

        code = ""
        if "```" in output:
            code = output.split("```")[1].strip("openscad")
        elif "YES" in output:
            print("finished generation")
            return generation_id, iteration - 1
        else:
            print("no code found")
            messages.append({"role": "user", "content": no_compile_prompt})
            continue

        print(code)

        if not render_scad(code, generation_id, iteration=iteration):
            print("code does not compile")
            messages.append({"role": "user", "content": no_compile_prompt})
            continue

        last_generated_image = f"generated/{generation_id}/{iteration}/output.png"
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image(last_generated_image)}",
                        },
                    },
                    {"type": "text", "text": feedback_prompt},
                ],
            }
        )

        iteration += 1

    return generation_id, iteration - 1
>>>>>>> ae537af (added image check):generate.py
