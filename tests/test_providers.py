"""
Unit Tests for LLM Providers

Tests for the Groq and Ollama provider implementations.
"""

import pytest
import os
from unittest.mock import Mock, patch

# Import from the new structure
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.providers import GroqProvider, OllamaProvider, DualLLMManager

class TestGroqProvider:
    """Test suite for GroqProvider"""
    
    def test_groq_provider_initialization(self):
        """Test GroqProvider initialization"""
        provider = GroqProvider("llama3-8b-8192", "test_api_key")
        assert provider.model_name == "llama3-8b-8192"
        assert provider.api_key == "test_api_key"
    
    def test_groq_provider_availability(self):
        """Test GroqProvider availability check"""
        provider = GroqProvider("llama3-8b-8192", "test_api_key")
        # Should be available with API key
        assert provider.is_available() == True
        
        provider_no_key = GroqProvider("llama3-8b-8192", None)
        # Should not be available without API key
        assert provider_no_key.is_available() == False

class TestOllamaProvider:
    """Test suite for OllamaProvider"""
    
    def test_ollama_provider_initialization(self):
        """Test OllamaProvider initialization"""
        provider = OllamaProvider("llama3.1:8b")
        assert provider.model_name == "llama3.1:8b"
        assert provider.base_url == "http://localhost:11434"
    
    @patch('requests.get')
    def test_ollama_availability_check(self, mock_get):
        """Test Ollama availability check"""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"models": [{"name": "llama3.1:8b"}]}
        mock_get.return_value = mock_response
        
        provider = OllamaProvider("llama3.1:8b")
        assert provider.is_available() == True

class TestDualLLMManager:
    """Test suite for DualLLMManager"""
    
    def test_manager_initialization(self):
        """Test DualLLMManager initialization"""
        manager = DualLLMManager()
        assert manager is not None
        assert hasattr(manager, 'groq_models')
        assert hasattr(manager, 'ollama_models')
    
    def test_get_available_providers(self):
        """Test getting available providers"""
        manager = DualLLMManager()
        providers = manager.get_available_providers()
        assert len(providers) > 0
        assert any("Groq" in p for p in providers)
        assert any("Ollama" in p for p in providers)

# Future test cases to implement:
# - Test actual API calls (with mocking)
# - Test error handling
# - Test response formatting
# - Test concurrent requests
# - Integration tests with FastAPI

if __name__ == "__main__":
    pytest.main([__file__])
