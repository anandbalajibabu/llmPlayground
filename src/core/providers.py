"""
LLM Providers - Dual Support for Groq (Cloud) and Ollama (Local)
Unified interface for multiple AI model providers
"""

import time
import os
import requests
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate_summary(self, text: str, max_length: int = 150) -> Dict[str, Any]:
        """Generate summary using the provider's API"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available and configured"""
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Get the model name"""
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the provider name"""
        pass
    
    @abstractmethod
    def get_display_name(self) -> str:
        """Get the display name for UI"""
        pass

class GroqProvider(BaseLLMProvider):
    """Groq cloud-based LLM provider"""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        self.model_name = model_name
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        self.model_info = {
            "llama3-70b-8192": {"provider": "Meta", "display_name": "Llama 3 70B", "type": "cloud"},
            "llama3-8b-8192": {"provider": "Meta", "display_name": "Llama 3 8B", "type": "cloud"},
            "llama-3.1-70b-versatile": {"provider": "Meta", "display_name": "Llama 3.1 70B", "type": "cloud"},
            "llama-3.1-8b-instant": {"provider": "Meta", "display_name": "Llama 3.1 8B", "type": "cloud"},
            "mixtral-8x7b-32768": {"provider": "Mistral AI", "display_name": "Mixtral 8x7B", "type": "cloud"},
            "gemma-7b-it": {"provider": "Google", "display_name": "Gemma 7B", "type": "cloud"},
            "gemma2-9b-it": {"provider": "Google", "display_name": "Gemma 2 9B", "type": "cloud"},
        }
        
        if self.api_key:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.api_key)
            except ImportError:
                self.client = None
        else:
            self.client = None
    
    def is_available(self) -> bool:
        """Check if Groq is available"""
        return self.client is not None and self.api_key is not None
    
    def generate_summary(self, text: str, max_length: int = 150) -> Dict[str, Any]:
        """Generate summary using Groq API"""
        start_time = time.time()
        
        if not self.is_available():
            return {
                "summary": "Groq API key not configured",
                "success": False,
                "response_time": 0,
                "token_count": None,
                "model": self.model_name,
                "provider": "Groq (Cloud)",
                "error": "API key not provided"
            }
        
        try:
            prompt = f"""Please provide a concise summary of the following text in approximately {max_length} words. Focus on the main points and key information:\n\n{text}\n\nSummary:"""
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_length * 2,
                temperature=0.3,
                top_p=1,
                stream=False
            )
            
            summary = response.choices[0].message.content.strip()
            response_time = time.time() - start_time
            
            return {
                "summary": summary,
                "success": True,
                "response_time": response_time,
                "token_count": response.usage.total_tokens if response.usage else None,
                "model": self.model_name,
                "provider": "Groq (Cloud)"
            }
            
        except Exception as e:
            return {
                "summary": f"Error generating summary: {str(e)}",
                "success": False,
                "response_time": time.time() - start_time,
                "token_count": None,
                "model": self.model_name,
                "provider": "Groq (Cloud)",
                "error": str(e)
            }
    
    def get_model_name(self) -> str:
        return self.model_name
    
    def get_provider_name(self) -> str:
        return "Groq (Cloud)"
    
    def get_display_name(self) -> str:
        model_info = self.model_info.get(self.model_name, {"display_name": self.model_name})
        return model_info["display_name"]

