import multiprocessing
import sys

rocket = 0

def func1():
    global rocket
    print('start func1')
    while rocket < 999999:
        rocket +=1
    return_dict[1] = 'end_func1'

def func2():
    global rocket
    print('start func2')
    while rocket < 9999999:
        rocket +=1
    return_dict[1] = 'end_func2'

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    p1 = multiprocessing.Process(target = func1)
    p1.start()
    p2 = multiprocessing.Process(target = func2)
    p2.start()

    while True:
        if p1.is_alive() == 0:
            p2.terminate()
            print('P2 is killed')
            break
        if p2.is_alive() == 0:
            p1.terminate()
            print('P1 is killed')
            break

    print(return_dict[1])
    print('Hello')
