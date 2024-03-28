from flask import Flask, send_from_directory, request, abort
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"
    


@app.route('/fetch_videos_json', methods=['GET'])
def fetch_videos_json():
    password = request.args.get('password')
    if password != 'Shadow1':
        abort(401)  # Unauthorized

    videos_file_path = 'videos.json'
    try:
        return send_from_directory(os.path.dirname(videos_file_path), os.path.basename(videos_file_path), as_attachment=True)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run()