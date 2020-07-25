import argparse
import random
import sys


def make_parser():
    """Make the ArgParser object."""
    parser = argparse.ArgumentParser(
        description=
        'Landscape generator using the tileset of pokemon fire red')

    parser.add_argument(
        '--w',
        dest='map_size_x',
        type=int,
        default=50,
        help='The horizontal amount of tiles the map consists of. full hd (1920x1088) -> 120x68')

    parser.add_argument(
        '--h',
        dest='map_size_y',
        type=int,
        default=50,
        help='The vertical amount of tiles the map consists of. full hd (1920x1088) -> 120x68')

    parser.add_argument(
        '--headless',
        dest='headless_opt',
        action='store_true',
        help='Run in headless mode.')

    parser.add_argument(
        '--save',
        dest='save_opt',
        action='store_true',
        help='Save generated image.')

    parser.add_argument(
        '--seed',
        dest='seed_opt',
        type=int,
        default=random.randint(0, sys.maxsize),
        help='The world generation seed')

    parser.add_argument(
        '--c',
        dest='credits_opt',
        action='store_true',
        help='Show credits')

    return parser
