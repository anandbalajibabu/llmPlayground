#!/bin/bash

# Ollama Setup Script for AI Summarization Platform
# This script helps install and configure Ollama with recommended models

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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
    echo -e "${BLUE}  OLLAMA SETUP FOR AI SUMMARIZATION PLATFORM${NC}"
    echo -e "${BLUE}================================================${NC}\n"
}

# Check if Ollama is installed
check_ollama_installation() {
    print_status "Checking Ollama installation..."
    
    if command -v ollama &> /dev/null; then
        OLLAMA_VERSION=$(ollama --version 2>/dev/null || echo "unknown")
        print_success "Ollama found: $OLLAMA_VERSION"
        return 0
    else
        print_warning "Ollama is not installed"
        return 1
    fi
}

# Install Ollama
install_ollama() {
    print_status "Installing Ollama..."
    
    case "$(uname -s)" in
        Darwin*)
            print_status "Detected macOS - Installing via curl..."
            curl -fsSL https://ollama.ai/install.sh | sh
            ;;
        Linux*)
            print_status "Detected Linux - Installing via curl..."
            curl -fsSL https://ollama.ai/install.sh | sh
            ;;
        CYGWIN*|MINGW32*|MSYS*|MINGW*)
            print_error "Windows detected. Please install Ollama manually from https://ollama.ai"
            echo "After installation, run this script again."
            exit 1
            ;;
        *)
            print_error "Unsupported operating system"
            exit 1
            ;;
    esac
    
    print_success "Ollama installation completed"
}

# Start Ollama service
start_ollama() {
    print_status "Starting Ollama service..."
    
    # Check if Ollama is already running
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        print_success "Ollama is already running"
        return 0
    fi
    
    # Start Ollama in background
    case "$(uname -s)" in
        Darwin*)
            print_status "Starting Ollama on macOS..."
            ollama serve > /dev/null 2>&1 &
            ;;
        Linux*)
            print_status "Starting Ollama on Linux..."
            systemctl --user start ollama || ollama serve > /dev/null 2>&1 &
            ;;
    esac
    
    # Wait for Ollama to start
    print_status "Waiting for Ollama to start..."
    for i in {1..30}; do
        if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
            print_success "Ollama is now running"
            return 0
        fi
        sleep 1
    done
    
    print_error "Failed to start Ollama service"
    exit 1
}

# Download recommended models
download_models() {
    print_status "Downloading recommended models..."
    
    # Models to download (ordered by priority and size)
    declare -a models=(
        "phi3:mini"        # 2.3GB - Fast, good for testing
        "gemma:7b"         # 4.8GB - Balanced performance
        "llama3.1:8b"      # 4.7GB - Popular, good quality
        "mistral:7b"       # 4.1GB - Good performance
    )
    
    # Ask user which models to download
    echo -e "\n${YELLOW}Available Models:${NC}"
    echo "1. phi3:mini (2.3GB) - Fast, good for testing"
    echo "2. gemma:7b (4.8GB) - Balanced performance"
    echo "3. llama3.1:8b (4.7GB) - Popular, good quality"
    echo "4. mistral:7b (4.1GB) - Good performance"
    echo "5. All recommended models (~16GB total)"
    echo "6. Custom selection"
    
    echo -e "\n${BLUE}Choose option (1-6):${NC} "
    read -r choice
    
    case $choice in
        1)
            download_model "phi3:mini"
            ;;
        2)
            download_model "gemma:7b"
            ;;
        3)
            download_model "llama3.1:8b"
            ;;
        4)
            download_model "mistral:7b"
            ;;
        5)
            for model in "${models[@]}"; do
                download_model "$model"
            done
            ;;
        6)
            echo -e "${BLUE}Enter model names (space-separated):${NC} "
            read -r custom_models
            for model in $custom_models; do
                download_model "$model"
            done
            ;;
        *)
            print_warning "Invalid choice. Downloading phi3:mini as default..."
            download_model "phi3:mini"
            ;;
    esac
}

# Download a specific model
download_model() {
    local model=$1
    print_status "Downloading model: $model"
    
    if ollama pull "$model"; then
        print_success "Successfully downloaded: $model"
    else
        print_error "Failed to download: $model"
    fi
}

# List installed models
list_models() {
    print_status "Listing installed models..."
    
    if ollama list 2>/dev/null; then
        print_success "Models listed above are available for use"
    else
        print_warning "No models installed or Ollama not running"
    fi
}

# Test model functionality
test_model() {
    print_status "Testing model functionality..."
    
    # Get the first available model
    local test_model=$(ollama list 2>/dev/null | tail -n +2 | head -n 1 | awk '{print $1}')
    
    if [ -z "$test_model" ]; then
        print_warning "No models available for testing"
        return 1
    fi
    
    print_status "Testing model: $test_model"
    
    local test_prompt="Summarize this text in one sentence: Artificial intelligence is transforming how we work and live."
    
    if echo "$test_prompt" | ollama run "$test_model" >/dev/null 2>&1; then
        print_success "Model test passed: $test_model"
        return 0
    else
        print_error "Model test failed: $test_model"
        return 1
    fi
}

# Main setup function
main() {
    print_header
    
    print_status "Setting up Ollama for local AI model inference..."
    
    # Check system requirements
    print_status "Checking system requirements..."
    
    # Check available RAM (basic check)
    if command -v free &> /dev/null; then
        TOTAL_RAM=$(free -m | awk 'NR==2{printf "%.0f", $2/1024}')
        if [ "$TOTAL_RAM" -lt 8 ]; then
            print_warning "System has ${TOTAL_RAM}GB RAM. 8GB+ recommended for optimal performance."
        else
            print_success "System has ${TOTAL_RAM}GB RAM - sufficient for most models"
        fi
    fi
    
    # Install Ollama if not present
    if ! check_ollama_installation; then
        install_ollama
    fi
    
    # Start Ollama service
    start_ollama
    
    # Download models
    download_models
    
    # List installed models
    echo ""
    list_models
    
    # Test functionality
    echo ""
    test_model
    
    print_success "Ollama setup completed successfully!"
    
    echo -e "\n${GREEN}================================================${NC}"
    echo -e "${GREEN}  OLLAMA READY FOR AI SUMMARIZATION PLATFORM${NC}"
    echo -e "${GREEN}================================================${NC}"
    echo -e "\n${YELLOW}Next Steps:${NC}"
    echo -e "1. Start your AI Summarization Platform: ${BLUE}./start_app.sh${NC}"
    echo -e "2. Open http://localhost:8000 in your browser"
    echo -e "3. Look for 🖥️ Local models in the interface"
    echo -e "\n${YELLOW}Ollama Commands:${NC}"
    echo -e "   ${BLUE}ollama list${NC}          # List installed models"
    echo -e "   ${BLUE}ollama pull <model>${NC}  # Download new models"
    echo -e "   ${BLUE}ollama run <model>${NC}   # Test a model directly"
    echo -e "   ${BLUE}ollama rm <model>${NC}    # Remove a model"
    echo -e "\n${GREEN}Enjoy your local AI models!${NC}\n"
}

# Run main function
main
