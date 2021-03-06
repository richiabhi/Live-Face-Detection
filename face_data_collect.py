import cv2
import numpy as np

# Init Camera
cap = cv2.VideoCapture(0)

# Face Detection
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")

skip = 0
face_data = []
dataset_path = "./data/"

file_name = input("Enter the name of the Person : ")

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(frame, 1.3, 5)
    faces = sorted(faces, key=lambda f: f[2] * f[3])

    for face in faces[-1:]:
        x, y, w, h = face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

        # Extract region of interest : Crop
        offset = 10
        face_section = frame[y - offset:y + h +
                             offset, x - offset:x + w + offset]
        face_section = cv2.resize(face_section, (100, 100))
    skip += 1
    # Store every 10th face
    if skip % 10 == 0:
        # Store the 10th face later on
        face_data.append(face_section)
        print(len(face_data))

    cv2.imshow("Capture Frame", frame)
    cv2.imshow("Cropped", face_section)

    key_pressed = cv2.waitKey(1) & 0xFF
    if key_pressed == ord('q'):
        break

# CONVERSION OF face list into numpy array
face_data = np.array(face_data)
face_data = face_data.reshape((face_data.shape[0], -1))
print(face_data.shape)

# SAVE THIS DATA INTO FILE System
np.save(dataset_path + file_name + '.npy', face_data)
print("Data Sucessfully Saved at" + dataset_path + file_name + '.npy')

cap.release()
cv2.destroyAllWindows()
