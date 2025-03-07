from flask import Flask, render_template, send_from_directory, abort
import markdown
from pathlib import Path

# Initialize Flask application
app = Flask(__name__)

# Constants for content and static directories
CONTENT_DIR = Path("content")
STATIC_DIR = Path("static")


# Utility function to render templates with Markdown content
def render_markdown(template_name, markdown_file, additional_data=None):
    """Render a template with Markdown content."""
    try:
        # Read and convert Markdown file to HTML
        markdown_path = CONTENT_DIR / markdown_file
        markdown_content = markdown_path.read_text(encoding="utf-8")
        html_content = markdown.markdown(markdown_content)
    except FileNotFoundError:
        html_content = "<p>Error: Content not found</p>"

    # Prepare data for rendering
    data = {
        "MarkdownHTML": html_content,
        "Title": template_name.capitalize(),
    }
    if additional_data:
        data.update(additional_data)

    try:
        return render_template(f"{template_name}.html", **data)
    except Exception as e:
        # Log the error in production (e.g., with a logging library)
        print(f"Error rendering template {template_name}: {e}")
        abort(500, description=f"Template {template_name} not found.")


# Route handlers
@app.route("/")
def home():
    """Render the Home page."""
    return render_markdown("home", "home.md", {"UserProfileImage": "/static/images/profile.jpg"})


@app.route("/projects")
def projects():
    """Render the Projects page."""
    return render_markdown("projects", "projects.md")


@app.route("/TechStack")
def tech_stack():
    """Render the TechStack page."""
    return render_markdown("TechStack", "TechStack.md")


@app.route("/experience")
def experience():
    """Render the Experience page."""
    return render_markdown("experience", "experience.md")


@app.route("/contact")
def contact():
    """Render the Contact page."""
    return render_markdown("contact", "contact.md")


# Serve static files (e.g., CSS, JS, images)
@app.route("/static/<path:filename>")
def static_files(filename):
    """Serve static files."""
    try:
        return send_from_directory(STATIC_DIR, filename)
    except FileNotFoundError:
        abort(404, description=f"Static file {filename} not found.")


# Main entry point
if __name__ == "__main__":
    # Disable debug mode in production
    app.run(host="0.0.0.0", port=8989, debug=True)
