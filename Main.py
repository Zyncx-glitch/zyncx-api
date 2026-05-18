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
    # Si el navegador envía la verificación previa (OPTIONS), respondemos OK con estado 200 de inmediato
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
        
        # Filtro de formatos inteligente para tráfico multimedia masivo
        format_str = 'bestaudio/best' if solo_audio else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        
        ydl_opts = {
            'quiet': True, 
            'noplaylist': True,
            'format': format_str,
            # Cabeceras de camuflaje para evitar bloqueos por IP compartida en la nube
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            },
            # Parámetro crítico para que TikTok no rechace las peticiones de Render
            'extractor_args': {
                'tiktok': {'app_version': '20.2.1', 'manifest_app_version': '20.2.1'}
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extraemos metadatos en milisegundos sin sobrecargar el servidor
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
        return jsonify({"status": "error", "msj": str(e)}), 400

if __name__ == "__main__":
    # Configuración dinámica del puerto asignado por Render
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
