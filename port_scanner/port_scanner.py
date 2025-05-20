import socket
import threading
from queue import Queue
from tqdm import tqdm

target = input("Enter target IP (e.g., 127.0.0.1): ")
start_port = int(input("Enter start port: "))
end_port = int(input("Enter end port: "))
num_threads = int(input("Enter number of threads (e.g., 10): "))

queue = Queue()
open_ports = []
lock = threading.Lock() 

def portScanner(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.5)
        sock.connect((target, port))
        sock.close()
        return True
    except (socket.timeout, socket.error):
        return False

def fill_queue(port_list):
    for port in tqdm(port_list, desc="Queueing Ports", unit="port"):
        queue.put(port)

def worker():
    while not queue.empty():
        port = queue.get()
        if portScanner(port):
            with lock: 
                print(f"Port {port} is open")
                open_ports.append(port)

port_list = range(start_port, end_port + 1)
fill_queue(port_list)

thread_list = []
for t in range(num_threads):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()

print(f"\nScan complete. Open ports on {target}: {open_ports}")

with open("scan_results.txt", "w") as f:
    for port in open_ports:
        f.write(f"Port {port} is open\n")

print("\nResults saved to scan_results.txt")

