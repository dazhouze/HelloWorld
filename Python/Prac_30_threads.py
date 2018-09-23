print('Normally we just use threading instead of __thread')

import time, threading
def loop():
    print ('thead %s is running.' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print ('thead %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s is ended.' % threading.current_thread().name)

print ('thread %s is running' % threading.current_thread().name)
t = threading.Thread(target =  loop, name = 'loopThread')
t.start()
t.join()
print('thread %s is ended' % threading.current_thread().name)

#bug example
import time, threading

# 假定这是你的银行存款:
balance = 0

def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(900000):
        change_it(n)

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)
