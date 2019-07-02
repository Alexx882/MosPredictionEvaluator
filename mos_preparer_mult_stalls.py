import json
from itu_p1203 import P1203Standalone
import statistics

STREAM_ID = 42

def prepareI11(segments):
    '''Prepares I.11 aka audio'''
    return {'streamId': STREAM_ID, 'segments': segments}

def createAudioSegment(codec, bitrate, start, duration):
    return {
        'codec': codec,
        'bitrate': bitrate,
        'start': start, 
        'duration': duration
    }

def prepareI13(segments):
    '''Prepares I.13 aka video'''
    return {'streamId': STREAM_ID, 'segments': segments}

def createVideoSegment(codec, bitrate, start, duration, resolution, fps):
    '''Creates a video segment for M0, so no frames or representation id'''
    return {
        'codec': codec,
        'bitrate': bitrate,
        'start': start, 
        'duration': duration, 
        'resolution': resolution,
        'fps': fps
    }

def prepareI23(stalls):
    '''Prepares I.14 aka stalling, here called I.23'''
    return {'streamId': STREAM_ID, 'stalling': stalls}
    
def createStallingSegment(start, duration):
    return [start, duration]

def prepareIGen(resolution, viewing_distance):
    '''Prepares device information'''
    return {
        "displaySize": resolution,
        "device": "pc",
        "viewingDistance": viewing_distance
    }

def runModel(input, expected):
      # create model ...
    itu_p1203 = P1203Standalone(input)
    # ... and run it
    output = itu_p1203.calculate_complete(False)

    return {'calculated': output['O46'],
            'expected': expected}


# Apply values from 'QoE of YouTube Video Streaming for Current Internet Transport Protocols'
output_file = 'result_conf_485'

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
        audio = []

        current_time = 0
        # create stalls
        for num_segments in range(stalling_amount+1):
            stalls.append(createStallingSegment(current_time, stalling_length if current_time != 0 else 0))
            current_time += stalling_distance

        segments.append(createVideoSegment(codec, bitrate, 0, video_length, resolution, framerate))
        audio.append(createAudioSegment('aaclc', 0, 0, video_length))

        # exec estimation
        input = {}
        input["I11"] = prepareI11(audio) # no audio
        input["I13"] = prepareI13(segments)
        input["I23"] = prepareI23(stalls)
        input["IGen"] = prepareIGen(resolution, 80)
        results.append(runModel(input, mos_scores[stalling_amount]))

# write json to file
with open(f'results/{output_file}.json', 'w') as file:
    file.write(json.dumps(results))