import argparse

from process_video.coordinate import Coordinate
from process_video.size import Size


class Parser:
    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser(
            prog="process_video",
            description="Downloads a video locally, edits it, applies an overlay, and then exports it.",
        )
        parser.add_argument(
            "--video",
            help='The url of the video file to download. Can be "http", "https", or "file" scheme.',
        )
        parser.add_argument(
            "--overlay",
            help='The url of the overlay file to download. Can be "http", "https", or "file" scheme.',
        )
        parser.add_argument(
            "--compress",
            help='Option to compress the video using "libx264".',
            action="store_true",
        )
        parser.add_argument(
            "--resize-overlay",
            help="Option to resize the image overlay (width, height)",
            type=size,
        )
        parser.add_argument(
            "--apply-overlay",
            help='Overlays the supplied image on top of the "video" at the specified coordinate.',
            type=coordinate,
            # TODO: Allow user to specify 'center', 'top-left', 'top-right', 'bot-right', 'bot_left'
        )
        return parser.parse_args()


def size(string: str) -> Size:
    return Size(string)


def coordinate(string: str) -> Coordinate:
    return Coordinate(string)
