#!/usr/bin/python3
# based on example python code:
# 

import os
import io
import random
import picamera

PROG_VER = "v0.0.1"
SCRIPT_PATH = os.path.abspath(__file__)
PROG_NAME = os.path.basename(SCRIPT_PATH)

# Parameters
VIDEO_RESOLUTION = (1280, 720)
LOOPTIME = 10   # seconds

# Globals
prior_image = None
motion_detected = False

###############################################################################

def detect_motion(camera):
    global prior_image
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg', use_video_port=True)
    stream.seek(0)

    if prior_image is None:
        prior_image = Image.open(stream)
        return False
    else:
        current_image = Image.open(stream)
        prior_image = current_image

        ###################################
        # Temporary random motion detection routine
        # Call function on two images
        result = random.randint(0, 10) == 0

        if motion_detected:
            if result:
                # if motion has already been detected, keep recording with 90% probability
                return True
            else:
                motion_detected = False
                return False

        if result:
            return False

        motion_detected = True
        return True


def circular_recording():
    """Record continuously with the camera. Save to disk on detected motion"""

    with picamera.PiCamera() as camera:
        camera.resolution = VIDEO_RESOLUTION
        stream = picamera.PiCameraCircularIO(camera, seconds=LOOPTIME)
        camera.start_recording(stream, format='h264')
        try:
            while True:
                camera.wait_recording(1)
                if detect_motion(camera):
                    print('Motion detected.')
                    camera.split_recording('after.h264')
                    stream.copy_to('before.h264', seconds=LOOPTIME)
                    stream.clear()
                    while detect_motion(camera):
                        camera.wait_recording(1)
                    print('Motion stopped.')
                    camera.split_recording(stream)
        finally:
            camera.stop_recording()


if __name__ == '__main__':
    count = 0
    print("INFO : Exit by pressing ctrl-c.")

    try:
        circular_recording()

    except KeyboardInterrupt:
        print("")
        print("INFO : User pressed ctrl-c")
        print("       Exiting {} {}".format(PROG_NAME, PROG_VER))

