import socket
import threading
import logging
import time
import uuid

logging.basicConfig(filename='klein_tesla_trap.log', level=logging.INFO, format='%(asctime)s %(message)s')

trap_ports = [445, 135, 139, 3389]
MAX_RECURSION_DEPTH = 5  # Prevent infinite system exhaustion

def loopback_connection(port, depth, parent_id):
	try:
		logging.info(f"[{parent_id}] Recursion depth {depth} on port {port}")
		
		if depth > MAX_RECURSION_DEPTH:
			logging.info(f"[{parent_id}] Max recursion depth reached. Stopping recursion on port {port}.")
			return

		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect(('127.0.0.1', port))
			logging.info(f"[{parent_id}] Loopback connection successful on port {port} at depth {depth}")

			# Optional: Delay to simulate Klein bottle folding time
			time.sleep(0.5)

			# Recursively create new loopback connection
			threading.Thread(
				target=loopback_connection,
				args=(port, depth + 1, parent_id),
				daemon=True
			).start()

	except Exception as e:
		logging.info(f"[{parent_id}] Loopback connection failed on port {port} at depth {depth}: {e}")

def trap_port(port):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		server.bind(('0.0.0.0', port))
		server.listen(5)
		logging.info(f"Klein-Tesla honeypot listening on port {port}")
		print(f"Klein-Tesla honeypot listening on port {port}")

		while True:
			client, addr = server.accept()
			parent_id = str(uuid.uuid4())[:8]  # Unique ID per connection

			logging.info(f"[{parent_id}] Incoming connection from {addr} on port {port}")

			# Launch loopback thread to simulate Tesla valve
			threading.Thread(
				target=loopback_connection,
				args=(port, 1, parent_id),
				daemon=True
			).start()

			# Close client immediately to simulate trapping the worm
			client.close()

	except Exception as e:
		logging.error(f"Failed to start honeypot on port {port}: {e}")
	finally:
		server.close()

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
