import socket
import threading
import time

# UDP broadcast settings
BROADCAST_PORT = 37020
BROADCAST_INTERVAL = 5  # in seconds, interval to broadcast "device discovery" messages
BUFFER_SIZE = 1024  # size of buffer for receiving responses
DISCOVERY_MSG = "DISCOVER_DEVICE"  # Message sent during device discovery

# List to hold discovered devices
discovered_devices = []


def broadcast_discovery_message():
    """Broadcast a device discovery message to the network."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    broadcast_address = ('<broadcast>', BROADCAST_PORT)
    while True:
        print(f"Broadcasting discovery message to {broadcast_address}")
        try:
            sock.sendto(DISCOVERY_MSG.encode(), broadcast_address)
        except Exception as e:
            print(f"Error broadcasting discovery message: {e}")
        time.sleep(BROADCAST_INTERVAL)


def listen_for_responses():
    """Listen for devices responding to discovery message."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', BROADCAST_PORT))
    print(f"Listening for responses on port {BROADCAST_PORT}...")

    while True:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            device_info = data.decode()

            # Check if device already discovered
            if addr[0] not in [device['ip'] for device in discovered_devices]:
                discovered_devices.append({'ip': addr[0], 'info': device_info})
                print(f"Device discovered: {device_info} at {addr[0]}")
        except Exception as e:
            print(f"Error receiving data: {e}")


def respond_to_discovery():
    """Respond to a discovery message from other devices."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', BROADCAST_PORT))

    response_msg = "DEVICE_RESPONSE"  # This device's response message

    print(f"Waiting for discovery messages to respond to on port {BROADCAST_PORT}...")
    while True:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            if data.decode() == DISCOVERY_MSG:
                print(f"Discovery message received from {addr}, sending response...")
                sock.sendto(response_msg.encode(), addr)
        except Exception as e:
            print(f"Error responding to discovery message: {e}")


def start_device_discovery():
    """Start the device discovery by broadcasting messages and listening for responses."""
    print("Starting device discovery...")

    # Start broadcasting discovery messages in a separate thread
    broadcast_thread = threading.Thread(target=broadcast_discovery_message, daemon=True)
    broadcast_thread.start()

    # Start listening for responses in another thread
    listen_thread = threading.Thread(target=listen_for_responses, daemon=True)
    listen_thread.start()

    # Keep the main thread alive
    while True:
        time.sleep(1)


if __name__ == "__main__":
    # To simulate a device responding to discovery messages,
    # you can uncomment the line below in a separate process or device.
    # threading.Thread(target=respond_to_discovery, daemon=True).start()

    start_device_discovery()
