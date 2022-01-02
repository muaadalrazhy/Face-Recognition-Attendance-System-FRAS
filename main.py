import face_recognition
import cv2
import os
import datetime
import mysql.connector

def main():

    x=os.getcwd()
    dir=x[:-4]
    # Define the database.
    myDatabase = mysql.connector.connect (
        host="localhost",
        user="root",
        passwd="123456",
        database="FRAS"
    )
    mycursor = myDatabase.cursor()

    data = []

    for root, dirs, files in os.walk(str(dir)+"/dataset"):
        for filename in files:
            data.append(str(dir)+"/dataset/"+str(filename))

    video_capture = cv2.VideoCapture(0)
    load_image = []
    load_face_recognition = []
    our_data = [] #known_face_encodings
    our_name = [] #known_name_encodings

    for img in data :
        x = face_recognition.load_image_file(str(img))
        y = face_recognition.face_encodings(x)[0]
        our_data.append(y)
        our_name.append(img[71:len(img)-4])

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    checked_in = []

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(our_data, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = our_name[first_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            if(name in checked_in):
                continue
            elif (name not in checked_in) :
                #print(name)
                checked_in.append(name)
                # Insert the data to the attendace database.
                Timing = datetime.datetime.now()
                val = (name, Timing.strftime("%Y-%m-%d"), Timing.strftime("%H:%M"))
                sql = "INSERT INTO Attendance (ID, Check_Date, Check_Time) VALUES (%s, %s, %s)"
                if name!="Unknown":
                    mycursor.execute(sql,val)
                    myDatabase.commit()
                    #print(name + " Checked in ")
                # print(datetime.datetime.now())

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
