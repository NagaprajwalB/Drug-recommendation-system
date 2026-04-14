import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# Get absolute path to .env file (in parent directory)
from pathlib import Path
current_dir = Path(__file__).resolve().parent
env_path = current_dir.parent / '.env'

# Load the .env file
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
else:
    # Try loading from current directory as fallback
    load_dotenv(override=True)

# Try to import Groq and initialize client
try:
    from groq import Groq
    
    api_key = os.getenv("GROQ_API_KEY")
    
    if api_key and len(api_key) > 20:  # Valid key should be longer
        try:
            client = Groq(api_key=api_key)
            GROQ_AVAILABLE = True
        except Exception as init_error:
            client = None
            GROQ_AVAILABLE = False
            print(f"Groq init error: {init_error}")
    else:
        client = None
        GROQ_AVAILABLE = False
        print("API key not found or invalid")
except ImportError as e:
    GROQ_AVAILABLE = False
    client = None
    print(f"Groq import error: {e}")

def get_drug_recommendations(name, age, weight, symptoms, allergies, current_medications):
    """
    Call LLM API to get medical guidance based on symptoms.
    """
    
    system_prompt = f"""You are a medical guidance assistant. Provide safe, preliminary health suggestions based on symptoms.

IMPORTANT RULES:
1. Keep response SHORT and SIMPLE
2. Suggest specific common medicine names (generic names preferred)
3. Calculate exact dosage based on patient's age ({age} years) and weight ({weight} kg)
4. {f'IMPORTANT: Patient is allergic to: {allergies}. DO NOT suggest these medicines!' if allergies else 'No known allergies reported.'}
5. {f'Patient is currently taking: {current_medications}. Check for drug interactions.' if current_medications else 'Not currently on any medications.'}
6. Provide only 2-3 lines of simple home remedies using common household items
7. Use non-technical language

RESPONSE FORMAT:

**Condition:**
(1-2 sentences explaining what this might be in simple terms)

**Medicine Name:**
(Specific medicine name - use generic names like Paracetamol, Ibuprofen, Cetirizine, etc.)

**Dosage:**
(Exact dosage based on age {age} years and weight {weight} kg. Be specific: e.g., "500mg tablet, take 1 tablet every 6-8 hours after food, maximum 3 tablets per day")

**Home Remedies:**
(2-3 short lines only - simple things using water, salt, honey, ginger, warm compress, rest, etc.)

**When to See Doctor:**
(1-2 lines about warning signs)

Do not mention "OTC" or "over-the-counter" in the response. Just give the medicine name directly. Keep entire response under 150 words."""
    
    user_prompt = f"""
Patient: {name}
Age: {age} years
Weight: {weight} kg
Symptoms: {symptoms}
{f'Allergies: {allergies}' if allergies else ''}
{f'Current Medications: {current_medications}' if current_medications else ''}

Provide brief medical guidance with specific medicine name, dosage, and home remedies.
    """
    
    try:
        if not GROQ_AVAILABLE:
            raise Exception("Groq library not available")
        if not client:
            raise Exception("Groq client not initialized - API key issue")
        
        # Make API call with timeout
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=500,
            temperature=0.7,
            timeout=30.0  # 30 second timeout
        )
        
        if response and response.choices:
            return response.choices[0].message.content
        else:
            raise Exception("Empty response from API")
            
    except Exception as e:
        error_msg = str(e)
        print(f"API Error: {error_msg}")
        return rule_based_guidance(name, age, weight, symptoms, allergies, current_medications, error_msg)

