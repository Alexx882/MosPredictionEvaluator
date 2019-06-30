import json

STREAM_ID = 42

def prepareI11():
    '''Prepares I.11 aka audio'''
    segments = [
        createAudioSegment('aaclc',331,1,5.48)
    ]
    return {'streamId': STREAM_ID, 'segments': segments}

def createAudioSegment(codec, bitrate, start, duration):
    return {
        'codec': codec,
        'bitrate': bitrate,
        'start': start, 
        'duration': duration
    }

def prepareI13():
    '''Prepares I.13 aka video'''
    segments = [
        createVideoSegment('h264', 690, 1, 5.48, '1920x1080', 25.0)
    ]
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

def prepareI23():
    '''Prepares I.14 aka stalling, here called I.23'''
    segments = [
         createStallingSegment(0, 1)
    ]
    return {'streamId': STREAM_ID, 'stalling': segments}
    
def createStallingSegment(start, duration):
    return [start, duration]

def prepareIGen():
    '''Prepares device information'''
    return {
        "displaySize": "1920x1080",
        "device": "pc",
        "viewingDistance": '150cm'
    }


input = {}
input["I11"] = prepareI11()
input["I13"] = prepareI13()
input["I23"] = prepareI23()
input["IGen"] = prepareIGen()

# write json to file
with open('input.json', 'w') as file:
    file.write(json.dumps(input))


from itu_p1203 import P1203Standalone
# create model ...
itu_p1203 = P1203Standalone(input)
# ... and run it
output = itu_p1203.calculate_complete(False)
print("Final MOS Score: " + str(output['O46']))