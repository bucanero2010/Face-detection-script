import cv2
import face_recognition
import kafka
import twilio
import os

KNOWN_FACES_DIR = 'known_faces'
FRAME_THICKNESS = 3
TOLERANCE = 0.6
FONT_THICKNESS = 2
MODEL = 'hog'
video = cv2.VideoCapture(0)
def color_gen(name):
    color = [(ord(c.lower()) - 97) * 8 for c in name[:3]]
    return color

print('Cargando personas conocidas')
known_faces = []
known_names = []
for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
        image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{name}/{filename}')
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(name)

print('Iniciando camara')
while True:
    ret, image = video.read()
    locations = face_recognition.face_locations(image, model=MODEL)
    encodings = face_recognition.face_encodings(image, locations)
    for face_encoding, face_location in zip(encodings, locations):
        results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
        match = None
        if True in results:
            match = known_names[results.index(True)]
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])
            color = color_gen(match)
            cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)
            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2] + 22)
            cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
            cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (200, 200, 200), FONT_THICKNESS)

    cv2.imshow(filename, image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break