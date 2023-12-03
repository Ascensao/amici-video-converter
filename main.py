import os
os.environ['PYTHONIOENCODING'] = 'utf-8'
import time
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

def main():
    while True:
        drives = list_drives()
        print("Available Drives/Directories:")
        for i, drive in enumerate(drives):
            print(f"{i + 1}. {drive}")

        choice = input("Select a drive/directory by number (or 'exit' to quit): ")
        if choice.lower() == 'exit':
            break

        try:
            selected_index = int(choice) - 1
            selected_drive = drives[selected_index]
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")
            continue

        min_size = input("Enter the minimum file size in MB for .mov files to be listed (enter 0 for all sizes): ")
        try:
            min_size_mb = float(min_size)
        except ValueError:
            print("Invalid size entered. Please enter a numeric value.")
            continue

        mov_files = []
        total_size_mb = 0
        for root, dirs, files in os.walk(selected_drive):
            for file in files:
                if file.lower().endswith('.mov'):
                    file_path = os.path.join(root, file)
                    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)  # Size in MB
                    if file_size_mb >= min_size_mb:
                        mov_files.append((file_path, file_size_mb))
                        total_size_mb += file_size_mb

        if not mov_files:
            print(f"No .mov files of {min_size_mb}MB or larger found in the selected drive/directory.")
            continue

        print(f"\nFound .mov files ({min_size_mb}MB or larger):")
        for file, size in mov_files:
            print(f"{file} - {size:.2f} MB")

        total_size_gb = total_size_mb / 1024  # Convert MB to GB
        print(f"\nTotal .mov file occupation space: {total_size_gb:.2f} GB")

        confirm = input("\nDo you really want to continue? All .mov files will be converted and then deleted. This action cannot be reversed. (yes/no): ")
        if confirm.lower() != 'yes':
            print("Operation cancelled.")
            continue

        total_saved = 0
        for file_path, size in mov_files:
            output_path = file_path.replace('.mov', '.mp4').replace('.MOV', '.mp4')

            print(f'\n\nConverting {file_path} ({size:.2f} MB) to {output_path}...')
            
            try:
                conversion_time = convert_mov_to_mp4(file_path, output_path)
            except UnicodeDecodeError:
                print("A Unicode decoding error occurred. Skipping this file.")
                continue
            
            print(f'Conversion completed in {conversion_time:.2f} seconds.')

            original_size = os.path.getsize(file_path)
            new_size = os.path.getsize(output_path)
            os.remove(file_path)

            saved = original_size - new_size
            total_saved += saved
            print(f"Saved {saved / (1024 * 1024):.2f} MB for {os.path.basename(file_path)}.")

        print(f"Total space saved: {total_saved / (1024 * 1024):.2f} MB.")

if __name__ == "__main__":
    main()