import cv2
import numpy as np

# Initialize video capture
cap = cv2.VideoCapture('D:\Roxana\Movies\Adele - Oh My God (Official Video).mp4')
#cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # DirectShow
#cap = cv2.VideoCapture(0, cv2.CAP_MSMF)  # Media Foundation
#cap = cv2.VideoCapture(0, cv2.CAP_VFW)   # VFW (Video for Windows)

if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

# Get the properties of the original video
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define el códec y crea el objeto VideoWriter
output_file = 'output_video.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Usa 'XVID' para AVI o 'mp4v' para MP4
out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

# Capturar el primer frame como referencia
ret, reference_frame = cap.read()
if not ret:
    print("Error: Could not read the reference frame.")
    exit()

reference_gray = cv2.cvtColor(reference_frame, cv2.COLOR_BGR2GRAY)

while True: 
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_diff = cv2.absdiff(reference_gray, gray_frame)
    _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 500:
            x, y, w, h = cv2.boundingRect(contour)
            cx, cy = x + w // 2, y + h // 2
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

    out.write(frame)
    cv2.imshow('Video with motion detection', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Video saved as {output_file}")
