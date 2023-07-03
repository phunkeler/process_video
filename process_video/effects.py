from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Optional

from moviepy.editor import *
from moviepy.editor import ImageClip, VideoClip
from moviepy.video.fx.resize import resize

from process_video.size import Size
from process_video.videoeffectrequest import VideoEffectRequest

# What is our request object in this case?
# How does each request
# Create "EffectRequest" object - Contains asset file paths and cmd-line args


class VideoEffectHandler(ABC):
    @abstractmethod
    def set_next(self, handler: VideoEffectHandler) -> VideoEffectHandler:
        pass

    @abstractmethod
    def handle(self, request: VideoEffectRequest) -> VideoEffectRequest:
        pass


class AbstractVideoEffectHandler(VideoEffectHandler):
    def __init__(self) -> None:
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )

    _next_handler: VideoEffectHandler = None

    def set_next(self, handler: VideoEffectHandler) -> VideoEffectHandler:
        self._next_handler = handler
        # Returning an effect from here let's us link
        # effects in a convenient way like this:
        # overlay.set_next(speedramp).set_next(compress)
        return handler

    @abstractmethod
    def handle(self, request: VideoEffectRequest) -> VideoEffectRequest:
        if self._next_handler:
            return self._next_handler.handle(request)

        return request

    def log_ignoring(self):
        self.logger.info("Ignoring")

    def log_handling(self):
        self.logger.info("Handling")


"""
All Concrete Handlers either handle a request or pass it to the next handler in
the chain.
"""


class ResizeOverlayHandler(AbstractVideoEffectHandler):
    def handle(self, request: VideoEffectRequest) -> VideoEffectRequest:
        if request.user_args.resize_overlay:
            self.log_handling()
            request.image_clip = self.resize_image(
                request.image_clip, request.user_args.resize_overlay
            )
        else:
            self.log_ignoring()
        return super().handle(request)

    def resize_image(self, image_clip: ImageClip, size: Size) -> VideoClip:
        return resize(image_clip, width=size.width)


class OverlayHandler(AbstractVideoEffectHandler):
    def handle(self, request: VideoEffectRequest) -> VideoEffectRequest:
        if request.user_args.apply_overlay:
            self.log_handling()
            # Set the duration of the image clip to match the duration of the video clip
            request.image_clip = request.image_clip.set_duration(
                request.video_clip.duration
            )

            # Set the position of the image clip on the video (top-left corner)
            request.image_clip = request.image_clip.set_position(
                request.user_args.apply_overlay.to_tuple()
            )

            # Overlay the image clip on the video clip
            request.video_clip = CompositeVideoClip(
                [request.video_clip, request.image_clip]
            )
        else:
            self.log_ignoring()

        return super().handle(request)


class SpeedRampHandler(AbstractVideoEffectHandler):
    def handle(self, request: VideoEffectRequest) -> VideoEffectRequest:
        if request.user_args.speed_ramp:
            request.video_clip = self.apply_speed_ramp(request.video_clip)
        else:
            self.log_ignoring()

        return super().handle(request)

    def apply_speed_ramp(self, video_clip: VideoClip) -> VideoClip:
        speed_factor1 = 0.6  # Speed factor
        start_time1 = 1.0  # Start time of the speed ramp (in seconds)
        end_time1 = 2.0  # End time of the speed ramp (in seconds)

        speed_factor2 = 0.8  # Speed factor (e.g., 2.0 for double speed)
        start_time2 = 2.0  # Start time of the speed ramp (in seconds)
        end_time2 = 3.0  # End time of the speed ramp (in seconds)

        speed_factor3 = -8.0  # Speed factor (e.g., 2.0 for double speed)
        start_time3 = 7.0  # Start time of the speed ramp (in seconds)
        end_time3 = 12.0  # End time of the speed ramp (in seconds)

        speed_factor4 = 1.0  # Speed factor (e.g., 2.0 for double speed)

        # Load the video clip

        # Split the clip into three parts: before, during, and after the speed ramp
        clip1 = video_clip.subclip(0, start_time1)
        clip2 = video_clip.subclip(start_time1, end_time1)
        clip3 = video_clip.subclip(end_time1, end_time2)
        clip4 = video_clip.subclip(end_time2, 8)

        # Apply speed ramp effect to the clips
        # clip1 = clip1.fx(vfx.speedx, 1.0)
        clip2 = clip2.fx(vfx.speedx, speed_factor1)
        clip3 = clip3.fx(vfx.speedx, speed_factor2)
        # clip4 = clip4.fx(vfx.speedx, speed_factor4)

        return concatenate_videoclips([clip1, clip2, clip3, clip4])
