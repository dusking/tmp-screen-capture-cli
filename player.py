import os
import sys
from subprocess import CalledProcessError

import file_utils
from file_utils import list_files
import ffmpeg_utils
from utils import get_video_duration

CONCAT_CONFIG_FILE = 'concat_config.txt'
CONCAT_VIDEO_VILE = 'concatenated_recording.mkv'


class Player:
    """
    A class to handle playback of video recordings.

    Attributes:
        output_dir (str): Path to the output directory containing video recordings.
        recording_files (list of str): List of recording file names in the output directory.
    """

    def __init__(self, output_dir, debug):
        """
        Initializes the Player with the specified output directory and lists the recording files.

        Args:
            output_dir (str): Path to the output directory containing video recordings.
            debug (bool): Flag for debug mode
        """
        self.output_dir = output_dir
        self.recording_files = list_files(output_dir)
        self.debug = debug

    def play(self, t):
        """
        Plays the last 't' seconds of the recordings.

        Args:
            t (float): Number of seconds from the end of the recordings to play.
        """

        # No recordings
        if len(self.recording_files) == 0:
            print('Error: No recording files to play.')
            return

        print(f"Playing last {t} seconds of recordings...")
        # Sort by the filename, which is the chunk number (e.g. 1.mkv)
        self.recording_files.sort(key=lambda x: int(x.split('.')[0]))

        # Prepare a configuration file that describes the chunks (and chunk portions) to merge for playback
        self.prepare_config_file_for_concatenation(self.recording_files, t)
        # Create concatenated video
        try:
            ffmpeg_utils.concatenate_videos(CONCAT_CONFIG_FILE, CONCAT_VIDEO_VILE)
            # Play concatenated video
            ffmpeg_utils.play_video(CONCAT_VIDEO_VILE)
        except CalledProcessError as e:
            print(f"FFMpeg failed to play back recordings with exception {e}")
            sys.exit(1)

        if not self.debug:
            file_utils.remove_file(CONCAT_CONFIG_FILE)
            file_utils.remove_file(CONCAT_VIDEO_VILE)

    def prepare_config_file_for_concatenation(self, recording_files, t):
        """
        Prepares a configuration file for concatenating video chunks to play the last 't' seconds of recordings.

        Example config file contents:
            file './recordings/1.mkv'
            inpoint 1.5700000000000003
            file './recordings/2.mkv'
            file './recordings/3_fixed.mkv'

        This means "Play 1.mvk starting at 1.57 seconds, then all of 2.mkv and all of 3.mkv"

        Args:
            recording_files (list of str): List of recording file names.
            t (int): Number of seconds from the end of the recordings to play.
        """
        remaining_time = t
        config_entries = []  # This will hold the lines to be written to the file

        # Process files in reverse so that we move backwards until we've included enough video
        for video_file in reversed(recording_files):
            file_path = os.path.join(self.output_dir, video_file)
            fixed_file_path = None

            # Sometimes the recorded file is incomplete, and the duration is unavailable
            # One solution is to remux the file usin FFmpeg
            # So, if we can't get the duration, we use a temporary fixed version of it
            try:
                try:
                    duration = get_video_duration(file_path)
                except IOError:
                    base_name, extension = os.path.splitext(video_file)
                    fixed_file_path = os.path.join(self.output_dir, f"{base_name}_fixed{extension}")
                    try:
                        ffmpeg_utils.remux_video(file_path, fixed_file_path)
                    except CalledProcessError as e:
                        print(f"FFmpeg failed to remux incomplete file with exception {e}")
                        sys.exit(1)

                    duration = get_video_duration(fixed_file_path)
            finally:
                if fixed_file_path is not None:
                    file_utils.remove_file(fixed_file_path)

            # Finished writing config file
            if remaining_time <= 0:
                break

            # Case where we need a portion fo the last video
            if remaining_time < duration:
                start_time = duration - remaining_time
                # We write the inpoint line first because while we are processing the videos
                # backwards now, we will reverse them back before writing to the actual file
                # so that they are listed in playback order, and the inpoint must be directly after
                # the file associated with it.
                inpoint_line = f"inpoint {start_time}\n"  # Tells FFmpeg when to start the video
                config_entries.append(inpoint_line)
                config_entries.append(f"file '{file_path}'\n")
                remaining_time = 0  # Stop after adding this entry
            else:
                # Need the entire file
                config_entries.append(f"file '{file_path}'\n")
                remaining_time -= duration

        # Reverse the entries so that they will be written to the file in playback order
        config_entries.reverse()
        # Write to the file
        file_utils.write_to_file(CONCAT_CONFIG_FILE, config_entries)
