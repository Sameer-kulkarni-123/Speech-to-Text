from flask import Flask, render_template, request, redirect, url_for
import speech_recognition as sr
from pydub import AudioSegment
import io
from datetime import datetime
import sqlite3

app = Flask(__name__)

def insert_upload(filename, transcript, timestamp):
    conn = sqlite3.connect('uploads.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO uploads (filename, transcript, timestamp)
        VALUES (?, ?, ?)
    ''', (filename, transcript, timestamp))
    conn.commit()
    conn.close()

def get_all_uploads():
    conn = sqlite3.connect('uploads.db')
    cursor = conn.cursor()
    cursor.execute('SELECT filename, transcript, timestamp FROM uploads')
    uploads = cursor.fetchall()
    conn.close()
    return uploads

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

            # Save the file details to the database
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_upload(file.filename, transcript, timestamp)

    return render_template('index.html', transcript=transcript)

@app.route("/history")
def history():
    upload_history = get_all_uploads()
    return render_template('history.html', upload_history=upload_history)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
