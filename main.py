import json
import os
import uuid
import base64
import capta2text
from flask import Flask, request
from capta2text import getCaptaText


def process_image(file_path):
    """Encode the saved image to a base64 string."""
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

def main():
    app =Flask("Agent_Handeler")
    agentHost = os.getenv("CONTAINER_NAME")

    @app.route("/capta", methods = ['POST'])
    def submitCapta():
        print(str(request))
        if 'file' not in request.files:
            return json.dumps({'error': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return json.dumps({'error': 'No selected file'})
        if file:
            f = f'captas/{str(uuid.uuid4())}.jpg'
            file.save(f)
            capText = getCaptaText(f)
            return json.dumps(capText)

        return json.dumps({'error': 'File upload failed'})




    @app.route("/api/canada/stats", methods = ['POST'])
    def home():
        print(request.json)
        return ""

    app.run(host=agentHost, port=8000)


if __name__=="__main__":
    main()



