import multiprocessing
import sys

def func1(test,rocket, return_dict):
    print('start func1')
    print(test)
    while rocket < 999999999:
        rocket +=1
    return_dict[1] = 12345
    return_dict[2] = 1234

def func2(rocket, return_dict):
    print('start func2')
    while rocket < 99999999:
        rocket +=1
    return_dict[1] = 123456
    return_dict[2] = 321

def main():
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    rocket = 0
    test = 1
    p1 = multiprocessing.Process(target = func1, args=(test, rocket, return_dict))
    p1.start()
    p2 = multiprocessing.Process(target = func2, args=(rocket, return_dict))
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
    print(return_dict[2])
    print('Hello')

main()
