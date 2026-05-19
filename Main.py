import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask("Zyncx_Media_Engine")

# Permiso exclusivo para tu dominio de GitHub Pages
CORS(app, resources={
    r"/*": {
        "origins": ["https://zyncx-glitch.github.io"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

@app.route('/analizar', methods=['POST', 'OPTIONS'])
def analizar():
    # Responder de inmediato al preflight del navegador
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "msj": "No se recibieron datos JSON"}), 400

        media_url = data.get('url', '').strip()
        solo_audio = data.get('solo_audio', False)
        
        if not media_url:
            return jsonify({"status": "error", "msj": "La URL está vacía"}), 400
        
        # Configuración de formatos óptimos para Redes Sociales
        # TikTok/Instagram ya entregan el video en MP4 optimizado para celulares
        format_str = 'bestaudio/best' if solo_audio else 'best[ext=mp4]/best'
        
        ydl_opts = {
            'quiet': True, 
            'noplaylist': True,
            'format': format_str,
            # Cabeceras móviles para camuflar el servidor de Render
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            },
            # Argumentos críticos para saltar bloqueos específicos de TikTok
            'extractor_args': {
                'tiktok': {
                    'app_version': '20.2.1', 
