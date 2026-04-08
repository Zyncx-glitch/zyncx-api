import os
from flask import Flask, request, jsonify
import yt_dlp

app = Flask("Zyncx")

@app.route('/analizar', methods=['POST'])
def analizar():
    try:
        data = request.get_json()
        video_url = data.get('url')
        solo_audio = data.get('solo_audio', False) # Recibe la orden de Godot
        
        # Si es solo audio, buscamos el mejor formato de audio
        # Si es video, buscamos el mejor formato que tenga audio y video juntos
        format_str = 'bestaudio/best' if solo_audio else 'best[ext=mp4]/best'
        
        ydl_opts = {
            'quiet': True, 
            'noplaylist': True,
            'format': format_str
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                "status": "ok",
                "titulo": info.get('title'),
                "url_descarga": info.get('url'),
                "miniatura": info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({"status": "error", "msj": str(e)}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
