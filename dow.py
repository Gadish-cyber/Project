import yt_dlp
import sys
import re

def download_yt_video(url, output_path="downloads/%(title)s.%(ext)s", verbose=False):
    # Basic URL validation
    if not re.match(r"(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)/", url):
        print("Error: Invalid YouTube URL.")
        return False

    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best',  # Try 1080p video + best audio
        'outtmpl': output_path,  # Specify output path and filename template
        'no-playlist': True,     # Download single video, not playlist
        'merge_output_format': 'mp4',  # Ensure output is in mp4 format (requires ffmpeg)
        'progress_hooks': [progress_hook],  # Add progress feedback
    }
    if verbose:
        ydl_opts['verbose'] = True

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download complete.")
        return True
    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading video: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def progress_hook(d):
    """Display download progress."""
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%').strip()
        speed = d.get('_speed_str', 'Unknown').strip()
        eta = d.get('_eta_str', 'Unknown').strip()
        print(f"Downloading: {percent} at {speed}, ETA: {eta}", end='\r')
    elif d['status'] == 'finished':
        print("\nDownload finished, post-processing...")

if __name__ == "__main__":
    try:
        video_url = input("Enter the YouTube video URL: ")
        success = download_yt_video(video_url, verbose=False)
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nDownload cancelled by user.")
        sys.exit(1)       