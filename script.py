import requests
from pynput import keyboard
import PIL.ImageGrab
import json
import datetime






def listen(stop_listener_flag):
    
    with open("config.json","r") as f:
        data = json.load(f)

    user = data["user"]
    webhook = data["webhook"]
    desiredKey = data["key"]
    def on_press(key):
        print(key)
        if str(key) == desiredKey:
            im = PIL.ImageGrab.grab()
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
            im.save(f"images/{formatted_time}.png")
            with open(f"images/{formatted_time}.png","rb") as image_file:
                files = {'image':(f"images/{formatted_time}.png",image_file)}
                data = {'content':f'Screenshot From {user}'}
                print("sending image")
                response = requests.post(webhook,files=files,data=data)
                print(response.json())


    def on_release(key):
        if stop_listener_flag.is_set():
            print('Exiting...')
            return False
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    stop_listener_flag.wait()
    listener.stop()
    listener.join()
    print("listener is stopped")


def select_key(stop_listener_flag):
    
    with open("config.json","r") as f:
        data = json.load(f)


    desiredKey = data["key"]
    
    def on_press(key):
        pass
    
    def on_release(key):
        print(key)
        data["key"] = str(key)
        with open("config.json","w") as f:
            json.dump(data,f,indent=2)
        stop_listener_flag.set()
        
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()


    stop_listener_flag.wait()
    listener.stop()
    listener.join()
    print("reader is stopped")
    stop_listener_flag.clear()


    






