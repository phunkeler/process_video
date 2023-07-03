import logging.config

from dependency_injector import containers, providers

from . import services


class Container(containers.DeclarativeContainer):
    logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini",
    )

    # Services
    file_service = providers.Factory(services.FileService)
    image_service = providers.Factory(services.ImageService)
    video_service = providers.Factory(services.VideoService)
    effect_service = providers.Factory(
        services.VideoEffectService, image_service=image_service
    )

    # VideoEffect handlers
