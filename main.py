import itertools
import os
import subprocess

import script

def main():
    print("Removing old result file...")
    if os.path.isfile("out/result.mp4"):
        os.remove("out/result.mp4")

    print("Joining audio files...")
    join_audio()

    print("Combining audio and video...")
    command = 'ffmpeg -v quiet'
    command = ''.join([command, ' -i in/', script.video])
    command = ''.join([command, ' -i in/', 'audio.mp3'])
    command = ''.join([command, ' out/result.mp4'])
    subprocess.run([command], shell=True)

    print("Cleaning up...")
    if os.path.isfile("in/audio.mp3"):
        os.remove("in/audio.mp3")

    print("Success!")

def join_audio():
    command = 'ffmpeg -v quiet'
    files = []
    plays = []
    durations = []
    silences = []

    for track in script.audio:
        files.append(list(track.keys())[0])
        plays.append(list(track.values())[0])

        durationAnalysis = subprocess.run([''.join(['ffmpeg -v quiet -stats -i in/', list(track.keys())[0], ' -f null -'])], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        duration = float(durationAnalysis.stderr.decode('utf-8').split('time=')[1][6:11])
        durations.append(duration)

    for i, play in enumerate(plays):
        if i < len(plays) - 1:
            silences.append(round(float(plays[i+1]) - float(play) - durations[i], 2))

    for file in files:
        command = ''.join([command, ' -i in/', file])

    command = ''.join([command, ' -filter_complex "'])

    for i, silence in enumerate(silences):
        # hacked because of negative pauses
        silence = 0
        command = ''.join([command, 'aevalsrc=exprs=0:d=', str(silence), '[silence', str(i), '], '])

    first = True
    for i, play in enumerate(plays):
        if first:
            command = ''.join([command, '[', str(i), ':a] '])
            first = False
        else:
            command = ''.join([command, '[silence', str(i-1), '] '])
            command = ''.join([command, '[', str(i), ':a] '])

    command = ''.join([command, 'concat=n=', str(len(files) + len(silences)), ':v=0:a=1[outa]" -map [outa] in/audio.mp3'])

    subprocess.run([command], shell=True)


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

main()
