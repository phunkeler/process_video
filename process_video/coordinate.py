import argparse


class Coordinate:
    def __init__(self, string: str):
        try:
            self.x, self.y = map(int, string.split(","))
        except:
            raise argparse.ArgumentTypeError("Coordinate must be x, y")

    def to_tuple(self):
        return (self.x, self.y)
