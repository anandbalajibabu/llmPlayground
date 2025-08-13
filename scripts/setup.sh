#!/bin/bash

# AI Summarization Platform - Automated Setup Script
# This script sets up the entire application on a new machine

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "\n${BLUE}================================================${NC}"
    echo -e "${BLUE}  AI SUMMARIZATION PLATFORM - SETUP SCRIPT${NC}"
    echo -e "${BLUE}================================================${NC}\n"
}

# Check if Python 3 is installed
check_python() {
    print_status "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
        print_success "Python $PYTHON_VERSION found"
        
        # Check if version is 3.8 or higher
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            print_success "Python version is compatible (3.8+)"
        else
            print_error "Python 3.8+ is required. Current version: $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 is not installed. Please install Python 3.8+ first."
        print_status "Visit: https://www.python.org/downloads/"
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    print_status "Checking pip installation..."
    
    if command -v pip3 &> /dev/null; then
        print_success "pip3 found"
    elif command -v pip &> /dev/null; then
        print_success "pip found"
    else
        print_error "pip is not installed. Installing pip..."
        python3 -m ensurepip --upgrade
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    
    if [ -d "llm_summarizer_env" ]; then
        print_warning "Virtual environment already exists. Removing old one..."
        rm -rf llm_summarizer_env
    fi
    
    python3 -m venv llm_summarizer_env
    print_success "Virtual environment created: llm_summarizer_env"
}

# Activate virtual environment and install dependencies
install_dependencies() {
    print_status "Activating virtual environment and installing dependencies..."
    
    source llm_summarizer_env/bin/activate
    
    # Upgrade pip first
    pip install --upgrade pip
    
    # Install dependencies
    if [ -f "config/requirements.txt" ]; then
        pip install -r config/requirements.txt
        print_success "Dependencies installed successfully"
    else
        print_error "config/requirements.txt not found!"
        exit 1
    fi
}

# Create environment file
create_env_file() {
    print_status "Creating environment configuration..."
    
    if [ ! -f ".env" ]; then
        cp config/env_example.txt .env
        print_success "Environment file created: .env"
        print_warning "Please edit .env file to add your Groq API key"
    else
        print_warning ".env file already exists"
    fi
}

# Create startup script
create_startup_script() {
    print_status "Creating startup script..."
    
    cat > start_app.sh << 'EOF'
#!/bin/bash

# AI Summarization Platform - Startup Script

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  AI SUMMARIZATION PLATFORM${NC}"
echo -e "${BLUE}================================================${NC}\n"

# Check if virtual environment exists
if [ ! -d "ai_summarizer_env" ]; then
    echo -e "\033[0;31m[ERROR]\033[0m Virtual environment not found!"
    echo "Please run setup.sh first"
    exit 1
fi

# Activate virtual environment
echo -e "${BLUE}[INFO]${NC} Activating virtual environment..."
source llm_summarizer_env/bin/activate

# Start the application
echo -e "${BLUE}[INFO]${NC} Starting AI Summarization Platform..."
echo -e "${GREEN}[SUCCESS]${NC} Application will be available at: http://localhost:8000"
echo -e "${BLUE}[INFO]${NC} Press Ctrl+C to stop the application"
echo ""

python main.py
EOF

    chmod +x start_app.sh
    print_success "Startup script created: start_app.sh"
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    
    source llm_summarizer_env/bin/activate
    
    # Test imports
    python3 -c "
import fastapi
import uvicorn
import groq
import PyPDF2
from dotenv import load_dotenv
print('✓ All dependencies imported successfully')
" 2>/dev/null && print_success "All dependencies are working correctly" || {
        print_error "Dependency test failed"
        exit 1
    }
}

# Main setup function
main() {
    print_header
    
    print_status "Starting automated setup for AI Summarization Platform..."
    
    # Check system requirements
    check_python
    check_pip
    
    # Setup project
    create_venv
    install_dependencies
    create_env_file
    create_startup_script
    test_installation
    
    print_success "Setup completed successfully!"
    
    echo -e "\n${GREEN}================================================${NC}"
    echo -e "${GREEN}  SETUP COMPLETE!${NC}"
    echo -e "${GREEN}================================================${NC}"
    echo -e "\n${YELLOW}Next Steps:${NC}"
    echo -e "1. Choose your AI provider setup:"
    echo -e "   ${BLUE}Cloud Models (Groq):${NC} Get API key from https://console.groq.com/keys"
    echo -e "   ${BLUE}Local Models (Ollama):${NC} Run ${BLUE}./setup_ollama.sh${NC}"
    echo -e "   ${BLUE}Both Providers:${NC} Do both of the above (recommended)"
    echo -e "2. Run: ${BLUE}./start_app.sh${NC} to start the application"
    echo -e "3. Open: ${BLUE}http://localhost:8000${NC} in your browser"
    echo -e "\n${YELLOW}Quick Commands:${NC}"
    echo -e "   ${BLUE}./start_app.sh${NC}        # Start the application"
    echo -e "   ${BLUE}./setup_ollama.sh${NC}     # Setup local AI models"
    echo -e "   ${BLUE}./setup.sh${NC}           # Re-run platform setup"
    echo -e "\n${YELLOW}Read More:${NC} ${BLUE}SETUP_GUIDE.md${NC} for detailed instructions"
    echo -e "\n${GREEN}Enjoy your dual-provider AI Summarization Platform!${NC}\n"
}

# Run main function
main
