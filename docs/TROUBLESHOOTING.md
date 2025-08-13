# 🔧 Troubleshooting Guide

## 🚨 **Common Issues and Solutions**

### **Issue 1: "Address already in use" (Port 8000 busy)**

**Symptoms:**
```
ERROR: [Errno 48] error while attempting to bind on address ('0.0.0.0', 8000): address already in use
```

**Solution:**
```bash
# Kill all running instances
pkill -f "python.*main.py"
pkill -f "uvicorn"

# Force kill anything on port 8000
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Start fresh
./scripts/start.sh
```

### **Issue 2: Blank page at http://0.0.0.0:8000**

**Problem:** Browser cannot resolve `0.0.0.0`

**Solution:** Use these URLs instead:
- ✅ **http://localhost:8000**
- ✅ **http://127.0.0.1:8000**

### **Issue 3: Virtual environment not found**

**Symptoms:**
```
Virtual environment not found. Please run setup first
```

**Solution:**
```bash
# Run the setup script
./scripts/setup.sh

# Or create manually
python3 -m venv llm_summarizer_env
source llm_summarizer_env/bin/activate
pip install -r config/requirements.txt
```

### **Issue 4: Import errors or missing dependencies**

**Symptoms:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
# Activate environment and reinstall
source llm_summarizer_env/bin/activate
pip install -r config/requirements.txt
```

### **Issue 5: Template not found**

**Symptoms:**
```
TemplateNotFound: index.html
```

**Solution:** Check file structure:
```bash
# Verify template exists
ls -la src/ui/templates/index.html

# If missing, check if files were moved incorrectly
find . -name "index.html"
```

## 🔄 **Quick Reset Commands**

### **Complete Reset:**
```bash
# Stop everything
pkill -f "python.*main.py" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Clean start
./scripts/start.sh
```

### **Force Port Change:**
```bash
# Use different port
python main.py --port 8080
```

### **Debug Mode:**
```bash
# Start with detailed logging
python main.py --debug --reload
```

## 🎯 **Preferred Launch Methods (In Order)**

### **Method 1: Start Script (Recommended)**
```bash
./scripts/start.sh
```
- ✅ Simplest and most reliable
- ✅ Handles environment activation
- ✅ Clean error messages

### **Method 2: Direct Python**
```bash
source llm_summarizer_env/bin/activate
python main.py
```
- ✅ Direct control
- ✅ Custom arguments supported

### **Method 3: Python Launcher (Advanced)**
```bash
python scripts/run_app.py
```
- ✅ Comprehensive checks
- ✅ Automatic port detection
- ✅ Best for troubleshooting

## 🌐 **URL Access Guide**

| URL | Status | Use Case |
|-----|--------|----------|
| `http://localhost:8000` | ✅ **Recommended** | Primary browser access |
| `http://127.0.0.1:8000` | ✅ **Works** | Alternative local access |
| `http://0.0.0.0:8000` | ❌ **Don't use** | Bind address, not for browsers |

## 📊 **Health Check Commands**

### **Check if app is running:**
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000
# Should return: 200
```

### **Check API endpoints:**
```bash
# Models endpoint
curl -s http://localhost:8000/api/models | python -m json.tool

# Groq status
curl -s http://localhost:8000/api/groq-status | python -m json.tool

# Ollama status
curl -s http://localhost:8000/api/ollama-status | python -m json.tool
```

### **Check running processes:**
```bash
# Check for Python processes
ps aux | grep "python.*main.py"

# Check port usage
lsof -i:8000
```

## 🔧 **Development Tips**

### **Live Reload Development:**
```bash
python main.py --debug --reload
```

### **Custom Host for Network Access:**
```bash
python main.py --host 0.0.0.0 --port 8000
# Then access via: http://YOUR_IP:8000
```

### **Multiple Instances:**
```bash
# Run on different ports for testing
python main.py --port 8001
python main.py --port 8002
```

## 🆘 **Emergency Recovery**

If everything breaks:

```bash
# 1. Kill all processes
pkill -f python 2>/dev/null || true
killall uvicorn 2>/dev/null || true

# 2. Clean ports
for port in 8000 8001 8080; do
    lsof -ti:$port | xargs kill -9 2>/dev/null || true
done

# 3. Restart fresh
cd /path/to/llmPlayground
./scripts/setup.sh
./scripts/start.sh
```

## 📞 **Getting Help**

If you encounter issues not covered here:

1. **Check logs:** Look for error messages in the terminal
2. **Verify structure:** Ensure all files are in correct locations
3. **Test APIs:** Use curl commands to check individual endpoints
4. **Clean restart:** Use the emergency recovery commands above

---

**Your AI Summarization Platform should now be running smoothly! 🚀**
