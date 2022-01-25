# iNKABULIZER  Camera ANDROID USB to Windows Camera
#Discord https://discord.gg/sh9bWrf8r7
#Install python-3.9.6-amd64.exe https://www.python.org/downloads/release/python-396/
#Install Open Broadcaster Software (include Obs Virtual  Camera) https://obsproject.com/
#pip install scrcpy
#pip install scrcpy-client
#pip install adbutils
#pip install pyvirtualcam

#Tested Windows 11

import scrcpy
from adbutils import adb
import pyvirtualcam
from pyvirtualcam import PixelFormat
from time import perf_counter_ns,perf_counter,sleep

Android_max_fps=60 # Андроид Количество кадров
Android_max_width=1920 # Андроид Ширина
Android_flip=0 # Андроид Поворот
Android_bitrate=16000000 # Андроид битрейт
Android_lock_screen_orientation=1 # Андроид блокировка поворота экрана

Cam_FPS=60 # Камера Количество кадров
Cam_width=1920 # Камера Ширина
Cam_height=1080 # Камера Высота

def list_devices(): #Ищет Андроид
    items = [i.serial for i in adb.device_list()]
    return items

def on_frame(frame): # Передаем кадр из Андроид в Камеру
    if frame is not None:
        cam.send(frame)

def closeEvent(): # отключает андроид
    client.remove_listener(scrcpy.EVENT_FRAME, on_frame)
    client.stop()

def Run_Client(): # Запуск 
    device = adb.device(0) # Выбирается Андроид 0 (первый найденный)
    global client
    # Инициализвция параметров Андроид
    client = scrcpy.Client(max_width=Android_max_width, device=device, flip=Android_flip,bitrate=Android_bitrate,max_fps=Android_max_fps,lock_screen_orientation=Android_lock_screen_orientation)      
    client.add_listener(scrcpy.EVENT_FRAME, on_frame) # Создает событие on_frame(frame)
    client.start(threaded=True) # Запуск Андройда в отдельном процессе
    print(client.device_name ,client.resolution)
    width,height = client.resolution # Берем ширину и высоту от Андройда
    length = int(0)
    #width = Cam_width # Камера Ширина
    #height = Cam_height # Камера Высота
    global cam 
    try:
        cam=pyvirtualcam.Camera(width, height, Cam_FPS, fmt=PixelFormat.BGR,device=None)  # ЗАпуск камеры
        print(f'Virtual cam started: {cam.device} ({cam.width}x{cam.height} @ {cam.fps}fps)')
    except:
        print("Virtual cam Не установлена, Скачать и Установить https://obsproject.com/forum/resources/obs-virtualcam.949/ ")
        closeEvent()
        sleep(5)
        exit()
        

Flag_Cleent_Start=0 # Флаг включен отключен Андроид
t1_start=0 # Время Начало
t1_stop=0 # Время Конец
print("Camera ANDROID to Windows Camera")
while True:
    t1_start = perf_counter() #  Замер времени
    if (t1_start - t1_stop) > 0.1: # Если разница во времени
        t1_stop = perf_counter()
        Current_Device=list_devices()  # Поиск Подключен ли Андроид    
        if Current_Device ==[] :
            if  Flag_Cleent_Start==1:  # Если Андроида нет то выключаем процесс Андроид и камеру
                Flag_Cleent_Start=0
                print("Стоп")
                closeEvent() # отключает андроид
                cam=0 # Отключает камеру
        else:
            if Flag_Cleent_Start==0:  # Если Андроид подключен то Запуск Андроид и камеры
                print("Старт Current_Device",Current_Device)
                Flag_Cleent_Start=1
                Run_Client() # Запуск Андроид и камеры
    else:
        sleep(100/1000) # Пауза


            