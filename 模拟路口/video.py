import time

import cv2
import threading

class Video():
    def __init__(self):
        self.runing = False
        self.stop = True
        self.path = None
    def start_video(self,path):
        if not self.runing:
            self.path = path
            self.stop = False
            self.runing = True
            self.thread = threading.Thread(target=self.run)
            self.thread.start()
    def stop_video(self):
        self.stop = True
        self.runing = False
        time.sleep(0.1)

    def run(self):
        cap = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print("width:",width, "height:", height)
        out = cv2.VideoWriter(self.path,fourcc, 20.0, (width, height),True)

        while (not self.stop):
            ret, frame = cap.read()
            out.write(frame)
        out.release()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    v = Video()
    v.start_video('static/movies/t1.mp4')
    time.sleep(3)
    v.stop_video()
    v.start_video('static/movies/t2.mp4')
    time.sleep(3)
    v.stop_video()