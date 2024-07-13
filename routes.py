from flask import Blueprint, render_template, request, send_file
import os
from app.generate_pdf import generate_pdf
from app.generate_img import generate_image
from app.models import create_models
from dotenv import load_dotenv

routes = Blueprint("routes", __name__, template_folder="templates", static_folder="static")

load_dotenv()

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/generate', methods=['POST'])
def generate_blog():
    project = create_models()
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

    pdf_filename = generate_pdf(blog_title, blog_intro, blog_body, blog_conclusion,image_url)
    
    return render_template('blog.html', topic=topic, title=blog_title,intro=blog_intro,body=blog_body,conclusion=blog_conclusion,image_url=image_url ,pdf_filename=pdf_filename,pdf_ready=True)

@routes.route('/download/<filename>', methods=['GET'])
def download(filename):
    file_path = os.path.join(routes.root_path, filename)
    return send_file(file_path, as_attachment=True)