#%%

import sys
import time
import re
import os
import yt_dlp
import pandas as pd

def get_video_transcript(video_url):
    ydl_opts = {
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "skip_download": True,
        "outtmpl": "captions.%(ext)s",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    captions_filename = "captions.en.vtt"

    if os.path.exists(captions_filename):
        with open(captions_filename, "r") as f:
            transcript = f.read()
        os.remove(captions_filename)
    else:
        print("No captions found for the video.")
        sys.exit(1)

    return transcript

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


#Used to remove all characters from the youtube script scraping that are nonsensical for gpt
def remove_noise(script):
    #with open(input_file, 'r') as f:
    #    content = f.read()

    
    
    # Remove header
    content_no_header = re.sub(r'^.*?Language: en\n\n', '', script, flags=re.DOTALL)

    # Remove timestamps and formatting tags
    content_clean = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3}.*?align:start position:0%\n|\s*<[^>]*>', '', content_no_header)

    # Remove consecutive blank lines
    content_no_blank_lines = re.sub(r'\n{2,}', '\n', content_clean)

    # Remove duplicate lines
    lines = content_no_blank_lines.split('\n')
    unique_lines = []
    for line in lines:
        if line not in unique_lines:
            unique_lines.append(line)
    content_final = '\n'.join(unique_lines)


    print("Cleaned: " + content_final)
    
    return content_final
    
    #with open(output_file, 'w') as f:
        #f.write(content_final)


#Extracts all scripts from every video into a dataframe to be translated into use for gpt
def main():

    
    titles = []
    scripts = []
    classLabels = []
    
    playlist_urls = ['https://www.youtube.com/playlist?list=PLmxpwhh4FDm5zuA_63jV6iiz5wrg76UHV', 'https://www.youtube.com/playlist?list=PLmxpwhh4FDm5MkEi6m1Tm9vu-MEyiIR5f']
    classes = ['392', '393']
    
    for i in range(len(playlist_urls)):
    
        playlist_url = playlist_urls[i]
        className = classes[i]
        video_urls = get_playlist_video_urls(playlist_url)

        for index, (video_url, video_title) in enumerate(video_urls):

            if index < 36:
                print(f"Processing video {index + 1}: {video_title}")
                transcript = get_video_transcript(video_url)
                #temp_filename = f"temp_video_{index + 1}_transcript.txt"
                #with open(temp_filename, "w") as f:
                #    f.write(transcript)
                
                #output_filename = f"video_{index + 1}_transcript.txt"
                #remove_noise(temp_filename, output_filename)
                #os.remove(temp_filename)

                print(f"{video_title} saved \n")
                
                titles.append(video_title)
                scripts.append(transcript)
                classLabels.append(className)
        
    df = pd.DataFrame({'Class':classLabels, 'Title': titles, 'Script': scripts})
    
    df['ScriptNoNoise'] = df['Script'].apply(remove_noise)
    
    df.to_csv('VideoScriptsNoNoise.csv',index=False)
    
    print('COMPLETED')


if __name__ == "__main__":
    main()