import os
from flask import Flask, request, jsonify
import yt_dlp

app = Flask("ZyncxAPI")

@app.route('/analizar', methods=['POST'])
def analizar():
    try:
        url = request.get_json().get('url')
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "status": "ok",
                "titulo": info.get('title'),
                "url_descarga": info.get('url'),
                "miniatura": info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({"status": "error", "msj": str(e)}), 400

if _name_ == "_main_":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
