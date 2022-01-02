import cv2
import os
def main():

    x=os.getcwd()
    dir=x[:-4]
    cam = cv2.VideoCapture(0)
    detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    Id="user"
    sampleNum=0
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

            #incrementing sample number
            sampleNum=sampleNum+1
            #saving the captured face in the dataset folder
            #print(str(dir)+"/dataset/"+str(Id) + ".jpg")
            cv2.imwrite(str(dir)+"/dataset/"+str(Id) + ".jpg", gray[y:y+h,x:x+w])

            cv2.imshow('frame',img)
        #wait for 100 miliseconds
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break
        # break if the sample number is morethan 1
        elif sampleNum > 1:
            break
    cam.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()
