import threading
def Thread1():
    global counter
    for i in range(100000):
        print(counter)
        counter +=1
def Thread2():
    global counter
    for i in range(100000):
        print(counter)
        counter -=1
counter = 0
thread1 = threading.Thread(target=Thread1)
thread1.start()
thread2 = threading.Thread(target=Thread2)
thread2.start()
thread1.join()
thread2.join()

print("the counter's value after using the threads is: " + str(counter))
 