from pathlib import Path
from overlay import Overlay
from video import Video

def main():
    yt_url = 'https://www.youtube.com/watch?v=a7V02xJVLI0'
    overlay_path = Path("assets/overlay.png")
    video = Video()
    video.download_from_youtube(yt_url)
    overlay = Overlay(overlay_path)
    overlay.scale(200, -1) # Specify -1 for either w/h to maintain aspect-ratio
    video.apply_overlay(overlay, 25, video.info.height - 80) # TODO: apply overlay without breaking sound...
    video.output()

# Execute 'main' function when running this script
if __name__ == "__main__":
    main()