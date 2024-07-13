import requests
import time
import os
def generate_image(prompt):
    url = "https://api.replicate.com/v1/predictions"
    payload = {
        "version": "72c05df2daf615fb5cc07c28b662a2a58feb6a4d0a652e67e5a9959d914a9ed2",
        "input": {
            "cfg": 3.5,
            "prompt": prompt,
            "aspect_ratio": "3:2",
            "output_format": "webp",
            "output_quality": 90,
            "negative_prompt": "",
            "prompt_strength": 0.85
        }
    }
    headers = {
        "Authorization": f"Token {os.getenv('REPLICATE_API_KEY')}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 201:
        prediction_id = response.json()['id']
        # Check the status of the prediction
        image_url = check_replicate_prediction(prediction_id)
        return image_url
    else:
        print(f"Failed to generate image: {response.status_code} - {response.text}")
        return None
    
def check_replicate_prediction(prediction_id):
    url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
    headers = {
        "Authorization": f"Token {os.getenv('REPLICATE_API_KEY')}"
    }
    
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            status = response.json()['status']
            if status == 'succeeded':
                return response.json()['output'][0]
            elif status == 'failed':
                print(f"Prediction failed: {response.json()}")
                return None
        else:
            print(f"Failed to check prediction status: {response.status_code} - {response.text}")
            return None
        time.sleep(5)