import os
from flask import Flask, request, render_template
from dotenv import load_dotenv
import mindsdb_sdk
import requests
import time

load_dotenv()

app = Flask(__name__)

server = mindsdb_sdk.connect()

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


try:
    server.ml_engines.create(
        name="minds_endpoint_engine",
        type="minds_endpoint",
        connection_data={"minds_endpoint_api_key": os.getenv("API_KEY")}
    )
except Exception as e:
    print(f"ML Engine creation failed: {e}")


try:
    project = server.create_project("ai_blog_bot")
except Exception as e:
    project = server.get_project("ai_blog_bot")

#For Droping the models
# try:
#     project.drop_model('blog_generator_title')
#     project.drop_model('blog_generator_intro')
#     project.drop_model('blog_generator_body')
#     project.drop_model('blog_generator_conclusion')
# except Exception as e:
#     print(f"Model deletion failed: {e}")

try:
    project.models.create(
        name="blog_generator_title",
        predict="blog_content",
        engine="minds_endpoint_engine",
        max_tokens=152,
        prompt_template="Write a Blog Post Title about {{topic}} in about 50 words."
    )
except Exception as e:
    print(f"Model creation failed: {e}")


try:
    project.models.create(
        name="blog_generator_intro",
        predict="blog_introduction",
        engine="minds_endpoint_engine",
        max_tokens=500,
        prompt_template="Write only the intro part for my blogpost regarding the topic {{topic}}.Do not generate the whole blog post, just the introduction part of it. The introduction should be around 50 words.Do not Write Introduction word in it."
    )
except Exception as e:
    print(f"Model creation failed: {e}")


try:
    project.models.create(
        name="blog_generator_body",
        predict="blog_body",
        engine="minds_endpoint_engine",
        max_tokens=2048,
        prompt_template="Write the Body of the Blog Post about {{topic}} and the body should be 300 words.Do it in a way that it should be a continuation of the introduction. Do not Write Body word in it.Also give in paragraph format.Dont include the conclusion part in it."
    )
except Exception as e:
    print(f"Model creation failed: {e}")

try:
    project.models.create(
        name="blog_generator_conclusion",
        predict="blog_conclusion",
        engine="minds_endpoint_engine",
        max_tokens=152,
        prompt_template="Write a Blog Post Conclusion about {{topic}}.Do not generate other parts of the blog post, just the conclusion part of it. The conclusion should be around 50 words. Do not Write Conclusion word in it."
    )
except Exception as e:
    print(f"Model creation failed: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_blog():
    topic = request.form['topic']

    model = project.models.get("blog_generator_title")
    model_intro = project.models.get("blog_generator_intro")
    model_body = project.models.get("blog_generator_body")
    model_conclusion = project.models.get("blog_generator_conclusion")

    result_intro = model_intro.predict({"topic": topic})
    result = model.predict({"topic": topic})
    result_body = model_body.predict({"topic": topic})
    result_conclusion = model_conclusion.predict({"topic": topic})
    
    blog_intro = result_intro['blog_introduction'][0]
    blog_title = result['blog_content'][0]
    blog_body = result_body['blog_body'][0]
    blog_conclusion = result_conclusion['blog_conclusion'][0]

    image_url = generate_image(f"{topic} blog post illustration")
    
    return render_template('blog.html', topic=topic, title=blog_title,intro=blog_intro,body=blog_body,conclusion=blog_conclusion,image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
