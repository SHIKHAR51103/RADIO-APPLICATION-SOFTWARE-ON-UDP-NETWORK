import socket
import os

# UDP settings
SERVER_IP = '0.0.0.0'  # Bind to all interfaces
SERVER_PORT = 8888
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"  # Separator used to distinguish filename and file size

# Define socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def file_transfer_server():
    """Function to receive files from the client."""
    print(f"File transfer server started on {SERVER_IP}:{SERVER_PORT}")
    sock.bind((SERVER_IP, SERVER_PORT))

    # Wait for the file transfer initiation
    data, client_address = sock.recvfrom(BUFFER_SIZE)
    filename, filesize = data.decode().split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)

    print(f"Receiving file: {filename} ({filesize} bytes) from {client_address}")

    # Open the file for writing
    with open(filename, "wb") as f:
        total_received = 0
        while total_received < filesize:
            # Receive file data
            data, _ = sock.recvfrom(BUFFER_SIZE)
            f.write(data)
            total_received += len(data)

    print(f"File received successfully: {filename}")


def file_transfer_client(target_ip, file_path):
    """Function to send files to the server."""
    filesize = os.path.getsize(file_path)
    filename = os.path.basename(file_path)

    print(f"Sending file: {filename} ({filesize} bytes) to {target_ip}:{SERVER_PORT}")

    # Send the filename and filesize to the server
    sock.sendto(f"{filename}{SEPARATOR}{filesize}".encode(), (target_ip, SERVER_PORT))

    # Open the file for reading in binary mode
    with open(file_path, "rb") as f:
        while True:
            # Read the file in chunks and send it
            data = f.read(BUFFER_SIZE)
            if not data:
                break
            sock.sendto(data, (target_ip, SERVER_PORT))

    print(f"File sent successfully: {filename}")


if __name__ == "__main__":
    mode = input("Enter 's' for server or 'c' for client: ").strip().lower()

    if mode == 's':
        file_transfer_server()
    elif mode == 'c':
        target_ip = input("Enter the server IP address: ").strip()
        file_path = input("Enter the path of the file to send: ").strip()
        file_transfer_client(target_ip, file_path)
    else:
        print("Invalid mode. Please enter 's' for server or 'c' for client.")
