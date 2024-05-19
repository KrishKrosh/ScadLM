import os
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv
import nomic
from nomic import AtlasDataset, embed
import numpy
import json
import requests
from prompts import (
    pre_prompt,
    openscad_cheatsheet,
    update_prompt,
    no_compile_prompt,
    feedback_prompt,
    system_msg,
)
from util import encode_image, get_last_generated_scad, render_scad

load_dotenv()

endpoint_id = os.environ.get("RUNPOD_ENDPOINT_ID")
# api_key = os.environ.get("RUNPOD_API_KEY")
api_key = os.environ.get("OPENAI_API_KEY")
nomic_api_key = os.environ.get("NOMIC_API_KEY")
llava_proxy = os.environ.get("LLAVA_PROXY")


client = OpenAI(
    # base_url=f"https://api.runpod.ai/v2/{endpoint_id}/openai/v1",
    api_key=api_key,
)

nomic.login(nomic_api_key)

# CONSTANTS
ITERATION_LIMIT = 2

project = AtlasDataset("bbldrizzy")
nomic_map = project.maps[0]


def generate_query_embedding(query):
    return embed.text(
        texts=[query],
        model="nomic-embed-text-v1.5",
        task_type="search_query",
    )


def similarity_search(query):
    query_embedding = generate_query_embedding(query)

    map = project.maps[0]
    neighbors, _ = map.embeddings.vector_search(
        queries=numpy.array(query_embedding["embeddings"]), k=3
    )

    similar_datapoints = project.get_data(ids=neighbors[0])
    proc_string = (
        "Here are some relevant examples showing openscad generation: "
        + json.dumps(similar_datapoints)
    )
    return proc_string



def query_llava_endpoint(input_prompt: str, image_encoded: str = None):
    payload = {
        "prompt": input_prompt,
    }
    if image_encoded:
        payload["image"] = image_encoded
    response = requests.post(
        llava_proxy,
        json=payload,
    )
    return response.json()



# Generates OpenSCAD code given an initial prompt
def generate_scad(input_prompt: str, old_generation_id: str = "", model="gpt"):
    iteration = 0
    examples = similarity_search(input_prompt)
    if old_generation_id == "":
        prompt = (
            f"{pre_prompt}\n\n{input_prompt}\n\n{openscad_cheatsheet}\n\n{examples}"
        )
    else:
        prompt = f"{get_last_generated_scad(old_generation_id)}\n\n{update_prompt}\n\n{examples}"
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt},
    ]
    response = ""

    # make the generation id the current time
    generation_id = datetime.now().strftime("%Y%m%d%H%M%S")

    while iteration < ITERATION_LIMIT:

        if model != "gpt":
            response = query_llava_endpoint(messages[-1]["content"])
        else:
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
