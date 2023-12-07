# amici-video-converter

## Overview
This Python script is designed to automate the process of finding and converting video files to a more efficient codec (H265). It's particularly useful for those looking to save disk space by re-encoding large video collections. The tool scans a specified folder or an entire drive, identifies video files, and re-encodes them using either CPU or GPU (NVIDIA GPUs specifically).


## Features
- Scans specified folders or entire drives for video files.
- Supports a range of video formats including .mov, .mp4, .mkv, .avi, .flv, .wmv, .mpeg, and .mpg.
- Determines the current encoding of video files and selectively re-encodes files not already in H265.
- Offers GPU-accelerated encoding for systems with NVIDIA GPUs.
- Calculates and displays the amount of disk space saved after conversion.
- Generates logs for successful conversions and errors.

## Prerequisites
- Python 3.x
- moviepy library
- ffmpeg and ffprobe binaries placed in the same directory as the script (for Windows users, .exe files are required).


## Note
This script performs irreversible operations on video files (deletes the original file after conversion). It's advised to have backups before proceeding with batch conversions.


## To-do
- 
