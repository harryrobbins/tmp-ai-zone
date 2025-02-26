from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g
from werkzeug.utils import secure_filename
import os
import json
import logging
import datetime
from config import Config
from utils.openai_client import OpenAIClient
from utils.document_parser import parse_document
from flask_session import Session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Configure sessions
if app.config['SUBDIRECTORY_PATH']:
    app.config['SESSION_COOKIE_PATH'] = app.config['SUBDIRECTORY_PATH']

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_session')
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)
Session(app)

# Initialize OpenAI client
openai_client = OpenAIClient(api_key=app.config['OPENAI_API_KEY'])


# Configure the app to work in a subdirectory
class PrefixMiddleware:
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix
        print(f"Configuring app with prefix: {prefix}")

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return [b'Not Found']


# Apply the prefix middleware if we're in a subdirectory
if app.config['SUBDIRECTORY_PATH']:
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=app.config['SUBDIRECTORY_PATH'])
    print(f"Using subdirectory: {app.config['SUBDIRECTORY_PATH']}")

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Store uploaded files in session
def get_session_uploads():
    if 'uploads' not in session:
        session['uploads'] = []
    return session['uploads']


@app.route('/')
def index():
    return render_template('index.html', uploads=get_session_uploads(),
                           is_connect=app.config['IS_CONNECT'])


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Determine file type
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        # Check if the file type is supported
        supported_extensions = ['.pdf', '.docx', '.xlsx', '.xls', '.csv', '.txt', '.md', '.html', '.htm', '.jpg',
                                '.jpeg', '.png']
        if ext not in supported_extensions:
            os.remove(file_path)  # Remove unsupported file
            logger.warning(f"Unsupported file type: {ext}")
            return redirect(url_for('index'))

        # Add file to session
        uploads = get_session_uploads()
        uploads.append({
            'filename': filename,
            'path': file_path,
            'status': 'Uploaded',
            'type': ext[1:]  # Remove the dot from extension
        })
        session['uploads'] = uploads
        session.modified = True

    return redirect(url_for('index'))


@app.route('/remove/<filename>')
def remove_file(filename):
    uploads = get_session_uploads()

    for i, upload in enumerate(uploads):
        if upload['filename'] == filename:
            # Remove file from disk
            try:
                os.remove(upload['path'])
            except Exception as e:
                logger.error(f"Error removing file {filename}: {str(e)}")

            # Remove from session
            uploads.pop(i)
            session['uploads'] = uploads
            session.modified = True
            break

    return redirect(url_for('index'))


@app.route('/submit', methods=['POST'])
def submit_prompt():
    prompt = request.form.get('prompt', '')
    selected_models = request.form.getlist('modelComparison')

    # Log the prompt to the console
    print("\n" + "=" * 50)
    print("PROMPT RECEIVED:")
    print(prompt)
    print("=" * 50 + "\n")

    if not prompt:
        # No prompt provided, redirect back to the index page
        return redirect(url_for('index'))

    if not selected_models:
        # No models selected, redirect back to the index page
        return redirect(url_for('index'))

    # Log selected models
    print(f"Selected models: {', '.join(selected_models)}")

    # Get uploaded files content
    uploads = get_session_uploads()
    files_content = []

    print(f"Processing {len(uploads)} uploaded files...")

    for upload in uploads:
        try:
            file_path = upload['path']
            file_type = upload.get('type', '')

            # Parse file based on type
            if file_type in ['jpg', 'jpeg', 'png']:
                # We can't parse image content directly, just mention it
                content = f"[Image file: {upload['filename']}]"
            else:
                # Use document parser for text-based files
                content = parse_document(file_path)

            files_content.append({
                'filename': upload['filename'],
                'content': content
            })
            print(f"Successfully processed file: {upload['filename']}")
        except Exception as e:
            logger.error(f"Error processing file {upload['filename']}: {str(e)}")
            print(f"Error processing file {upload['filename']}: {str(e)}")

    # Create a combined prompt with file content if available
    combined_prompt = prompt
    if files_content:
        combined_prompt += "\n\nReference Documents:\n"
        for file_info in files_content:
            combined_prompt += f"\n--- {file_info['filename']} ---\n{file_info['content']}\n"

    # Log the combined prompt length
    print(f"Combined prompt length: {len(combined_prompt)} characters")
    print("Sending prompt to OpenAI API...")

    # Get responses from each selected model
    responses = {}
    for model in selected_models:
        try:
            response = openai_client.get_completion(combined_prompt, model)
            responses[model] = response
            print(f"Got response from {model}, length: {len(response)} characters")
        except Exception as e:
            error_message = str(e)
            logger.error(f"Error from OpenAI API ({model}): {error_message}")
            responses[model] = f"Error: {error_message}"

    # Store responses in session for display
    session['responses'] = responses
    session['prompt'] = prompt
    session.modified = True

    # Debug: print the stored session data
    print(f"Stored in session - prompt length: {len(session.get('prompt', ''))}")
    print(f"Stored in session - responses: {list(session.get('responses', {}).keys())}")

    # Use url_for with _scheme and _external to ensure proper redirection
    results_url = url_for('results')
    print(f"Redirecting to: {results_url}")
    return redirect(results_url)


