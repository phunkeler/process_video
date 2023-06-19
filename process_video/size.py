import argparse


class Size:
    def __init__(self, string: str):
        try:
            self.width, self.height = map(int, string.split(","))
        except:
            raise argparse.ArgumentTypeError("Size must be width, height")

    def to_tuple(self):
        return (self.width, self.height)
