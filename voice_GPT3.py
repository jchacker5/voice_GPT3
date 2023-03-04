import openai
import pyttsx3
import speech_recognition as sr
import config

# OpenAI API Key
openai.api_key = config.api_key

# Text to Speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile() as source:
       audio = recognizer.record(source)
    try:
        text = r.recognize_google(audio)
        print("You said: ", text)
        return text
    except:
        print("Sorry, I did not get that")
        return ""

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-033",
        prompt=prompt,
        temperature=0.9,
        max_tokens=4000,
        n =1,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
    )
    return response.choices[0].text

def speak(text):
    engine.say(text)
    engine.runAndWait() 

def main():
    while True:
        # wait for user to say genius
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say Sarah!")
            audio = r.listen(source)
            try:
                transcription = r.recognize_google(audio)
                if transcription.lower == "Sarah":
                    # record audio
                    filename = "input.wav"
                    print("im listening Dre")
                    with sr.microphone() as source:
                        source.adjust_for_ambient_noise(source)
                        source.pause_threshold = 1
                        audio = r.listen(source, phrase_time_limit=5)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                    # Transcribe Audio to Text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print("papi you said:", text)

                        # Generate Response using GPT-3
                        response = generate_response(text)
                        print("GPT-3 says: ", response)

                        # read response using text to speech
                        speak(response) 
            except Exception as e:
                print("an error occured: {}".format(e))

if __name__ == "__main__":
    main()
                    