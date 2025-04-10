import streamlit as st
from pytube import YouTube, Playlist
import os
import ffmpeg
import re
from pytube.innertube import _default_clients
from pytube import cipher
import logging

# Patch for pytube cipher issue
_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
cipher._get_cipher = lambda *args, **kwargs: None  # Disable cipher check as fallback

# Function to clean YouTube URL
def clean_url(url):
    match = re.match(r"(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[^\?&]+)", url)
    return match.group(0) if match else url

# Download function with enhanced error handling
def download_single_video(url, resolution, output_path, include_audio=True, progress_callback=None):
    try:
        yt = YouTube(clean_url(url))
        
        video_stream = yt.streams.filter(res=resolution, adaptive=True, only_video=True).first()
        if not video_stream:
            st.error(f"No video stream found for {resolution} in {yt.title}")
            return False

        audio_stream = None
        if include_audio:
            audio_stream = yt.streams.filter(adaptive=True, only_audio=True).order_by('abr').desc().first()
            if not audio_stream:
                st.error(f"No audio stream found for {yt.title}")
                return False

        safe_title = "".join([c if c.isalnum() or c in " -_" else "_" for c in yt.title])
        video_path = os.path.join(output_path, f"{safe_title}_video_temp.mp4")
        output_file = os.path.join(output_path, f"{safe_title} - {resolution}.mp4")
        audio_path = os.path.join(output_path, f"{safe_title}_audio_temp.mp3") if include_audio else None

        if progress_callback:
            progress_callback(f"Downloading video: {yt.title} at {resolution}")
        video_stream.download(output_path=output_path, filename=f"{safe_title}_video_temp.mp4")

        if include_audio and audio_stream:
            if progress_callback:
                progress_callback(f"Downloading audio for: {yt.title}")
            audio_stream.download(output_path=output_path, filename=f"{safe_title}_audio_temp.mp3")
            if progress_callback:
                progress_callback(f"Merging video and audio for: {yt.title}")
            stream = ffmpeg.input(video_path)
            stream = ffmpeg.input(audio_path).output(stream, output_file, c='copy', loglevel='quiet')
            ffmpeg.run(stream)
            os.remove(audio_path)
        else:
            os.rename(video_path, output_file)

        if os.path.exists(video_path):
            os.remove(video_path)
        if progress_callback:
            progress_callback(f"Completed: {yt.title}")
        return True

    except Exception as e:
        st.error(f"Error with {url}: {str(e)}. Trying fallback...")
        try:
            yt = YouTube(clean_url(url))
            stream = yt.streams.filter(res=resolution, progressive=True).first()
            if stream:
                stream.download(output_path=output_path, filename=f"{safe_title} - {resolution}.mp4")
                if progress_callback:
                    progress_callback(f"Fallback completed: {yt.title}")
                return True
            else:
                st.error("Fallback failed: No suitable stream found.")
                return False
        except Exception as e2:
            st.error(f"Fallback failed: {str(e2)}")
            return False

# Batch download function
def download_batch(urls, resolution, output_path, include_audio=True):
    url_list = []
    if "playlist" in urls.lower():
        try:
            playlist = Playlist(clean_url(urls))
            url_list = [clean_url(url) for url in playlist.video_urls]
            st.write(f"Found playlist with {len(url_list)} videos")
        except Exception as e:
            st.error(f"Error processing playlist: {str(e)}")
            return
    else:
        url_list = [clean_url(url.strip()) for url in urls.replace(",", "\n").split("\n") if url.strip()]

    if not url_list:
        st.warning("No valid URLs provided")
        return

    progress_bar = st.progress(0)
    status_text = st.empty()
    total_videos = len(url_list)
    completed = 0

    def update_progress(message):
        nonlocal completed
        status_text.text(message)
        if "Completed" in message:
            completed += 1
            progress_bar.progress(completed / total_videos)

    for i, url in enumerate(url_list, 1):
        st.write(f"Processing video {i}/{total_videos}: {url}")
        download_single_video(url, resolution, output_path, include_audio, update_progress)

    st.success(f"Batch download completed! Processed {completed}/{total_videos} videos")

