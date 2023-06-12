import ffmpeg
from pathlib import Path
from typing import Optional
from info import Info
from pytube import YouTube
from overlay import Overlay

class Video:
    def __init__(self) -> None:
        self._file_path: Path = None
        self._info: Info = None
        self._url: str = None
        self._stream: ffmpeg.nodes.FilterableStream = None

    @property
    def file_path(self) -> Path:
        """
        Get the video's file path.

        :rtype: Path
        """
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        """
        Sets the video's file path.
        """
        self._file_path = value

    @property
    def info(self) -> Optional[Info]:
        """
        Get useful information about this video.
        Must be called AFTER 'file_path' has been set.

        :rtype: Path
        """
        if self._info:
            return self._info
        
        if not self.file_path.is_file():
            raise FileNotFoundError("The 'file_path' property is not a regular file or it hasn't been set.")

        self._info = Info(self.file_path)
        return self._info
    
    @property
    def stream(self) -> ffmpeg.nodes.FilterableStream:
        if self._stream:
            return self._stream

        if not self.file_path.is_file():
            raise FileNotFoundError("The 'file_path' property is not a regular file or it hasn't been set.")
        
        self._stream = ffmpeg.input(str(self.file_path))
        return self._stream
    
    def apply_overlay(
        self,
        overlay: Overlay,
        x: int,
        y: int
    ) -> None:
        self._stream = ffmpeg.overlay(self.stream, overlay.stream, **{"x": x, "y": y})
    
    def download_from_youtube(
        self,
        url: str,
        output_path: Optional[str] = 'videos/youtube',
        filename: Optional[str] = 'video.mp4') -> Path:
        """
        Downloads a youtube video specified by the supplied 'url'.
        Defaults to the 'videos/youtube/video.mp4' file location'.

        :param str url:
            A valid YouTube watch URL.

        :param str output_path:  
            (Optional) Output path for writing media file. If one is not 
            specified, defaults to 'videos/youtube' in the current 
            working directory.

        :param str filename:
            (Optional) Output filename for the YouTube video.
            If one is not specified, the default 'video.mp4' is used.
        """
        try:
            (
                YouTube(url)
                    .streams
                    .get_highest_resolution()
                    .download(output_path=output_path, filename=filename)
            )
            self.file_path = Path(f"{output_path}/{filename}")
        except:
            print("An exception occurred while trying to download & save the YouTube vide.")

    def output(
            self, 
            file_extension: str = '.avi',
            encoder: str = 'libx264'):
        if not self.file_path.is_file():
            raise FileNotFoundError("The 'file_path' property is not a regular file or it hasn't been set.")
        
        out_file = str(self.file_path.with_suffix(file_extension))
        stream = ffmpeg.output(self.stream, out_file, **{"c:v": encoder})
        ffmpeg.run(stream)