def rule_based_guidance(name, age, weight, symptoms, allergies, current_medications, error_msg):
    s = (symptoms or "").lower()
    is_child = age < 12
    allergy_note = f" Avoid if allergic to: {allergies}." if allergies else ""

    # Default values
    condition = "General, self-limited condition"
    med_name = "Supportive care"
    dosage = "Use age/weight-appropriate dosing per label"
    home = "- Hydrate well with warm fluids\n- Adequate rest and sleep\n- Light, balanced meals"

    # Cough (dry vs productive)
    if any(k in s for k in ["cough","chest congestion","phlegm","sputum","bronchial"]):
        condition = "Possibly simple cough or upper airway irritation"
        med_name = "Dextromethorphan (dry cough), Guaifenesin (productive cough)"
        if is_child:
            dosage = (
                "Dextromethorphan: 2.5–5 mg every 4h (age-dependent). "
                f"Guaifenesin pediatric syrup per label. Weight {weight} kg."
            )
        else:
            dosage = (
                "Dextromethorphan: 10–20 mg every 4h or 30 mg every 6–8h. "
                "Guaifenesin: 200–400 mg every 4h or 600 mg ER every 12h."
            )
        home = "- Steam inhalation 10 min 2–3×/day\n- Warm honey–lemon water (age >1)\n- Elevate head while sleeping; avoid smoke/irritants"

    # Cold / allergic rhinitis
    elif any(k in s for k in ["cold","runny nose","sneeze","sneezing","allergy","nasal congestion"]):
        condition = "Possibly common cold or allergic rhinitis"
        med_name = "Cetirizine or Loratadine; Saline nasal spray"
        if is_child:
            dosage = "Cetirizine: 5 mg once daily or per pediatric label; Loratadine: 5 mg once daily"
        else:
            dosage = "Cetirizine: 10 mg once daily; Loratadine: 10 mg once daily"
        home = "- Warm fluids\n- Steam inhalation or saline nasal rinse\n- Humidify room air"

    # Fever / headache / body ache
    elif any(k in s for k in ["fever","pyrexia","high temperature","headache","body ache","pain"]):
        condition = "Possibly viral fever or minor pain"
        med_name = "Paracetamol (Acetaminophen); Ibuprofen (if appropriate)"
        if is_child:
            dosage = (
                f"Paracetamol: 10–15 mg/kg per dose every 6–8h (weight {weight} kg). "
                f"Ibuprofen: 5–10 mg/kg per dose every 6–8h with food (if age ≥6 months)."
            )
        else:
            dosage = (
                "Paracetamol: 500 mg every 6–8h (max 3–4 doses/day). "
                "Ibuprofen: 200–400 mg every 6–8h with food (max 1200 mg/day OTC)."
            )
        home = "- Lukewarm sponge bath\n- Fluids and light meals\n- Rest; monitor temperature"

    # Nausea / vomiting
    elif any(k in s for k in ["nausea","vomit","vomiting","motion sickness","queasy"]):
        condition = "Possibly gastritis or motion-related nausea"
        med_name = "Oral Rehydration Solution (ORS); Dimenhydrinate (as needed)"
        if is_child:
            dosage = (
                f"ORS small, frequent sips. Dimenhydrinate ~1 mg/kg per dose every 6h (weight {weight} kg), per pediatric label."
            )
        else:
            dosage = "ORS frequent sips. Dimenhydrinate 50 mg every 4–6h as needed"
        home = "- Ginger tea; small bland meals\n- ORS to prevent dehydration\n- Avoid heavy/oily foods"

    # Sore throat
    elif any(k in s for k in ["sore throat","throat pain","tonsil","laryngitis","hoarse"]):
        condition = "Possibly viral sore throat"
        med_name = "Throat lozenges; Paracetamol for pain; Cetirizine if allergic component"
        dosage = "Lozenges per label; Paracetamol per above; Cetirizine 10 mg adult / 5 mg child"
        home = "- Warm saltwater gargle 3–4×/day\n- Warm fluids (tea/clear soups)\n- Voice rest; avoid irritants"

    # Heartburn / acid reflux
    elif any(k in s for k in ["heartburn","acid reflux","acidity","reflux","indigestion"]):
        condition = "Possibly acid reflux/dyspepsia"
        med_name = "Famotidine; Antacid (calcium carbonate)"
        if is_child:
            dosage = "Pediatric dosing per label/physician advice; consider antacid per label"
        else:
            dosage = "Famotidine 10–20 mg once or twice daily; Antacid per label"
        home = "- Avoid spicy/fatty meals; smaller portions\n- Do not lie down within 3 hours of meals\n- Elevate head while sleeping"

    # Diarrhea (non-bloody, non-febrile)
    elif any(k in s for k in ["diarrhea","loose stools","watery stools"]):
        condition = "Possibly simple non-infectious diarrhea"
        med_name = "ORS; Loperamide (adult, non-infectious); Bismuth subsalicylate"
        if is_child:
            dosage = "ORS per label; avoid Loperamide in young children; consult pediatrician"
        else:
            dosage = (
                "Loperamide: 4 mg initially, then 2 mg after each loose stool (max 8 mg/day). "
                "Bismuth subsalicylate: 524 mg every 30–60 min (max 8 doses/day)."
            )
        home = "- ORS frequent small sips\n- BRAT-style bland diet (banana, rice, applesauce, toast)\n- Avoid dairy/oily foods temporarily"

    # Gas / bloating
    elif any(k in s for k in ["gas","bloating","flatulence"]):
        condition = "Possibly simple gas/bloating"
        med_name = "Simethicone; Antacid if dyspepsia"
        if is_child:
            dosage = "Simethicone pediatric drops per label"
        else:
            dosage = "Simethicone 80–125 mg every 6h as needed"
        home = "- Ginger tea\n- Avoid gassy foods (beans, carbonated drinks)\n- Gentle walking after meals"

    # Compose result
    result = (
        f"""**Condition:**\n{condition}\n\n**Medicine Name:**\n{med_name}\n\n**Dosage:**\n{dosage}{allergy_note}\n\n**Home Remedies:**\n{home}\n\n**When to See Doctor:**\n- Symptoms persist >3 days or worsen\n- High fever (>102°F), severe pain, blood in stool, breathing issues\n\n**API Error (for transparency):** {error_msg}\n"""
    )
    return result


