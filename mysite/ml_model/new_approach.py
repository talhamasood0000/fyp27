import tensorflow as tf
import cv2
import numpy as np
import math
from fyp.models import VideoOutput

def detect_video(VIDEO_PATH,detect_fn):
    MIN_CONF_THRESH = float(0.95)
    TIME_IN_FPS=25*3

    cap = cv2.VideoCapture(VIDEO_PATH)
    width = cap. get(cv2. CAP_PROP_FRAME_WIDTH )
    height = cap. get(cv2. CAP_PROP_FRAME_HEIGHT )
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = math.ceil(cap.get(cv2.CAP_PROP_FPS))
    total_time=int(total_frames/fps)


    frameNumber=TIME_IN_FPS
    while frameNumber >= 0 and frameNumber <= total_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES,frameNumber)
    
        ret, frame = cap.read()
        if ret:
            input_tensor = tf.convert_to_tensor(frame)
            input_tensor = input_tensor[tf.newaxis, ...]
            detections = detect_fn(input_tensor)

            num_detections = int(detections.pop('num_detections'))

            detections = {key: value[0, :num_detections].numpy()
               for key, value in detections.items()}
            detections['num_detections'] = num_detections
            detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
            image_with_detections = frame.copy()
            img_hei,img_wid,c = image_with_detections.shape

            for i in range(detections['detection_boxes'].shape[0]):
                if detections['detection_scores'][i] > MIN_CONF_THRESH: 
                    c=int(detections['detection_scores'][i]*100)
                    ymin, xmax, ymax, xmin=detections['detection_boxes'][i]
                    (right, left, top, bottom) = (xmin*img_wid, xmax*img_wid, ymin*img_hei, ymax*img_hei)
                    right, left, top, bottom = int(right), int(left), int(top), int(bottom)
                    image_with_detections = cv2.rectangle(image_with_detections, (left,top) ,(right, bottom),(36,255,12),4)
                    (w, h), _ = cv2.getTextSize(f'car: {c}%', cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                    image_with_detections=cv2.rectangle(image_with_detections, (left,top) ,(left+w, top-h-5),(36,255,12),-1)
                    image_with_detections = cv2.putText(image_with_detections, f'car: {c}%', (left, top - 5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,30,0), 2)

            total_cars_detected=(detections['detection_scores'] > MIN_CONF_THRESH).sum()
        
            output_time_sec=frameNumber/fps
            output_time_sec=output_time_sec % (24 * 3600)
            output_time_hr = output_time_sec // 3600
            output_time_sec %= 3600
            output_time_min = output_time_sec // 60
            output_time_sec %= 60
        
            # print(f'{output_time_hr}:{output_time_min}:{output_time_sec:.2f}')
            print(f'Total cars detected: {total_cars_detected}')
            # cv2.imwrite(f'output/car_detected_{frameNumber}.jpg',image_with_detections)
            record=VideoOutput(total_detected_card=total_cars_detected,
            detected_time=output_time_hr+":"+output_time_min+":"+output_time_sec,
            detected_image=image_with_detections)
        frameNumber=frameNumber+TIME_IN_FPS
    cv2.waitKey(0) 
    cap.release()
    cv2.destroyAllWindows() 
