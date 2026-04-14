# Drug Recommendation Demo

An educational demonstration project showing how AI-powered drug recommendation systems might work conceptually. This project uses fake medications and is designed for learning purposes only.

## ⚠️ Important Disclaimer

**This is an educational demo only.** It uses fake medication names (MedA, MedB, MedC, etc.) and should never be used for actual medical advice, diagnosis, or treatment decisions. Always consult qualified healthcare professionals for medical concerns.

## Features

- Simple Streamlit web interface
- Patient information form (age, symptoms, allergies, current medications)
- LLM integration for generating educational recommendations
- Fake medication suggestions with reasoning
- Clear disclaimers and educational context

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (or other LLM API key)

### Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Set up environment variables:**
   \`\`\`bash
   cp .env.template .env
   \`\`\`
   
   Edit `.env` and add your API key:
   \`\`\`
   OPENAI_API_KEY=your_actual_api_key_here
   \`\`\`

4. **Run the application:**
   \`\`\`bash
   streamlit run app.py
   \`\`\`

5. **Open your browser** to the URL shown in the terminal (usually `http://localhost:8501`)

## How It Works

1. **Input Form:** Users enter patient-like information including age, symptoms, allergies, and current medications.

2. **LLM Processing:** The system sends a carefully crafted prompt to the LLM API requesting fake medication suggestions from a predefined list.

3. **Results Display:** The app shows 3 dummy medications with simple reasoning, clearly marked as educational content.

4. **Safety Features:**
   - Uses only fake medication names
   - Excludes medications mentioned in allergies
   - Displays prominent disclaimers
   - Shows full LLM response for transparency

## Educational Value

This project demonstrates:
- Web application development with Streamlit
- API integration patterns
- Prompt engineering for LLMs
- Responsible AI development practices
- Medical software safety considerations

## Customization

- **Different LLM APIs:** Modify the `get_drug_recommendations()` function to use other APIs
- **UI Changes:** Update the Streamlit interface in `main()`
- **Fake Medications:** Add more dummy medications to the predefined list
- **Reasoning Logic:** Enhance the prompt engineering for more sophisticated responses

## File Structure

\`\`\`
drug_recommendation/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.template      # Environment variables template
├── .env              # Your actual environment variables (create this)
└── README.md         # This file
\`\`\`

## Troubleshooting

- **API Errors:** Check your API key in the `.env` file
- **Module Not Found:** Ensure all requirements are installed with `pip install -r requirements.txt`
- **Port Issues:** Streamlit will automatically find an available port, or specify one with `streamlit run app.py --server.port 8502`

## Learning Extensions

Students can extend this project by:
- Adding more sophisticated UI elements
- Implementing user authentication
- Adding data persistence
- Creating unit tests
- Exploring different LLM APIs
- Adding more safety checks and validations

Remember: This is purely educational. Real medical software requires extensive testing, regulatory approval, and should only be developed by qualified teams with medical expertise.
