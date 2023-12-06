import os
import subprocess
import json

def list_drives():
    # For Windows
    if os.name == 'nt':
        drives = [f"{chr(c)}:\\" for c in range(65, 91) if os.path.exists(f"{chr(c)}:\\")]
    # For Unix/Linux/MacOS
    else:
        drives = ["/"]  # Root directory as a starting point; modify as needed
    return drives

def get_video_encoding(file_path):
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        ffprobe_path = os.path.join(dir_path, 'ffprobe.exe')

        cmd = [
            ffprobe_path,
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_streams',
            file_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.stderr:
            print(f"ffprobe error for {file_path}: {result.stderr.strip()}")

        if result.stdout:
            info = json.loads(result.stdout)
            for stream in info.get("streams", []):
                if stream.get("codec_type") == "video":
                    return stream.get("codec_name")
    except Exception as e:
        print(f"Error getting encoding for {file_path}: {e}")
    return "Unknown"

def list_video_files(directory):
    video_extensions = ['.avi', '.mp4', '.mov', '.mkv', '.flv', '.wmv']
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in video_extensions):
                file_path = os.path.join(root, file)
                encoding = get_video_encoding(file_path)
                print(f"{file_path} - Encoding: {encoding}")

def main():
    drives = list_drives()
    print("Available Drives/Directories:")
    for i, drive in enumerate(drives):
        print(f"{i + 1}. {drive}")

    choice = input("Select a drive/directory by number (or 'exit' to quit): ")
    if choice.lower() == 'exit':
        return

    try:
        selected_index = int(choice) - 1
        selected_drive = drives[selected_index]
    except (ValueError, IndexError):
        print("Invalid selection. Please try again.")
        return

    list_video_files(selected_drive)

if __name__ == "__main__":
    main()