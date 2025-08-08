# Instagram Reels Downloader

Flask API that extracts Instagram Reels download URLs using yt-dlp.

## Usage

```bash
docker build -t instagram-downloader .
docker run -p 8080:8080 instagram-downloader
```

POST to `/download` with JSON: `{"url": "instagram_url"}`

