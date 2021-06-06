#testing page
import numpy as np
import time

while True:
    choice = np.random.choice([1,2,3,4],
                              p=[1,0,0,0])
    print(choice)
    time.sleep(0.3)
    
