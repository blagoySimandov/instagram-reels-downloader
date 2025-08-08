import yt_dlp
from flask import Flask, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# yt-dlp options
YDL_OPTIONS = {
    "quiet": True,  # Suppress console output
    "no_warnings": True,
    "format": "best",  # Get the best quality available
}


@app.route("/download", methods=["POST"])
def download_instagram_video():
    """
    Webhook endpoint to extract the video download URL from an Instagram URL
    using the yt-dlp library.
    """
    # Get the Instagram URL from the incoming JSON request
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify(
            {"error": "Please provide an Instagram 'url' in the JSON body."}
        ), 400

    instagram_url = data["url"]

    try:
        # Use yt-dlp to extract video information
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            # Extract info without downloading the video on the server
            info = ydl.extract_info(instagram_url, download=False)

            # The direct download URL is in the 'url' key of the info dict
            download_url = info.get("url")

            if download_url:
                return jsonify({"download_url": download_url})
            else:
                return jsonify({"error": "yt-dlp could not find a download URL."}), 404

    except yt_dlp.utils.DownloadError as e:
        # Handle errors from yt-dlp (e.g., private video, invalid URL)
        return jsonify({"error": f"Failed to process URL: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500


if __name__ == "__main__":
    # Run the app and make it accessible from your network
    app.run(host="0.0.0.0", port=8080, debug=True)
