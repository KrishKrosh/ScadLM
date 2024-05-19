#!/bin/bash

# Ensure OpenSCAD and ImageMagick are installed
if ! command -v openscad &> /dev/null; then
    echo "OpenSCAD could not be found. Please install it and try again."
    exit
fi

if ! command -v convert &> /dev/null; then
    echo "ImageMagick could not be found. Please install it and try again."
    exit
fi

# Input OpenSCAD file
input_file=$1

# Check if the input file is provided
if [ -z "$input_file" ]; then
    echo "Usage: $0 <path_to_scad_file>"
    exit 1
fi

# Define the output directory
output_dir=$(dirname "$input_file")/renders
mkdir -p "$output_dir"

# Determine optimal camera distance for views (adjust as necessary)
camera_distance=200

# Function to capture a view
capture_view() {
    local output_file=$1
    local camera_params=$2
    openscad -o "$output_file" --camera=$camera_params --viewall "$input_file"
}

# Capture isometric view (6 parameters: px,py,pz,cx,cy,cz)
capture_view "$output_dir/isometric.png" "$camera_distance,$camera_distance,$camera_distance,0,0,0"

# Capture specific angle view from the second image (adjust parameters)
capture_view "$output_dir/specific_angle.png" "0,0,0,0,90,1"

# Capture side view (6 parameters: px,py,pz,cx,cy,cz)
capture_view "$output_dir/side.png" "$camera_distance,0,0,0,0,0"

# Capture front view (6 parameters: px,py,pz,cx,cy,cz)
capture_view "$output_dir/front.png" "0,0,$camera_distance,0,0,0"

# Capture back view (6 parameters: px,py,pz,cx,cy,cz)
capture_view "$output_dir/back.png" "0,0,-$camera_distance,0,0,0"

# Add caption to the isometric view
convert \
    -background white \
    -gravity center \
    -size 200x50 caption:"Isometric Back View" \
    "$output_dir/isometric.png" +swap -append "$output_dir/isometric_labeled.png"

# Add caption to the specific angle view
convert \
    -background white \
    -gravity center \
    -size 200x50 caption:"Front View" \
    "$output_dir/specific_angle.png" +swap -append "$output_dir/specific_angle_labeled.png"

# Add caption to the side view
convert \
    -background white \
    -gravity center \
    -size 200x50 caption:"Side View" \
    "$output_dir/side.png" +swap -append "$output_dir/side_labeled.png"

# Add caption to the front view
convert \
    -background white \
    -gravity center \
    -size 200x50 caption:"Top View" \
    "$output_dir/front.png" +swap -append "$output_dir/front_labeled.png"

# Create a final combined image
convert \
    \( "$output_dir/isometric_labeled.png" "$output_dir/specific_angle_labeled.png" "$output_dir/side_labeled.png" "$output_dir/front_labeled.png" +append \) \
    -background white -append "$output_dir/final_image.png"

# Clean up intermediate images
rm "$output_dir/isometric.png" "$output_dir/specific_angle.png" "$output_dir/side.png" "$output_dir/front.png" 

echo "Combined image saved to $output_dir/final_image.png"
