import socket
import threading
import logging
import time

logging.basicConfig(filename='klein_tesla_trap.log', level=logging.INFO, format='%(asctime)s %(message)s')

trap_ports = [445, 135, 139, 3389]

def loopback_connection(port):
	# Tesla valve: Only allow loopback (localhost) connections, block all others
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Only connect to localhost — no outside connections allowed
		s.connect(('127.0.0.1', port))
		logging.info(f"Loopback connection successful on port {port}")
		s.close()
	except Exception as e:
		logging.info(f"Loopback connection failed on port {port}: {e}")

def trap_port(port):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind(('0.0.0.0', port))
	server.listen(5)
	logging.info(f"Klein-Tesla honeypot listening on port {port}")
	print(f"Klein-Tesla honeypot listening on port {port}")

	while True:
		client, addr = server.accept()
		logging.info(f"Incoming connection from {addr} on port {port}")

		# Here is the Tesla valve effect:
		# Accept inbound connections, but do NOT initiate connections outward to any external IP.
		# Only initiate internal loopbacks to trap worm traffic in the Klein bottle loop.
		threading.Thread(target=loopback_connection, args=(port,), daemon=True).start()

		# Immediately close client connection to simulate trapping the worm
		client.close()

def main():
	threads = []
	for port in trap_ports:
		t = threading.Thread(target=trap_port, args=(port,), daemon=True)
		t.start()
		threads.append(t)

	print("Klein bottle + Tesla valve worm trap running. Press Ctrl+C to stop.")
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		print("Stopping Klein-Tesla worm trap...")

if __name__ == "__main__":
	main()
