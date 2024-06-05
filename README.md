# ScadLM

Open source agentic AI CAD generation built on OpenSCAD. We decided to build it because we didn't see any ideas of using a visual transformer to create feedback of the model generation process. We wanted to create a tool that would allow users to see the model being generated in real-time and download the model once it's done. In the end, it didn't work that well, but think there is still hope for the idea if the other parts of this project were improved.

We also attempted finetuning the model on a labeled dataset of descriptions and openscad files, but the model didn't learn anything useful. We think this is because the dataset was too small, and not high quality.

![image](https://github.com/KrishKrosh/ScadLM/assets/50386081/89324674-f635-4c9d-bd62-22d855ee768d)
![image](https://github.com/KrishKrosh/ScadLM/assets/50386081/8dea3644-9e1e-43e3-b152-9536415c2faa)


## Features

- Generate CAD models with a simple input
- View the generated model in the browser
- Download the generated model as STL or OpenSCAD file
- View iterations of the agent working on the model

## Requirements

- Python 3.6+
- OpenSCAD
  - You can download with brew: `brew install openscad`

## Installation

1. Clone the repository
2. Install the requirements: `pip install -r requirements.txt`
3. Run the server: `python server.py`
4. Run the frontend: `yarn start`
5. Open your browser to `localhost:3000`
6. Start generating CAD models!

## Usage

1. Fill out the input with what you want to generate
2. Hit generate
3. Wait for the model to generate
4. Download the model and use it in your CAD software

## Credits
Lots of inspiration and code from https://github.com/OpenOrion/CQAsk implementation!
Was made in ~15 hours at Runpod Open Source Hackathon.
