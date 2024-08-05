import argparse
from player import Player
from recorder import Recorder


def main():
    """
    Main function to handle command-line interface for screen capture and playback.
    """
    parser = argparse.ArgumentParser(description="CLI tool for screen capture and playback.")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Commands")

    # start command
    parser_start = subparsers.add_parser("start", help="Begin screen capture")
    parser_start.add_argument("--chunk", type=float, default=3, help="Duration of each video chunk in seconds")
    parser_start.add_argument("--output", type=str, default="./recordings", help="Output directory for video files")
    parser_start.add_argument("--force", action='store_true',
                               help="If set, and output directory already exists, removes it and creates a new one.")

    # play command
    parser_play = subparsers.add_parser("play", help="Play the video from a specified number of seconds ago")
    parser_play.add_argument("--seconds", type=float, required=True, help="Number of seconds ago to start playback from")
    parser_play.add_argument("--output", type=str, default="./recordings", help="Output directory for video files")
    parser_play.add_argument("--debug", action='store_true', help="Debug mode")

    args = parser.parse_args()

    if args.command == 'start':
        handle_start(args.chunk, args.output, args.force)
    elif args.command == 'play':
        handle_play(args.seconds, args.output, args.debug)


def handle_start(chunk, output, force):
    """
    Handles the 'start' command to initiate screen capture.

    Args:
        chunk (float): Duration of each video chunk in seconds.
        output (str): Output directory for video files.
        force (bool): If True, removes existing output directory and creates a new one.
    """
    start_summary = (
        f"Screen capture will start with the following settings:\n"
        f"- Chunk size: {chunk} seconds per file\n"
        f"- Output folder: {output}"
    )
    print(start_summary)
    Recorder(output, force).start(chunk)


def handle_play(seconds, output, debug):
    """
    Handles the 'play' command to play the video from a specified number of seconds ago.

    Args:
        seconds (float): Number of seconds ago to start playback from.
        output (str): Output directory for video files.
        debug (bool): Debug mode will not remove concatenation files
    """
    print(f"Playback will start from {seconds} seconds ago.")
    Player(output, debug).play(seconds)


if __name__ == '__main__':
    main()
