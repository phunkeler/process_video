from dependency_injector.wiring import Provide, inject

from process_video.containers import Container
from process_video.parser import Parser

from .services import FileService, ImageService, VideoService


@inject
def main(
    file_service: FileService = Provide[Container.file_service],
    image_service: ImageService = Provide[Container.image_service],
    video_service: VideoService = Provide[Container.video_service],
) -> None:
    args = Parser.get_args()
    video = file_service.get_file(args.video)
    overlay = file_service.get_file(args.overlay)

    if args.compress:
        file_service.compress_file(video)

    if args.resize_overlay:
        image_service.resize_image(overlay, args.resize_overlay)

    if args.apply_overlay:
        video_service.overlay_image(video, overlay, args.apply_overlay)

    end = "END"


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    main()
