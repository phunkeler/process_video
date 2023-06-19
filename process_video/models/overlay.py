from typing import Optional
import ffmpeg
from pathlib import Path

class Overlay:
    def __init__(self, file_path: Path) -> None:
        self._file_path: Path = file_path
        self._stream: ffmpeg.nodes.FilterableStream = None

    @property
    def file_path(self) -> Path:
        """
        Get the video's file path.

        :rtype: Path
        """
        return self._file_path
    
    @property
    def stream(self) -> ffmpeg.nodes.FilterableStream:
        if self._stream:
            return self._stream

        if not self.file_path.is_file():
            raise FileNotFoundError("The 'file_path' property is not a regular file or it hasn't been set.")
        
        self._stream = ffmpeg.input(str(self.file_path))
        return self._stream
    
    def scale(
            self,
            w: Optional[int] = None,
            h: Optional[int] = None
    ) -> None:
        
        if not self.stream:
            raise AttributeError("The 'stream' property cannot be None.")

        self._stream = ffmpeg.filter(self.stream, 'scale', w, h)