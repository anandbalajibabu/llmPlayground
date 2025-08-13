"""
Document processing utilities for the LLM Summarization App
Handles PDF text extraction and document management
"""

import PyPDF2
import io
from typing import Dict, Optional
import streamlit as st

class DocumentProcessor:
    """Handle document processing operations"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_file) -> Dict[str, any]:
        """
        Extract text from uploaded PDF file
        
        Args:
            pdf_file: Uploaded PDF file (file-like object or BytesIO)
            
        Returns:
            Dict containing extracted text, metadata, and status
        """
        try:
            # Handle different file input types
            if hasattr(pdf_file, 'read'):
                pdf_content = pdf_file.read()
                if hasattr(pdf_file, 'seek'):
                    pdf_file.seek(0)  # Reset file pointer if possible
            else:
                pdf_content = pdf_file
            
            # Read PDF content
            if isinstance(pdf_content, bytes):
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
            else:
                pdf_reader = PyPDF2.PdfReader(pdf_content)
            
            # Extract text from all pages
            text_content = ""
            for page_num, page in enumerate(pdf_reader.pages):
                text_content += page.extract_text() + "\n"
            
            # Clean up the text
            text_content = text_content.strip()
            
            if not text_content:
                return {
                    "success": False,
                    "error": "No text content found in PDF",
                    "text": "",
                    "metadata": {}
                }
            
            # Calculate metadata
            word_count = len(text_content.split())
            char_count = len(text_content)
            page_count = len(pdf_reader.pages)
            
            # Get filename
            filename = getattr(pdf_file, 'name', 'uploaded_document.pdf')
            
            # Get file size
            file_size = 0
            if hasattr(pdf_file, 'getvalue'):
                file_size = len(pdf_file.getvalue())
            elif isinstance(pdf_content, bytes):
                file_size = len(pdf_content)
            
            metadata = {
                "filename": filename,
                "page_count": page_count,
                "word_count": word_count,
                "char_count": char_count,
                "file_size": file_size
            }
            
            return {
                "success": True,
                "text": text_content,
                "metadata": metadata,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing PDF: {str(e)}",
                "text": "",
                "metadata": {}
            }
    
    @staticmethod
    def get_sample_documents() -> Dict[str, str]:
        """
        Return a set of sample documents for testing
        
        Returns:
            Dict of sample document titles and their content
        """
        return {
            "AI and Machine Learning": """
            Artificial Intelligence (AI) and Machine Learning (ML) have emerged as transformative technologies 
            that are reshaping industries and society. AI refers to the simulation of human intelligence in 
            machines, enabling them to perform tasks that typically require human cognition, such as learning, 
            reasoning, and problem-solving. Machine Learning, a subset of AI, focuses on algorithms that can 
            learn and improve from data without explicit programming.
            
            The applications of AI and ML are vast and growing. In healthcare, these technologies assist in 
            medical diagnosis, drug discovery, and personalized treatment plans. In finance, they power 
            algorithmic trading, fraud detection, and risk assessment. The automotive industry leverages AI 
            for autonomous vehicles, while tech companies use ML for recommendation systems, natural language 
            processing, and computer vision.
            
            Recent breakthroughs in deep learning, particularly with neural networks, have accelerated AI 
            capabilities. Large language models like GPT and BERT have revolutionized natural language 
            understanding, while computer vision models can now recognize and classify images with superhuman 
            accuracy. These advances have made AI more accessible and practical for real-world applications.
            
            However, the rapid advancement of AI also brings challenges. Ethical considerations around bias, 
            privacy, and job displacement are increasingly important. The need for explainable AI, where 
            algorithms can provide reasoning for their decisions, has become crucial for trust and 
            accountability. Additionally, the environmental impact of training large AI models and the 
            concentration of AI power in few large corporations raise concerns about sustainability and 
            democratization of AI benefits.
            """,
            
            "Climate Change Solutions": """
            Climate change represents one of the most pressing challenges of our time, requiring immediate 
            and comprehensive action. The scientific consensus is clear: human activities, particularly the 
            emission of greenhouse gases from fossil fuel combustion, are driving unprecedented changes in 
            Earth's climate system. Rising global temperatures, melting ice caps, rising sea levels, and 
            extreme weather events are already impacting ecosystems and human societies worldwide.
            
            Renewable energy technologies offer the most promising pathway to decarbonization. Solar and wind 
            power have become increasingly cost-competitive with fossil fuels, with dramatic price reductions 
            over the past decade. Energy storage solutions, particularly battery technology, are advancing 
            rapidly to address intermittency challenges. Additionally, emerging technologies like green 
            hydrogen production and carbon capture and storage show potential for hard-to-decarbonize sectors.
            
            Beyond energy, climate solutions span multiple sectors. In transportation, electric vehicles are 
            gaining mainstream adoption, while sustainable aviation fuels and hydrogen-powered ships offer 
            solutions for long-distance travel. In agriculture, precision farming, regenerative practices, 
            and alternative proteins can reduce emissions while maintaining food security. Urban planning 
            that promotes public transportation, green buildings, and urban forests can significantly reduce 
            city-level emissions.
            
            International cooperation is essential for effective climate action. The Paris Agreement provides 
            a framework for global collaboration, though current commitments fall short of limiting warming 
            to 1.5°C. Carbon pricing mechanisms, technology transfer, and climate finance for developing 
            countries are critical tools for accelerating the transition to a sustainable economy. Individual 
            actions, while important, must be coupled with systemic changes in policy, business practices, 
            and social norms to achieve the scale of transformation required.
            """,
            
            "Digital Privacy and Security": """
            In our increasingly connected digital world, privacy and security have become fundamental concerns 
            for individuals, businesses, and governments. The proliferation of smart devices, social media 
            platforms, and online services has created an unprecedented amount of personal data collection 
            and sharing. This digital ecosystem offers tremendous benefits, including personalized experiences, 
            improved services, and enhanced connectivity, but it also poses significant risks to individual 
            privacy and security.
            
            Data breaches have become alarmingly common, with major companies experiencing security incidents 
            that expose millions of users' personal information. These breaches can lead to identity theft, 
            financial fraud, and other serious consequences for affected individuals. Moreover, the business 
            model of many tech companies relies on collecting and monetizing user data, often without users 
            fully understanding what information is being collected or how it's being used.
            
            Governments worldwide are responding with new privacy regulations. The European Union's General 
            Data Protection Regulation (GDPR) has set a global standard for data protection, giving individuals 
            greater control over their personal data. Similar legislation, such as the California Consumer 
            Privacy Act (CCPA), is being implemented in other jurisdictions. These regulations require 
            companies to be more transparent about data collection practices and give users rights to access, 
            correct, and delete their personal information.
            
            Technological solutions are also emerging to enhance privacy and security. End-to-end encryption 
            protects communications from unauthorized access, while privacy-preserving technologies like 
            differential privacy allow for data analysis without compromising individual privacy. Blockchain 
            technology offers potential for decentralized identity management, and artificial intelligence 
            is being used to detect and prevent cyber threats. However, the arms race between security 
            measures and malicious actors continues to evolve, requiring constant vigilance and adaptation.
            """
        }
    
    @staticmethod
    def validate_text_content(text: str, min_words: int = 50, max_words: int = 10000) -> Dict[str, any]:
        """
        Validate text content for summarization
        
        Args:
            text: Text content to validate
            min_words: Minimum word count required
            max_words: Maximum word count allowed
            
        Returns:
            Dict containing validation results
        """
        if not text or not text.strip():
            return {
                "valid": False,
                "error": "Text content is empty",
                "word_count": 0
            }
        
        words = text.split()
        word_count = len(words)
        
        if word_count < min_words:
            return {
                "valid": False,
                "error": f"Text too short. Minimum {min_words} words required, got {word_count}",
                "word_count": word_count
            }
        
        if word_count > max_words:
            return {
                "valid": False,
                "error": f"Text too long. Maximum {max_words} words allowed, got {word_count}",
                "word_count": word_count
            }
        
        return {
            "valid": True,
            "error": None,
            "word_count": word_count
        }
