#!/usr/bin/env python
"""
Setup Script for Chemical Equipment Parameter Visualizer
Creates database, migrations, and initial data
"""

import os
import sys
import subprocess


def run_command(command, cwd=None):
    """Run a command and print output"""
    print(f"\n> {command}")
    result = subprocess.run(command, shell=True, cwd=cwd)
    return result.returncode == 0


def main():
    """Setup the project"""
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    backend_dir = os.path.join(project_root, 'backend')
    
    print("=" * 60)
    print("FOSSEE Chemical Equipment Parameter Visualizer - Setup")
    print("=" * 60)
    
    # Check Python version
    print(f"\nPython version: {sys.version}")
    
    # Create virtual environment if needed
    venv_path = os.path.join(project_root, 'venv')
    if not os.path.exists(venv_path):
        print("\nCreating virtual environment...")
        if not run_command(f"{sys.executable} -m venv venv", cwd=project_root):
            print("Failed to create virtual environment")
            return False
    
    # Install Python dependencies
    print("\nInstalling Python dependencies...")
    pip_path = os.path.join(venv_path, 'bin', 'pip')
    if os.name == 'nt':
        pip_path = os.path.join(venv_path, 'Scripts', 'pip.exe')
    
    req_file = os.path.join(project_root, 'requirements.txt')
    if not run_command(f"{pip_path} install -r {req_file}"):
        print("Failed to install dependencies")
        return False
    
    # Run Django migrations
    print("\nRunning Django migrations...")
    python_path = os.path.join(venv_path, 'bin', 'python')
    if os.name == 'nt':
        python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
    
    manage_py = os.path.join(backend_dir, 'manage.py')
    
    if not run_command(f"{python_path} {manage_py} makemigrations equipment"):
        print("Failed to create migrations")
        return False
    
    if not run_command(f"{python_path} {manage_py} migrate"):
        print("Failed to run migrations")
        return False
    
    # Load sample data
    print("\nLoading sample data...")
    load_script = os.path.join(project_root, 'scripts', 'load_sample_data.py')
    run_command(f"{python_path} {load_script}")
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print(f"""
Next steps:

1. Start the Django backend:
   cd backend
   ../venv/bin/python manage.py runserver

2. Start the React frontend:
   cd web-frontend
   npm install
   npm start

3. Or run the desktop application:
   cd desktop
   ../venv/bin/python main.py

Login credentials:
   Username: admin
   Password: admin123
""")
    
    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
