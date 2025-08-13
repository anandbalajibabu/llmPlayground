"""
Modern LLM Summarization App - FastAPI Backend
Ultra-modern, sleek web application for AI model comparison
"""

from fastapi import FastAPI, File, UploadFile, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import json
import asyncio
import time

from document_processor import DocumentProcessor
from llm_providers import DualLLMManager

# Initialize FastAPI app
app = FastAPI(
    title="AI Summarization Platform",
    description="Professional AI-powered text summarization with multiple model comparison",
    version="2.0.0"
)

# Mount templates only (no static files needed - using inline CSS/JS)
templates = Jinja2Templates(directory="templates")

# Global LLM manager with dual provider support
# Initialize with environment API key if available
groq_api_key = os.getenv("GROQ_API_KEY")
llm_manager = DualLLMManager(groq_api_key=groq_api_key)

# Pydantic models
class APIKeyRequest(BaseModel):
    api_key: str

class SummarizationRequest(BaseModel):
    text: str
    models: List[str]
    max_length: int = 150

class SummaryResponse(BaseModel):
    model: str
    summary: str
    response_time: float
    token_count: Optional[int]
    success: bool
    error: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the modern main interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/configure-key")
async def configure_api_key(request: APIKeyRequest):
    """Configure Groq API key"""
    try:
        global llm_manager
        
        # Handle special case where frontend sends 'use_env_key'
        if request.api_key == 'use_env_key':
            # Use the environment variable API key
            env_api_key = os.getenv("GROQ_API_KEY")
            if env_api_key:
                llm_manager.update_groq_api_key(env_api_key)
                api_key_source = "environment variable"
            else:
                return {
                    "success": False,
                    "message": "❌ No environment API key found.",
                    "models": []
                }
        else:
            # Use the provided API key (user override)
            llm_manager.update_groq_api_key(request.api_key)
            api_key_source = "user input"
        
        enabled_models = llm_manager.get_enabled_providers()
        
        if enabled_models:
            groq_models = [m for m in enabled_models if m.startswith('Groq')]
            if groq_models:
                return {
                    "success": True,
                    "message": f"✅ API key configured ({api_key_source})! {len(groq_models)} Groq models available.",
                    "models": enabled_models
                }
            else:
                return {
                    "success": True,
                    "message": f"✅ API key configured ({api_key_source})! Note: Groq models may take a moment to become available.",
                    "models": enabled_models
                }
        else:
            return {
                "success": False,
                "message": "❌ Invalid API key. Please check and try again.",
                "models": []
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Error: {str(e)}",
            "models": []
        }

@app.get("/api/models")
async def get_available_models():
    """Get list of available models"""
    return {
        "available": llm_manager.get_available_providers(),
        "enabled": llm_manager.get_enabled_providers()
    }

@app.get("/api/ollama-status")
async def get_ollama_status():
    """Get Ollama server status and available models"""
    return llm_manager.get_ollama_status()

@app.get("/api/groq-status")
async def get_groq_status():
    """Get Groq API key status (masked for security)"""
    api_key = os.getenv("GROQ_API_KEY")
    if api_key:
        # Mask the API key for security (show only first 4 and last 4 chars)
        if len(api_key) > 8:
            masked_key = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
        else:
            masked_key = "*" * len(api_key)
        
        return {
            "has_env_key": True,
            "masked_key": masked_key,
            "source": "environment variable"
        }
    else:
        return {
            "has_env_key": False,
            "masked_key": "",
            "source": "none"
        }

@app.post("/api/process-pdf")
async def process_pdf(file: UploadFile = File(...)):
    """Process uploaded PDF file"""
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Save temporarily and process
        content = await file.read()
        
        # Create a temporary file-like object
        import io
        file_obj = io.BytesIO(content)
        file_obj.name = file.filename
        
        result = DocumentProcessor.extract_text_from_pdf(file_obj)
        
        if result['success']:
            validation = DocumentProcessor.validate_text_content(result['text'])
            
            if validation['valid']:
                return {
                    "success": True,
                    "text": result['text'],
                    "metadata": result['metadata'],
                    "preview": result['text'][:500] + "..." if len(result['text']) > 500 else result['text']
                }
            else:
                return {
                    "success": False,
                    "error": validation['error']
                }
        else:
            return {
                "success": False,
                "error": result['error']
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error processing PDF: {str(e)}"
        }

@app.get("/api/sample-documents")
async def get_sample_documents():
    """Get available sample documents"""
    return DocumentProcessor.get_sample_documents()

@app.post("/api/summarize")
async def generate_summaries(request: SummarizationRequest):
    """Generate summaries using selected models"""
    try:
        if not llm_manager.get_enabled_providers():
            return {
                "success": False,
                "error": "No API key configured. Please set up your Groq API key first.",
                "results": []
            }
        
        if not request.text.strip():
            return {
                "success": False,
                "error": "No text provided for summarization.",
                "results": []
            }
        
        if not request.models:
            return {
                "success": False,
                "error": "No models selected for comparison.",
                "results": []
            }
        
        # Generate summaries
        results = []
        
        for model in request.models:
            try:
                result = llm_manager.generate_summary(model, request.text, request.max_length)
                
                summary_response = SummaryResponse(
                    model=model,
                    summary=result['summary'],
                    response_time=result['response_time'],
                    token_count=result.get('token_count'),
                    success=result['success'],
                    error=result.get('error') if not result['success'] else None
                )
                
                results.append(summary_response.dict())
                
            except Exception as e:
                error_response = SummaryResponse(
                    model=model,
                    summary="",
                    response_time=0.0,
                    token_count=None,
                    success=False,
                    error=str(e)
                )
                results.append(error_response.dict())
        
        successful_results = [r for r in results if r['success']]
        
        return {
            "success": len(successful_results) > 0,
            "message": f"Generated {len(successful_results)} of {len(results)} summaries successfully.",
            "results": results,
            "stats": {
                "total": len(results),
                "successful": len(successful_results),
                "failed": len(results) - len(successful_results),
                "avg_response_time": sum(r['response_time'] for r in successful_results) / len(successful_results) if successful_results else 0,
                "total_tokens": sum(r['token_count'] or 0 for r in successful_results)
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "results": []
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "2.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "modern_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
