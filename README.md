# Screen Capture and Playback CLI Tool

## Description

This CLI tool provides functionalities for screen capturing and video playback. It allows users to record their screen in chunks and then play back the recordings from a specified number of seconds ago. The tool is designed to be simple and flexible, making it easy to capture and review screen activities.

## Features

- **Screen Capture:** Record your screen in configurable chunk sizes.
- **Playback:** Play the video from a specified number of seconds ago.

## Running the tool
### System Requirements
- **Operating System:** macOS
- **Python:** Version 3.6 or higher
- **FFmpeg:** Installed and available in the system PATH
- Mac users be aware that FFmpeg will need screen capture permissions, so it must be enabled on the app that is running the CLI (e.g. iTerm, pyCharm, etc.)

### Setup steps
1. Clone the repository
2. Install [ffmpeg](https://www.ffmpeg.org/download.html), for example: ```brew install ffmpeg```
3. Make sure the app you are running the tool from has permissions (i.e. camera/microphone). This must be configured in the Mac Privacy & Security settings.
4. In the project, ``pip install -r requirements.txt`
5. Run the tool (see example usages below)

## Example Usages

### Start Screen Capture

To start screen capturing with chunks of 5 seconds each and save the recordings to the default `./recordings` directory:

```
python main.py start --chunk 5
```

To save to a directory of your choice:

```
python main.py start --chunk 5 --output ./my_recordings
```

If the output directory already exists, you will get an error. To force overriding the existing directory:

```
python main.py start --chunk 5 --force
```

### Play back "t" seconds

To play the last 10 seconds of recordings from the default ./recordings directory:

```
python main.py play --seconds 10
```

And for a specified output directory:
```
python main.py play --seconds 10 --output ./my_recordings
```

#### Debugging

To aid in debugging, use the debug flag to not clean out the output files (i.e. the configuration file FFmpeg uses to generated the concatenated video file, and the concatenated video file)
```
python main.py play --seconds 10 --debug
```

## Next Steps/Improvements
1. **Operating system support**: The code is written and tested primarily for macOS. It utilizes the AVFoundation input device (-i '2') in FFmpeg, which is specific to macOS.
2. **Dependencies**: FFmpeg must be installed and accessible. Handling the cases which it isn't can be done in a more user-friendly way.
3. **Error handling & Logging**: Error handling & logging can be improved, especially to enhance user experience with the tool. Using a logging library, for example, would be more appropriate.
4. **Configuration File Management**: Better organization + handling of the generated output files, and, clean up after, especially to enhance user experience.
5. **Testing**: Unit tests and scenarios using `unittest` or `pytest`
6. **More sophisticated user feedback + interaction**: Can Add more interactive prompts for user actions, especially for actions like clearing or overriding directories, and provide progress via logging.
7. **More input options**: The ffmpeg commands can be more dynamic and accept more custom inputs, such as which input devices to use, framerate, etc.



