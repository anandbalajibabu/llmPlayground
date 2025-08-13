# AI Summarization Platform - Complete Setup Guide

## 🎯 **Dual Provider System**

Your AI Summarization Platform now supports **both cloud and local AI models**:

- **☁️ Groq (Cloud)**: Fast, high-quality models via API
- **🖥️ Ollama (Local)**: Privacy-focused, offline models on your machine

## 🚀 **Quick Start (3 Steps)**

### **1. Setup the Platform**
```bash
./setup.sh
```

### **2a. Setup Cloud Models (Groq)**
- Get your free API key from [Groq Console](https://console.groq.com/keys)
- Enter it in the web interface when you start the app

### **2b. Setup Local Models (Ollama)**
```bash
./setup_ollama.sh
```

### **3. Start the Application**
```bash
./start_app.sh
```

**🌐 Access**: Open http://localhost:8000 in your browser

---

## 📋 **Detailed Setup Instructions**

### **Option A: Cloud Models Only (Groq)**

**Pros**: ✅ No local setup, ✅ High performance, ✅ Latest models
**Cons**: ❌ Requires internet, ❌ API costs (has free tier)

1. **Platform Setup**:
   ```bash
   ./setup.sh
   ```

2. **Get Groq API Key**:
   - Visit [console.groq.com/keys](https://console.groq.com/keys)
   - Sign up for free account
   - Generate API key

3. **Start & Configure**:
   ```bash
   ./start_app.sh
   ```
   - Enter API key in the web interface
   - Select from: Llama 3.1, Mixtral, Gemma models

---

### **Option B: Local Models Only (Ollama)**

**Pros**: ✅ Complete privacy, ✅ No API costs, ✅ Offline operation
**Cons**: ❌ Requires good hardware, ❌ Slower inference, ❌ Large downloads

1. **Platform Setup**:
   ```bash
   ./setup.sh
   ```

2. **Ollama Setup**:
   ```bash
   ./setup_ollama.sh
   ```
   This will:
   - Install Ollama
   - Download recommended models
   - Start the service

3. **Start Application**:
   ```bash
   ./start_app.sh
   ```
   - Look for 🖥️ Local models in the interface

---

### **Option C: Both Providers (Recommended)**

**Best of both worlds**: Use cloud for speed, local for privacy

1. **Platform Setup**:
   ```bash
   ./setup.sh
   ```

2. **Setup Both Providers**:
   ```bash
   # Setup local models
   ./setup_ollama.sh
   
   # Get Groq API key from console.groq.com/keys
   ```

3. **Start & Configure**:
   ```bash
   ./start_app.sh
   ```
   - Enter Groq API key for cloud models
   - Local models will be auto-detected

---

## 🖥️ **System Requirements**

### **For Cloud Models (Groq)**
- ✅ Any computer with internet
- ✅ 1GB RAM minimum
- ✅ Modern web browser

### **For Local Models (Ollama)**
- **Minimum**: 8GB RAM, 20GB storage
- **Recommended**: 16GB+ RAM, 50GB+ storage, SSD
- **Optimal**: 32GB+ RAM, GPU with 8GB+ VRAM

### **Model Size Guide**
```
Light Models (2-4GB):
├── phi3:mini (2.3GB) - Fast, good for testing
├── gemma:7b (4.8GB) - Balanced performance

Heavy Models (15-40GB):
├── llama3.1:70b (40GB) - Best quality, needs 64GB+ RAM
├── codellama:34b (19GB) - Code-focused, needs 32GB+ RAM
```

---

## 🔧 **Configuration Options**

### **Environment Variables (.env)**
```bash
# Cloud Provider
GROQ_API_KEY=your_groq_api_key_here

# Local Provider
OLLAMA_BASE_URL=http://localhost:11434

# Application
APP_NAME=AI Summarization Platform
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

### **Model Selection Strategy**
- **Speed Priority**: Use Groq cloud models
- **Privacy Priority**: Use Ollama local models
- **Cost Priority**: Use Ollama (free after setup)
- **Quality Priority**: Use both and compare results

---

## 🛠️ **Management Commands**

### **Application Commands**
```bash
./setup.sh              # Initial platform setup
./start_app.sh           # Start the application
python run_app.py        # Alternative startup method
```

### **Ollama Commands**
```bash
ollama list              # List installed models
ollama pull llama3.1:8b  # Download a specific model
ollama run llama3.1:8b   # Test a model directly
ollama rm llama3.1:8b    # Remove a model to save space
ollama serve             # Start Ollama service manually
```

### **Development Commands**
```bash
# Test providers
python llm_providers.py

# Check Ollama status
curl http://localhost:11434/api/tags

# View application logs
# (logs appear in terminal where you run start_app.sh)
```

---

## 🔍 **Troubleshooting**

### **Groq Issues**
- ❌ "Invalid API key": Check key at console.groq.com
- ❌ "Rate limit": Wait or upgrade Groq plan
- ❌ "Network error": Check internet connection

### **Ollama Issues**
- ❌ "Ollama offline": Run `ollama serve` or `./setup_ollama.sh`
- ❌ "Model not found": Run `ollama pull <model_name>`
- ❌ "Out of memory": Try smaller models (phi3:mini)
- ❌ "Slow inference": Ensure sufficient RAM/GPU

### **Application Issues**
- ❌ "Port 8000 busy": App will auto-select another port
- ❌ "Module not found": Run `./setup.sh` again
- ❌ "No models available": Configure at least one provider

### **Performance Tips**
1. **For Ollama**: Close other applications to free RAM
2. **For Groq**: Use smaller models for faster responses
3. **For Both**: Compare results to find best model for your use case

---

## 📊 **Model Comparison**

| Model | Provider | Size | Speed | Quality | Use Case |
|-------|----------|------|-------|---------|----------|
| Groq - Llama 3.1 8B | Cloud | API | ⚡⚡⚡ | ⭐⭐⭐⭐ | General purpose |
| Groq - Mixtral 8x7B | Cloud | API | ⚡⚡ | ⭐⭐⭐⭐⭐ | Complex tasks |
| Ollama - Phi3 Mini | Local | 2.3GB | ⚡⚡ | ⭐⭐⭐ | Testing/light use |
| Ollama - Llama 3.1 8B | Local | 4.7GB | ⚡ | ⭐⭐⭐⭐ | Balanced local |
| Ollama - Llama 3.1 70B | Local | 40GB | 🐌 | ⭐⭐⭐⭐⭐ | Best quality |

---

## 🎉 **Success Indicators**

### **Platform Ready**
- ✅ Web interface loads at http://localhost:8000
- ✅ Professional UI with 3 columns visible
- ✅ No error messages in terminal

### **Groq Working**
- ✅ API key accepted (green checkmark)
- ✅ ☁️ Cloud models appear in interface
- ✅ Fast summary generation (< 5 seconds)

### **Ollama Working**
- ✅ Status shows "✅ Online X models"
- ✅ 🖥️ Local models appear in interface
- ✅ Models respond (may take 10-30 seconds first time)

---

## 🆘 **Getting Help**

### **Quick Diagnostics**
```bash
# Check if everything is running
curl http://localhost:8000/health
curl http://localhost:11434/api/tags

# Test providers
python llm_providers.py
```

### **Reset Everything**
```bash
# Reset platform
rm -rf ai_summarizer_env .env
./setup.sh

# Reset Ollama
ollama rm $(ollama list | tail -n +2 | awk '{print $1}')
./setup_ollama.sh
```

---

## 🎯 **Next Steps**

1. **✅ Choose your setup**: Cloud only, Local only, or Both
2. **✅ Run setup scripts**: Follow the commands above
3. **✅ Start application**: `./start_app.sh`
4. **✅ Upload a document**: Test with PDF or sample text
5. **✅ Compare models**: Try both cloud and local models
6. **✅ Optimize settings**: Find the best models for your needs

**🚀 You're now ready to use both cloud and local AI models for professional text summarization!**
