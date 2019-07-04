import json
import mos_calculation

# create initial delay estimations from 'Initial Delay Vs. Interruptions: Between the Devil and the Deep Blue Sea'
# assume values as they are not in the paper
output_file = '06263849_initial_delay'

codec = 'h264'
framerate = 25
bitrate = 5000
resolution = '1920x1080'
info_IGen = mos_calculation.prepareIGen('1920x1080', 80)

# input from paper
delay_infos = [
    # video duration; waiting time; mos
    [60, 1, 4.07],
    [60, 8, 4.02],
    [60, 16, 4.0],
    [30, 0, 4.15],
    [30, 1, 4.1],
    [30, 8, 4.02],
    [30, 16, 3.95]
]
results = []

for delay_info in delay_infos:
    video_duration = delay_info[0]
    waiting_time = delay_info[1]
    mos = delay_info[2]

    stalls = [mos_calculation.createStallingSegment(0, waiting_time)]
    segments = [mos_calculation.createVideoSegment(codec, bitrate, 0, video_duration, resolution, framerate)]

    res = mos_calculation.runModelFromSegments(segments, stalls, info_IGen, mos)
    results.append(res)

mos_calculation.writeJsonToFile(output_file, results)
