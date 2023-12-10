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



## Disk Space Savings
The conversion process not only makes files more efficient but also significantly reduces disk space usage. Below are two graphs that illustrate the average size reduction by the original codec and the relationship between the original size and the percentage reduction.

### Average Size Reduction by Original Codec
*This bar chart shows the average percentage reduction in file size after conversion, categorized by the original codec of the video files. As seen, the re-encoding process yields substantial savings, especially for older codecs.*

### Original Size vs. Percentage Reduction
*This scatter plot provides a detailed view of the percentage reduction in file size relative to the original size of the video files. Each point represents a file, demonstrating the variance in efficiency gains across different file sizes.*

## Prerequisites
- Python 3.x
- moviepy library
- ffmpeg and ffprobe binaries placed in the same directory as the script (for Windows users, .exe files are required).

## Note
This script performs irreversible operations on video files (deletes the original file after conversion). It's advised to have backups before proceeding with batch conversions.


## To-do
- 
