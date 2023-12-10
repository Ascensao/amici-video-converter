import os
import moviepy.editor as mp
from collections import defaultdict

def list_drives():
    # For Windows
    if os.name == 'nt':
        drives = [f"{chr(c)}:\\" for c in range(65, 91) if os.path.exists(f"{chr(c)}:\\")]
    # For Unix/Linux/MacOS
    else:
        drives = ["/"]  # Root directory as a starting point; modify as needed
    return drives

def find_videos_with_same_duration(drives):
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    videos_with_duration = defaultdict(list)

    for drive in drives:
        for root, dirs, files in os.walk(drive):
            for file in files:
                if file.endswith(tuple(video_extensions)):
                    try:
                        full_path = os.path.join(root, file)
                        video = mp.VideoFileClip(full_path)
                        duration = round(video.duration)
                        videos_with_duration[duration].append(full_path)
                    except Exception as e:
                        print(f"Error processing {file}: {e}")

    return videos_with_duration




def main():
    # Get all drives
    drives = list_drives()

    # Find videos with the same duration
    videos = find_videos_with_same_duration(drives)

    # Print the results
    for duration, video_paths in videos.items():
        if len(video_paths) > 1:
            print(f"\nVideos with duration {duration} seconds:")
            for path in video_paths:
                print(path)
            
if __name__ == "__main__":
    main()