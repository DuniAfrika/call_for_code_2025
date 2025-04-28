import requests
import base64

def analyze_image_for_safety(image_path):
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
    access_token = "eyJraWQiOiIyMDI1MDMzMTA4NDUiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJJQk1pZC02NjIwMDRMS1dMIiwiaWQiOiJJQk1pZC02NjIwMDRMS1dMIiwicmVhbG1pZCI6IklCTWlkIiwianRpIjoiMWY4OTM5YjgtZjA0ZC00ZDM2LWFjMDgtNWJmOGVjMjk5YWFiIiwiaWRlbnRpZmllciI6IjY2MjAwNExLV0wiLCJnaXZlbl9uYW1lIjoiSGF3b25hIiwiZmFtaWx5X25hbWUiOiJXaXNkb20iLCJuYW1lIjoiSGF3b25hIFdpc2RvbSIsImVtYWlsIjoidHJ1bHloYXdvbmFAZ21haWwuY29tIiwic3ViIjoidHJ1bHloYXdvbmFAZ21haWwuY29tIiwiYXV0aG4iOnsic3ViIjoidHJ1bHloYXdvbmFAZ21haWwuY29tIiwiaWFtX2lkIjoiSUJNaWQtNjYyMDA0TEtXTCIsIm5hbWUiOiJIYXdvbmEgV2lzZG9tIiwiZ2l2ZW5fbmFtZSI6Ikhhd29uYSIsImZhbWlseV9uYW1lIjoiV2lzZG9tIiwiZW1haWwiOiJ0cnVseWhhd29uYUBnbWFpbC5jb20ifSwiYWNjb3VudCI6eyJ2YWxpZCI6dHJ1ZSwiYnNzIjoiZjc3MDA1ZGI0NzVjNDdmOTljYjNmM2VhMDJhMDkzOWYiLCJpbXNfdXNlcl9pZCI6IjEzNjAxNDg5IiwiZnJvemVuIjp0cnVlLCJpbXMiOiIyOTk2ODMyIn0sIm1mYSI6eyJpbXMiOnRydWV9LCJpYXQiOjE3NDU4Nzc5NjUsImV4cCI6MTc0NTg4MTU2NSwiaXNzIjoiaHR0cHM6Ly9pYW0uY2xvdWQuaWJtLmNvbS9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOmFwaWtleSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImRlZmF1bHQiLCJhY3IiOjEsImFtciI6WyJwd2QiXX0.FUyS1k4RPAPtwUPebM0-AfOL39CvyVfwz3VpxT06ODYzYSQx80huJ7orkj9fCBsdXTD95oshaDw4gD3E795QgG7-7tj0KgC9nRxjJG5x374Zo-4lca_vNbYAMh7dzsFm7c8JiYvk8sywqBQSedBkV9IhjYL-PKQ_-5cRYVsfDBRR9dtEDiWYHbH5qdBKEe57MhbwzuBdo6Ox4-Lfb9ytCyDd3mn9-sUDZIu22MUfOkcPDZpzKe7f5QAV6nWbv2998h3HB7W2Ov2KqAYiFSv1ZTobSZ--5iV4ZicPtYK8maxXsaZ096msWUG5TTALgRlhY32YGxDY5HynX53wPHwWAQ"  # <-- Put your token here
    project_id = "3c70b7b1-189e-4150-b142-523b51048706"
    model_id = "ibm/granite-vision-3-2-2b"
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

# --- Example usage ---
if __name__ == "__main__":
    try:
        result = analyze_image_for_safety("/home/ratego/call_for_code_25/data/african_welder.jpg")  # Just pass image path now
        print(result)
    except Exception as e:
        print(f"Error: {e}")

