# 🤖 AI Summarization Platform

> **Professional text summarization with dual AI provider support**

A modern, enterprise-grade web application that provides intelligent text summarization using both cloud-based and local AI models. Compare results from multiple AI providers through a sleek, responsive interface.

![Platform Features](https://img.shields.io/badge/AI-Dual%20Provider-blue) ![Models](https://img.shields.io/badge/Models-16%20Available-green) ![Interface](https://img.shields.io/badge/UI-Modern%20Glass%20Morphism-purple) ![Setup](https://img.shields.io/badge/Setup-Automated-orange)

## ✨ **Key Features**

### 🔄 **Dual Provider System**
- **☁️ Groq (Cloud)**: Ultra-fast inference with Llama, Mixtral, and Gemma models
- **🖥️ Ollama (Local)**: Privacy-focused, offline models running on your machine
- **🔄 Seamless Switching**: Compare results from cloud and local models side-by-side

### 🎨 **Modern Interface**
- **Glass Morphism Design**: Professional, translucent UI with backdrop blur effects
- **Single-Page Layout**: No scrolling needed - everything visible at once
- **Responsive Design**: Perfect experience on desktop, tablet, and mobile
- **Real-time Status**: Live indicators for API connections and model availability

### 🔒 **Smart Security**
- **Masked API Keys**: Environment variables automatically loaded and masked (gsk_****xyz)
- **User Override**: Click to override environment keys with custom ones
- **No Data Logging**: Your documents and API keys stay private

### 📄 **Document Processing**
- **PDF Upload**: Drag & drop PDF files for instant text extraction
- **Sample Documents**: Built-in sample documents for testing
- **Text Validation**: Smart content validation and error handling

## 🚀 **Quick Start**

### **1. Platform Setup**
```bash
git clone https://github.com/anandbalajibabu/llmPlayground.git
cd llmPlayground
./scripts/setup.sh
```

**📁 Important:** Configuration files are now organized in the `config/` directory:
- `config/requirements.txt` - Python dependencies  
- `config/env_example.txt` - Environment template

### **2. Choose Your AI Provider**

#### **Option A: Cloud Models (Groq) - Fast & Easy**
```bash
# 1. Get free API key from https://console.groq.com/keys
# 2. Create .env file from template
cp config/env_example.txt .env
# 3. Add your API key to .env file
echo "GROQ_API_KEY=your_actual_groq_key_here" >> .env
# OR edit .env manually with your preferred editor
```

#### **Option B: Local Models (Ollama) - Private & Free**
```bash
# Install Ollama and download models
./setup_ollama.sh
```

#### **Option C: Both Providers (Recommended)**
```bash
# 1. Setup local models
./setup_ollama.sh
# 2. Create .env file from template
cp config/env_example.txt .env
# 3. Add your Groq API key
echo "GROQ_API_KEY=your_actual_groq_key_here" >> .env
```

### **3. Start Application**
```bash
./scripts/start.sh
# Open http://localhost:8000
```

## 🎯 **Available AI Models**

### ☁️ **Groq (Cloud Models)**
| Model | Provider | Size | Speed | Use Case |
|-------|----------|------|-------|----------|
| **Llama 3.1 70B** | Meta | API | ⚡⚡⚡ | Best quality, complex tasks |
| **Llama 3.1 8B** | Meta | API | ⚡⚡⚡ | Balanced performance |
| **Mixtral 8x7B** | Mistral AI | API | ⚡⚡ | Excellent reasoning |
| **Gemma 7B** | Google | API | ⚡⚡⚡ | Fast, efficient |

### 🖥️ **Ollama (Local Models)**
| Model | Provider | Size | Privacy | Use Case |
|-------|----------|------|---------|----------|
| **Llama 3.1 8B** | Meta | 4.7GB | 🔒 100% | General purpose, private |
| **Mistral 7B** | Mistral AI | 4.1GB | 🔒 100% | Balanced local inference |
| **Phi-3 Mini** | Microsoft | 2.3GB | 🔒 100% | Lightweight, fast |
| **CodeLlama 7B** | Meta | 4.8GB | 🔒 100% | Code and technical content |

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    Modern Web Interface                     │
│           (Glass Morphism • Responsive • Real-time)        │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                  FastAPI Backend                           │
│              (Async • REST API • Validation)               │
└─────────────────┬───────────────┬───────────────────────────┘
                  │               │
        ┌─────────▼─────────┐   ┌─▼────────────────┐
        │   Groq Provider   │   │  Ollama Provider │
        │   (Cloud API)     │   │  (Local Server)  │
        │                   │   │                  │
        │ • Llama 3.1       │   │ • Llama 3.1      │
        │ • Mixtral         │   │ • Mistral        │
        │ • Gemma           │   │ • Phi-3          │
        └───────────────────┘   └──────────────────┘
```

## 📁 **Project Structure**

```
ai-summarization-platform/
├── 🚀 Core Application
│   ├── modern_app.py              # FastAPI backend
│   ├── llm_providers.py           # Dual provider system
│   ├── document_processor.py      # PDF processing
│   └── templates/index.html       # Modern web interface
├── ⚙️ Setup & Deployment
│   ├── setup.sh                   # Platform setup
│   ├── setup_ollama.sh           # Local models setup
│   ├── run_app.py                # Application launcher
│   └── requirements.txt          # Python dependencies
├── 📚 Documentation
│   ├── README.md                 # This file
│   ├── SETUP_GUIDE.md           # Detailed setup guide
│   └── PROJECT_STRUCTURE.md     # Architecture details
└── 🔧 Configuration
    ├── .env                      # Environment variables
    └── env_example.txt          # Environment template
```

## 🎨 **User Interface Features**

### **Step 1: Configure AI Providers**
- 🔑 **Groq API Key**: Auto-loaded from environment, masked for security
- 🖥️ **Ollama Status**: Real-time connection monitoring
- 🔄 **Model Selection**: Visual grid of available models with cloud/local indicators

### **Step 2: Upload Document**
- 📤 **Drag & Drop**: Intuitive PDF upload with visual feedback
- 📋 **Sample Documents**: Built-in test documents
- 👁️ **Preview**: Instant document preview and metrics

### **Step 3: Generate & Compare**
- 🎯 **Model Selection**: Choose multiple models for comparison
- 📏 **Length Control**: Adjust summary length with slider
- 📊 **Results**: Side-by-side comparison with performance metrics

## 🛠️ **System Requirements**

### **For Cloud Models (Groq)**
- ✅ Any computer with internet connection
- ✅ 2GB RAM minimum
- ✅ Modern web browser
- ✅ Groq API key (free tier available)

### **For Local Models (Ollama)**
- 💾 **Minimum**: 8GB RAM, 20GB storage
- 🚀 **Recommended**: 16GB RAM, 50GB storage, SSD
- ⚡ **Optimal**: 32GB RAM, GPU with 8GB VRAM

## 🔧 **Environment Variables**

```bash
# Cloud Provider (Optional)
GROQ_API_KEY=your_groq_api_key_here

# Local Provider (Optional)
OLLAMA_BASE_URL=http://localhost:11434

# Application Settings
APP_NAME=AI Summarization Platform
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

## 📊 **Performance Comparison**

| Aspect | Groq (Cloud) | Ollama (Local) |
|--------|--------------|----------------|
| **Speed** | ⚡⚡⚡ Ultra-fast (2-5s) | ⚡ Moderate (10-30s) |
| **Privacy** | ⚠️ API calls to cloud | ✅ 100% local/private |
| **Cost** | 💰 Pay per use (free tier) | 🆓 Free after setup |
| **Setup** | 🎯 API key only | 🔧 Local installation |
| **Internet** | 📡 Required | ❌ Offline capable |
| **Models** | 🚀 Latest, curated | 🏠 Full control |

## 🚀 **Deployment Options**

### **Local Development**
```bash
./start_app.sh
# Access: http://localhost:8000
```

### **Production Server**
```bash
# With environment variables
export GROQ_API_KEY="your_key"
export HOST="0.0.0.0"
export PORT="8000"
python modern_app.py
```

### **Docker Deployment**
```bash
# Build and run (Dockerfile not included, but easily adaptable)
docker build -t ai-summarization-platform .
docker run -p 8000:8000 -e GROQ_API_KEY="your_key" ai-summarization-platform
```

## 🔍 **API Endpoints**

### **Web Interface**
- `GET /` - Main application interface

### **API Endpoints**
- `POST /api/configure-key` - Configure Groq API key
- `GET /api/models` - List available models
- `GET /api/groq-status` - Check Groq connection
- `GET /api/ollama-status` - Check Ollama status
- `POST /api/process-pdf` - Upload and process PDF
- `POST /api/summarize` - Generate summaries
- `GET /api/sample-documents` - Get sample documents

## 🤝 **Contributing**

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** Pull Request

## 📄 **License**

This project is open source and available under the [MIT License](LICENSE).

## 🆘 **Support & Documentation**

- 📖 **Setup Guide**: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- 🏗️ **Architecture**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/anandbalajibabu/llmPlayground/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/anandbalajibabu/llmPlayground/discussions)

## 🎯 **Roadmap**

- [ ] **More Providers**: Add support for OpenAI, Anthropic, Google AI
- [ ] **Document Types**: Support for Word, PowerPoint, text files
- [ ] **Batch Processing**: Multiple document processing
- [ ] **Export Options**: PDF, Word, JSON export
- [ ] **API Authentication**: User accounts and API keys
- [ ] **Performance Analytics**: Detailed model comparison metrics

---

<div align="center">

**🚀 Built with FastAPI • ⚡ Powered by Groq & Ollama • 🎨 Modern Design**

[⭐ Star this repo](https://github.com/anandbalajibabu/llmPlayground) • [🐛 Report Issues](https://github.com/anandbalajibabu/llmPlayground/issues) • [💬 Discussions](https://github.com/anandbalajibabu/llmPlayground/discussions)

</div>