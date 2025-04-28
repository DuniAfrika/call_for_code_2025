"""Granite Instruct Engine"""
import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv

load_dotenv()

def process_nlp(text_input):
    # try:
    credentials = Credentials(
      url = os.getenv("WATSONX_URL"),
      api_key = os.getenv("WATSONX_API_KEY"),
    )

    client = APIClient(credentials)
    params = {
        "decoding_method": "greedy",
        "max_new_tokens": 100
    }

    model_id = os.getenv("NLP_MODEL_ID")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    space_id = None # optional
    verify = False

    model = ModelInference(
      model_id=model_id,
      api_client=client,
      params=params,
      project_id=project_id,
      space_id=space_id,
      verify=verify,
    )

    prompt = text_input
    response = model.generate_text(prompt)

    # print(model.generate(prompt))

    # print(model.generate_text(prompt))
    return response
    # except Exception as e:
    #     print("❌ Error processing message:", str(e))
