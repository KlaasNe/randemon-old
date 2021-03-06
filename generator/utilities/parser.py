import argparse
import random
from sys import maxsize


def make_parser():
    """Make the ArgParser object."""
    parser = argparse.ArgumentParser(
        description='Landscape generator using the tileset of pokemon fire red')

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
        default=random.randint(0, maxsize),
        help='The world generation seed')

    parser.add_argument(
        '-c',
        dest='credits_opt',
        action='store_true',
        help='Show credits')

    parser.add_argument(
        '--splith',
        dest='x_split',
        type=int,
        default=1,
        help='Split the result horizontally')

    parser.add_argument(
        '--splitv',
        dest='y_split',
        type=int,
        default=1,
        help='Split the result vertically')

    parser.add_argument(
        '--export',
        dest='export_opt',
        action='store_true',
        help='Export the map as a json file')

    parser.add_argument(
        '--maxheight',
        dest='max_hill_height',
        type=int,
        default=5,
        help='Maximal height of a hill')

    parser.add_argument(
        '--grass',
        dest='tall_grass_coverage',
        type=int,
        default=30,
        help='Percentage of the map to be covered with tall grass')

    parser.add_argument(
        '--trees',
        dest='tree_coverage',
        type=int,
        default=10,
        help='Percentage of the map to be covered with trees')

    return parser
