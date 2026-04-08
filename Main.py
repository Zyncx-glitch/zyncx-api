import os
from flask import Flask, request, jsonify
import yt_dlp

app = Flask("Zyncx")

@app.route('/analizar', methods=['POST'])
def analizar():
    try:
        data = request.get_json()
        video_url = data.get('url')
        
        with yt_dlp.YoutubeDL({'quiet': True, 'noplaylist': True}) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                "status": "ok",
                "titulo": info.get('title'),
                "url_descarga": info.get('url'),
                "miniatura": info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({"status": "error", "msj": str(e)}), 400

# Esta es la forma más simple que Render siempre entiende:
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
