import ffmpeg # https://github.com/kkroening/ffmpeg-python
from vapoursynth import core # https://github.com/vapoursynth/vapoursynth
from pytube import YouTube # https://github.com/pytube/pytube
from pathlib import Path
from typing import Optional

def download_from_youtube(
        url: str,
        output_path: Optional[str] = 'videos/youtube',
        filename: Optional[str] = 'video.mp4'):
    """
    Downloads a youtube video specified by the supplied 'url'
    to the 'output_path' directory with the name 'filename'.

    :param url:
        The address to a YouTube video.

    :param output_path:  
        (optional) Output path for writing media file. If one is not 
        specified, defaults to 'videos/youtube' in the current 
        working directory.
    :type output_path: str or None

    :param filename:
        (optional) Output filename for writing media file.
        If one is not specified, the default 'video.mp4' is used.
    :type filename: str or None
    """
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    stream.download(output_path=output_path, filename=filename)

def process_video(in_file: Path, encoder: str = 'libx264'):
    """
    Uses 'ffmpeg' to encode video with 'libx264'
    """
    out_file    = str(in_file.with_suffix('.avi'))
    stream      = ffmpeg.input(str(in_file))
    overlay     = ffmpeg.input("D:\Freelance\Projects\Konspiracy_AviSynth\process_video\logo.png")

    # Get video dimensions (useful for overlay positioning)
    probe = ffmpeg.probe(str(in_file), **{"show_frames":None})
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    width = int(video_stream['width'])
    height = int(video_stream['height'])
    
    # Scale overlay (specify -1 for either w/h to maintain aspect-ratio)
    overlay = ffmpeg.filter(overlay, 'scale', 200, -1)

    # TODO: Apply "speed ramp"
        # 800% for first 5 seconds, then normal speed (100%) for 2 seconds and then back to 800% for next 2 seconds) 
    #stream = ffmpeg.filter(stream, 'trim', start=0, duration=10)

    # Apply overlay at bottom-left (More accurate/re-usable positioning will require more complex arithmetic)
    stream = ffmpeg.overlay(stream, overlay, **{"x": 25, "y": height - 80})

    # Encodes video streams with libx264
    stream = ffmpeg.output(stream, out_file, **{"c:v": encoder})

    ffmpeg.run(stream)

    # Speed Ramp
    #core.avs.LoadPlugin(path='D:\\Plugins\\SickJumps.dll')
    #core.avs.SickJumps(clip, 0, 30, 8, 2, 2)

def main():
    youtube_video_url = 'https://www.youtube.com/watch?v=a7V02xJVLI0'
    output_path = 'videos/youtube'
    filename = 'video.mp4'
    video = Path(f"{output_path}/{filename}")

    download_from_youtube(youtube_video_url)

    if video.is_file():
        process_video(video)

# Execute 'main' function when running this script
if __name__ == "__main__":
    main()