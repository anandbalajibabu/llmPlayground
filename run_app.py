#!/usr/bin/env python3
"""
AI Summarization Platform - Application Launcher
Simple launcher script to start the application with proper configuration
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

# Colors for terminal output
class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'  # No Color
    BOLD = '\033[1m'

def print_header():
    """Print application header"""
    print(f"\n{Colors.BLUE}{'='*50}{Colors.NC}")
    print(f"{Colors.BLUE}  AI SUMMARIZATION PLATFORM{Colors.NC}")
    print(f"{Colors.BLUE}{'='*50}{Colors.NC}\n")

def print_status(message):
    """Print status message"""
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {message}")

def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {message}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")

def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}[ERROR]{Colors.NC} {message}")

def check_virtual_environment():
    """Check if virtual environment exists and is activated"""
    venv_paths = [
        Path("ai_summarizer_env"),
        Path("llm_summarizer_env"),  # Legacy name
        Path("venv"),
        Path(".venv")
    ]
    
    for venv_path in venv_paths:
        if venv_path.exists():
            print_success(f"Virtual environment found: {venv_path}")
            return venv_path
    
    print_error("No virtual environment found!")
    print_warning("Please run setup.sh first to create the environment")
    return None

def check_dependencies(venv_path):
    """Check if required dependencies are installed"""
    print_status("Checking dependencies...")
    
    # Get the Python executable from virtual environment
    if platform.system() == "Windows":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"
    
    if not python_exe.exists():
        print_error(f"Python executable not found in {venv_path}")
        return False
    
    # Test critical imports
    test_script = """
try:
    import fastapi
    import uvicorn
    import groq
    import PyPDF2
    from dotenv import load_dotenv
    print("✓ All dependencies available")
except ImportError as e:
    print(f"✗ Missing dependency: {e}")
    exit(1)
"""
    
    try:
        result = subprocess.run([str(python_exe), "-c", test_script], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print_success("All dependencies are installed")
            return True
        else:
            print_error(f"Dependency check failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print_error("Dependency check timed out")
        return False
    except Exception as e:
        print_error(f"Error checking dependencies: {e}")
        return False

def check_environment_file():
    """Check if .env file exists"""
    env_file = Path(".env")
    if env_file.exists():
        print_success("Environment file found")
        return True
    else:
        print_warning("No .env file found")
        print_status("Creating .env from template...")
        
        # Create .env from template if it exists
        env_example = Path("env_example.txt")
        if env_example.exists():
            try:
                with open(env_example, 'r') as src, open('.env', 'w') as dst:
                    dst.write(src.read())
                print_success("Created .env file from template")
                print_warning("Please edit .env file to add your API keys")
                return True
            except Exception as e:
                print_error(f"Failed to create .env file: {e}")
                return False
        else:
            print_warning("No env_example.txt found - continuing without .env")
            return True

def get_available_port():
    """Find an available port for the application"""
    import socket
    
    preferred_ports = [8000, 8001, 8080, 8888, 3000]
    
    for port in preferred_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return port
            except OSError:
                continue
    
    # If all preferred ports are taken, find any available port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 0))
        return s.getsockname()[1]

def start_application(venv_path, port=8000):
    """Start the FastAPI application"""
    print_status("Starting AI Summarization Platform...")
    
    # Get the Python executable from virtual environment
    if platform.system() == "Windows":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"
    
    # Check if main app file exists
    app_file = Path("modern_app.py")
    if not app_file.exists():
        print_error("Main application file (modern_app.py) not found!")
        return False
    
    try:
        print_success(f"Application starting at: http://localhost:{port}")
        print_status("Press Ctrl+C to stop the application")
        print("")
        
        # Start the application
        subprocess.run([str(python_exe), "modern_app.py"], check=True)
        
    except KeyboardInterrupt:
        print_status("\nApplication stopped by user")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Application failed to start: {e}")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def main():
    """Main launcher function"""
    print_header()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print_status("Initializing AI Summarization Platform...")
    
    # Check virtual environment
    venv_path = check_virtual_environment()
    if not venv_path:
        print_status("Run the following command to set up the environment:")
        print(f"  {Colors.BOLD}./setup.sh{Colors.NC}")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies(venv_path):
        print_error("Dependencies not properly installed")
        print_status("Try running setup.sh again:")
        print(f"  {Colors.BOLD}./setup.sh{Colors.NC}")
        sys.exit(1)
    
    # Check environment file
    check_environment_file()
    
    # Get available port
    port = get_available_port()
    if port != 8000:
        print_warning(f"Port 8000 is busy, using port {port} instead")
    
    # Start application
    success = start_application(venv_path, port)
    
    if success:
        print_success("Application terminated successfully")
    else:
        print_error("Application encountered an error")
        sys.exit(1)

if __name__ == "__main__":
    main()
