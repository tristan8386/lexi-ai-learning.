# 🚀 Lexi AI - English Master

Lexi AI is a premium, AI-powered English learning application built with Streamlit and Google's Gemini AI. It provides a comprehensive suite of tools for IELTS learners to improve their vocabulary, speaking, reading, and writing skills.

![Lexi AI Logo](img/logo.png)

## ✨ Key Features

- **🔍 AI Vocabulary Lookup**: Deep analysis of words, including IPA, definitions, word families, synonyms/antonyms, and IELTS-specific nuances.
- **📚 Topic-Based Learning**: High-quality flashcards categorized by IELTS topics (Environment, Technology, Education, etc.).
- **🗣️ Speaking AI**: Mock speaking tests with real-time feedback on fluency, vocabulary, grammar, and pronunciation. Includes audio support via gTTS.
- **📖 IELTS Reading Simulator**: Generates academic reading passages and comprehension quizzes on-demand using AI.
- **✍️ Writing**: AI-driven evaluation of writing tasks with band score estimates and improvement suggestions.
- **📒 Digital Notebook**: Save and organize new vocabulary into a personal word bank for long-term retention.
- **🧠 Coaching**: An AI-powered assistant that provides guidance an feedback to help users improve their English learning.
- **🎯 Revision Arena**: Gamified review sessions to test your knowledge and track progress with XP.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **AI Engine**: [Google Generative AI (Gemini 1.5 Flash)](https://ai.google.dev/)
- **Database**: SQLite3
- **Audio**: gTTS (Google Text-to-Speech)
- **Styling**: Custom CSS for a premium dark-themed experience.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- A Google AI Studio API Key (Gemini API)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tristan8386/lexi-ai-learning.git
   cd lexi-ai-learning
   ```

2. **Set up the virtual environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Secrets**:
   Create a directory `.streamlit` and a file `secrets.toml`:
   ```toml
   # .streamlit/secrets.toml
   GENAI_API_KEY = "YOUR_GEMINI_API_KEY"
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 📂 Project Structure

- `app.py`: Main entry point and UI navigation.
- `views/`: Module-specific UI components (reading, writing, speaking, etc.).
- `modules/`: Backend logic for AI handling, database management, and data storage.
- `data/`: SQLite database files.
- `img/`: Assets and logo.

---
Developed with ❤️ by [Tristan](https://github.com/tristan8386)


