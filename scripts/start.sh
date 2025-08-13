#!/bin/bash

# AI Summarization Platform - Start Script
# Simple script to start the application with the new structure

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 Starting AI Summarization Platform...${NC}"

# Check if virtual environment exists
if [ ! -d "llm_summarizer_env" ]; then
    echo -e "${BLUE}⚠️  Virtual environment not found. Please run setup first:${NC}"
    echo -e "   ./scripts/setup.sh"
    exit 1
fi

# Activate virtual environment
echo -e "${BLUE}📦 Activating virtual environment...${NC}"
source llm_summarizer_env/bin/activate

# Start the application
echo -e "${GREEN}✅ Starting server at http://localhost:8000${NC}"
echo -e "${BLUE}📚 Configure your AI providers in the web interface${NC}"
echo -e "${BLUE}⚡ Press Ctrl+C to stop${NC}"
echo ""

python main.py
