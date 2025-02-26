# Gen AI Exploration Zone

A Flask application for experimenting with AI prompts using GOV.UK design system.

## Features

- Upload and manage documents for AI analysis
- Submit prompts to AI models
- Compare results between different AI models
- Responsive design following GOV.UK Design System

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gen-ai-exploration-zone.git
cd gen-ai-exploration-zone
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running the application

Start the development server:

```bash
flask run
```

The application will be available at http://localhost:5000/

## Deployment

This application is designed to be deployed at a subdirectory path:
`https://example.com/app-subdirectory/`

The subdirectory path can be configured in `config.py` or via the `SUBDIRECTORY_PATH` environment variable.

## Project Structure

- `app.py`: Main Flask application
- `config.py`: Configuration settings
- `static/`: Static files (CSS, JS, images)
- `templates/`: Jinja2 templates
- `uploads/`: Directory for uploaded files (created automatically)

## License

This project is licensed under the Open Government License v3.0.