from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import speech_recognition as sr
from pydub import AudioSegment
import io
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db_connection():
    conn = sqlite3.connect('upload_history.db')
    conn.row_factory = sqlite3.Row
    return conn

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
            # Save the uploaded file to the upload folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Convert the uploaded MP3 file to WAV
            audio = AudioSegment.from_file(filepath, format="mp3")
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
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO uploads (filename, transcript, timestamp, filepath) VALUES (?, ?, ?, ?)',
                (file.filename, transcript, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filepath)
            )
            conn.commit()
            conn.close()

    return render_template('index.html', transcript=transcript)

@app.route("/history")
def history():
    conn = get_db_connection()
    uploads = conn.execute('SELECT * FROM uploads').fetchall()
    conn.close()
    return render_template('history.html', uploads=uploads)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
