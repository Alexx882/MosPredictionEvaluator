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


# Apply values from 'Flicker Effects in Adaptive Video Streaming to Handheld Devices'
output_file = 'result_acmmm2011-perception'

# they claim independence from video parameters, so choose appropriate ones
codec = 'h264'
base_framerate = 30.0
base_resolution = '480x320'
bitrate = 1000 # not defined, appropriate chosen
video_length = 12

# values are given in frames
durations = [30,60,90,180]
durations = [d/30 for d in durations]

results = []

#region Blur Flicker
target_resolutions = [
    {'Res': '240x160',
    'Mos': [-1, -0.8, -0.2, -0.7]},
    {'Res': '120x80',
    'Mos': [-1.5, -1.3, -1.2, -1.15]}
    ]

for target_res_info in target_resolutions:
    target_res = target_res_info['Res']
    mos_scores = target_res_info['Mos']
    for i in range(len(durations)):
        duration = durations[i]
        mos = mos_scores[i] + 3 # paper uses range [-2,+2]
        segments = []
        current_time = 0
        base_res_used = True
        while current_time < video_length:
            segments.append(createVideoSegment(codec, bitrate, current_time, duration, base_resolution if base_res_used else target_res , base_framerate))
            current_time += duration
            base_res_used = not base_res_used
         
        # exec estimation
        input = {}
        input["O21"] = [1] # no audio
        input["I13"] = prepareI13(segments)
        # input["I23"] = prepareI23(stalls)
        input["IGen"] = prepareIGen('480x320', 40, 'mobile')

        results.append(runModel(input, mos))
#endregion Blur Flicker

#region Motion Flicker
target_framerates = [
    {'Fps': 15.0,
    'Mos': [0, .05, .15, .08]},
    {'Fps': 10.0,
    'Mos': [-.8, -.6, -.5, -.55]},
    {'Fps': 5.0,
    'Mos': [-1.25, -1.15, -1.1, -1.15]},
    {'Fps': 3.0,
    'Mos': [-1.45, -1.4, -1.4, -1.25]},
    ]

for target_fps_info in target_framerates:
    target_fps = target_fps_info['Fps']
    mos_scores = target_fps_info['Mos']
    for i in range(len(durations)):
        duration = durations[i]
        mos = mos_scores[i] + 3 # paper uses range [-2,+2]
        segments = []
        current_time = 0
        base_fps_used = True
        while current_time < video_length:
            segments.append(createVideoSegment(codec, bitrate, current_time, duration, base_resolution, base_framerate if base_fps_used else target_fps))
            current_time += duration
            base_fps_used = not base_fps_used
        

        # exec estimation
        input = {}
        input["O21"] = [1] # no audio
        input["I13"] = prepareI13(segments)
        # input["I23"] = prepareI23(stalls)
        input["IGen"] = prepareIGen('480x320', 50, 'mobile')

        results.append(runModel(input, mos))
#endregion Motion Flicker

# write json to file
with open(f'results/{output_file}.json', 'w') as file:
    file.write(json.dumps(results))