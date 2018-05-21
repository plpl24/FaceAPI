import io
import time
import threading
import picamera
import numpy as np
import cv2

# Create a pool of image processors
done = False
lock = threading.Lock()
pool = []

cascade_path = "haarcascade_frontalface_default.xml"


class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()
        self.cascade = cv2.CascadeClassifier(cascade_path)

    def run(self):
        # This method runs in a separate thread
        global done
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    self.stream.seek(0)
                    data = np.fromstring(self.stream.getvalue(), dtype=np.uint8)  # numpyの配列に変換
                    image = cv2.imdecode(data, 1)

                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    facerect = self.cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(50, 50),
                                                             maxSize=(200, 200))
                    if facerect:
                        print("detect")

                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the pool
                    with lock:
                        pool.append(self)


def streams():
    while not done:
        with lock:
            if pool:
                processor = pool.pop()
            else:
                processor = None
        if processor:
            yield processor.stream
            processor.event.set()
        else:
            # When the pool is starved, wait a while for it to refill
            time.sleep(0.1)


with picamera.PiCamera() as camera:
    pool = [ImageProcessor() for i in range(10)]
    camera.resolution = (640, 480)
    camera.framerate = 30
    camera.start_preview()
    time.sleep(2)
    camera.capture_sequence(streams(), use_video_port=True)

# Shut down the processors in an orderly fashion
while pool:
    with lock:
        processor = pool.pop()
    processor.terminated = True
    processor.join()
