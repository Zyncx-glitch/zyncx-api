from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL

app = Flask(_name_)

@app.route('/analizar', methods=['POST'])
def analizar():
    data = request.get_json()
    url = data.get('url')
    
    # Configuración para obtener solo el enlace, no descargar al servidor
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }
    
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "status": "ok",
                "titulo": info.get('title', 'Video de Zyncx'),
                "url_descarga": info.get('url'),
                "miniatura": info.get('thumbnail')
            })
        except Exception as e:
            return jsonify({"status": "error", "msj": str(e)}), 400

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=10000)