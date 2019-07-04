import json
import mos_calculation

# Assume values from 'On subjective quality assessment of adaptive video streaming
# via crowdsourcing and laboratory based experiments' and partially from their previous 
# publication 'About Subjective Evaluation of Adaptive Video Streaming'
output_file = 'FULLTEXT01_bitrates_and_stalling'

codec = 'h264'
framerate = 24
resolution = '1280x720'
bitrates = {.6: 600,
    1: 1000,
    3: 3000,
    5: 5000
    }
segment_durations = [2, 10]
video_length = [14, 40]

info_IGen = mos_calculation.prepareIGen('1920x1080', 190)

def createVideoSegmentsFromRates(rates, duration):
    segments = []
    cur_dur = 0
    for r in rates:
        segments.append(mos_calculation.createVideoSegment(codec, bitrates[r], cur_dur, duration, resolution, framerate))
        cur_dur = cur_dur+duration
    return segments

results = []

## bitrate changes
# gradual decrease 5-3-1-0.6 Mbps
rates = [5,5,5,3,1,.6,.6]
segments = createVideoSegmentsFromRates(rates, duration=2)
results.append(mos_calculation.runModelFromSegments(segments, None, info_IGen, 3.45))

# rates = [5,3,1,.6]
# segments = createVideoSegmentsFromRates(rates, duration=10)
# results.append(mos_calculation.runModelFromSegments(segments, None, info_IGen, 3.45))

# rapid decrease 5-0.6 Mbps
rates = [5,5,5,5,.6,.6,.6]
segments = createVideoSegmentsFromRates(rates, duration=2)
results.append(mos_calculation.runModelFromSegments(segments, None, info_IGen, 3.3))

# rates = [5,5,.6,.6]
# segments = createVideoSegmentsFromRates(rates, duration=10)
# results.append(mos_calculation.runModelFromSegments(segments, None, info_IGen, 3.3))

def runModelForStaticBitrate(bitrate, expected):
    results = []
    results.append(
        mos_calculation.runModelFromSegments(
            [mos_calculation.createVideoSegment(codec, bitrates[.6], 0, video_length[0], resolution, framerate)]
            , None, info_IGen, expected)
        )
    # results.append(
    #     mos_calculation.runModelFromSegments(
    #         [mos_calculation.createVideoSegment(codec, bitrates[.6], 0, video_length[1], resolution, framerate)]
    #         , None, info_IGen, expected)
    #     )
    return results

# static .6, 1, 3, 5
results.extend(runModelForStaticBitrate(bitrates[.6], 3))

results.extend(runModelForStaticBitrate(bitrates[1], 3.35))

results.extend(runModelForStaticBitrate(bitrates[3], 4.15))

results.extend(runModelForStaticBitrate(bitrates[5], 4.2))

## stalling events
# 1x 2s freeze in 3mbps
segments = [mos_calculation.createVideoSegment(codec, bitrates[3], 0, video_length[0], resolution, framerate)]
stalls = [mos_calculation.createStallingSegment(0, 0), mos_calculation.createStallingSegment(video_length[0]/2, 2)]
results.append(mos_calculation.runModelFromSegments(segments, stalls, info_IGen, 3.05))

# 2x 1s freeze in 3mpbs
segments = [mos_calculation.createVideoSegment(codec, bitrates[3], 0, video_length[0], resolution, framerate)]
stalls = [mos_calculation.createStallingSegment(0, 0), 
    mos_calculation.createStallingSegment(video_length[0]/3, 1),
    mos_calculation.createStallingSegment(video_length[0]/3*2, 1)]
results.append(mos_calculation.runModelFromSegments(segments, stalls, info_IGen, 2.55))

# 1x 2s freeze in 1mpbs
segments = [mos_calculation.createVideoSegment(codec, bitrates[1], 0, video_length[0], resolution, framerate)]
stalls = [mos_calculation.createStallingSegment(0, 0), mos_calculation.createStallingSegment(video_length[0]/2, 2)]
results.append(mos_calculation.runModelFromSegments(segments, stalls, info_IGen, 2.3))

mos_calculation.writeJsonToFile(output_file, results)