# Enhanced UI
def main():
    # Theme-agnostic colors
    st.markdown("""
        <style>
        .stApp {
            background-color: #FFFFFF; /* Light theme default */
        }
        [data-baseweb="tab"] { /* Tab styling */
            font-size: 16px;
        }
        div.stButton > button {
            width: 100%;
            height: 50px;
            font-size: 18px;
            background-color: #E63946; /* Vibrant red */
            color: #FFFFFF;
            border: none;
            border-radius: 5px;
        }
        div.stButton > button:hover {
            background-color: #D00000; /* Darker red */
        }
        .stTextInput > div > div > input, .stTextArea > div > textarea {
            border: 1px solid #457B9D; /* Blue-gray */
            border-radius: 5px;
            background-color: #F1FAEE; /* Light cream */
            color: #1D3557; /* Dark blue */
        }
        .stSelectbox > div > div > select {
            border: 1px solid #457B9D;
            border-radius: 5px;
            background-color: #F1FAEE;
            color: #1D3557;
        }
        </style>
    """, unsafe_allow_html=True)

    # Logo (YouTube-inspired from internet)
    st.markdown("<div style='text-align: center;'>"
                f"<img src='https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png' "
                "width='100' alt='YouTube Downloader'/>"
                "<p>YouTube Downloader</p>"
                "</div>", unsafe_allow_html=True)

    # Sidebar for Help
    with st.sidebar:
        st.header("Help")
        st.markdown("""
        - **Single Video**: Use a URL like `https://youtu.be/tuxsXLpv40s`.
        - **Multiple Videos/Playlist**: List URLs or use `https://www.youtube.com/playlist?list=...`.
        - **Troubleshooting**: 
          - Ensure URLs are valid.
          - Update `pytube`: `pip install --upgrade pytube`.
          - Check FFmpeg: `ffmpeg -version`.
          - If errors persist, try a different video or report the issue.
        """)

    # Tabs with logos
    tab1, tab2 = st.tabs([
        f"![Single](https://img.favpng.com/6/16/21/logo-brand-red-font-png-favpng-BmwkuRkvZyW0jHuASRDVJXJne.jpg) Single Video",
        f"![Batch](https://cdn.iconscout.com/icon/free/png-256/free-youtube-playlist-logo-icon-download-in-svg-png-gif-file-formats--music-social-media-pack-logos-icons-5582748.png?f=webp) Batch/Playlist"
    ])

    # Common options
    resolutions = ["360p", "480p", "720p", "1080p", "1440p", "2160p"]
    default_path = os.path.join(os.path.expanduser("~"), "Downloads")

    with tab1:
        single_url = st.text_input("YouTube URL", placeholder="e.g., https://youtu.be/tuxsXLpv40s", key="single_url")
        resolution_single = st.selectbox("Select Resolution", resolutions, key="res_single")
        output_path_single = st.text_input("Save to folder", default_path, key="path_single")
        include_audio_single = st.toggle("Include Audio", value=True, key="audio_single")
        if st.button("Download", key="download_single"):
            if single_url:
                with st.spinner("Downloading..."):
                    download_single_video(single_url, resolution_single, output_path_single, include_audio_single, st.write)
            else:
                st.warning("Please enter a YouTube URL")

    with tab2:
        multi_urls = st.text_area("YouTube URL(s) or Playlist URL", 
                                 placeholder="Enter one URL per line, comma-separated, or a playlist URL",
                                 height=150, key="multi_urls")
        resolution_multi = st.selectbox("Select Resolution", resolutions, key="res_multi")
        output_path_multi = st.text_input("Save to folder", default_path, key="path_multi")
        include_audio_multi = st.toggle("Include Audio", value=True, key="audio_multi")
        if st.button("Download", key="download_multi"):
            if multi_urls:
                with st.spinner("Starting batch download..."):
                    download_batch(multi_urls, resolution_multi, output_path_multi, include_audio_multi)
            else:
                st.warning("Please enter at least one YouTube URL or playlist URL")

if __name__ == "__main__":
    main()