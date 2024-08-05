import subprocess


def record_video_in_chunks(output_path, chunk_size):
    """
    Records video in chunks using FFmpeg.

    Args:
        output_path (str): Path to save the video chunks.
        chunk_size (int): Duration of each video chunk in seconds.
    """
    command = [
        'ffmpeg',
        '-f', 'avfoundation',
        '-framerate', '30',
        '-i', '2',
        '-r', '30',
        '-v', 'quiet',
        '-f', 'segment',
        '-segment_time', str(chunk_size),
        '-reset_timestamps', '1',
        '-c', 'copy',
        f"{output_path}/%d.mkv"
    ]
    subprocess.run(command, stderr=subprocess.PIPE, text=True, check=True)


def play_video(video_file, start_time=None):
    """
    Plays a video file using FFplay.

    Args:
        video_file (str): Path to the video file.
        start_time (str, optional): Start time in seconds to begin playback.
    """
    if not start_time:
        command = [
            'ffplay',
            video_file,
            '-v', 'quiet'
        ]
    else:
        command = [
            'ffplay',
            '-ss', start_time,
            '-v', 'quiet',
            video_file,
        ]
    subprocess.run(command, check=True)


def concatenate_videos(config_file, result_file):
    """
    Concatenates multiple videos into one using FFmpeg.

    Args:
        config_file (str): Path to the configuration file listing the videos to concatenate.
        result_file (str): Path to save the concatenated video.
    """
    command = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-v', 'quiet',
        '-i', config_file,
        '-c', 'copy',
        result_file
    ]
    subprocess.run(command, check=True)


def remux_video(input_path, output_path):
    """
    Remuxes a video file using FFmpeg.

    Args:
        input_path (str): Path to the input video file.
        output_path (str): Path to save the remuxed video file.
    """
    command = [
        'ffmpeg',
        '-v', 'quiet',
        '-i', input_path,
        '-c', 'copy',
        '-map', '0',
        output_path
    ]
    subprocess.run(command, stderr=subprocess.PIPE, text=True, check=True)
