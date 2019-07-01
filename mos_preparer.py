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


# Copy values from 'Cross-Dimensional Perceptual Quality Assessment for Low Bit-Rate Videos'
output_file = 'result_04660307'

codec = 'h264'
resolution = '1408x1152' # '352x288'

def createFrameAndBitRate(framerate, bitrate, mos):
    return {'Framerate': framerate, 'Bitrate': bitrate, 'MOS': mos}

rates = [
    # container
    createFrameAndBitRate(15, 128, 3.42),
    createFrameAndBitRate(30, 128, 3.74),
    createFrameAndBitRate(30, 384, 4.53),

    createFrameAndBitRate(7.5, 64, 2.84),
    createFrameAndBitRate(7.5, 128, 3.32),
    createFrameAndBitRate(15, 64, 3.42),

    # foreman
    createFrameAndBitRate(30, 128, 2.16),
    createFrameAndBitRate(15, 128, 2.42),
    createFrameAndBitRate(30, 384, 4.58),

    createFrameAndBitRate(15, 64, 1.53),
    createFrameAndBitRate(7.5, 64, 2.05),
    createFrameAndBitRate(7.5, 128, 3.37),

    # coastguard
    createFrameAndBitRate(30, 128, 2.11),
    createFrameAndBitRate(15, 128, 2.32),
    createFrameAndBitRate(30, 384, 3.16),

    createFrameAndBitRate(15, 64, 1.74),
    createFrameAndBitRate(7.5, 128, 2.53),
    createFrameAndBitRate(7.5, 64, 2.63),

    # news
    createFrameAndBitRate(15, 128, 4.0),
    createFrameAndBitRate(30, 128, 4.16),
    createFrameAndBitRate(30, 384, 5),

    createFrameAndBitRate(15, 64, 3.32),
    createFrameAndBitRate(7.5, 64, 3.47),
    createFrameAndBitRate(7.5, 128, 4.05),

    # tempete
    createFrameAndBitRate(30, 128, 2.47),
    createFrameAndBitRate(15, 128, 3.47),
    createFrameAndBitRate(30, 384, 4.53),

    createFrameAndBitRate(15, 64, 2),
    createFrameAndBitRate(7.5, 64, 3.05),
    createFrameAndBitRate(7.5, 128, 3.37)
]

##region prepare individual results with multiple MOS per M0 info
prepared_input_segments = []
for values in rates:
    segments = [createVideoSegment(codec, values['Bitrate'], 0, 10, resolution, values['Framerate'])]
    prepared_input_segments.append([segments, values['MOS']])

# exec all estimations
results = []
for seg in prepared_input_segments:
    input = {}
    input["I11"] = prepareI11([createAudioSegment('aaclc', 0, 0, 10)]) # no audio
    input["I13"] = prepareI13(seg[0])
    input["IGen"] = prepareIGen('1760x1440', 120)
    results.append(runModel(input, seg[1]))

# write json to file
with open(f'results/{output_file}.json', 'w') as file:
    file.write(json.dumps(results))
#endregion

##region prepare results with average mos and calculate again
prepared_input_segments = []

all_rates = [[30,128],[15,128],[30,384],[15,64],[7.5,64],[7.5,128]]
for (f, b) in all_rates:
    avg_mos_lst = [x['MOS'] for x in rates if x['Framerate'] == f and x['Bitrate'] == b]
    assert len(avg_mos_lst) == 5, 'not all videos have framerate and bitrate'
    prepared_input_segments.append([[createVideoSegment(codec, b, 0, 10, resolution, f)], statistics.mean(avg_mos_lst)])

# exec all estimations
results = []
for seg in prepared_input_segments:
    input = {}
    input["I11"] = prepareI11([createAudioSegment('aaclc', 0, 0, 10)]) # no audio
    input["I13"] = prepareI13(seg[0])
    input["IGen"] = prepareIGen('1760x1440', 120)
    results.append(runModel(input, seg[1]))

# write json to file
with open(f'results/{output_file}_avg.json', 'w') as file:
    file.write(json.dumps(results))
#endregion