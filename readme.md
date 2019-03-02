# Video+Audio

Join video files with audio tracks using ffmpeg.

## Install

Install `ffmpeg`:
```
$ brew install ffmpeg
```

## Usage

1. Move the video file (mp4) and all audio files (mp3s) into the `in` folder.
2. Add your `script.py` file in the root folder. You will need to add the name
of the video file and all the audio files together with the time in the video
they should start (in seconds). Use `script.example.py` for reference.
3. Run the `main.py` file from the main folder:
```
$ python3 main.py
```

## Debugging

To see the commands being run and outputs from `ffmpeg` run with `debug` option:
```
$ python3 main.py debug
```
