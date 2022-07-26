#Credit: face_recognition
import face_recognition
import cv2
import numpy as np

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)

matthew_image = face_recognition.load_image_file("photo/Volunteer.jpg")
matthew_face_encoding = face_recognition.face_encodings(matthew_image)[0]

ryan_image = face_recognition.load_image_file("photo/ryan.jpeg")
ryan_face_encoding = face_recognition.face_encodings(ryan_image)[0]

andrea_image = face_recognition.load_image_file("photo/andrea.jpg")
andrea_face_encoding = face_recognition.face_encodings(andrea_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    matthew_face_encoding,
    ryan_face_encoding,
    andrea_face_encoding
]
known_face_names = [
    "Volunteer",
    "Ryan Rivera",
    "Andrea Casassa Sian"
]


def recognition(frame, person_of_interest):


    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    poi_info=[[0,0],0,10] #[[center_x,center_y],face_area, confidence(not applied in this)]

    # Only process every other frame of video to save time
    if True:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=1.3, fy=1.3)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top //= 1.3
        right //= 1.3
        bottom //= 1.25
        left //= 1.25
        top = int(top)
        right = int(right)
        bottom = int(bottom)
        left = int(left)
        color = (150,150,150)
        
        # Save info of person of interest
        if name == person_of_interest:
            poi_info[0][0] = (left + right)//2
            poi_info[0][1] = (top + bottom)//2
            poi_info[1] = (left - right)*(top - bottom)
            color = (0,0,225)

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 10), (right, bottom), color, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)

    return frame, poi_info