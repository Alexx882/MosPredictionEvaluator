import json
import mos_calculation
import statistics

# Copy values from 'Cross-Dimensional Perceptual Quality Assessment for Low Bit-Rate Videos'
output_file = '04660307_constant'

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

info_IGen = mos_calculation.prepareIGen('1760x1440', 120)

##region prepare individual results with multiple MOS per M0 info
# prepared_input_segments = []
# for values in rates:
#     segments = [mos_calculation.createVideoSegment(codec, values['Bitrate'], 0, 10, resolution, values['Framerate'])]
#     prepared_input_segments.append([segments, values['MOS']])

# # exec all estimations
# results = []
# for seg in prepared_input_segments:
#     res = mos_calculation.runModelFromSegments(seg[0], None, info_IGen, seg[1])
#     results.append(res)

# mos_calculation.writeJsonToFile(f'{output_file}', results)
##endregion

##region prepare results with average mos and calculate again
prepared_input_segments = []

all_rates = [[30,128],[15,128],[30,384],[15,64],[7.5,64],[7.5,128]]
for (f, b) in all_rates:
    avg_mos_lst = [x['MOS'] for x in rates if x['Framerate'] == f and x['Bitrate'] == b]
    assert len(avg_mos_lst) == 5, 'not all videos have framerate and bitrate'
    prepared_input_segments.append([[mos_calculation.createVideoSegment(codec, b, 0, 10, resolution, f)], statistics.mean(avg_mos_lst)])

# exec all estimations
results = []
for seg in prepared_input_segments:
    res = mos_calculation.runModelFromSegments(seg[0], None, info_IGen, seg[1])
    results.append(res)

mos_calculation.writeJsonToFile(f'{output_file}_avg', results)
##endregion