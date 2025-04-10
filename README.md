# YouTube Batch Video Downloader

A Python application that allows users to download YouTube videos or entire playlists in various resolutions (up to 4K) using a simple Streamlit web interface. It supports batch downloading from multiple URLs or playlists, merging video and audio streams with FFmpeg, and provides progress tracking.

## Features

- **Batch Downloading**: Download multiple videos by entering URLs (comma-separated or one per line) or a YouTube playlist URL.
- **High Resolutions**: Supports resolutions from 360p to 4K (2160p) using adaptive streams.
- **Streamlit UI**: User-friendly interface for inputting URLs, selecting resolutions, and choosing output folders.
- **Progress Tracking**: Displays a progress bar and status updates for each video.
- **Error Handling**: Robust error reporting and cleanup of temporary files on failure.
- **Free Tools**: Built with open-source libraries (`pytube`, `ffmpeg-python`, `streamlit`) and FFmpeg.

## Requirements

### Software

- **Python 3.11+**: Ensure Python is installed on your system.
- **FFmpeg**: Required for merging video and audio streams. Install it based on your operating system:
  - **Windows**: Download from [FFmpeg's official site](https://ffmpeg.org/download.html) or install via Chocolatey (`choco install ffmpeg`).
  - **Mac**: Install via Homebrew (`brew install ffmpeg`).
  - **Linux**: Install via your package manager (e.g., `sudo apt install ffmpeg` for Ubuntu).
  - Verify installation: Run `ffmpeg -version` in your terminal.

### Python Libraries

Install the required libraries using pip:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/yourusername/youtube-downloader.git
cd youtube-downloader
```

2. Run the Streamlit app:

```bash
streamlit run app.py
```

3. Open the provided URL (e.g., `http://localhost:8501`) in your web browser.

In the interface:

- Enter URLs or Playlist:
  - For single/multiple videos: Input YouTube URLs (e.g., `https://www.youtube.com/watch?v=...`), separated by commas or newlines.
  - For playlists: Input a playlist URL (e.g., `https://www.youtube.com/playlist?list=...`).
- Select Resolution: Choose from 360p, 480p, 720p, 1080p, 1440p, or 2160p (4K).
- Choose Output Folder: Specify where to save videos (defaults to your Downloads folder).
- Click Download to start the process.

4. Monitor progress via the progress bar and status updates.

### Example Inputs

- Single Video:

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

- Multiple Videos:

```
https://www.youtube.com/watch?v=video1
https://www.youtube.com/watch?v=video2
```

- Playlist:

```
https://www.youtube.com/playlist?list=PL1234567890
```

## Notes

- The application uses the `pytube` library to download videos.
- The `ffmpeg-python` library is used to merge video and audio streams.
- The `streamlit` library is used to create the web interface.

1. Resolution Availability: Not all videos support all resolutions (e.g., 4K). The script will notify you if a selected resolution is unavailable.
2. Playlist Limitations: Private or restricted playlists may not work due to YouTube's API constraints.
3. Storage: High-resolution videos (like 4K) can be large. Ensure sufficient disk space.
4. pytube Issues: YouTube frequently updates its API, which may cause pytube errors. Update the library if needed:

```bash
pip install --upgrade pytube
```

5. Filename Sanitization: Video titles are cleaned to avoid file system issues (special characters replaced with underscores).
