# 🤖 LLM Summarization Comparison App (Powered by Groq)

A comprehensive web application built with Streamlit that allows users to compare text summarization results from multiple AI language models through Groq's ultra-fast inference platform.

## ✨ Features

- **Multi-LLM Support**: Compare summaries from Meta Llama, Mistral AI, and Google models via Groq
- **Single API Key**: Access multiple LLM providers through one Groq API key
- **Ultra-Fast Inference**: Groq's optimized hardware delivers lightning-fast results
- **Interactive Web Interface**: Elegant, sidebar-free Streamlit interface with real-time comparison
- **Database Integration**: Store and retrieve documents and summarization results
- **Performance Analytics**: Compare response times, token usage, and efficiency metrics
- **Historical Tracking**: View trends and historical performance data
- **Customizable Settings**: Adjust summary length and select specific models
- **Sample Data**: Pre-loaded with diverse sample documents for immediate testing

## 🛠️ Tech Stack

- **Frontend**: Streamlit (elegant, sidebar-free design)
- **Backend**: Python 3.13+
- **Database**: SQLite with SQLAlchemy ORM
- **LLM Infrastructure**: Groq API for ultra-fast inference
- **Available Models**: 
  - Meta Llama 3 & 3.1 (8B, 70B parameters)
  - Mistral AI Mixtral 8x7B
  - Google Gemma 7B & Gemma 2 9B
- **Visualization**: Plotly
- **Data Processing**: Pandas

## 📋 Prerequisites

- Python 3.9 or higher
- Groq API key (free tier available)
  - Sign up at [Groq Console](https://console.groq.com/)
  - Generate your API key
  - Access to multiple LLM models with one key!

## 🚀 Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd llmPlayground
   ```

2. **Activate the virtual environment** (already created):
   ```bash
   source llm_summarizer_env/bin/activate
   ```

3. **Set up environment variables**:
   - Copy the example environment file:
     ```bash
     cp env_example.txt .env
     ```
   - Edit `.env` and add your API keys:
     ```bash
     OPENAI_API_KEY=your_openai_api_key_here
     ANTHROPIC_API_KEY=your_anthropic_api_key_here
     GOOGLE_API_KEY=your_google_api_key_here
     ```

4. **Run the setup script**:
   ```bash
   python setup_app.py
   ```

5. **Start the application**:
   ```bash
   streamlit run app.py
   ```

## 🎯 Usage

### Getting Started

1. **Open your browser** and navigate to `http://localhost:8501`

2. **Initialize sample data** by clicking the "🔄 Initialize Sample Data" button in the sidebar

3. **Select a document** from the dropdown menu in the sidebar

4. **Choose LLM providers** you want to compare (requires valid API keys)

5. **Adjust summary settings** like maximum length

6. **Generate summaries** and compare the results!

### Main Features

#### 📄 Document Management
- View pre-loaded sample documents covering various topics
- Add custom documents through the interface
- Browse document metadata (category, word count, creation date)

#### 🧠 LLM Provider Comparison
- Support for multiple models from each provider:
  - **OpenAI**: GPT-3.5 Turbo, GPT-4, GPT-4 Turbo
  - **Anthropic**: Claude 3 Sonnet, Claude 3 Opus, Claude 3 Haiku
  - **Google**: Gemini Pro, Gemini Pro Vision

#### 📊 Analysis & Visualization
- **Summary Comparison**: Side-by-side view of generated summaries
- **Performance Metrics**: Response time and token usage analysis
- **Efficiency Analysis**: Words per second and cost-effectiveness
- **Historical Trends**: Track performance over time

#### 💾 Data Persistence
- All summaries are stored in the database
- Historical results for each document
- Performance tracking across different sessions

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# LLM API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./app_database.db

# Application Settings
APP_NAME=LLM Summarization App
DEBUG=True
```

### API Key Setup

#### OpenAI
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add it to your `.env` file

#### Anthropic
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Generate an API key
3. Add it to your `.env` file

#### Google AI
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Add it to your `.env` file

## 📁 Project Structure

```
llmPlayground/
├── app.py                 # Main Streamlit application
├── database.py            # Database models and management
├── llm_providers.py       # LLM provider integrations
├── setup_app.py           # Setup and initialization script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── env_example.txt        # Environment variables template
├── README.md              # This file
├── llm_summarizer_env/    # Virtual environment
└── app_database.db        # SQLite database (created automatically)
```

## 🔍 API Usage Examples

The application provides a clean interface, but you can also use the underlying components programmatically:

```python
from database import DatabaseManager
from llm_providers import LLMManager

# Initialize managers
db = DatabaseManager()
llm = LLMManager()

# Get available providers
providers = llm.get_available_providers()
print(f"Available providers: {providers}")

# Generate a summary
text = "Your text to summarize here..."
result = llm.generate_summary("OpenAI - GPT-3.5 Turbo", text, max_length=150)
print(f"Summary: {result['summary']}")
```

## 🛠️ Troubleshooting

### Common Issues

1. **"No LLM providers available"**
   - Check that your API keys are correctly set in the `.env` file
   - Ensure the `.env` file is in the project root directory
   - Verify your API keys are valid and have sufficient credits

2. **"No documents found"**
   - Click the "🔄 Initialize Sample Data" button in the sidebar
   - Or add a custom document using the interface

3. **Database errors**
   - Delete `app_database.db` and run `python setup_app.py` again
   - Check file permissions in the project directory

4. **Import errors**
   - Make sure the virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

### Performance Tips

- Start with shorter documents for faster response times
- Use GPT-3.5 for quicker results during testing
- Limit the number of providers when comparing many documents

## 🤝 Contributing

This is a demonstration project. To extend it:

1. Add new LLM providers by implementing the `LLMProvider` interface
2. Enhance the UI with additional Streamlit components
3. Add more analysis features and visualizations
4. Implement export functionality for results

## 📄 License

This project is for educational and demonstration purposes.

## 🙋‍♂️ Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify your API keys and environment setup
3. Run `python setup_app.py` to diagnose common problems

---

## 🎉 Quick Start Summary

```bash
# 1. Activate virtual environment
source llm_summarizer_env/bin/activate

# 2. Set up your API keys in .env file
cp env_example.txt .env
# Edit .env with your API keys

# 3. Initialize the application
python setup_app.py

# 4. Run the app
streamlit run app.py
```

Visit `http://localhost:8501` and start comparing LLM summaries! 🚀
