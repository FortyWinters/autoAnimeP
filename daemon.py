import sys
import os
import time
import schedule
import subprocess


def job1():
    subprocess.call(['python3', 'runTask.py'])

def job2():
    subprocess.call(['python3', 'logTest2.py'])

def execAllTask():
    schedule.every(2).minutes.do(job1)
    # schedule.every(5).seconds.do(job2)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    pid = os.fork()
    if pid > 0:
        sys.exit(0)
    
    execAllTask()