import openai
import sounddevice as sd
import soundfile as sf
import config
import pyttsx3
import os
import config

# Set up OpenAI credentials
openai.api_key = config.api_key

# Define trigger word and phrase for activation
TRIGGER_WORD = "sarah"
ACTIVATION_PHRASE = "how can I help you, Dre?"

# Initialize the TTS engine
engine = pyttsx3.init(driverName='espeak' ,libraryPath= '/usr/local/Cellar/espeak/1.48.04_1')
# Set the TTS voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) # you can change the voice by changing the index value

# Define sample rate and duration for audio recording
SAMPLE_RATE = 16000
DURATION = 5  # seconds

# Define function for transcribing audio to text using OpenAI API
def transcribe_audio_to_text(audio_path):
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Transcribe the following audio file: {audio_path}",
        temperature=0,
        max_tokens=4024,
    )

    return response.choices[0].text.strip()

# Define function for generating text response using OpenAI API
def generate_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
    )

    return response.choices[0].text.strip()

# Define main function for running the voice assistant
def main():
    while True:
        # Listen for trigger word
        print("Say sarah to activate the voice assistant...")
        # Speak the text
        engine.say("Hello, how can I help you?")
        engine.runAndWait()
        
        recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
        sd.wait()
        sf.write("input.wav", recording, SAMPLE_RATE)

        transcription = transcribe_audio_to_text("input.wav")

        if TRIGGER_WORD in transcription.lower():
            # Play activation phrase
            print("Trigger word detected. Activating voice assistant...")
            engine.say(ACTIVATION_PHRASE)
            engine.runAndWait()

            # Listen for user input
            print("Listening for user input...")
            recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
            sd.wait()
            sf.write("input.wav", recording, SAMPLE_RATE)

            # Transcribe user input to text
            text = transcribe_audio_to_text("input.wav")
            print(f"User input: {text}")

            # Generate response
            response = generate_response(text)
            print(f"Response: {response}")

            # Output response as audio
            engine.say(response)
            engine.runAndWait()
            
if __name__ == "__main__":
    main()
