import subprocess
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'
import time
import json
import traceback
from moviepy.editor import VideoFileClip


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


def convert_mov_to_mp4(input_path, output_path):
    start_time = time.time()
    clip = VideoFileClip(input_path)
    clip.write_videofile(output_path, codec='libx265')
    clip.close()
    end_time = time.time()
    return end_time - start_time


def convert_mov_to_mp4_gpu(input_path, output_path):
    start_time = time.time()
    
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # FFmpeg command for GPU acceleration
    # This example uses h264_nvenc for encoding which is specific to NVIDIA GPUs
    cmd = [
        os.path.join(dir_path, 'ffmpeg.exe'),
        '-y',
        '-i', input_path,
        '-c:v', 'hevc_nvenc',  # Changed to HEVC NVENC for 10-bit support
        '-preset', 'fast',
        '-cq', '0',
        '-c:a', 'copy',
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        return None

    end_time = time.time()
    return end_time - start_time



def main():
    
    log_file_path = 'log.txt'
    error_log_file_path = 'error_log.txt'

    
    print("Do you like to convert a specific folder or a full drive?\n1. Folder\n2. Full Drive")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        # User chooses to convert a specific folder
        folder_path = input("Enter the full path of the folder: ")
        if not os.path.exists(folder_path):
            print("The specified folder path does not exist. Please try again.")
            return

        # Use the specified folder path as the base directory
        selected_drive = folder_path

    elif choice == '2':
        # User chooses to convert a full drive
        drives = list_drives()
        print("Available Drives/Directories:")
        for i, drive in enumerate(drives):
            print(f"{i + 1}. {drive}")

        drive_choice = input("Select a drive/directory by number (or 'exit' to quit): ")
        if drive_choice.lower() == 'exit':
            return

        try:
            selected_index = int(drive_choice) - 1
            selected_drive = drives[selected_index]
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")
            return
    else:
        print("Invalid choice. Please enter 1 or 2.")
        return

    min_size = input("Enter the minimum file size in MB for video files to be listed (enter 0 for all sizes): ")
    try:
        min_size_mb = float(min_size)
    except ValueError:
        print("Invalid size entered. Please enter a numeric value.")
        return

    # List of common video file extensions
    video_extensions = ['.mov', '.mp4', '.mkv', '.avi', '.flv', '.wmv', '.mpeg', '.mpg']

    video_files = []
    total_size_mb = 0
    for root, dirs, files in os.walk(selected_drive):
        for file in files:
            if any(file.lower().endswith(ext) for ext in video_extensions):
                file_path = os.path.join(root, file)
                file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                if file_size_mb >= min_size_mb:
                    codec = get_video_encoding(file_path)
                    if codec != "h265" or codec == "Unknown":
                        video_files.append((file_path, file_size_mb, codec))  # Include codec in the tuple
                        total_size_mb += file_size_mb

    if not video_files:
        print(f"No video files that can be recoded found in the selected drive/directory.\n")
        return

    print(f"\nFiles that can be re-encoded to h265 codec:")
    for file, size, codec in video_files:
        print(f"{file} - {size:.2f} MB - Codec: {codec}")

    total_size_gb = total_size_mb / 1024
    print(f"\nTotal video file occupation space: {total_size_gb:.2f} GB")

    confirm = input("\nDo you really want to continue? All .mov files will be converted and then deleted. This action cannot be reversed. (yes/no): ")
    if confirm.lower() != 'yes':
        print("Operation cancelled.")
        return

    total_saved = 0
    
    for file_path, size, codec in video_files:
        
        original_size = os.path.getsize(file_path) / (1024 * 1024)
        file_name_without_ext, original_extension = os.path.splitext(file_path)
        original_extension = original_extension.lower()
            
        if original_extension not in ['.mov', '.mp4', '.mkv']:
            temp_extension = '.mp4'
        else:
            temp_extension = original_extension

        # Generate a temporary output file name
        temp_output_path = f"{file_name_without_ext}_temp{temp_extension}"

        print(f'\n\nConverting {file_path} ({codec}) ({size:.2f} MB) to {temp_output_path}...')

        
        conversion_successful = False
        try:
            conversion_file = convert_mov_to_mp4_gpu(file_path, temp_output_path)
            if conversion_file is not None:
                print(f'Conversion completed in {conversion_file:.2f} seconds.')
                conversion_successful = True
            else:
                print("Conversion failed.")
                with open(error_log_file_path, 'a') as error_log:
                    error_log.write(f"File {file_path} failed to convert.\n")
                continue
        except UnicodeDecodeError:
            print("Conversion failed.")
            with open(error_log_file_path, 'a') as error_log:
                error_log.write(f"File {file_path} failed to convert.\n")
            continue
                    
        
        if conversion_successful:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
                continue
            
            # Rename the temporary file to the original file name
            final_output_path = file_name_without_ext + temp_extension
            try:
                os.rename(temp_output_path, final_output_path)
            except Exception as e:
                print(f"Error renaming file {temp_output_path}: {e}")
                continue
            
            new_size = os.path.getsize(final_output_path) / (1024 * 1024)
            saved_size = original_size - new_size
            saved_percentage = (saved_size / original_size) * 100 if original_size != 0 else 0
            
            
            with open(log_file_path, 'a') as log_file:
                log_entry = f"{final_output_path}\t{conversion_file:.2f} seconds\t{original_size:.2f} MB\t{new_size:.2f} MB\t-{saved_size:.2f} MB\t-{saved_percentage:.2f}%\t{codec}\n"
                log_file.write(log_entry)

            total_saved += saved_size
            print(f"Saved {saved_size:.2f} MB for {os.path.basename(file_path)}.")
            
        else:
            print(f"Error converting {file_path}.")
        

    print(f"Total space saved: {total_saved / (1024 * 1024):.2f} MB.")

if __name__ == "__main__":
    main()