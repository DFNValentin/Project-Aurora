from flask import Flask, request, jsonify
import yt_dlp
from functools import lru_cache

app = Flask(__name__)

@lru_cache(maxsize=128)
def search_and_get_audio(query):
    ydl_opts = {
        'quiet': False,
        'extract_flat': False,  
        'format': 'bestaudio',
        'noplaylist': True,
        'socket_timeout': 10,
        'extractor_args': {'youtube': {'skip': ['dash', 'hls']}},  
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if 'entries' in result:
                video = result['entries'][0]
                return {
                    'title': video.get('title'),
                    'uploader': video.get('uploader'),
                    'audio_url': video.get('url')
                }
    except Exception as e:
        print(f"Error processing {query}: {str(e)}")
        return None

@app.route("/")
def __main__():
    return "http://127.0.0.1:5000/search?query=`Nameofmelody`"

@app.route("/get_audio", methods=['POST', 'GET'])
def get_audio():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({"error": "query not provided"}), 400
    return jsonify({"received": query})

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    try:
        audio_url = search_and_get_audio(query)
        if audio_url:
            return jsonify({'audio_url': audio_url})
        else:
            return jsonify({'error': 'No results found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000,)  