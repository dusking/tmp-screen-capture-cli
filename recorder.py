from subprocess import CalledProcessError
import sys

import file_utils
from file_utils import create_output_dir, does_dir_exist
import ffmpeg_utils


class Recorder:
    """
    A class to handle video recording in chunks and manage output directory.

    Attributes:
        output_dir (str): Path to the output directory for video recordings.
    """

    def __init__(self, output_dir, force):
        """
        Initializes the Recorder with the specified output directory and handles directory creation or clearance.

        Args:
            output_dir (str): Path to the output directory.
            force (bool): If True, clears the existing directory if it exists.
        """
        self.output_dir = output_dir
        self.initialize_output_dir(output_dir, force)

    @staticmethod
    def initialize_output_dir(output_dir, force):
        """
        Initializes the output directory, creating or clearing it based on the 'force' parameter.

        Args:
            output_dir (str): Path to the output directory.
            force (bool): If True, clears the existing directory if it exists.
        """
        if does_dir_exist(output_dir):
            if force:
                file_utils.clear_dir(output_dir)
            else:
                print(f"Output directory {output_dir} already exists. Please specify an output directory that does not "
                      f"exist.")
                sys.exit(1)
        create_output_dir(output_dir)
        print(f"Created output directory {output_dir}")

    def start(self, chunk_size):
        """
        Starts the recording process, recording video in chunks of specified size.

        Args:
            chunk_size (int): Duration of each video chunk in seconds.
        """
        output_dir_path = f"{self.output_dir}"
        try:
            print(f"Starting recording with chunk size: {chunk_size} seconds")
            ffmpeg_utils.record_video_in_chunks(output_dir_path, chunk_size)
        except CalledProcessError as e:
            print(f"FFmpeg Failed to complete recording: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            print("Recording stopped by user.")
            # Handle edge case: last file did not flush any content
            recordings = file_utils.list_files(output_dir_path)
            if len(recordings) > 0:
                file_utils.handle_empty_file(recordings[-1])
