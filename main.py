import yt_dlp
from flask import Flask, request, jsonify

app = Flask(__name__)

YDL_OPTIONS = {
    "quiet": True,
    "no_warnings": True,
    "format": "best",
}


@app.route("/download", methods=["POST"])
def download_instagram_video():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify(
            {"error": "Please provide an Instagram 'url' in the JSON body."}
        ), 400

    instagram_url = data["url"]

    try:
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(instagram_url, download=False)
            download_url = info.get("url")

            if download_url:
                return jsonify({"download_url": download_url})
            else:
                return jsonify({"error": "yt-dlp could not find a download URL."}), 404

    except yt_dlp.utils.DownloadError as e:
        return jsonify({"error": f"Failed to process URL: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
