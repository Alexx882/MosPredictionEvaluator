import json
from itu_p1203 import P1203Standalone

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


# craete stalls from 'Estimating the impact of single and multiple freezes on video quality'
codec = 'h264'
framerate = 25.0
bitrate = 3500
resolution = '704x576'
stall_durations = [[0.12, 4],
    [0.2, 3.8],
    [0.52, 3],
    [1, 2.5],
    [2, 1.8],
    [3, 1.5]]
results = []

for stall in stall_durations:
    stalls = []
    segments = []
    stall_duration = stall[0]
    stalls.append(createStallingSegment(0, 0))
    segments.append(createVideoSegment(codec, bitrate, 0, 10, resolution, framerate))
    stalls.append(createStallingSegment(10, stall_duration))
    segments.append(createVideoSegment(codec, bitrate, 10, 20, resolution, framerate))

    input = {}
    input["I11"] = prepareI11([createAudioSegment('aaclc', 0, 0, 20)]) # no audio
    input["I13"] = prepareI13(segments)
    input["I23"] = prepareI23(stalls)
    input["IGen"] = prepareIGen('1400x1050', 80)

    results.append(runModel(input, stall[1]))

# write json to file
with open('results/result_279425.json', 'w') as file:
    file.write(json.dumps(results))
