from ctypes import *
import datetime
import math
import random
import os,sys
import cv2,base64
import numpy as np
import time
import darknet
import urllib.request as urllib
from itertools import combinations
import psycopg2

def is_close(p1, p2):
    dst = math.sqrt(p1**2 + p2**2)
    return dst 


def convertBack(x, y, w, h): 
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def cvDrawBoxes(detections, img):
    global degermax,hedefzaman
    if len(detections) > 0:
        centroid_dict = dict()
        objectId = 0
        for detection in detections:
            name_tag = str(detection[0].decode())
            if name_tag == 'person':                
                x, y, w, h = detection[2][0],\
                            detection[2][1],\
                            detection[2][2],\
                            detection[2][3]
                xmin, ymin, xmax, ymax = convertBack(float(x), float(y), float(w), float(h))
                centroid_dict[objectId] = (int(x), int(y), xmin, ymin, xmax, ymax)
                objectId += 1    

        for idx, box in centroid_dict.items():
                cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), (0, 255, 0), 2)


        if len(centroid_dict) > degermax:
            degermax = len(centroid_dict)

        gecerlizaman = datetime.datetime.now().time().minute
        if(gecerlizaman == hedefzaman):
            cursor.execute(f"""insert into "Kamera553_reports" (r_insansay,r_camid) VALUES ({degermax},{camid})""")
            degermax = 0
            if(gecerlizaman + periot > 60):
                    hedefzaman = gecerlizaman + periot - 60
            elif(gecerlizaman == 60):
                    hedefzaman = periot
            else:
                    hedefzaman = gecerlizaman + periot

        text = "Insan Sayisi: %s" % str(len(centroid_dict))
        text2 = f"Maximum Insan Sayisi: {str(degermax)}"
        location = (20,45)
        location2 = (20,95)
        cv2.putText(img, text, location, cv2.FONT_HERSHEY_DUPLEX, 1, (231,76,60), 2, cv2.LINE_AA)
        cv2.putText(img, text2, location2, cv2.FONT_HERSHEY_DUPLEX, 1, (46,204,113), 2, cv2.LINE_AA)
    return img


netMain = None
metaMain = None
altNames = None

def alarmvekamerakontrol():
                global saatbaslangic,saatbitis
                cursor.execute(f"""select cam_status,cam_alarmstatus from "Kamera553_camera" where id = {camid}""")
                sonuc1 = cursor.fetchall()
                for satir in sonuc1:
                    cam_durum = satir[0]
                    alarm_durum = satir[1]
                    if cam_durum == False:
                        exit()
                    else:
                        if alarm_durum == True:
                            if saatbaslangic == 0:
                                cursor.execute(f"""select a_start,a_end from "Kamera553_alertme" """)
                                durum = cursor.fetchall()
                                for satir in durum:
                                    saatbaslangic = satir[0]
                                    saatbitis = satir[1]
                                    print(type(saatbaslangic))
                                    print(type(saatbitis))
                        else:
                                saatbaslangic = 0
                                saatbitis = 0

def YOLO():
    global degermax,metaMain, netMain, altNames
    
    degermax,deger = 0,0

    configPath = f"{usedpath}/cfg/yolov4.cfg"
    weightPath = f"{usedpath}/yolov4.weights"
    metaPath = f"{usedpath}/cfg/coco.data"
    if not os.path.exists(configPath):
        raise ValueError("Invalid config path `" +
                         os.path.abspath(configPath)+"`")
    if not os.path.exists(weightPath):
        raise ValueError("Invalid weight path `" +
                         os.path.abspath(weightPath)+"`")
    if not os.path.exists(metaPath):
        raise ValueError("Invalid data file path `" +
                         os.path.abspath(metaPath)+"`")
    if netMain is None:
        netMain = darknet.load_net_custom(configPath.encode(
            "ascii"), weightPath.encode("ascii"), 0, 1)
    if metaMain is None:
        metaMain = darknet.load_meta(metaPath.encode("ascii"))
    if altNames is None:
        try:
            with open(metaPath) as metaFH:
                metaContents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", metaContents,
                                  re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            namesList = namesFH.read().strip().split("\n")
                            altNames = [x.strip() for x in namesList]
                except TypeError:
                    pass
        except Exception:
            pass


    stream = urllib.urlopen(camurl)
    bytes = b''
    while True:
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.COLOR_BGR2RGB)
            
            if deger == 0:
                new_height, new_width, channels = img.shape
                darknet_image = darknet.make_image(new_width, new_height, 3)
                deger = 1
            prev_time = time.time()
            frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb,
                                    (new_width, new_height),
                                    interpolation=cv2.INTER_LINEAR)
            darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())
            detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=0.25)
            image = cvDrawBoxes(detections, frame_resized)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            print(1/(time.time()-prev_time))
            retval, buffer = cv2.imencode('.jpg', image)
            jpg_as_text = base64.b64encode(buffer)
            try:
                sql_update_query = """Update "Kamera553_camera" set cam_image = %s where id = %s"""
                cursor.execute(sql_update_query, (jpg_as_text, camid))
                connection.commit()
            except:
                print("Bağlantı kayboldu")
                exit()

            alarmvekamerakontrol()
            
            cv2.imshow(str(os.path.basename(sys.argv[0]))[:-3], image)
            cv2.imwrite(f"E:/Code/Python/Development/Kamera553-Django/camera553/static/image/resim.jpg",image)
            if cv2.waitKey(3) & 0xFF == ord('q'):
                if(connection):
                    cursor.close()
                    connection.close()
                break

if __name__ == "__main__":
    usedpath = sys.argv[1]
    try:
        connection = psycopg2.connect(
            user="newbie",
            password="12345kamera",
            host = "localhost",
            port = "5432",
            database = "kamera553django"
        )
        cursor = connection.cursor()
        try:
            cursor.execute(f"""select cam_url,cam_period,id from "Kamera553_camera" WHERE cam_name = '{str(os.path.basename(sys.argv[0]))[:-3]}'""")
            sonuc = cursor.fetchall()
            if len(sonuc) == 0:
                print("Tanımlı görev bulunamadı!")
                exit()
            elif len(sonuc) > 1:
                print("Database verilerinde sıkıntı var!")
                exit()
            else:
                for satir in sonuc:
                        degermax = 0
                        gecerlizaman = datetime.datetime.now().time().minute
                        periot = satir[1]
                        camurl = satir[0]
                        camid = satir[2]
                        saatbaslangic = 0
                        saatbitis = 0
                        if(gecerlizaman + periot > 60):
                            hedefzaman = gecerlizaman + periot - 60
                        elif(gecerlizaman == 60):
                            hedefzaman = periot
                        else:
                            hedefzaman = gecerlizaman + periot
        except:
            print("Veri çekilirken hata oluştu!")
            print(f"""Error 01: Kamera ismi databasede bulunumadı! İşlem ismi = [{str(os.path.basename(sys.argv[0]))[:-3]}] 
            Seçim komutu = select cam_url,cam_period from "Kamera553_camera" WHERE cam_name = '{str(os.path.basename(sys.argv[0]))[:-3]}'""")
            exit()
        
    except:
        print("Database bağlantısı gerçekleşemedi!")
        exit()
    YOLO()