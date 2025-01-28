import torch
import cv2
import numpy as np
from incident_alerts import send_alert_email

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

video_path = "static/sample_video.mp4"
cap = cv2.VideoCapture(video_path)

ALLOWED_CLASSES = ['car', 'bus', 'truck', 'motorbike', 'person', 'bicycle']
MIN_CONFIDENCE = 0.5
anomaly_count = 0

def detect_anomalies(frame):
    global anomaly_count
    results = model(frame)
    detections = results.pandas().xyxy[0]

    for _, row in detections.iterrows():
        confidence = row['confidence']
        if confidence < MIN_CONFIDENCE:
            continue

        class_name = row['name']
        x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])

        if class_name in ALLOWED_CLASSES:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            anomaly_count += 1
            anomaly_image_path = f"static/anomaly_{anomaly_count}.jpg"
            cv2.imwrite(anomaly_image_path, frame[y1:y2, x1:x2])
            send_alert_email(f"Anomaly: {class_name}", anomaly_image_path)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, f"Anomaly: {class_name}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    return frame

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = detect_anomalies(frame)
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
