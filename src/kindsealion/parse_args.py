import argparse
import pathlib


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--outdir",
        type=pathlib.Path,
        help="Output directory",
        default="rendered",
    )
    parser.add_argument(
        "-s",
        "--starting-image",
        type=str,
        help="Starting image for the first manifest",
        default="images:ubuntu/20.04/cloud",
    )
    parser.add_argument(
        "--skip-publish",
        action="store_true",
        help="Skip publishing the output image",
    )
    parser.add_argument(
        "-m",
        "--manifest-url",
        type=str,
        help="URL or file path of the manifest.yml",
        default="https://raw.githubusercontent.com/taylormonacelli/kindsealion/master/manifest.yml",
    )
    return parser.parse_args()
