import json
import mos_calculation
import statistics

# Apply values from 'QoE of YouTube Video Streaming for Current Internet Transport Protocols'
output_file = 'conf_485_mult_stalls'

# they claim independence from video parameters, so choose appropriate ones
codec = 'h264'
resolution = '1920x1080' 
framerate = 25.0
bitrate = 5000
video_length = 30

# multiple stalling lengths
paper_infos = [{
    'StallingLength': 1,
    'MosResults': [5, 3.5, 3.05, 3.1, 2.2, 1.95, 2.0]
    },
    {
    'StallingLength': 3,
    'MosResults': [5, 3.2, 2.5, 2.1, 2.2, 2.0, 2.1]
    }]

results = []
for paper_info in paper_infos:
    stalling_length = paper_info[ 'StallingLength']
    mos_scores = paper_info[ 'MosResults']
    assert len(mos_scores) == 7, f'Missed a result {mos_scores}'

    for stalling_amount in range(7):
        # periodic stalling
        stalling_distance = video_length/(stalling_amount+1)
        
        segments = []
        stalls = []

        current_time = 0
        # create stalls
        for num_segments in range(stalling_amount+1):
            stalls.append(mos_calculation.createStallingSegment(current_time, stalling_length if current_time != 0 else 0))
            current_time += stalling_distance

        segments.append(mos_calculation.createVideoSegment(codec, bitrate, 0, video_length, resolution, framerate))

        # exec estimation
        res = mos_calculation.runModelFromSegments(segments, stalls, mos_calculation.prepareIGen(resolution, 80), mos_scores[stalling_amount])
        results.append(res)

mos_calculation.writeJsonToFile(output_file, results)