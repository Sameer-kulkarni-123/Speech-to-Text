import speech_recognition as sr
import pyttsx3

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()


def record_text():
    while True:
        try:
            with sr.Microphone() as source2:
                # Adjust the recognizer sensitivity to ambient noise
                r.adjust_for_ambient_noise(source2, duration=0.2)

                print("Listening...")
                # Listen for the first phrase and extract it into audio data
                audio2 = r.listen(source2)

                # Recognize (convert from speech to text)
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()

                print("You said: " + MyText)
                return MyText

        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")


def output_text(text):
    # Open file in append mode and write the text
    with open("output.txt", "a") as f:
        f.write(text + "\n")


# if __name__ == "__main__":
a = 10
while True:
    try:
        # Record the text from the microphone
        text = record_text()

        # Write the text to the file
        output_text(text)

        print("Text written to file")

    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")
        break
