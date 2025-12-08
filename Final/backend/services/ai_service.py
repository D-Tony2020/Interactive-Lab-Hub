from openai import OpenAI
import json
import os

# Using the key provided by user. 
# In production, this should be in os.environ.get("OPENAI_API_KEY")
API_KEY = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")

client = OpenAI(api_key=API_KEY)

def generate_recipes_from_inventory(inventory_items):
    """
    Generates recipes based on a list of inventory items.
    """
    if not inventory_items:
        return [{"name": "No items", "ingredients": [], "instructions": "Add items to your fridge first!", "time": "0 min"}]

    prompt = f"""
    You are a smart kitchen assistant. Based on these ingredients: {', '.join([i['name'] for i in inventory_items])},
    suggest 3 simple, health-conscious recipes.
    
    Return ONLY valid JSON in this format:
    [
        {{
            "name": "Recipe Name",
            "ingredients": ["Ingredient 1", "Ingredient 2"],
            "time": "15 min",
            "type": "seafood" | "meat" | "veg" | "fruit" | "egg" | "other",
            "instructions": "Short instructions..."
        }}
    ]
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message.content
        # Clean up code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1]
            
        return json.loads(content.strip())
    except Exception as e:
        print(f"AI Error: {e}")
        return []

def process_voice_query(query_text, inventory_context):
    """
    Answers user voice queries about the fridge.
    """
    import datetime
    
    def get_days_remaining(expiry_date_str):
        try:
            today = datetime.date.today()
            expiry = datetime.datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
            return (expiry - today).days
        except:
            return 0

    context_str = ", ".join([f"{i['name']} (expires in {get_days_remaining(i.get('expiry_date'))} days)" for i in inventory_context])
    
    prompt = f"""
    Context: The user has a smart fridge with these items: {context_str}.
    User Query: "{query_text}"
    
    Answer briefly and helpfully. If they ask what to cook, suggest something based on expiring items.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are FridgeMind, a helpful kitchen usage assistant."},
                      {"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I couldn't process that. Error: {str(e)}"

def transcribe_audio(audio_data):
    """
    Transcribes SpeechRecognition AudioData using OpenAI Whisper.
    """
    if not audio_data:
        return ""
    
    # Save to temp wav file for upload
    temp_filename = "temp_speech.wav"
    with open(temp_filename, "wb") as f:
        f.write(audio_data.get_wav_data())
        
    try:
        with open(temp_filename, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        print(f"Transcription Error: {e}")
        return ""
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

def generate_speech(text):
    """
    Generates speech audio from text using OpenAI TTS.
    """
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        return response.content
    except Exception as e:
        print(f"TTS Error: {e}")
        return None
