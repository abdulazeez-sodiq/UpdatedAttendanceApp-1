from decimal import InvalidOperation
from operator import is_, length_hint
from tokenize import Name
from turtle import clear
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
import serial
import pythonAttend

import pickle
from typing_extensions import IntVar
import cv2
import numpy as np
import os
from datetime import datetime
import face_recognition
import serial
import time


global fullnamedel
global showsuccess
global processStatus
global connectionStatus
global availableIDtoDelete
global nametodelete
nametodelete=''
showsuccess=''
processStatus=''
connectionStatus=''
availableIDtoDelete=[]



# Create your views here.
def home(request):
    global showsuccess
    global processStatus
    global connectionStatus
    showsuccess=''
    processStatus=''
    connectionStatus=''
    return render(request, "MAINAPP/signin.html")

def terminal(request):
    global showsuccess
    global processStatus
    global connectionStatus
    return render(request, "MAINAPP/terminal.html", {'connectionStatus': connectionStatus,
                             'processStatus': processStatus})

def about(request):
    return render(request, "MAINAPP/about.html")

def about2(request):
    return render(request, "MAINAPP/about2.html")

def signup(request):
    global showsuccess
    global Fn

    # new_field=FIRMNAME.objects.all()
    # new_field.delete()

    if request.method == "POST":
        #you can also get the variables using this method also...
        firmName = request.POST['firmName']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['password2']
        agree = request.POST['Agree']
        knowStatus = request.POST['floatingSelect']


        Fn=firmName
        username= firmName

        if pass1 != pass2:
            messages.warning(request, 'Password does not match')
            return redirect('signup')

        is_found=False
        new_field=FIRM.objects.all()
        for names in new_field:
            temp_name=new_field.get(Name=names)
            if temp_name.Name.lower() == firmName.lower():
                is_found=True
                break

        if is_found == True:
            messages.warning(request, "Name already exist!")
            return redirect('signup')



        is_found=False
        new_field=FIRM.objects.all()
        for names in new_field:
            temp_email=new_field.get(Name=names)
            if temp_email.Email.lower() == email.lower():
                is_found=True
                break

        if is_found == True:
            messages.warning(request, "Email already used!")
            return redirect('signup')
        

        new_field=FIRM(Name=Fn, Email=email, HowYouKnowUs=knowStatus, Agree=agree, ConnectionStatus=processStatus)
        new_field.save()


        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()

        showsuccess = 'warning'
        messages.success(request, "Your account has been sucessfully created")

        return redirect('signin')


    return render(request, "MAINAPP/signup.html")

def signin(request):
    global showsuccess
    global firmName
    global showsuccess
    global processStatus
    global connectionStatus
    global email

    if request.method == "POST":
        email = request.POST['email']
        pass1 = request.POST['password']

        is_found=False
        new_field=FIRM.objects.all()

        for names in new_field:
            temp_name=new_field.get(Name=names)
            if temp_name.Email.lower() == email.lower():
                is_found=True
                break
        if is_found==True:
            new_field=FIRM.objects.get(Email=email)
            firmName=new_field.Name
        else:
            messages.warning(request, "Invalid login credentials!")
            return redirect('signin')

        user = authenticate(username=firmName, password=pass1)

        if user is not None:
            login(request, user)
            # global fname
            # global lname
            
            # fname = user.first_name
            # lname = user.last_name
            email = user.email
            firmName = user.username

            is_found=False
            new_field=FIRM.objects.all()

            for names in new_field:
                temp_name=new_field.get(Name=names)
                if temp_name.Email.lower() == email.lower():
                    is_found=True
                    break

            if is_found == True:
                new_field=FIRM.objects.get(Name=firmName)
                processStatus= new_field.ConnectionStatus

                return redirect('dashboard')

            elif is_found == False:
                return redirect('dashboardadmin')

        else:
            showsuccess = 'warning'
            messages.warning(request, "Invalid login credentials!")
            return redirect('signin')

    return render(request, "MAINAPP/signin.html")     

