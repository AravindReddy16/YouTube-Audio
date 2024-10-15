from flask import Flask, request, redirect, url_for, render_template
import yt_dlp
import io

app = Flask(__name__)

def download_audio_stream(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(youtube_url, download=False)
        audio_url = result.get('url')
        return audio_url

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/audio', methods=['POST'])
def extract():
    if "youtube_url" in request.form:
        youtube_url = request.form['youtube_url']
        if "https://youtu.be/" in youtube_url:
            try:
                audio_url = download_audio_stream(youtube_url)
                if audio_url:
                    return render_template("index.html", audio_url=audio_url)
                else:
                    return redirect(url_for('home'))
            except Exception:
                return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)