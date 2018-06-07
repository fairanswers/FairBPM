
import time
from subprocess import call
while True:
    call(["pytest"])
    time.sleep(5)