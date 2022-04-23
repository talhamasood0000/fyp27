import cv2
import math

import mediapipe as mp
import time

from fyp.models import VideoOutput
from django.core.files.base import ContentFile

class FaceDetector():
    def __init__(self, minDetectionCon=0.5):

        self.minDetectionCon = minDetectionCon

        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils

        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)

    def findFaces(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        bboxs = [0]
        c: int = 0
        if self.results.detections:
            c: int = 0
            for id, detection in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                       int(bboxC.width * iw), int(bboxC.height * ih)
                bboxs.append([id, bbox, detection.score])
                if draw:
                    img = self.fancyDraw(img, bbox)
                    cv2.putText(img, f'{int(detection.score[0] * 100)}%',
                                (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2)
                    c = c + 1
                    cv2.putText(img, f'People: {c}', (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                    cv2.putText(img, f'Time: {time.asctime(time.localtime(time.time()))}', (250, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

        return img, bboxs, c

def detect_people(video):
    # VIDEO_PATH=r'C:\Users\Talha Masood\Downloads\check1.mp4'
    VIDEO_PATH='media/'+video.videofile.name
    TIME_IN_FPS=25*60*5
    cap = cv2.VideoCapture(VIDEO_PATH)
    detector = FaceDetector()
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = math.ceil(cap.get(cv2.CAP_PROP_FPS))

    frameNumber=TIME_IN_FPS
    while frameNumber >= 0 and frameNumber <= total_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES,frameNumber)
        ret, frame = cap.read()
        if ret:
            # cv2.imshow("Image", frame)
            img_with_detections, bboxs, c = detector.findFaces(frame, False)
        
            output_time_sec=frameNumber/fps
            output_time_sec=output_time_sec % (24 * 3600)
            output_time_hr = output_time_sec // 3600
            output_time_sec %= 3600
            output_time_min = output_time_sec // 60
            output_time_sec %= 60
        
            print(f'Total persons detected: {c}')
            
            ret, buf=cv2.imencode('.jpg',img_with_detections)

            record=VideoOutput(video=video,
                total_detected_card=c,
            detected_time=str(output_time_hr)+":"+str(output_time_min)+":"+str(output_time_sec))
            record.detected_image.save(f'car_detected_{frameNumber}.jpg',ContentFile(buf.tobytes()))
            record.save()
        frameNumber=frameNumber+TIME_IN_FPS
    cv2.waitKey(0) 
    cap.release()
    cv2.destroyAllWindows() 