class OllamaProvider(BaseLLMProvider):
    """Ollama local LLM provider"""
    
    def __init__(self, model_name: str, base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        
        # Common Ollama models with their display names
        self.model_info = {
            "llama3.1:8b": {"provider": "Meta", "display_name": "Llama 3.1 8B", "type": "local"},
            "llama3.1:70b": {"provider": "Meta", "display_name": "Llama 3.1 70B", "type": "local"},
            "llama3:8b": {"provider": "Meta", "display_name": "Llama 3 8B", "type": "local"},
            "mistral:7b": {"provider": "Mistral AI", "display_name": "Mistral 7B", "type": "local"},
            "gemma:7b": {"provider": "Google", "display_name": "Gemma 7B", "type": "local"},
            "gemma2:9b": {"provider": "Google", "display_name": "Gemma 2 9B", "type": "local"},
            "phi3:mini": {"provider": "Microsoft", "display_name": "Phi-3 Mini", "type": "local"},
            "codellama:7b": {"provider": "Meta", "display_name": "CodeLlama 7B", "type": "local"},
            "neural-chat:7b": {"provider": "Intel", "display_name": "Neural Chat 7B", "type": "local"},
        }
    
    def is_available(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            # Check if Ollama server is running
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                # Check if the specific model is available
                models = response.json().get("models", [])
                available_models = [model["name"] for model in models]
                return self.model_name in available_models
            return False
        except (requests.exceptions.RequestException, Exception):
            return False
    
    def generate_summary(self, text: str, max_length: int = 150) -> Dict[str, Any]:
        """Generate summary using Ollama API"""
        start_time = time.time()
        
        if not self.is_available():
            return {
                "summary": f"Ollama model '{self.model_name}' not available. Please ensure Ollama is running and model is installed.",
                "success": False,
                "response_time": 0,
                "token_count": None,
                "model": self.model_name,
                "provider": "Ollama (Local)",
                "error": f"Model {self.model_name} not available"
            }
        
        try:
            prompt = f"""Please provide a concise summary of the following text in approximately {max_length} words. Focus on the main points and key information:\n\n{text}\n\nSummary:"""
            
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "top_p": 1.0,
                    "num_predict": max_length * 2
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120  # Longer timeout for local processing
            )
            
            if response.status_code == 200:
                result = response.json()
                summary = result.get("response", "").strip()
                response_time = time.time() - start_time
                
                return {
                    "summary": summary,
                    "success": True,
                    "response_time": response_time,
                    "token_count": result.get("eval_count"),  # Ollama's token count
                    "model": self.model_name,
                    "provider": "Ollama (Local)"
                }
            else:
                return {
                    "summary": f"Ollama API error: {response.status_code}",
                    "success": False,
                    "response_time": time.time() - start_time,
                    "token_count": None,
                    "model": self.model_name,
                    "provider": "Ollama (Local)",
                    "error": f"API error: {response.status_code}"
                }
                
        except requests.exceptions.Timeout:
            return {
                "summary": "Request timed out. Local model may be too large for available resources.",
                "success": False,
                "response_time": time.time() - start_time,
                "token_count": None,
                "model": self.model_name,
                "provider": "Ollama (Local)",
                "error": "Request timeout"
            }
        except Exception as e:
            return {
                "summary": f"Error generating summary: {str(e)}",
                "success": False,
                "response_time": time.time() - start_time,
                "token_count": None,
                "model": self.model_name,
                "provider": "Ollama (Local)",
                "error": str(e)
            }
    
    def get_model_name(self) -> str:
        return self.model_name
    
    def get_provider_name(self) -> str:
        return "Ollama (Local)"
    
    def get_display_name(self) -> str:
        model_info = self.model_info.get(self.model_name, {"display_name": self.model_name})
        return model_info["display_name"]

class DualLLMManager:
    """Unified manager for both Groq and Ollama providers"""
    
    def __init__(self, groq_api_key: Optional[str] = None, ollama_base_url: str = "http://localhost:11434"):
        self.groq_api_key = groq_api_key
        self.ollama_base_url = ollama_base_url
        
        # Define available models for both providers
        self.groq_models = {
            "Groq - Llama 3.1 70B": "llama-3.1-70b-versatile",
            "Groq - Llama 3.1 8B": "llama-3.1-8b-instant",
            "Groq - Llama 3 70B": "llama3-70b-8192",
            "Groq - Llama 3 8B": "llama3-8b-8192",
            "Groq - Mixtral 8x7B": "mixtral-8x7b-32768",
            "Groq - Gemma 7B": "gemma-7b-it",
            "Groq - Gemma 2 9B": "gemma2-9b-it",
        }
        
        self.ollama_models = {
            "Ollama - Llama 3.1 8B": "llama3.1:8b",
            "Ollama - Llama 3.1 70B": "llama3.1:70b",
            "Ollama - Llama 3 8B": "llama3:8b",
            "Ollama - Mistral 7B": "mistral:7b",
            "Ollama - Gemma 7B": "gemma:7b",
            "Ollama - Gemma 2 9B": "gemma2:9b",
            "Ollama - Phi-3 Mini": "phi3:mini",
            "Ollama - CodeLlama 7B": "codellama:7b",
            "Ollama - Neural Chat 7B": "neural-chat:7b",
        }
    
    def get_available_providers(self) -> List[str]:
        """Get all available provider names"""
        all_models = list(self.groq_models.keys()) + list(self.ollama_models.keys())
        return all_models
    
    def get_enabled_providers(self) -> List[str]:
        """Get only enabled/available providers"""
        enabled = []
        
        # Check Groq models
        if self.groq_api_key:
            enabled.extend(self.groq_models.keys())
        
        # Check Ollama models
        enabled_ollama = self._get_available_ollama_models()
        enabled.extend(enabled_ollama)
        
        return enabled
    
    def _get_available_ollama_models(self) -> List[str]:
        """Get available Ollama models by checking which ones are installed"""
        available = []
        
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                installed_models = [model["name"] for model in response.json().get("models", [])]
                
                for display_name, model_name in self.ollama_models.items():
                    if model_name in installed_models:
                        available.append(display_name)
        except:
            pass  # Ollama not available
        
        return available
    
    def get_provider_instance(self, provider_name: str) -> Optional[BaseLLMProvider]:
        """Get provider instance for a given provider name"""
        if provider_name in self.groq_models:
            model_name = self.groq_models[provider_name]
            return GroqProvider(model_name, self.groq_api_key)
        elif provider_name in self.ollama_models:
            model_name = self.ollama_models[provider_name]
            return OllamaProvider(model_name, self.ollama_base_url)
        return None
    
    def generate_summary(self, provider_name: str, text: str, max_length: int = 150) -> Dict[str, Any]:
        """Generate summary using specified provider"""
        provider = self.get_provider_instance(provider_name)
        
        if provider is None:
            return {
                "summary": f"Provider '{provider_name}' not found",
                "success": False,
                "response_time": 0,
                "token_count": None,
                "model": "Unknown",
                "provider": "Unknown",
                "error": f"Provider '{provider_name}' not available"
            }
        
        return provider.generate_summary(text, max_length)
    
    def generate_multiple_summaries(self, provider_names: List[str], text: str, max_length: int = 150) -> Dict[str, Dict[str, Any]]:
        """Generate summaries using multiple providers"""
        results = {}
        
        for provider_name in provider_names:
            results[provider_name] = self.generate_summary(provider_name, text, max_length)
        
        return results
    
    def update_groq_api_key(self, api_key: str):
        """Update Groq API key"""
        self.groq_api_key = api_key
    
    def get_ollama_status(self) -> Dict[str, Any]:
        """Get Ollama server status and available models"""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return {
                    "available": True,
                    "model_count": len(models),
                    "models": [model["name"] for model in models]
                }
            else:
                return {"available": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"available": False, "error": str(e)}

# For backward compatibility, keep the original LLMManager class
class LLMManager(DualLLMManager):
    """Legacy LLMManager for backward compatibility"""
    pass

def demo_providers():
    """Demo function to test both providers"""
    print("🧪 Testing AI Providers...")
    
    # Test text
    test_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. Leading AI textbooks define the field as the study of "intelligent agents": any system that perceives its environment and takes actions that maximize its chance of achieving its goals. Some popular accounts use the term "artificial intelligence" to describe machines that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving".
    """
    
    manager = DualLLMManager()
    
    print(f"Available providers: {len(manager.get_available_providers())}")
    print(f"Enabled providers: {len(manager.get_enabled_providers())}")
    
    # Test Ollama status
    ollama_status = manager.get_ollama_status()
    print(f"Ollama status: {ollama_status}")
    
    # Test a summary if any providers are available
    enabled = manager.get_enabled_providers()
    if enabled:
        print(f"\n📝 Testing summary with: {enabled[0]}")
        result = manager.generate_summary(enabled[0], test_text, 100)
        print(f"Success: {result['success']}")
        print(f"Provider: {result['provider']}")
        if result['success']:
            print(f"Summary: {result['summary'][:100]}...")

if __name__ == "__main__":
    demo_providers()