def parse_medical_guidance(response_text):
    sections = {
        'condition': '',
        'medicine_name': '',
        'dosage': '',
        'home_remedies': '',
        'when_to_seek': ''
    }
    current = None
    for line in (response_text or '').splitlines():
        lower = line.lower().strip()
        if lower.startswith("**condition"):
            current = 'condition'; continue
        elif lower.startswith("**medicine name"):
            current = 'medicine_name'; continue
        elif lower.startswith("**dosage"):
            current = 'dosage'; continue
        elif lower.startswith("**home remedies"):
            current = 'home_remedies'; continue
        elif lower.startswith("**when to see doctor"):
            current = 'when_to_seek'; continue
        if current and line.strip():
            sections[current] += line + "\n"
    # Trim trailing newlines
    for k in list(sections.keys()):
        sections[k] = sections[k].strip()
    # Fallback: if nothing parsed, put entire text under condition
    if not any(sections.values()):
        sections['condition'] = (response_text or '').strip()
    return sections


def main():
    st.set_page_config(
        page_title="Drug Recommendation Demo",
        page_icon="💊",
        layout="wide"
    )
    
    # Header
    st.title("🏥 AI-Powered Drug Recommendation System")
    st.markdown("### Intelligent Medical Guidance Based on Your Symptoms")
    
    # Warning banner - simple and clean
    st.info("💡 This AI system provides preliminary guidance. Always consult a healthcare professional for proper diagnosis and treatment.")
    
    # Create form
    with st.form("patient_form"):
        st.subheader("Patient Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Patient Name", placeholder="Enter patient name")
            age = st.number_input("Age (years)", min_value=1, max_value=120, value=30)
            weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.5)
        
        with col2:
            allergies = st.text_input("Known Allergies (Optional)", placeholder="e.g., penicillin, aspirin")
            current_medications = st.text_input("Current Medications (Optional)", placeholder="e.g., vitamin D, ibuprofen")
        
        symptoms = st.text_area("Brief Description of Symptoms/Suffering", 
                               placeholder="Describe your symptoms in detail (e.g., experiencing severe headache for 3 days, accompanied by fever and nausea)",
                               height=100)
        
        submitted = st.form_submit_button("Get AI Recommendations", type="primary")
    
    # Process form submission
    if submitted:
        if not name.strip():
            st.error("Please enter patient name to continue.")
            return
        if not symptoms.strip():
            st.error("Please enter a description of symptoms to continue.")
            return
        
        with st.spinner("Analyzing symptoms and generating guidance..."):
            # Get medical guidance from LLM
            response = get_drug_recommendations(name, age, weight, symptoms, allergies, current_medications)
            guidance = parse_medical_guidance(response)
        
        # Display results
        st.success(f"✅ Medical Guidance for {name}")
        st.caption(f"Patient Profile: {age} years old, {weight} kg")
        st.divider()
        
        # Display in separate sections
        if guidance['condition']:
            st.markdown("### 🔍 Possible Condition")
            st.info(guidance['condition'])
        
        if guidance['medicine_name']:
            st.markdown("### 💊 Recommended Medicine")
            st.success(guidance['medicine_name'])
        
        if guidance['dosage']:
            st.markdown("### 📏 Dosage Instructions")
            st.warning(guidance['dosage'])
        
        if guidance['home_remedies']:
            st.markdown("### 🏠 Simple Home Remedies")
            st.info(guidance['home_remedies'])
        
        if guidance['when_to_seek']:
            st.markdown("### 🚨 When to See a Doctor")
            st.error(guidance['when_to_seek'])
        
        # Display full response for educational purposes
        with st.expander("🔍 View Full AI Response & Debug Info"):
            st.text(response)
            st.divider()
            st.caption(f"API Status: {'✅ Groq Available' if GROQ_AVAILABLE else '❌ Groq Not Available'}")
            st.caption(f"Client Initialized: {'✅ Yes' if client else '❌ No'}")
            st.caption(f"API Key Set: {'✅ Yes' if os.getenv('GROQ_API_KEY') else '❌ No'}")
            if os.getenv('GROQ_API_KEY'):
                key = os.getenv('GROQ_API_KEY') or ""
                if key:
                    st.caption(f"API Key Preview: {key[:10]}...{key[-10:] if len(key) > 20 else ''}")
    
    # Footer disclaimer
    st.markdown("---")
    st.markdown("""
    **IMPORTANT DISCLAIMER:** This application provides preliminary health suggestions based on AI analysis 
    and should NOT replace professional medical advice, diagnosis, or treatment. The suggestions are general 
    in nature and may not be suitable for your specific condition. Always consult with qualified healthcare 
    professionals for accurate diagnosis and personalized treatment plans.
    """)

if __name__ == "__main__":
    main()
