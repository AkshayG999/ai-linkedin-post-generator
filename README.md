# AI LinkedIn Post Generator 🤖✍️

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

An AI-powered application that generates professional LinkedIn posts by researching current tech trends. Built with Streamlit, OpenAI GPT, and Metaphor API.

## ✨ Key Features

- 🎯 AI-driven content research and generation
- 📊 Multiple content formats (How-to, Lists, Polls)
- 🌍 Multi-language support
- 🔍 Real-time trend research
- 📋 One-click copy and download
- 🎨 Clean, modern UI

## 🛠️ Prerequisites

- Python 3.8+
- OpenAI API key
- Metaphor API key

## 📦 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Post_Generator
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export OPENAI_API_KEY='your-openai-api-key'
export METAPHOR_API_KEY='your-metaphor-api-key'
```

## 🚀 Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Access the application in your web browser at `http://localhost:8501`

3. Enter your desired keywords and select options:
   - Choose post type
   - Select post length
   - Pick language
   - Click "Generate LinkedIn Post"

## 🔧 Configuration Options

- **Post Types**: General, How-to Guides, Polls, Listicles, Reality Check Posts, Job Posts, FAQs, Checklists/Cheat Sheets
- **Post Length**: 1000 words, Long Form, Short Form
- **Languages**: English, Vietnamese, Chinese, Hindi, Spanish

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool uses AI to generate content. Always review and modify the generated content before posting on LinkedIn.
