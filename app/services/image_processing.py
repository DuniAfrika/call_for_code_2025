import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

def process_image(image_path):
    """
    Uploads an image to IBM Granite Vision model to assess work safety.
    
    Args:
        image_path (str): Path to the local image file.

    Returns:
        dict: JSON response from the model.
    Raises:
        Exception: If the API call fails.
    """
    
    # --- CONFIG (hardcoded inside) ---
    access_token = os.getenv("WATSONX_IAM")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    model_id = os.getenv("IMAGE_MODEL_ID")
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29"

    # --- PREPARE IMAGE BASE64 ---
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        raise Exception(f"Failed to read and encode image: {e}")

    # --- BUILD REQUEST BODY ---
    body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Please analyze the uploaded image and assess the safety preparedness "
                            "of the work environment. Identify any safety hazards, such as improper equipment usage, "
                            "lack of protective gear, or unsafe work practices. Provide recommendations for improving safety."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ],
        "project_id": project_id,
        "model_id": model_id,
        "frequency_penalty": 0,
        "max_tokens": 2000,
        "presence_penalty": 0,
        "temperature": 0,
        "top_p": 1
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    # --- SEND REQUEST ---
    response = requests.post(url, headers=headers, json=body)

    # --- HANDLE RESPONSE ---
    if response.status_code != 200:
        raise Exception(f"Request failed [{response.status_code}]: {response.text}")

    return response.json()
