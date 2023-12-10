# amici-video-converter

## Overview


This Python script is designed to automate the process of finding and converting video files to a more efficient codec (H265). It's particularly useful for those looking to save disk space by re-encoding large video collections. The tool scans a specified folder or an entire drive, identifies video files, and re-encodes them using either CPU or GPU (NVIDIA GPUs specifically).

![visual-drive-size-reduction](https://github.com/Ascensao/amici-video-converter/assets/8701603/ffb01512-e4f2-40ba-b06d-598061ab9c4a)

---

## Space Reduction Example
To demonstrate the effectiveness of the `amici-video-converter`, is presented a before-and-after snapshot of a disk drive's usage. This example illustrates how the script can significantly reduce the amount of disk space occupied by video files.

![wiz-tree-file-reduction](https://github.com/Ascensao/amici-video-converter/assets/8701603/9904d102-f0b3-4aa4-8c16-b663163438cd)

*In this image, we see a comparison of the disk space before and after the conversion process on a 1TB WD Blue drive. Initially, video file types such as .mp4 and .mov constituted the bulk of the disk usage, taking up 45.1% and 31.4% of the space respectively. After running the script, not only has the percentage of space used by these file types decreased to 35.8% and 18.8%, but the overall disk usage has also dramatically reduced from 92.1% to 45.7%. This showcases the script's capacity to effectively reclaim disk space.*

This case study clearly demonstrates the benefits of converting video files to the H265 codec, which is known for its high efficiency and compression capabilities.

## Features
- Scans specified folders or entire drives for video files.
- Supports a range of video formats including .mov, .mp4, .mkv, .avi, .flv, .wmv, .mpeg, and .mpg.
- Determines the current encoding of video files and selectively re-encodes files not already in H265.
- Offers GPU-accelerated encoding for systems with NVIDIA GPUs.
- Calculates and displays the amount of disk space saved after conversion.
- Generates logs for successful conversions and errors.

---

## Disk Space Savings
The conversion process not only makes files more efficient but also significantly reduces disk space usage. Below are two graphs that illustrate the average size reduction by the original codec and the relationship between the original size and the percentage reduction, based on a sample of 850 files.

### Average Size Reduction by Original Codec
![graph](https://github.com/Ascensao/amici-video-converter/assets/8701603/84ce3f5b-27d8-4988-bffe-8321e4147d5d)

*This bar chart represents the average percentage reduction in file size after conversion, categorized by the original codec of the video files, based on a sample of 850 files. As seen, the re-encoding process yields substantial savings, especially for older codecs.*

---


### Original Size vs. Percentage Reduction
![b86d918f-0071-4e30-9368-88286132dc29](https://github.com/Ascensao/amici-video-converter/assets/8701603/81b443b6-21c3-4f57-a23e-ebef81bc39ee)


*This scatter plot provides a detailed view of the percentage reduction in file size relative to the original size of the video files, for a sample of 850 files. Each point represents a file, demonstrating the variance in efficiency gains across different file sizes.*

---

## Prerequisites
- Python 3.x
- moviepy library
- ffmpeg and ffprobe binaries placed in the same directory as the script (for Windows users, .exe files are required).

## Note
This script performs irreversible operations on video files (deletes the original file after conversion). It's advised to have backups before proceeding with batch conversions.


## To-do
- 
