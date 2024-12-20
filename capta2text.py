import os
import json
import cv2
import numpy as np
import base64
from openai import OpenAI
client = OpenAI()

def getText(data):
    try:
        content = []
        for image in data:
            val = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{image}"
                    }
                }
            content.append(val)
        response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": "Extract the text contained within an image provided by the user and return it in JSON format.\n\n# Steps\n\n1. Analyze the image to identify and extract any visible text.\n2. Ensure the extracted text is accurately captured.\n3. Structure the extracted text into the specified JSON format.\n\n# Output Format\n\n- The output should be a JSON object containing a single key-value pair.\n- Use the following format:\n  ```\n  {\n    \"text\": \"extracted text\"\n  }\n  ```\n\n# Notes\n\n- Ensure the accuracy of text extraction, especially regarding special characters, numbers, and punctuation.\n- Consider variations in font size, orientation, and color that may affect text extraction."
                                }
                            ]
                        },
                    {
                        "role": "user",
                        "content": content
                        }
                    ],
                response_format={
                    "type": "text"
                    },
                temperature=1,
                #max_completion_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
                )
        return json.loads(response.choices[0].message.content.replace("```","").replace('json',""))
    except Exception as e:
        print(response)
        print(e)
        return {"text":"NUL"}


def adjust_image(image_path, contrast=1.0, brightness=0, saturation=1.0, gamma=1.0):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Error: Image not found. Check the image path.")

    # Apply contrast and brightness
    adjusted_image = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)

    # Convert to HSV for saturation adjustment
    hsv_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv_image[..., 1] = hsv_image[..., 1] * saturation
    hsv_image = np.clip(hsv_image, 0, 255).astype(np.uint8)
    adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    # Apply gamma correction
    inv_gamma = 1.0 / gamma if gamma != 0 else 1.0  # Avoid division by zero
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    adjusted_image = cv2.LUT(adjusted_image, table)

    # Encode the image to base64
    retval, buffer = cv2.imencode('.png', adjusted_image)
    if not retval:
        raise RuntimeError("Error encoding image to PNG format.")
    b64_string = base64.b64encode(buffer).decode('utf-8')

    return b64_string

# Example usage
def getCaptaText(image):
    print("----------------------------------------------------")
    images = []
    images.append(adjust_image(image))
    images.append(adjust_image(image, 
                              contrast=3.0,  # Applying the contrast value as given
                              brightness=-100,  # Static brightness of 0
                              saturation=0,  # Static saturation of 0 (might turn image B&W)
                              gamma=0.1))  # Avoid zero gamma which causes division by zero
    images.append(adjust_image(image, 
                              contrast=3.0,  # Applying the contrast value as given
                              brightness=-100,  # Static brightness of 0
                              saturation=3.0,  # Static saturation of 0 (might turn image B&W)
                              gamma=0.1))  # Avoid zero gamma which causes division by zer

    text = getText(images)
    print(f"File{image} Text:{text}")
    return text

def main():
    paths = [f"captas{os.path.sep}{a}" for a in os.listdir("captas")]
    for path in paths:
        getCaptaText(path)
#    getCaptaText("")

if __name__=="__main__":
    main()



