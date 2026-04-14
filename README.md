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
- Groq API key (get one at https://console.groq.com)
- Docker (optional, for containerized setup)

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
   
   Edit `.env` and add your Groq API key:
   \`\`\`
   GROQ_API_KEY=your_actual_groq_api_key_here
   \`\`\`

4. **Run the application:**
   \`\`\`bash
   streamlit run scripts/app.py
   \`\`\`

5. **Open your browser** to the URL shown in the terminal (usually `http://localhost:8501`)

### Docker Setup (Alternative)

If you prefer to run the application in Docker:

1. **Build the Docker image:**
   \`\`\`bash
   docker build -t drug-recommendation .
   \`\`\`

2. **Set up environment file:**
   Create a `.env` file in the project root:
   \`\`\`
   GROQ_API_KEY=your_actual_groq_api_key_here
   \`\`\`

3. **Run the container:**
   \`\`\`bash
   docker run -p 8501:8501 --env-file .env drug-recommendation
   \`\`\`

4. **Access the application** at `http://localhost:8501`

**Note:** The Docker container exposes port 8501 and automatically loads environment variables from the `.env` file.

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
Drug-recommendation-system/
├── dockerfile          # Docker container configuration
├── package.json        # Project metadata
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── scripts/
│   └── app.py         # Main Streamlit application
└── .env               # Your environment variables (create this)
\`\`\`

## Troubleshooting

### Local Setup
- **API Errors:** Check your Groq API key in the `.env` file
- **Module Not Found:** Ensure all requirements are installed with `pip install -r requirements.txt`
- **Port Issues:** Streamlit will automatically find an available port, or specify one with `streamlit run scripts/app.py --server.port 8502`
- **Python Version:** Ensure you have Python 3.8 or higher installed

### Docker Setup
- **Build Issues:** Clear Docker cache with `docker system prune` and rebuild
- **Port Already in Use:** Change the port mapping with `docker run -p 8502:8501 drug-recommendation`
- **API Errors in Container:** Verify `.env` file exists and contains valid Groq API key before running container
- **Permission Denied:** On Linux/Mac, prefix docker commands with `sudo`

## Learning Extensions

Students can extend this project by:
- Adding more sophisticated UI elements
- Implementing user authentication
- Adding data persistence
- Creating unit tests
- Exploring different LLM APIs
- Adding more safety checks and validations

Remember: This is purely educational. Real medical software requires extensive testing, regulatory approval, and should only be developed by qualified teams with medical expertise.
