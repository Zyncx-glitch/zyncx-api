from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(_name_)

@app.route('/analizar', methods=['POST'])
def analizar():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({"status": "error", "msj": "No URL provided"}), 400

        ydl_opts = {'quiet': True, 'noplaylist': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                "status": "ok",
                "titulo": info.get('title'),
                "url_descarga": info.get('url'),
                "miniatura": info.get('thumbnail')
            })
    except Exception as e:
        return jsonify({"status": "error", "msj": str(e)}), 400

if _name_ == '_main_':
    # Render usa el puerto 10000 por defecto
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
