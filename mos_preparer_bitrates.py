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


# Assume values from 'A Study on Quality of Experience for Adaptive Streaming Service'
output_file = 'result_06649320.json'

codec = 'h264'
framerate = 25
resolution = '1280x720'
bitrates = {'R1': 256,
    'R2': 384,
    'R3': 512,
    'R4': 768,
    'R5': 1024,
    'R6': 1538,
    'R7': 2048
    }
segment_dur = 9

def createVideoSegmentsFromRates(rates):
    assert len(rates) == 12, "Misread some rates"
    segments = []
    cur_dur = 0
    for r in rates:
        segments.append(createVideoSegment(codec, bitrates[r], cur_dur, segment_dur, resolution, framerate))
        cur_dur = cur_dur+segment_dur
    return segments

prepared_input_segments = []

#region avg 384
# rising
rates = ['R1','R1','R1','R1','R2','R2','R2','R2','R3','R3','R3','R3']
prepared_input_segments.append([createVideoSegmentsFromRates(rates), 1.7])

# falling
rates = ['R3','R3','R3','R3','R2','R2','R2','R2','R1','R1','R1','R1']
prepared_input_segments.append([createVideoSegmentsFromRates(rates), 3.45])

# convex
rates = ['R2','R2','R2','R2','R3','R3','R3','R3','R1','R1','R1','R1']
prepared_input_segments.append([createVideoSegmentsFromRates(rates), 2.55])
#endregion

#region avg 768
# rising
rates = ['R3','R3','R3','R3','R4','R4','R4','R4','R5','R5','R5','R5']
prepared_input_segments.append([createVideoSegmentsFromRates(rates), 3.55])

# falling
rates = ['R5','R5','R5','R5','R4','R4','R4','R4','R3','R3','R3','R3']
prepared_input_segments.append([createVideoSegmentsFromRates(rates), 3.5])

# convex
rates = ['R4','R4','R4','R4','R5','R5','R5','R5','R3','R3','R3','R3']
prepared_input_segments.append([createVideoSegmentsFromRates(rates), 3.15])
#endregion

#region avg 768 (5 rates)
# rising
rates = ['R1','R3','R3','R3','R4','R4','R4','R4','R4','R5','R5','R6']
prepared_input_segments.append([createVideoSegmentsFromRates(rates), 3.25])

# falling
rates = ['R6','R5','R5','R4','R4','R4','R4','R4','R3','R3','R3','R1']
prepared_input_segments.append([createVideoSegmentsFromRates(rates), 3.6])

# convex
rates = ['R1','R3','R4','R4','R5','R6','R5','R4','R4','R4','R3','R3']
prepared_input_segments.append([createVideoSegmentsFromRates(rates), 2.55])
#endregion

#region avg 1024 (5 rates)
# rising
rates = ['R1','R3','R4','R4','R4','R5','R5','R5','R6','R6','R6','R6']
prepared_input_segments.append([createVideoSegmentsFromRates(rates), 3.0])

# falling
rates = ['R6','R6','R6','R6','R5','R5','R5','R4','R4','R4','R3','R1']
prepared_input_segments.append([createVideoSegmentsFromRates(rates), 3.75])

# convex
rates = ['R1','R4','R4','R4','R6','R6','R6','R6','R5','R5','R5','R3']
prepared_input_segments.append([createVideoSegmentsFromRates(rates), 3.4])
#endregion

# exec all estimations
results = []
for seg in prepared_input_segments:
    input = {}
    input["I11"] = prepareI11([createAudioSegment('aaclc', 0, 0, 9*12)]) # no audio
    input["I13"] = prepareI13(seg[0])
    input["IGen"] = prepareIGen(resolution, 80)
    results.append(runModel(input, seg[1]))

# write json to file
with open(f'results/{output_file}', 'w') as file:
    file.write(json.dumps(results))
