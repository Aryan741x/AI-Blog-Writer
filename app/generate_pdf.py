from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import textwrap
import requests

def generate_pdf(title, intro, body, conclusion, image_url):
    pdf = canvas.Canvas("blog_post.pdf", pagesize=letter)
    pdf.setTitle(title)

    width, height = letter

    # Set margins
    margin = inch

    pdf.setFont("Helvetica-Bold", 16)
    title_lines = textwrap.wrap(title, width=80)  # wrap title to 80 characters per line
    curr = height - margin
    for line in title_lines:
        pdf.drawCentredString(width / 2.0, curr, line)  # center the title
        curr -= 0.3 * inch
    pdf.line(0, height - margin - 0.5 * inch, width, height - margin - 0.5 * inch)  # horizontal line
    current_height = height - 2 * margin

    # Introduction
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(margin, current_height, "Introduction")
    current_height -= 0.5 * inch
    pdf.setFont("Helvetica", 12)
    intro_lines = textwrap.wrap(intro, width=80)  # wrap text to 80 characters per line
    for line in intro_lines:
        pdf.drawString(margin, current_height, line)
        current_height -= 0.3 * inch
        if current_height < margin:
            pdf.showPage()
            current_height = height - 2 * margin

    current_height -= 0.5 * inch 
    # Body
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(margin, current_height, "Body")
    current_height -= 0.5 * inch
    pdf.setFont("Helvetica", 12)
    body_lines = textwrap.wrap(body, width=80)  # wrap text to 80 characters per line
    for line in body_lines:
        pdf.drawString(margin, current_height, line)
        current_height -= 0.3 * inch
        if current_height < margin:
            pdf.showPage()
            current_height = height - 2 * margin

    # Image
    if image_url:
        response = requests.get(image_url)
        if response.status_code == 200:
            image_path = "image.webp"
            with open(image_path, 'wb') as f:
                f.write(response.content)
            image_width = 5 * inch
            image_height = (image_width * 2) / 3  # Maintain aspect ratio 3:2
            pdf.drawImage(image_path, margin, current_height - image_height - inch, width=image_width, height=image_height)
            current_height -= image_height + inch

    current_height -= 0.6 * inch 

    # Conclusion
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(margin, current_height, "Conclusion")
    current_height -= 0.5 * inch
    pdf.setFont("Helvetica", 12)
    conclusion_lines = textwrap.wrap(conclusion, width=80)  # wrap text to 80 characters per line
    for line in conclusion_lines:
        pdf.drawString(margin, current_height, line)
        current_height -= 0.3 * inch
        if current_height < margin:
            pdf.showPage()
            current_height = height - 2 * margin

    pdf.showPage()
    pdf.save()
    return "blog_post.pdf"