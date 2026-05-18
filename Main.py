import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask("Zyncx_Engine")

# Liberación absoluta de CORS para tu dominio de GitHub Pages
CORS(app, resources={
    r"/*": {
        "origins": ["https://zyncx-glitch.github.io"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

@app.route('/analizar', methods=['POST', 'OPTIONS'])
def analizar():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "msj": "No se recibieron datos JSON"}), 400

        video_url = data.get('url', '').strip()
        solo_audio = data.get('solo_audio', False)
        
        if not video_url:
            return jsonify({"status": "error", "msj": "La URL está vacía"}), 400
        
        format_str = 'bestaudio/best' if solo_audio else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        
        ydl_opts = {
            'quiet': True, 
            'noplaylist': True,
            'format': format_str,
            # FUERZA A YT-DLP A USAR LOS CLIENTES DE ANDROID/IOS
            # Esto se salta el bloqueo de "Sign in to confirm you're not a bot" en Render
            'youtube_include_dash_manifest': False,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios'],
                    'skip': ['webpage', 'authcheck']
                },
                'tiktok': {
                    'app_version': '20.2.1', 
                    'manifest_app_version': '20.2.1'
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            return jsonify({
                "status": "ok",
                "titulo": info.get('title', 'Zyncx Media File'),
                "url_descarga": info.get('url'),
                "miniatura": info.get('thumbnail', 'https://via.placeholder.com/160x90?text=Zyncx+Media'),
                "duracion": info.get('duration'),
                "plataforma": info.get('extractor_key', 'Unknown')
            })

    except Exception as e:
        # Si ocurre un error, devolvemos el mensaje exacto para saber qué pasó
        return jsonify({"status": "error", "msj": str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
