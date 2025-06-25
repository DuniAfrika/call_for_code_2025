"""Granite Instruct Engine"""
import os
import json
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv
from app.mcp.chat_context import ChatContext

load_dotenv()

def process_nlp(context: ChatContext) -> str:
    credentials = Credentials(
      url = os.getenv("WATSONX_URL"),
      api_key = os.getenv("WATSONX_API_KEY"),
    )

    client = APIClient(credentials)
    params = {
        "decoding_method": "greedy",
        "max_new_tokens": 250
    }

    model_id = os.getenv("NLP_MODEL_ID")
    project_id = os.getenv("WATSONX_PROJECT_ID")
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

    with open("/home/ratego/call_for_code_25/app/services/ruleset.json") as f:
        ruleset_data = json.load(f)
        
    # Get user message from context
    text_input = context.get_last_message(role="user")
    # Construct prompt (combine user input with ruleset)
    prompt = f"{text_input}+{ruleset_data}"
    response = model.generate_text(prompt)
    
     # Return just the content, depending on the structure of `response`
    if isinstance(response, dict) and "results" in response:
        return response["results"][0]["generated_text"]
    else:
        return str(response)
