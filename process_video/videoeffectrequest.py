from argparse import Namespace

from moviepy.editor import *


class VideoEffectRequest:
    def __init__(
        self, video_clip: VideoClip, image_clip: VideoClip, user_args: Namespace
    ) -> None:
        self.video_clip = video_clip
        self.image_clip = image_clip
        self.user_args = user_args
