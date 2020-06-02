import sys
from os import path,remove,walk
import xml.etree.cElementTree as ET
import ctypes
import base64
import io
import cv2
from time import sleep
##Kullanıcı Adı-Ve Kullanıcının CamIDsi veritabanından Çekilecek

vid = cv2.VideoCapture(0)

username = input("Kullanıcı adını girin")
userid = input("id girin")

def CreateFile(username,userid,bytecode):
    infos = ET.Element("infos")
    info = ET.SubElement(infos, "info")
    ET.SubElement(info, "code").text = bytecode
    tree = ET.ElementTree(infos)
    tree.write(username + '-' + userid + ".xml")

while True:
    cv2
    _,frame = vid.read()
    deger = frame
    _, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer)
    CreateFile(username,userid,str(jpg_as_text))
    print("ok")
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()