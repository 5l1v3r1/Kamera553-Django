from ctypes import *
from datetime import datetime,time
from itertools import combinations
import math,random,os,sys,cv2,base64,darknet,psycopg2
import numpy as np
import urllib.request as urllib

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
    global degermax,hedefzaman,degertehlikemax,alarmver
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

        red_zone_list = [] 
        red_line_list = []
        for (id1, p1), (id2, p2) in combinations(centroid_dict.items(), 2):
            if(p1[0] > p2[0]):
                if(p1[1] > p2[1]):
                    dx,dy = p1[0] - p2[0],p1[1] - p2[1]
                else:
                    dx,dy = p1[0] - p2[0], p2[1] - p2[1]
            else:
                if(p1[1] > p2[1]):
                    dx,dy = p2[0] - p1[0],p1[1] - p2[1]
                else:
                    dx,dy = p2[0] - p1[0], p2[1] - p2[1]  
            distance = is_close(dx, dy) 	
            if distance < 75.0:						
                if id1 not in red_zone_list:
                    red_zone_list.append(id1)     
                    red_line_list.append(p1[0:2])   
                if id2 not in red_zone_list:
                    red_zone_list.append(id2)	
                    red_line_list.append(p2[0:2])

        for idx, box in centroid_dict.items():
            if idx in red_zone_list:  
                cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), (255, 0, 0), 2)
                cv2.putText(img, "Tehlikede", (box[2],box[3]-15), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
            else:
                cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), (0, 255, 0), 1)
                cv2.putText(img, "Insan", (box[2],box[3]-15), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)


        if len(centroid_dict) > degermax:
            degermax = len(centroid_dict)

        if(len(red_zone_list) > degertehlikemax):
            degertehlikemax = len(red_zone_list)
        
        gecerlizaman = datetime.now().time()
        gecerlidakika = gecerlizaman.minute

        if saatbaslangic != None:
            if(len(centroid_dict) != 0):
                if ikincibaslangictime != None:
                    if gecerlizaman <= bitistime or gecerlizaman >= baslangictime:
                        cursor.execute("""select a_status from "Kamera553_alertme" """)
                        deger = cursor.fetchall()
                        for veri in deger:
                            if veri[0] == True:
                                alarmver = 1
                            else:
                                pass
                    else:
                        pass
                else:
                    if gecerlizaman <= bitistime and gecerlizaman >= baslangictime:
                        cursor.execute("""select a_status from "Kamera553_alertme" """)
                        deger = cursor.fetchall()
                        for veri in deger:
                            if veri[0] == True:
                                alarmver = 1
                            else:
                                pass
                    else:
                        pass
            else:
                pass

        if(gecerlidakika == hedefzaman):
            cursor.execute(f"""insert into "Kamera553_reports" (r_yakinsay,r_insansay,r_camid) VALUES ({degertehlikemax},{degermax},{camid})""")
            degermax,degertehlikemax = 0,0
            if(gecerlidakika + periot > 60):
                    hedefzaman = gecerlidakika + periot - 60
            elif(gecerlidakika == 60):
                    hedefzaman = periot
            else:
                    hedefzaman = gecerlidakika + periot

        text = "Insan Sayisi: %s" % str(len(centroid_dict))
        text2 = f"Maximum Insan Sayisi: {str(degermax)}"
        text3 = f"Tehlike Altindaki Insan Sayisi: {str(len(red_zone_list))}"
        text4 = f"Maximum Tehlikedeki Insan Sayisi: {degertehlikemax}"
        location = (20,45)
        location2 = (20,95)
        location3 = (20,145)
        location4 = (20,195)
        cv2.putText(img, text, location, cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img, text2, location2, cv2.FONT_HERSHEY_DUPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
        cv2.putText(img, text3, location3, cv2.FONT_HERSHEY_DUPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
        cv2.putText(img, text4, location4, cv2.FONT_HERSHEY_DUPLEX, 1, (255,0,0), 2, cv2.LINE_AA)

        for check in range(0, len(red_line_list)-1):					
            start_point = red_line_list[check] 
            end_point = red_line_list[check+1]
            check_line_x = abs(end_point[0] - start_point[0])   		 
            check_line_y = abs(end_point[1] - start_point[1])			
            if (check_line_x < 75) and (check_line_y < 25):		
                cv2.line(img, start_point, end_point, (255, 0, 0), 1) 
    return img


netMain = None
metaMain = None
altNames = None

def olustur():
    global ikincibaslangictime,ikincibitistime
    ikincibaslangictime = time(0,0,0)
    ikincibitistime = time(23,59,0)


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
                            if saatbaslangic == None:
                                global bitistime,baslangictime
                                cursor.execute(f"""select a_start,a_end from "Kamera553_alertme" """)
                                durum = cursor.fetchall()
                                for satir in durum:
                                    saatbaslangic = int(satir[0].strftime("%H"))
                                    dakikabaslangic = int(satir[0].strftime("%M"))
                                    saatbitis = int(satir[1].strftime("%H"))
                                    dakikabitis = int(satir[1].strftime('%M'))
                                    bitistime = time(saatbitis,dakikabitis,0)
                                    baslangictime = time(saatbaslangic,dakikabaslangic,0)
                                    if saatbitis < saatbaslangic:
                                        olustur()
                                    elif saatbitis == saatbaslangic:
                                        if dakikabitis < dakikabitis:
                                            olustur()
                                        elif dakikabitis == baslangictime:
                                            baslangictime = time(23,59,0)
                                            bitistime = time(0,0,0)
                                    
                        else:
                                saatbaslangic = None
                                ikincibaslangictime = None


def YOLO():
    global degermax,metaMain, netMain, altNames,degertehlikemax,alarmver
    
    degermax,degertehlikemax,deger = 0,0,0

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
                frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                frame_resized = cv2.resize(frame_rgb,
                                        (new_width, new_height),
                                        interpolation=cv2.INTER_LINEAR)
                darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())
                detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=0.25)
                image = cvDrawBoxes(detections, frame_resized)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                retval, buffer = cv2.imencode('.jpg', image)
                jpg_as_text = base64.b64encode(buffer)
                
                if alarmver == 1:
                    sql_update_query = """Update "Kamera553_alertme" set a_status = %s, alert_image = %s """
                    cursor.execute(sql_update_query, ("false",jpg_as_text))
                    connection.commit()
                    alarmver = 0

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
                        degermax,dagertehlikemax,alarmver = 0,0,0
                        gecerlidakika = datetime.now().time().minute
                        periot,camurl,camid = satir[1],satir[0],satir[2]
                        saatbaslangic,saatbitis,ikincibaslangictime,ikincibitistime = None,None,None,None
                        if(gecerlidakika + periot > 60):
                            hedefzaman = gecerlidakika + periot - 60
                        elif(gecerlidakika == 60):
                            hedefzaman = periot
                        else:
                            hedefzaman = gecerlidakika + periot
        except:
            print("Veri çekilirken hata oluştu!")
            print(f"""Error 01: Kamera ismi databasede bulunumadı! İşlem ismi = [{str(os.path.basename(sys.argv[0]))[:-3]}] 
            Seçim komutu = select cam_url,cam_period from "Kamera553_camera" WHERE cam_name = '{str(os.path.basename(sys.argv[0]))[:-3]}'""")
            exit()
        
    except:
        print("Database bağlantısı gerçekleşemedi!")
        exit()
    YOLO()