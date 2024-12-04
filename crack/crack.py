import time
from multiprocessing import Process, Manager
import logging

from audible_hash import audible_hash

def brute_force(hash, start, end, process_id, status_dict):
    key = start

    range = end - start

    while key < end:
        activation_bytes = key.to_bytes(4, 'big')

        checksum = audible_hash(activation_bytes)

        if checksum == hash:
            # logging.info("Key found: " + activation_bytes.hex())
            status_dict[process_id] = "Key found: " + activation_bytes.hex()
            return key

        progress = (key - start)
        if (progress % (range // 100) == 0):
            percent = progress / range * 100
            status_dict[process_id] = "Progress: " + str(percent) + "%"
            # logging.info("Progress: " + str(percent) + "%")

        key += 1

    status_dict[process_id] = "Key not found"
    return -1

hash = bytes.fromhex('5aec795d3261d67c566e1a2a353178676fbc74f7')

if __name__ == "__main__":
    t0 = time.time()

    manager = Manager().dict()

    threadCount = 4
    keyCount = 2 ** 32
    keysPerThread = keyCount // threadCount

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    processes = []

    for i in range(threadCount):
        start = keysPerThread * i
        end = keysPerThread * (i + 1)

        p = Process(target=brute_force, args=(hash, start, end, i, manager))
        p.start()
        processes.append(p)
        logging.info("Thread " + str(i) + " started")

    #for p in processes:
    #    p.join()

    while True:
        time.sleep(1)
        status = manager.values()

        allDone = True

        print("Status:")
        for s in status:
            if (s.startswith("Key found")):
                print(s)

                for p in processes:
                    p.terminate()

                allDone = True
                break
            elif (s.startswith("Key not found")):
                print(s)
            else:
                allDone = False
                print(s)
        print("-----")

        if allDone:
            break

    t1 = time.time()

    logging.info("Time: " + str(t1 - t0) + "s")