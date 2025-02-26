#!/usr/bin/env python3
"""
Bootstrap script for the Gen AI Exploration Zone Flask application.
This script creates all necessary directories and files without content.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command):
    """Run a shell command and print the output"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    
    if result.stdout:
        print(result.stdout)
    
    return True

def main():
    # Define the project root directory
    root_dir = Path.cwd()
    
    # Create main directories
    directories = [
        "static",
        "static/stylesheets",
        "static/javascripts",
        "static/images",
        "templates",
        "templates/partials",
        "uploads"
    ]
    
    # Create directory structure
    for directory in directories:
        dir_path = root_dir / directory
        if not dir_path.exists():
            run_command(f"mkdir -p {dir_path}")
    
    # Define files to create
    files = [
        # Python files
        "app.py",
        "config.py",
        "wsgi.py",
        # Project files
        "requirements.txt",
        ".gitignore",
        ".env.example",
        "README.md",
        # Templates
        "templates/base.html",
        "templates/index.html",
        "templates/partials/header.html",
        "templates/partials/footer.html",
        # Static files
        "static/stylesheets/application.css",
        "static/javascripts/application.js"
    ]
    
    # Create empty files
    for file_path in files:
        full_path = root_dir / file_path
        if not full_path.exists():
            run_command(f"touch {full_path}")
    
    print("\nProject structure created successfully.")
    print("\nNext steps:")
    print("1. Create a virtual environment: python -m venv venv")
    print("2. Activate the virtual environment:")
    print("   - On Windows: venv\\Scripts\\activate")
    print("   - On Unix/Mac: source venv/bin/activate")
    print("3. Install requirements: pip install -r requirements.txt")
    print("4. Set up environment variables: cp .env.example .env (and edit as needed)")
    print("5. Run the application: flask run")
    print("\nMake sure to paste the content into the files!")

if __name__ == "__main__":
    main()
