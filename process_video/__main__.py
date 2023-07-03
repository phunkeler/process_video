from dependency_injector.wiring import Provide, inject
from moviepy.editor import *

from process_video.containers import Container
from process_video.effects import VideoEffectRequest
from process_video.parser import Parser

from .services import FileService, ImageService, VideoEffectService, VideoService


@inject
def main(
    file_service: FileService = Provide[Container.file_service],
    image_service: ImageService = Provide[Container.image_service],
    video_service: VideoService = Provide[Container.video_service],
    effect_service: VideoEffectService = Provide[Container.effect_service],
) -> None:
    args = Parser.get_args()

    # get assets
    video_file = file_service.get_file(args.video)
    overlay_file = file_service.get_file(args.overlay)

    # Construct request object
    video_clip = VideoFileClip(str(video_file))
    image_clip = ImageClip(str(overlay_file), transparent=True)
    effect_request = VideoEffectRequest(video_clip, image_clip, args)

    # Apply effects
    effect_service.apply_effects(effect_request)

    end = "END"


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    main()
