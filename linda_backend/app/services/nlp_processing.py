"""Granite Instruct Engine"""
import os
import json
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv

load_dotenv()

def process_nlp(text_input):
    credentials = Credentials(
      #url = os.getenv("WATSONX_URL"),
      url = "https://eu-de.ml.cloud.ibm.com",
      api_key = "LKOUzUw1whXTJYd_Wk-JC2_dCVVPehOh5ekcB4Ci2NaK"
      #api_key = os.getenv("WATSONX_API_KEY"),
    )

    client = APIClient(credentials)
    params = {
        "decoding_method": "greedy",
        "max_new_tokens": 250
    }

    #model_id = os.getenv("NLP_MODEL_ID")
    model_id = "ibm/granite-3-8b-instruct"
    #project_id = os.getenv("WATSONX_PROJECT_ID")
    project_id = "459773d2-c05b-41c5-99fb-6300e6456992"
    space_id = None
    verify = False

    model = ModelInference(
      model_id=model_id,
      api_client=client,
      params=params,
      project_id=project_id,
      space_id=space_id,
      verify=verify,
    )

    with open("/home/ubuntu/call_for_code_2025/linda_backend/app/services/ruleset.json") as f:
        ruleset_data = json.load(f)

    prompt = f"{text_input}+{ruleset_data}"
    response = model.generate_text(prompt)

    return response
