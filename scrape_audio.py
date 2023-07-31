import sys
import os
import yt_dlp

def download_video_audio(video_url, output_template):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_template,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def get_playlist_video_urls(playlist_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
    
    if 'entries' in result:
        return [(entry['url'], entry['title']) for entry in result['entries']]
    else:
        return []


def main():
    playlist_url = "https://youtube.com/playlist?list=PLmxpwhh4FDm5MkEi6m1Tm9vu-MEyiIR5f"
    video_urls = get_playlist_video_urls(playlist_url)
    for index, (video_url, video_title) in enumerate(video_urls):
        print(f"Downloading audio for video {index + 1}: {video_title}")
        output_template = f"video_{index + 1}_audio.%(ext)s"
        download_video_audio(video_url, output_template)
        print(f"{video_title} saved as {output_template}\n")

        if index >= 3:
            break

if __name__ == "__main__":
    main()
