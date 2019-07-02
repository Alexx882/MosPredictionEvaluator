import json
import mos_calculation
import statistics

# Apply values from 'Flicker Effects in Adaptive Video Streaming to Handheld Devices'
output_file = 'result_acmmm2011-perception'

# they claim independence from video parameters, so choose appropriate ones
codec = 'h264'
base_framerate = 30.0
base_resolution = '480x320'
bitrate = 1000 # not defined, appropriate chosen
video_length = 12
info_IGen =  mos_calculation.prepareIGen('480x320', 50, 'mobile')

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
            segments.append(mos_calculation.createVideoSegment(codec, bitrate, current_time, duration, base_resolution if base_res_used else target_res , base_framerate))
            current_time += duration
            base_res_used = not base_res_used
         
        # exec estimation
        res = mos_calculation.runModelFromSegments(segments, None, info_IGen, mos)
        results.append(res)
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
            segments.append(mos_calculation.createVideoSegment(codec, bitrate, current_time, duration, base_resolution, base_framerate if base_fps_used else target_fps))
            current_time += duration
            base_fps_used = not base_fps_used
        

        # exec estimation
        res = mos_calculation.runModelFromSegments(segments, None, info_IGen, mos)
        results.append(res)
#endregion Motion Flicker

mos_calculation.writeJsonToFile(output_file, results)