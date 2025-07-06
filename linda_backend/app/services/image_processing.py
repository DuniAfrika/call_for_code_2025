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
    #access_token = os.getenv("WATSONX_IAM")
    access_token = "eyJraWQiOiIyMDE5MDcyNCIsImFsZyI6IlJTMjU2In0.eyJpYW1faWQiOiJJQk1pZC02OTgwMDBZOVhFIiwiaWQiOiJJQk1pZC02OTgwMDBZOVhFIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiMDdhZGQzNzItODFmYy00NGZmLWE5NDMtNTBlODMxMjA5ODE5IiwiaWRlbnRpZmllciI6IjY5ODAwMFk5WEUiLCJnaXZlbl9uYW1lIjoiUm9kZ2VycyIsImZhbWlseV9uYW1lIjoiSGF3b25hIiwibmFtZSI6IlJvZGdlcnMgSGF3b25hIiwiZW1haWwiOiJoYXdvbmEuMTc1NjlAc3R1ZGVudHMua3l1LmFjLmtlIiwic3ViIjoiaGF3b25hLjE3NTY5QHN0dWRlbnRzLmt5dS5hYy5rZSIsImF1dGhuIjp7InN1YiI6Imhhd29uYS4xNzU2OUBzdHVkZW50cy5reXUuYWMua2UiLCJpYW1faWQiOiJJQk1pZC02OTgwMDBZOVhFIiwibmFtZSI6IlJvZGdlcnMgSGF3b25hIiwiZ2l2ZW5fbmFtZSI6IlJvZGdlcnMiLCJmYW1pbHlfbmFtZSI6Ikhhd29uYSIsImVtYWlsIjoiaGF3b25hLjE3NTY5QHN0dWRlbnRzLmt5dS5hYy5rZSJ9LCJhY2NvdW50Ijp7InZhbGlkIjp0cnVlLCJic3MiOiIxNzkyNmNjMzY3YzE0ODJhODY3YzNlZTY3YmRlZWJhMSIsImZyb3plbiI6dHJ1ZX0sImlhdCI6MTc1MTgzNzE5MywiZXhwIjoxNzUxODQwNzkzLCJpc3MiOiJodHRwczovL2lhbS5jbG91ZC5pYm0uY29tL2lkZW50aXR5IiwiZ3JhbnRfdHlwZSI6InVybjppYm06cGFyYW1zOm9hdXRoOmdyYW50LXR5cGU6YXBpa2V5Iiwic2NvcGUiOiJpYm0gb3BlbmlkIiwiY2xpZW50X2lkIjoiZGVmYXVsdCIsImFjciI6MSwiYW1yIjpbInB3ZCJdfQ.C9P2BYzzp-7OUtnRb1P4569d2s-GwOkhKqw4Df1z3XX1N1fJT5JK_MTN0V-mun6bNM_UrcJHN3twK0TpFLm3XQ06k1-43d48zCCwfaZ1NeOLdzIyvnsc7Slifui8fysh3YPVGQiUnZhXoG20CTtuPDXFxfKOYkjAw6FI0OzjmKQ3LOZXs3bcD-TJIbA6cX1tkjb6ALDyPuhqsNtQyEkmvQrQJcmaLezELuAJZfKbu2a_3_2XTI0hfzt4O_MBjmqWXERnhD_xN4TK443YutglwV4nQNIssNrtVUJ-q0x5sX7MTrB3e-zKzX1RZkke3M-OA3C3tWPorB96WGY8cfcMTQ"
    #project_id = os.getenv("WATSONX_PROJECT_ID")
    project_id = "459773d2-c05b-41c5-99fb-6300e6456992"
    #model_id = os.getenv("IMAGE_MODEL_ID")
    model_id = "meta-llama/llama-3-2-11b-vision-instruct" 
    url = "https://eu-de.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29"

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