@app.route('/results')
def results():
    # Get responses and prompt from session
    responses = session.get('responses', {})
    prompt = session.get('prompt', '')

    print(f"Results route - found prompt: {bool(prompt)}, responses: {list(responses.keys()) if responses else 'None'}")

    if not responses:
        print("No responses found in session, redirecting to index")
        return redirect(url_for('index'))

    # Get model display names
    model_names = {
        'gpt-4o': 'GPT-4o',
        'gpt-4o-mini': 'GPT-4o Mini'
    }

    # Format responses for template
    formatted_responses = []
    for model_id, response in responses.items():
        formatted_responses.append({
            'model_id': model_id,
            'model_name': model_names.get(model_id, model_id),
            'response': response
        })

    print(f"Rendering results template with {len(formatted_responses)} responses")
    return render_template('results.html',
                           prompt=prompt,
                           responses=formatted_responses,
                           single_response=len(formatted_responses) == 1,
                           is_connect=app.config['IS_CONNECT'])


@app.route('/debug')
def debug_info():
    """Debug route to show configuration information"""
    debug_data = {
        'SUBDIRECTORY_PATH': app.config['SUBDIRECTORY_PATH'],
        'IS_CONNECT': app.config['IS_CONNECT'],
        'URL_MAP': str(app.url_map),
        'SESSION_COOKIE_PATH': app.config.get('SESSION_COOKIE_PATH', 'Not set'),
        'SESSION_TYPE': app.config.get('SESSION_TYPE', 'Not set'),
        'SESSION_DATA': {
            'has_prompt': 'prompt' in session,
            'has_responses': 'responses' in session,
            'session_keys': list(session.keys())
        }
    }

    # Generate URLs for all routes
    routes = {}
    for rule in app.url_map.iter_rules():
        if 'GET' in rule.methods and rule.endpoint != 'static':
            try:
                routes[rule.endpoint] = url_for(rule.endpoint, _external=True)
            except:
                routes[rule.endpoint] = "Cannot generate URL"

    debug_data['ROUTES'] = routes

    return jsonify(debug_data)


@app.before_request
def before_request():
    # Add current deployment info to global template variables
    g.deployment_env = "Posit Connect" if app.config['IS_CONNECT'] else "Development"
    g.current_year = datetime.datetime.now().year


@app.context_processor
def utility_processor():
    def url_for_static(filename):
        return url_for('static', filename=filename)

    return dict(url_for_static=url_for_static)


@app.template_filter('nl2br')
def nl2br(value):
    # Convert newlines to <br> tags for displaying multiline text
    return value.replace('\n', '<br>')


if __name__ == '__main__':
    app.run(debug=True)