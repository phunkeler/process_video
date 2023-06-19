import logging.config

from dependency_injector import containers, providers

from . import services


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(ini_files=["config.ini"])

    logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini",
    )

    # Services
    file_service = providers.Factory(services.FileService)
    image_service = providers.Factory(services.ImageService)
    video_service = providers.Factory(services.VideoService)
