import logging
import os
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import ffmpeg
import requests
from moviepy.editor import *
from PIL import Image
from pytube import YouTube
from requests_file import FileAdapter

from process_video.coordinate import Coordinate
from process_video.size import Size


class BaseService:
    def __init__(self) -> None:
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )


class FileService(BaseService):
    def __init__(self) -> None:
        super().__init__()
        self._session = requests.Session()
        self._session.mount("file://", FileAdapter())
        self._output_path = Path(__file__).parent.resolve()

    def get_file(self, url: str) -> Optional[Path]:
        parsedUrl = urlparse(url)
        self.log_download(url)
        file = None

        if (
            "youtube.com" in parsedUrl.hostname.lower()
            and parsedUrl.path.lower() == "/watch"
        ):
            file = Path(
                YouTube(url)
                .streams.get_highest_resolution()
                .download(self._output_path)
            )
        else:
            response = self._session.get(url, stream=True, verify=False)
            if response.status_code == requests.codes.ok:
                fileName = os.path.basename(url)
                file = Path(self._output_path, fileName)
                out = open(file, "wb")
                for block in response.iter_content(1024):
                    if not block:
                        break
                    out.write(block)
                out.close()
        return file

    def compress_file(self, file: Path) -> None:
        newFile = file.with_name(f"{file.stem}_compressed{file.suffix}")
        stream = ffmpeg.input(str(file))
        stream = ffmpeg.output(stream, str(newFile), **{"c:v": "libx264"})
        ffmpeg.run(stream)
        self.replace_file(file, newFile)

    def replace_file(self, old: Path, new: Path) -> None:
        if old.is_file() and new.is_file():
            old.unlink()
            new.rename(old)

    def log_download(self, url: str):
        self.logger.info(f'Downloading "{url}".')


class ImageService(FileService):
    def __init__(self) -> None:
        super().__init__()

    def resize_image(self, file: Path, size: Size):
        newFile = file.with_name(f"{file.stem}_resized{file.suffix}")
        with Image.open(str(file)) as image:
            image.thumbnail(size.to_tuple())
            image.save(newFile)
            super().replace_file(file, newFile)


class VideoService(FileService):
    def __init__(self) -> None:
        super().__init__()

    def overlay_image(self, video: Path, image: Path, coordinate: Coordinate) -> None:
        newVideo = video.with_name(f"{video.stem}_overlayed{video.suffix}")

        vidClip = VideoFileClip(str(video))
        overlay = (
            ImageClip(str(image), transparent=True)
            .set_duration(vidClip.duration)
            .set_position(coordinate.to_tuple())
        )
        # .resize(height=50) # if you need to resize...
        final = CompositeVideoClip([vidClip, overlay])
        final.write_videofile(str(newVideo))
        super().replace_file(video, newVideo)
