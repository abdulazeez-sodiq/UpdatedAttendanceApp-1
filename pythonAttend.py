import pickle
from typing_extensions import IntVar
import cv2
import numpy as np
import os
from datetime import datetime
import dateutil 
import face_recognition
import serial
import time
import MAINAPP.views


serialcomm=serial.Serial()
class program():
    def __init__(self):
        pass

    def initiate():
        serialcomm=serial.Serial('COM10',115200)
        serialcomm.timeout=1
        serialcomm.close()
        serialcomm.open()
        Continue=False
        while(Continue==False):
            inbyte=serialcomm.readline().decode()
            mess=inbyte.strip()
            if mess == 'Are you there':
                message='Am here'
                serialcomm.write(message.encode())
                Continue=True
        now = datetime.now()
        dateString = now.strftime('%B %d, %Y')
        year = int(now.strftime('%Y'))
        month = (now.strftime('%B'))
        day = int(now.strftime('%d'))
        meridian = now.strftime('%p')
        #print(f'date={meridian}')
        #print(f'year={year}')
        #print(f'month={month}')
        #print(f'day={day}')

        #creating initial file path
        path = r'C:\Users\Abdulsalam Hauwa\Documents\Python\Attendance System Using Face Recognition\image_folder'
        #url='http://192.168.231.162/cam-hi.jpg'
        ##'''cam.bmp / cam-lo.jpg /cam-hi.jpg / cam.mjpeg '''
        parent_directory=r'C:\Users\Abdulsalam Hauwa\Documents\ATTENDANCE RECORD' + "\\" + str(year) + "\\" + month + "\\"
        os.makedirs(parent_directory, exist_ok=True)
        csv_file_name="Attendance for " + str(dateString)
        extention='.csv'
        #print(parent_directory)
        with open(parent_directory+"\\"+"Attendance for " + str(dateString) + ".csv", 'w+') as f:
            f.write("S/N,NAMES,TIME OF ENTRY")   
        f.close()
        print('Done creating first .csv file')
        print('Booting...')

        #initializing storage variable
        images = []
        classNames = []
        Encodedlist=[]
        new_pictures=[]
        new_pictures_names=[]
        FormerEncodedlist=[]
        FormerPictureslist=[]
        myList=[]
        #Retrieving data from formerly saved .txt file
        with open('Encoded List.pkl', 'rb') as buffer:
            FormerEncodedlist=pickle.load(buffer)
        #print(FormerEncodedlist)

        with open('Picture List.pkl', 'rb') as buffer:
            FormerPictureslist=pickle.load(buffer)
        #print(FormerPictureslist)

        myList = os.listdir(path)
        #print(myList)

        #saving myList in Picture list.txt file
        with open('Picture List.pkl', 'wb') as buffer:
            pickle.dump(myList,buffer,protocol=pickle.HIGHEST_PROTOCOL) 
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        #print('Full class names:')
        #print(classNames)

        #getting new images saved in the directory
        New=False
        new_pictures=[item for item in FormerPictureslist if item not in myList]
        print(new_pictures)
        if new_pictures != []:
            New=True
            new_images=[]
            new_classNames=[]
            for newPic in new_pictures:
                curImg = cv2.imread(f'{path}/{newPic}')
                new_images.append(curImg)
                new_classNames.append(os.path.splitext(cl)[0])
            print('New class names:')
            print(new_classNames)

        
        
        def findEncodings(images):
            message='Updating face list\n'
            serialcomm.write(message.encode())
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            with open('Encoded List.pkl', 'wb') as buffer:
                pickle.dump(encodeList,buffer,protocol=pickle.HIGHEST_PROTOCOL)
            print('Done creating .csv file')
            message='Face list Updated\n'
            serialcomm.write(message.encode())
            return encodeList
        
        if FormerEncodedlist == []:
            encodeListKnown = findEncodings(images)
            print('Encoding Complete')
        else:
            pass
        if New==True:
            encodeListKnown=FormerEncodedlist
            newEncodeList=findEncodings(new_images)
            encodeListKnown=encodeListKnown+newEncodeList
        
        def markAttendance(names,file_name,parent_dir,Serial_number):
            newSerialNo=0
            with open(parent_dir+file_name+".csv", 'r+') as f:
                myDataList = f.readlines()
                nameList = []
                for line in myDataList:
                    entry = line.split(',')
                    nameList.append(entry[1].upper())
                f.close()
                newSerialNo=int(Serial_number)

            if names not in nameList:
                with open(parent_dir+file_name+".csv", 'a+') as f:
                    now = datetime.now()
                    dtString = now.strftime('%H:%M:%S %p')
                    f.writelines('\n'+str(Serial_number)+f',{names},{dtString}')
                    print('Done writing to .csv file')
                    newSerialNo=int(Serial_number)+1
                    message=names
                    serialcomm.write(message.encode())
            return newSerialNo

    def go():
        print("am in")
        serialcomm=serial.Serial('COM10',115200)
        serialcomm.timeout=1
        Continue=False
        serialcomm.close()
        serialcomm.open()
        while(Continue==False):
            inbyte=serialcomm.readline().decode()
            mess=inbyte.strip()
            if mess == 'Are you there':
                message='Am here'
                serialcomm.write(message.encode())
                Continue=True
        now = datetime.now()
        # tz=tz.tzlocal()
        dateString = now.strftime('%B %d, %Y')
        year = int(now.strftime('%Y'))
        month = (now.strftime('%B'))
        day = int(now.strftime('%d'))
        meridian = now.strftime('%p')
        #print(f'date={meridian}')
        #print(f'year={year}')
        #print(f'month={month}')
        #print(f'day={day}')

        #creating initial file path
        path = r'C:\Users\Abdulsalam Hauwa\Documents\Python\Attendance System Using Face Recognition\image_folder'
        #url='http://192.168.231.162/cam-hi.jpg'
        ##'''cam.bmp / cam-lo.jpg /cam-hi.jpg / cam.mjpeg '''
        parent_directory=r'C:\Users\Abdulsalam Hauwa\Documents\ATTENDANCE RECORD' + "\\" + str(year) + "\\" + month + "\\"
        os.makedirs(parent_directory, exist_ok=True)
        csv_file_name="Attendance for " + str(dateString)
        extention='.csv'
        #print(parent_directory)
        with open(parent_directory+"\\"+"Attendance for " + str(dateString) + ".csv", 'w+') as f:
            f.write("S/N,NAMES,TIME OF ENTRY")   
        f.close()
        print('Done creating first .csv file')
        print('Booting...')

        #initializing storage variable
        images = []
        classNames = []
        Encodedlist=[]
        new_pictures=[]
        new_pictures_names=[]
        FormerEncodedlist=[]
        FormerPictureslist=[]
        #Retrieving data from formerly saved .txt file
        with open('Encoded List.pkl', 'rb') as buffer:
            FormerEncodedlist=pickle.load(buffer)
        #print(FormerEncodedlist)

        with open('Picture List.pkl', 'rb') as buffer:
            FormerPictureslist=pickle.load(buffer)
        #print(FormerPictureslist)

        myList = os.listdir(path)
        #print(myList)

        #saving myList in Picture list.txt file
        with open('Picture List.pkl', 'wb') as buffer:
            pickle.dump(myList,buffer,protocol=pickle.HIGHEST_PROTOCOL) 
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        #print('Full class names:')
        #print(classNames)

        #getting new images saved in the directory
        New=False
        new_pictures=[item for item in FormerPictureslist if item not in myList]
        print(new_pictures)
        if new_pictures != []:
            New=True
            new_images=[]
            new_classNames=[]
            for newPic in new_pictures:
                curImg = cv2.imread(f'{path}/{newPic}')
                new_images.append(curImg)
                new_classNames.append(os.path.splitext(cl)[0])
            print('New class names:')
            print(new_classNames)

        
        
        def findEncodings(images):
            message='Updating face list\n'
            serialcomm.write(message.encode())
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            with open('Encoded List.pkl', 'wb') as buffer:
                pickle.dump(encodeList,buffer,protocol=pickle.HIGHEST_PROTOCOL)
            print('Done creating .csv file')
            message='Face list Updated\n'
            serialcomm.write(message.encode())
            return encodeList
        
        if FormerEncodedlist == []:
            encodeListKnown = findEncodings(images)
            print('Encoding Complete')
        else:
            pass
        if New==True:
            encodeListKnown=FormerEncodedlist
            newEncodeList=findEncodings(new_images)
            encodeListKnown=encodeListKnown+newEncodeList
        
        def markAttendance(names,file_name,parent_dir,Serial_number):
            newSerialNo=0
            with open(parent_dir+file_name+".csv", 'r+') as f:
                myDataList = f.readlines()
                nameList = []
                for line in myDataList:
                    entry = line.split(',')
                    nameList.append(entry[1].upper())
                f.close()
                newSerialNo=int(Serial_number)

            if names not in nameList:
                with open(parent_dir+file_name+".csv", 'a+') as f:
                    now = datetime.now()
                    dtString = now.strftime('%H:%M:%S %p')
                    f.writelines('\n'+str(Serial_number)+f',{names},{dtString}')
                    print('Done writing to .csv file')
                    newSerialNo=int(Serial_number)+1
                    message=names
                    serialcomm.write(message.encode())
            return newSerialNo
        
        #Getting frames from the webcam 
        cap=cv2.VideoCapture(0)
        SerialNo=1
        former_picture_list=[]
        f_day=day
        encodeListKnown=FormerEncodedlist
        go_on=False
        print('Booting completed')
        while True:
            now = datetime.now()
            # tz=tz.tzlocal()
            dateString = now.strftime('%B %d, %Y')
            dtString = now.strftime('%H:%M:%S %p')
            year = int(now.strftime('%Y'))
            month = (now.strftime('%B'))
            day = int(now.strftime('%d'))
            meridian = now.strftime('%p')
            
            parent_directory=r'C:\Users\Abdulsalam Hauwa\Documents\ATTENDANCE RECORD' + "\\" + str(year) + "\\" + month + "\\"
            os.makedirs(parent_directory, exist_ok=True)

            if f_day != day:
                SerialNo=1
                csv_file_name="Attendance for " + str(dateString)
                extention='.csv'
                with open(parent_directory+"\\"+"Attendance for " + str(dateString) + ".csv", 'w+') as f:
                    f.write("S/N,NAMES,TIME OF ENTRY")   
                f.close()
                print('Attendance.csv file has been updated')
            
            
            inbyte=serialcomm.readline().decode()
            mess=inbyte.strip()
            print(mess)
            if mess== 'Present':
                Ignore, img = cap.read()
                #img_resp=urllib.request.urlopen(url)
                #imgnp=np.array(bytearray(img_resp.read()),dtype=np.uint8)
                #img=cv2.imdecode(imgnp,-1)
                #img = captureScreen()
                imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                facesCurFrame = face_recognition.face_locations(imgS)
                encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
                #print(facesCurFrame)
                if facesCurFrame ==[]:
                    message='no face\n'
                    serialcomm.write(message.encode())
            
                SerialNo2=0
                for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace) 
                    #print(faceDis)
                    matchIndex = np.argmin(faceDis)
        
                    if matches[matchIndex]:
                        name = classNames[matchIndex].upper()
                        print('>>>'+name+'         '+dtString)
                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = int(y1 - 10), int(x2 + 10), int(y2 + 10), int(x1 - 10)
                        #print(f'the value of x1, x2, y1, y2 are {x1}, {x2}, {y1}, {y2} respectively')
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(img, (x1, y2), (x2+150, y2+40), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, name, (x1 + 4, y2 + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (125, 0, 125), 2)
                        SerialNo2=markAttendance(name,csv_file_name,parent_directory,SerialNo)
                        if SerialNo == SerialNo2:
                            #not working
                            #the code sends an empty string for already present faces
                            message='User Already Present\n'
                            serialcomm.write(message.encode())
                            time.sleep(0.5)
                        SerialNo=SerialNo2
                        #print('rectangle done')
                    else:
                        message='Face does not exist\n'
                        serialcomm.write(message.encode())
                facesCurFrame = face_recognition.face_locations(imgS)
                encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
                #print('encoders done')
                cv2.imshow('Webcam', img)
            print('>>>')
            #Dealing with newly saved images
            display_new_class_names=False
            encode_new_pictures=False
            with open('Encoded List.pkl', 'rb') as buffer:
                FormerEncodedlist=pickle.load(buffer)
            with open('Picture List.pkl', 'rb') as buffer:
                FormerPictureslist=pickle.load(buffer)
            myList = os.listdir(path)
            #print('Present pictures in'+ path +"are :")
            #print(myList)
            if myList != former_picture_list:
                with open('Picture List.pkl', 'wb') as buffer:
                    pickle.dump(FormerPictureslist,buffer,protocol=pickle.HIGHEST_PROTOCOL)
                new_pictures=[item for item in myList if item not in FormerPictureslist]
                new_images=[]
                new_classNames=[]
                for newPic in new_pictures:
                    curImg = cv2.imread(f'{path}/{newPic}')
                    new_images.append(curImg)
                    new_classNames.append(os.path.splitext(cl)[0])
                    display_new_class_names=True
                if display_new_class_names == True:
                    #print('New class names in'+path+'are :')
                    #print(new_classNames)
                    display_new_class_names=False
                    encode_new_pictures=True
                if encode_new_pictures == True:
                    encodeListKnown=FormerEncodedlist
                    newEncodeList=findEncodings(new_images)
                    encodeListKnown=encodeListKnown+newEncodeList
                    print('Done updating Encoded list.pkl file')
                    encode_new_pictures=False
            
            former_picture_list=myList
            f_day=day         
            #cv2.imshow('Webcam', img)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break
        serialcomm.close()
        cv2.destroyAllWindows()
        cv2.imread


    def destroy():
        serialcomm.close()
        cv2.destroyAllWindows()
        cv2.imread