def signout(request):
    if connectionStatus == 'connected':
        messages.warning(request, 'Your Device is still connected')
        return redirect('terminal')
    messages.success(request, "Logged out sucessful")
    return redirect('Welcome Page')

def dashboard(request):
    # global fname
    # global lname
    global firmName
    global email
    global registeredstaff
    global Fn
    Fn = firmName

    user = FIRM.objects.get(Email=email)
    staffs=user.staff_set.all()

    counter=0
    for i in staffs:
        t=i
        counter=counter+1

    registeredstaff=counter
    presentstaff=0
    absentstaff=registeredstaff-presentstaff
    return render(request, "MAINAPP/dashboard.html", {'firmName': firmName, 'email': email, 'registeredstaff':registeredstaff,
                        'absentstaff':absentstaff, 'presentstaff': presentstaff})

def dashboardadmin(request):
    # global fname
    # global lname
    global firmName
    global email
    global registeredstaff
    global Fn
    Fn = firmName

    totaluser = FIRM.objects.count()

    # counter=0
    # for i in staffs:
    #     t=i
    #     counter=counter+1

    registeredstaff=0
    presentstaff=0
    absentstaff=registeredstaff-presentstaff
    return render(request, "MAINAPP/dashboardadmin.html", {'firmName': firmName, 'email': email, 'registeredstaff':registeredstaff,
                        'absentstaff':absentstaff, 'presentstaff': presentstaff, 'totaluser':totaluser})

def showpresentstaffs(request):
    presentkeys=['adewale sodie']
    presentvalues=[3]
    serialnumber=[1]
    return render(request, "MAINAPP/showpresentstaffs.html", {'presentkeys': presentkeys, 'presentvalues':presentvalues, 'serialnumber': serialnumber})

def showabsentstaffs(request):
    # currentabsentkeys=[item for item in keys if item not in presentkeys]
    # currentabsentvalues=[item for item in values if item not in presentvalues]
    currentabsentkeys=['adewale sodie']
    currentabsentvalues=[3]
    serialnumber=[1]
    return render(request, "MAINAPP/showabsentstaffs.html", {'absentkeys': currentabsentkeys, 'absentvalues': currentabsentvalues, 'serialnumber': serialnumber})

def enable(request):
    global showsucess
    global processStatus
    global connectionStatus
    processStatus='Started'
    connectionStatus='connected'
    showsuccess = 'sucess'
    messages.success(request, "Process started")
    go("")
    new_field=FIRM.objects.get(Email=email)
    new_field.ConnectionStatus=processStatus
    new_field.save()
    return redirect('terminal')

def disable(request):
    global showsuccess
    global processStatus
    global connectionStatus
    if processStatus == 'Started':
        processStatus='Ended'
        connectionStatus='diconnected'
        showsuccess = 'sucess'
        new_field=FIRM.objects.get(Email=email)
        new_field.ConnectionStatus=processStatus
        new_field.save()
        return redirect('terminal')
    else:
        showsuccess = 'warning'
        messages.warning(request, "Process not started")
        return redirect('terminal')

def register(request):
    return render(request, "MAINAPP/register.html")

def savescan(request):
    global Fn

    if request.method == "POST":
        #you can also get the variables using this method also...
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        ID = request.POST['ID']

        fullname= firstname + ' ' + lastname

        is_found=False
        new_field=FIRM.objects.get(Email=email)
        all_staff=new_field.staff_set.all()

        for names in all_staff:
            temp_name=all_staff.get(Name=names)
            if temp_name.Name.lower() == fullname.lower():
                is_found=True
                break

        if is_found == True:
            messages.warning(request, "Name already exist!")
            return redirect('scan')

        firm_object=FIRM.objects.get(Name=Fn)
        new_field=Staff(Name=fullname, ID_Number=ID, user=firm_object)
        new_field.save()

        return redirect('register')

def scan(request):
    IDnumber=[]
    for i in range(1, 121):
        IDnumber.append(i)

    firm_object=FIRM.objects.get(Email=email)
    all_staffs=firm_object.staff_set.all()

    used_id=[]
    for name in all_staffs:
        tempStaff=all_staffs.get(Name=name)
        tempID=tempStaff.ID_Number
        used_id.append(tempID)


    availableID=[item for item in IDnumber if item not in used_id]

    return render(request, "MAINAPP/scan.html", {'All_users': availableID})
    
