from flask import Flask, render_template, request, redirect
import speech_recognition as sr
from pydub import AudioSegment
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            # Convert the uploaded MP3 file to WAV
            audio = AudioSegment.from_file(file, format="mp3")
            wav_io = io.BytesIO()
            audio.export(wav_io, format="wav")
            wav_io.seek(0)

            # Use speech_recognition to transcribe the WAV file
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(wav_io)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)

    return render_template('index.html', transcript=transcript)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
