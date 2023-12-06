import subprocess
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'
import time
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
        '-i', input_path,
        '-c:v', 'hevc_nvenc',  # Changed to HEVC NVENC for 10-bit support
        '-preset', 'fast',
        '-crf', '0',
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


    with open(log_file_path, 'a') as log_file:
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


        min_size = input("Enter the minimum file size in MB for .mov files to be listed (enter 0 for all sizes): ")
        try:
            min_size_mb = float(min_size)
        except ValueError:
            print("Invalid size entered. Please enter a numeric value.")
            return

        mov_files = []
        total_size_mb = 0
        for root, dirs, files in os.walk(selected_drive):
            for file in files:
                if file.lower().endswith('.mov'):
                    file_path = os.path.join(root, file)
                    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                    if file_size_mb >= min_size_mb:
                        mov_files.append((file_path, file_size_mb))
                        total_size_mb += file_size_mb

        if not mov_files:
            print(f"No .mov files of {min_size_mb}MB or larger found in the selected drive/directory.")
            return

        print(f"\nFound .mov files ({min_size_mb}MB or larger):")
        for file, size in mov_files:
            print(f"{file} - {size:.2f} MB")

        total_size_gb = total_size_mb / 1024
        print(f"\nTotal .mov file occupation space: {total_size_gb:.2f} GB")

        confirm = input("\nDo you really want to continue? All .mov files will be converted and then deleted. This action cannot be reversed. (yes/no): ")
        if confirm.lower() != 'yes':
            print("Operation cancelled.")
            return

        total_saved = 0
        for file_path, size in mov_files:
            output_path = file_path.replace('.mov', '.mp4').replace('.MOV', '.mp4')

            print(f'\n\nConverting {file_path} ({size:.2f} MB) to {output_path}...')
            
            try:
                conversion_time = convert_mov_to_mp4_gpu(file_path, output_path)
                if conversion_time is not None:
                    print(f'Conversion completed in {conversion_time:.2f} seconds.')
                else:
                    print("Conversion failed.")
                    with open(error_log_file_path, 'a') as error_log:
                        error_log.write(f"File {file_path} failed to convert.\n")
                    continue
            except UnicodeDecodeError:
                print("A Unicode decoding error occurred. Skipping this file.")
                with open(error_log_file_path, 'a') as error_log:
                    error_log.write(f"Unicode decoding error for file {file_path}.\n")
                continue
                        
            print(f'Conversion completed in {conversion_time:.2f} seconds.')

            try:
                original_size = os.path.getsize(file_path) / (1024 * 1024)
                new_size = os.path.getsize(output_path) / (1024 * 1024)
                os.remove(file_path)

                saved_size = original_size - new_size
                saved_percentage = (saved_size / original_size) * 100 if original_size != 0 else 0

                log_entry = f"{output_path}\t{conversion_time:.2f} seconds\t{original_size:.2f} MB\t{new_size:.2f} MB\t-{saved_size:.2f} MB\t-{saved_percentage:.2f}%\n"
                log_file.write(log_entry)

                total_saved += saved_size
                print(f"Saved {saved_size:.2f} MB for {os.path.basename(file_path)}.")
            except Exception as e:
                print(f"Error processing file {file_path}. Check error_log.txt for details.")

        print(f"Total space saved: {total_saved / (1024 * 1024):.2f} MB.")

if __name__ == "__main__":
    main()