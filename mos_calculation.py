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

def prepareIGen(resolution, viewing_distance, device='pc'):
    '''Prepares device information'''
    return {
        "displaySize": resolution,
        "device": device,
        "viewingDistance": viewing_distance
    }

def runModel(input, expected):
      # create model ...
    itu_p1203 = P1203Standalone(input)
    # ... and run it
    output = itu_p1203.calculate_complete(False)

    return {'calculated': output['O46'],
            'expected': expected}

def runModelFromSegments(video_segments, stall_segments, igen_info, expected_result):
    input = {}
    video_length = video_segments[-1]['start'] + video_segments[-1]['duration']
    input["I11"] = prepareI11([createAudioSegment('aaclc', 0, 0, video_length)]) # no audio
    input["I13"] = prepareI13(video_segments)
    if stall_segments != None:
        input["I23"] = prepareI23(stall_segments)
    input["IGen"] = igen_info

    return runModel(input, expected_result)

def writeJsonToFile(filename, content):
    with open(f'results/{filename}.json', 'w') as file:
        file.write(json.dumps(content))
