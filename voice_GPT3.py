import openai
import pyttsx3
import speech_recognition as sr
import config
import whisper

# OpenAI API Key
openai.api_secret_key = config.whisper_api_key
# Set Whisper API Key
whisper_api_key = config.whisper_api_key
model = whisper.load_model("base")

# Set up the Whisper API client
whisper = openai.api_client(api_key=config.whisper_api_key)
whisper = openai.api_client(api_key=whisper_api_key)


# intialize text to speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)


def transcribe_audio_to_text(filename):
    # Use whisper to transcribe the audio file
    response = whisper.speech_to_text(
        audio=open(filename, "rb"),
        model="commercial",
        language="en-US"
    )
    return response["text"]


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-013",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop="\n",
        temperature=0.9,
    )
    return response["choices"][0]["text"]


def speak_text(text):
    engine.say(text)
    engine.runAndWait()


def main():
    while True:
        # wait for user to say sarah
        print("Say Sarah! to start recording")

        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            print("Say Sarah!")
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "sarah":
                    # record audio
                    filename = "input.wav"
                    print("i'm listening Dre")
                    speak_text("I'm listening Dre")
                    with sr.Microphone() as source:
                        source.adjust_for_ambient_noise(source)
                        source.pause_threshold = 2
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    # Transcribe Audio to Text
                    text = model.transcribe(filename)
                    if text:
                        print("papi you said:", text)

                        # Generate Response using GPT-3
                        response = generate_response(text)
                        print("GPT-3 says: {response}")

                        # read response using text to speech
                        speak_text(response)
            except Exception as e:
                print("\n an error occured: {}".format(e))


if __name__ == "__main__":
    main()
