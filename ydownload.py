from flask import Flask, request, render_template, session, url_for, redirect, send_file, flash
from pytube import YouTube
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = "654c0fb3968af9d5e6a9b3edcbc7051b"

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        session['link'] = request.form.get('url')
        try:
            url = YouTube(session['link'])
            url.check_availability()
        except:
            return redirect(url_for('error'))
        else:
            return render_template("download.html", url = url)
    return render_template("home.html")

@app.route("/download", methods=["GET", "POST"])
def ydownload():
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        itag = request.form.get('itag')
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name = f'{url.title}.mp4', mimetype = 'video/mp4')
    return redirect(url_for('home'))
@app.route("/error")
def error():
    return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")