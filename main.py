import threading
import random

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

# resources
buffer = []
lock = threading.Lock()
producer_done = False
even_file = open("even.txt", "w")
odd_file = open("odd.txt", "w")
all_file = open("all.txt", "w")

# producer
def producer():
    global buffer, producer_done
    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)
        with lock:
            buffer.append(num)
            all_file.write(str(num) + '\n')
    producer_done = True

# customer
def customer(is_even):
    global buffer, producer_done
    while not producer_done or buffer:
        with lock:
            if buffer:
                num = buffer.pop()
                if num % 2 == is_even:
                    if is_even:
                        odd_file.write(str(num) + '\n')
                    else:
                        even_file.write(str(num) + '\n')
                else:
                    buffer.append(num)

# creating threads
producer_thread = threading.Thread(target=producer)
even_customer_thread = threading.Thread(target=customer, args=(True,))
odd_customer_thread = threading.Thread(target=customer, args=(False,))

# start threads
producer_thread.start()
even_customer_thread.start()
odd_customer_thread.start()

# wait for threads to finish
producer_thread.join()
even_customer_thread.join()
odd_customer_thread.join()

# close files
even_file.close()
odd_file.close()
all_file.close()

print("program terminated successfully")

