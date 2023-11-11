# Translation to EN using DeepL, some comments might not be helpful at all.

# iNKABULIZER  Camera ANDROID USB to Windows Camera
#Discord https://discord.gg/sh9bWrf8r7
#Install python-3.9.6-amd64.exe https://www.python.org/downloads/release/python-396/
#Install Open Broadcaster Software (include Obs Virtual  Camera) https://obsproject.com/
#pip install scrcpy
#pip install scrcpy-client
#pip install adbutils
#pip install pyvirtualcam

#Tested on Windows 11

import scrcpy
from adbutils import adb
import pyvirtualcam
from pyvirtualcam import PixelFormat
from time import perf_counter_ns,perf_counter,sleep

#Device
Android_max_fps=60 # Android Max FPS
Android_max_width=1920 # Android Max Width
Android_flip=0 # Vertical/Horizontal Rotation
Android_bitrate=16000000 # Android Bitrate
Android_lock_screen_orientation=1 # Lock Screen Rotation

# Camera
Cam_FPS=60 # Camera FPS (24/30/60/90/120)
Cam_width=1920 # Camera Width
Cam_height=1080 # Camera Height

def list_devices(): # ADB Searching Devive 
    items = [i.serial for i in adb.device_list()]
    return items

def on_frame(frame): # Transferring frame from Device to Camera
    if frame is not None:
        cam.send(frame)

def closeEvent(): # Stop Device / Stop scrcpy
    client.remove_listener(scrcpy.EVENT_FRAME, on_frame)
    client.stop()

def Run_Client(): # Launching 
    device = adb.device(0) # ADB Device 0 is selected (First Found)
    global client
    # Initializing Device parameters
    client = scrcpy.Client(max_width=Android_max_width, device=device, flip=Android_flip,bitrate=Android_bitrate,max_fps=Android_max_fps,lock_screen_orientation=Android_lock_screen_orientation)      
    client.add_listener(scrcpy.EVENT_FRAME, on_frame) # Creates on_frame(frame) event
    client.start(threaded=True) # Starting Device in a separate process
    print(client.device_name ,client.resolution)
    width,height = client.resolution # Width/Height
    length = int(0)
    width = 1920 # Insert Camera Pixel Width (Default 1920)
    height = 1080 # Insert Camera Pixel Height (Default 1080)
    global cam 
    try:
        cam=pyvirtualcam.Camera(width, height, Cam_FPS, fmt=PixelFormat.BGR,device=None)  # Starting Camera
        print(f'Virtual cam started: {cam.device} ({cam.width}x{cam.height} @ {cam.fps}fps)')
    except:
        print("OBS Virtual Cam not installed. Download at https://obsproject.com/forum/resources/obs-virtualcam.949/")
        closeEvent()
        sleep(5)
        exit()
        

Flag_Cleent_Start=0 # Client Start Flag
t1_start=0 # Timed Start
t1_stop=0 # Timed Stop
print("Running Android to OBS Virtual Cam")
while True:
    t1_start = perf_counter() #  Timing
    if (t1_start - t1_stop) > 0.1: # If there's a time difference(?)
        t1_stop = perf_counter()
        Current_Device=list_devices()  # Searching Whether Device is Connected   
        if Current_Device ==[] :
            if  Flag_Cleent_Start==1:  # If there is no device found, kill android task and disable/close camera 
                Flag_Cleent_Start=0
                print("Stopped")
                closeEvent() 
                cam=0 # Disconnects Camera
        else:
            if Flag_Cleent_Start==0:  # If Device is connected, start Android and Camera
                print("Start Current_Device",Current_Device)
                Flag_Cleent_Start=1
                Run_Client() # Starts Task and enables Camera
    else:
        sleep(100/1000) # Pause


            
