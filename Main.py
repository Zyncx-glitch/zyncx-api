import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask("Zyncx_Engine")
# Habilitamos CORS nativo en Flask para evitar CUALQUIER bloqueo desde GitHub Pages
CORS(app)

@app.route('/analizar', methods=['POST'])
def analizar():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "msj": "No se recibieron datos JSON"}), 400

        video_url = data.get('url', '').strip()
        solo_audio = data.get('solo_audio', False)
        
        if not video_url:
            return jsonify({"status": "error", "msj": "La URL está vacía"}), 400
        
        # Configuramos el formato según la petición
        # Si es audio: buscamos el mejor audio
        # Si es video: buscamos mp4 o el mejor formato combinado disponible
        format_str = 'bestaudio/best' if solo_audio else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        
        ydl_opts = {
            'quiet': True, 
            'noplaylist': True,
            'format': format_str,
            # Añadimos cabeceras para que TikTok/Instagram no confundan a Render con un bot malicioso
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            },
            # Argumento especial para saltarse bloqueos específicos de TikTok
            'extractor_args': {
                'tiktok': {'app_version': '20.2.1', 'manifest_app_version': '20.2.1'}
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extraemos la información sin descargar el archivo al servidor
            info = ydl.extract_info(video_url, download=False)
            
            # Formateamos la respuesta limpia para el Frontend de Zyncx
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
    # Render asigna el puerto dinámicamente mediante variables de entorno
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
