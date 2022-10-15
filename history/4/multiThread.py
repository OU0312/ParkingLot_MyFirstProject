from pytest import importorskip
from tqdm import trange
import time
import threading

def prog():
    for i in trange(100):
        time.sleep(0.01)
    return
    
progth1= threading.Thread(target=prog)
progth1.start()
progth2= threading.Thread(target=prog)
progth2.start()
prog()
