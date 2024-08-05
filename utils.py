from moviepy.editor import VideoFileClip


def get_video_duration(video_path):
    """
    Gets the duration of a video file.

    Args:
        video_path (str): Path to the video file.

    Returns:
        float: Duration of the video in seconds.
    """
    with VideoFileClip(video_path) as video:
        return video.duration
