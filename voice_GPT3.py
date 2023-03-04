import openai, whisper 
import sounddevice as sd
import soundfile as sf
import config
# Set up OpenAI credentials
openai.api_key = config.api_key

# Define trigger word and phrase for activation
TRIGGER_WORD = "hey assistant"
ACTIVATION_PHRASE = "how can I help you?"

# Define sample rate and duration for audio recording
SAMPLE_RATE = 16000
DURATION = 5  # seconds

# Define function for transcribing audio to text using OpenAI Whisper API
def transcribe_audio_to_text(audio_path):
    response = openai.Completion.create(
        engine="davinci-whisper-1",
        prompt=f"Transcribe the following audio file: {audio_path}",
        temperature=0,
        max_tokens=1024,
    )

    return response.choices[0].text.strip()

# Define function for generating text response using OpenAI GPT-3 API
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
        print("Listening for trigger word...")
        recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
        sd.wait()
        sf.write("input.wav", recording, SAMPLE_RATE)

        transcription = transcribe_audio_to_text("input.wav")

        if TRIGGER_WORD in transcription.lower():
            # Play activation phrase
            print("Trigger word detected. Activating voice assistant...")
            os.system(f"say {ACTIVATION_PHRASE}")

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
            os.system(f"say {response}")
            
if __name__ == "__main__":
    main()
