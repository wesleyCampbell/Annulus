import socket
import time
import picamera

#camera setup
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15

#stream setup
stream_socket = socket.socket()
stream_socket.bind(('127.0.0.1', 8080))
stream_socket.listen(0)

connection = stream_socket.accept()[0].makefile('wb')

# video streaming inialization and termination

camera.start_recording(connection, format='h264')

try:
    while True:
        camera.wait_recording(1)
        
except KeyboardInterrupt:
    camera.stop_recording() 
    
finally:
    connection.close()
    stream_socket.close()
    print('connection terminated')

