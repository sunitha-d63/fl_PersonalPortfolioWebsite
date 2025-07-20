from flask import Flask, render_template, request, redirect, url_for,send_from_directory
import json
from datetime import datetime

app = Flask(__name__)

# Load project data
with open('data/projects.json') as f:
    projects = json.load(f)

# Inject current year into all templates (for footer)
@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}

@app.route('/')
def index():
    # Featured projects for home page
    featured = projects[:3]
    return render_template('index.html', projects=featured)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects_page():
    tag = request.args.get('tag')
    filtered = [p for p in projects if (tag in p.get('tags', []))] if tag else projects
    return render_template('projects.html', projects=filtered, tag=tag)


@app.route('/project/<slug>')
def project_detail(slug):
    project = next((p for p in projects if p['slug'] == slug), None)
    if not project:
        return render_template('404.html'), 404
    return render_template('project_detail.html', project=project)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Example: handle submitted form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        print(f"Received contact form from {name} <{email}>: {message}")
        return redirect(url_for('contact_success'))
    return render_template('contact.html')

@app.route('/contact/success')
def contact_success():
    return render_template('contact_success.html')

@app.route('/download-cv')
def download_cv():
    # Make sure the file exists at static/files/your_cv.pdf
    return send_from_directory(
        directory='static/files',
        filename='your_cv.pdf',
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)
