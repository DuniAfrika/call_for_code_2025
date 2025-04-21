#!/usr/bin/env python3

from transformers import AutoProcessor, AutoModelForVision2Seq
#from huggingface_hub import hf_hub_download
from PIL import Image
# import torch

# device = "cuda" if torch.cuda.is_available() else "cpu"
device = "cpu"

model_path = "ibm-granite/granite-vision-3.2-2b"
processor = AutoProcessor.from_pretrained(model_path)
model = AutoModelForVision2Seq.from_pretrained(model_path).to(device)

# prepare image and text prompt, using the appropriate prompt template

#img_path = hf_hub_download(repo_id=model_path, filename='data/african_welder.jpg')
img_path = "/home/ratego/call_for_code_25/data/african_welder.jpg"
image = Image.open(img_path).convert("RGB")

conversation = [
    {
        "role": "user",
        "content": [
            {"type": "image", "url": image},
            {"type": "text", "text": "What is PPE is the person in the image lacking that is exposing him to danger?"},
        ],
    },
]
inputs = processor.apply_chat_template(
    conversation,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt"
).to(device)


# autoregressively complete prompt
output = model.generate(**inputs, max_new_tokens=100)
print(processor.decode(output[0], skip_special_tokens=True))

