import json
import mos_calculation

# Assume values from 'A Study on Quality of Experience for Adaptive Streaming Service'
output_file = 'result_06649320'

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
        segments.append(mos_calculation.createVideoSegment(codec, bitrates[r], cur_dur, segment_dur, resolution, framerate))
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
    res = mos_calculation.runModelFromSegments(seg[0], None, mos_calculation.prepareIGen(resolution, 80), seg[1])
    results.append(res)

mos_calculation.writeJsonToFile(output_file, results)