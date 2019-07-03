import json
import mos_calculation

# craete stalls from 'Estimating the impact of single and multiple freezes on video quality'
output_file = 'result_279425'

codec = 'h264'
framerate = 25.0
bitrate = 3500
resolution = '704x576'
stall_durations = [[0.12, 3.85],
    [0.2, 3.75],
    [0.52, 3.2],
    [1, 2.85],
    [2, 2],
    [3, 1.75]]
results = []

for stall in stall_durations:
    stalls = []
    segments = []
    stall_duration = stall[0]
    stalls.append(mos_calculation.createStallingSegment(0, 0))
    segments.append(mos_calculation.createVideoSegment(codec, bitrate, 0, 10, resolution, framerate))
    stalls.append(mos_calculation.createStallingSegment(10, stall_duration))
    segments.append(mos_calculation.createVideoSegment(codec, bitrate, 10, 10, resolution, framerate))

    res = mos_calculation.runModelFromSegments(segments, 
        stalls, 
        mos_calculation.prepareIGen('1400x1050', 80), 
        stall[1])
    results.append(res)

mos_calculation.writeJsonToFile(output_file, results)
