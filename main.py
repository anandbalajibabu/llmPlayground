#!/usr/bin/env python3
"""
AI Summarization Platform - Main Application Entry Point

Professional text summarization with dual AI provider support.
Supports both Groq (cloud) and Ollama (local) models.

Usage:
    python main.py              # Start the application
    python main.py --host 0.0.0.0 --port 8080  # Custom host/port
"""

import uvicorn
import argparse
import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.api.main import app

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description='AI Summarization Platform')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    # Set debug mode
    if args.debug:
        os.environ['DEBUG'] = 'True'
    
    print("🚀 Starting AI Summarization Platform...")
    print(f"📍 Server will be available at: http://{args.host}:{args.port}")
    print("🔧 Configure providers in the web interface")
    print("📚 Documentation: README.md")
    print("⚡ Press Ctrl+C to stop")
    print("")
    
    # Start the server
    uvicorn.run(
        "src.api.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload or args.debug,
        log_level="info" if not args.debug else "debug"
    )

if __name__ == "__main__":
    main()
