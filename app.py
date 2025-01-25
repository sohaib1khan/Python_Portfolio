from flask import Flask, render_template, send_from_directory
import markdown
from pathlib import Path

app = Flask(__name__)

# Function to render templates with Markdown content
def render_markdown(template_name, markdown_file, additional_data=None):
    content_dir = Path("content")
    try:
        with open(content_dir / markdown_file, "r", encoding="utf-8") as md_file:
            markdown_content = md_file.read()
        html_content = markdown.markdown(markdown_content)
    except FileNotFoundError:
        html_content = "<p>Error loading content</p>"

    data = {
        "MarkdownHTML": html_content,
        "Title": template_name.capitalize(),
    }
    if additional_data:
        data.update(additional_data)
    return render_template(f"{template_name}.html", **data)

# Handlers for each page
@app.route("/")
def home():
    return render_markdown("home", "home.md", {"UserProfileImage": "/static/images/profile.jpg"})

@app.route("/projects")
def projects():
    return render_markdown("projects", "projects.md")

@app.route("/TechStack")
def tech_stack():
    return render_markdown("TechStack", "TechStack.md")

@app.route("/experience")
def experience():
    return render_markdown("experience", "experience.md")

@app.route("/contact")
def contact():
    return render_markdown("contact", "contact.md")

# Static file serving (CSS, JS, Images)
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

# Main entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8989, debug=True)
