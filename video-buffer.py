#!/usr/bin/python3
import os
import io
import random
import picamera

PROG_VER = "v0.0.1"
SCRIPT_PATH = os.path.abspath(__file__)
PROG_NAME = os.path.basename(SCRIPT_PATH)

camera = picamera.PiCamera()
stream = picamera.PiCameraCircularIO(camera, seconds = 60)
camera.start_recording(stream, format='h264')

def motion_detected():
    """ Randomly detect motion"""
    return random.randint(0,10) == 0

if __name__ == '__main__':
    count = 0
    try:
        while True:
            camera.wait_recording(1)
            if motion_detected():
                # Keep recording for 10 seconds and only then write the stream to disk.
                camera.wait_recording(30)
                stream.copy_to('modion_{}.h264'.format(count))
                count = count + 1

    except KeyboardInterrupt:
        print("")
        print("INFO : User pressed ctrl-c")
        print("       Exiting {} {}".format(PROG_NAME, PROG_VER))

    finally: 
        camera.stop_recording()
