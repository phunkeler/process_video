import ffmpeg
from pathlib import Path
from py_linq import Enumerable

class Info:
    def __init__(self, video_file: Path) -> None:
        probe           = self.execute_ffprobe(video_file)
        self.streams    = Enumerable(probe['streams'])
        self.frames     = Enumerable(probe['frames'])
        self.format     = probe['format']
        self.set_video_dims()

    def execute_ffprobe(self, video_file: Path):
        return ffmpeg.probe(str(video_file), **{"show_frames":None})

    def set_video_dims(self):
        info = (
            self
            .streams
            .first_or_default(lambda x: x['codec_type'] == 'video')
        )
        self.width  = int(info['width'])
        self.height = int(info['height'])