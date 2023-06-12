# Overview
Proof-of-concept Python 'app' for downloading, editing, and exporting video files.

# Current State
- Downloads the `https://www.youtube.com/watch?v=a7V02xJVLI0` video from YouTube
- Saves the video as `videos/youtube/video.mp4`
- Scales the `assets/overlay.png` image before placing it in the bottom-left of the video
- Encodes video as H.264
- Exports the edited video to `videos/youtube/video.avi`

# TODO
1. Parameterize `process_video.py` to accept command-line args
2. Apply "speed ramp"
3. Mechanism for downloading video files from web (Not YouTube)
4. Apply overlay without breaking existing sound

# Dependencies
- [Python](https://www.python.org/)
- [ffmpeg](https://github.com/FFmpeg/FFmpeg)
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)
- [pytube](https://github.com/pytube/pytube)

# Environment Setup
1. Install the latest stable Python version ([3.11.4](https://www.python.org/downloads/) as of 6/12/2023)
    - [Instructions](https://wiki.python.org/moin/BeginnersGuide/Download)
2. Install the latest FFmpeg version ([Link](https://ffmpeg.org/download.html))
    - [Instructions](https://www.hostinger.com/tutorials/how-to-install-ffmpeg)
3. Verify `ffmpeg` has been added to your PATH by running `ffmpeg` in the command-line/terminal. 
    If the command cannot be found, try following these instructions to add the FFmpeg binary directory to
    your PATH ([Mac](https://techpp.com/2021/09/08/set-path-variable-in-macos-guide/) / [Windows](https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/))
4. Once Python and FFmpeg are installed, proceed with "Run App" instructions

# Run App
1. Clone this repository or Download as .zip
2. Open the command-line/terminal
3. `cd` to the `process_video` directory
4. Execute the `process_video.py` script by entering the following command:
    - `py ./process_video.py`