def deletealluser(request):
    firm_object=FIRM.objects.get(Email=email)
    all_staffs=firm_object.staff_set.all()
    all_staffs.delete()
    messages.warning(request, 'All registered user has been deleted sucessfully')
    return redirect('deletestaff')

def confirmdelete(request):
    return render(request, 'MAINAPP/confirmdelete.html')

def checkforID(request):
    global fullnamedel
    global availableIDtoDelete

    if request.method == "POST":
        #you can also get the variables using this method also...
        fullnamedel = request.POST['fullname']

        if fullnamedel == "Select the staff's name":
            availableIDtoDelete=[]
            return redirect('deletestaff')

        firm_object=FIRM.objects.get(Email=email)
        all_staffs=firm_object.staff_set.all()

        availableIDtoDelete=[]
        # for name in all_staffs:
        tempStaff=all_staffs.get(Name=fullnamedel)
        tempID=tempStaff.ID_Number
        availableIDtoDelete.append(tempID)

    return redirect('deletestaff')


def delete(request):
    global nametodelete
    if request.method == "POST":
        #you can also get the variables using this method also...
        ID = request.POST['ID']
        
        if ID == " ":
            return redirect('deletestaff')

        firm_object=FIRM.objects.get(Email=email)
        all_staffs=firm_object.staff_set.all()
        tempStaff=all_staffs.get(ID_Number=ID)
        tempStaff.delete()

        messages.success(request, "Staff details has been deleted sucessfully")

        return redirect('register')

def deletestaff(request):
    firm_object=FIRM.objects.get(Email=email)
    all_staffs=firm_object.staff_set.all()

    staffNames=[]
    for name in all_staffs:
        tempStaff=all_staffs.get(Name=name)
        tempName=tempStaff.Name
        staffNames.append(tempName)

    # if availableIDtoDelete.length() == 0:
    #     availableIDtoDelete.clear()

    return render(request, "MAINAPP/deletestaff.html", {'Available_users': staffNames, 'Available_ID': availableIDtoDelete})

def showallstaff(request):
    # with open('staffdetails.pkl', 'rb') as buffer:
    #     stafflist=pickle.load(buffer)
    # print(stafflist)
    # keys=stafflist.keys()
    # values=stafflist.values()
    # serialnumber=[]
    # counter=1
    # for i in keys:
    #     t=i
    #     serialnumber.append(counter)
    #     counter=counter+1

    user = FIRM.objects.get(Email=email)
    staffs=user.staff_set.all()

    serialnumber=[]
    counter=1
    for i in staffs:
        t=i
        serialnumber.append(counter)
        counter=counter+1

    return render(request, "MAINAPP/showallstaff.html", {'All_users': staffs, 'serialnumber': serialnumber})#stafflist, 'keys': keys, 'values': values, 'serialnumber': serialnumber})


def showallusers(request):
    # with open('staffdetails.pkl', 'rb') as buffer:
    #     stafflist=pickle.load(buffer)
    # print(stafflist)
    # keys=stafflist.keys()
    # values=stafflist.values()
    # serialnumber=[]
    # counter=1
    # for i in keys:
    #     t=i
    #     serialnumber.append(counter)
    #     counter=counter+1

    user = FIRM.objects.all()
    # staffs=user.staff_set.all()

    serialnumber=[]
    counter=1
    for i in user:
        t=i
        serialnumber.append(counter)
        counter=counter+1

    return render(request, "MAINAPP/showallusers.html", {'All_users': user, 'serialnumber': serialnumber})#stafflist, 'keys': keys, 'values': values, 'serialnumber': serialnumber})



def go(processStat):
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
    global processStatus
    while processStatus != 'Ended':
        print(processStatus)
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
            #cv2.imshow('Webcam', img)
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
    serialcomm.close()
    cv2.destroyAllWindows()
    cv2.imread