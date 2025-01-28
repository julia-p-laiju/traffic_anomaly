import torch
import cv2


model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  


ROAD_CLASSES = ['road']

def detect_road(frame):
    """Detect if a road exists in the given frame."""
    results = model(frame)
    detections = results.pandas().xyxy[0]  
    
    for _, row in detections.iterrows():
        class_name = row['name']
        if class_name in ROAD_CLASSES:
            return True  
    return False 

def generate_realtime_frames():
    """Generate real-time video frames from the laptop camera."""
    cap = cv2.VideoCapture(0)  
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        road_found = detect_road(frame)
        if road_found:
            label = "Road Found"
            color = (0, 255, 0)  
        else:
            label = "No Road Found"
            color = (0, 0, 255)  
        
        
        cv2.putText(frame, label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
       
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
