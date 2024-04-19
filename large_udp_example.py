"""
Example of sending a webcam image using udp and showing it on receive
"""

import netpywork as networking
import cv2 as cv
import numpy as np

def server_receive(msg,proto,self):
    msg: networking.udp_msg = msg
    data = np.frombuffer(msg.data,dtype='uint8')
    final_frame = cv.imdecode(data,1)
    cv.imshow("Test",final_frame)
    cv.waitKey(1)

server = networking.server(12345)
server.on_receive = server_receive
server.run()

client = networking.client('127.0.0.1',12345)
client.connect()

webcam = cv.VideoCapture(0)
while True:
    try:
        res,frame = webcam.read()
        encode_param = [int(cv.IMWRITE_JPEG_QUALITY), 100]
        result, encimg = cv.imencode('.jpg', frame, encode_param)
        client.send(encimg.tobytes(),networking.protocol.UDP)
    except KeyboardInterrupt:
        print("Exiting...")
        client.close()
        server.close()
        break