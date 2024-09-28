import cv2
import socket
import struct
import pickle

# UDP settings
SERVER_IP = '0.0.0.0'  # Server IP, use '0.0.0.0' to bind to all interfaces
SERVER_PORT = 9999  # Port number for streaming
BUFFER_SIZE = 65536  # Buffer size for receiving frames

# Define socket for communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFFER_SIZE)
server_address = (SERVER_IP, SERVER_PORT)


def video_stream_server():
    """Function to receive video stream and display it."""
    print(f"Starting video stream server on {SERVER_IP}:{SERVER_PORT}")

    # Bind the socket to the address and port
    sock.bind(server_address)

    # Initialize OpenCV window to display the video stream
    cv2.namedWindow('Video Stream', cv2.WINDOW_NORMAL)

    while True:
        # Receive the packet from client
        packet, client_address = sock.recvfrom(BUFFER_SIZE)

        # Deserialize the received packet (frame)
        data = pickle.loads(packet)

        # Decode the frame (assuming it's encoded as JPEG)
        frame = cv2.imdecode(data, cv2.IMREAD_COLOR)

        # Display the frame in OpenCV window
        cv2.imshow('Video Stream', frame)

        # Press 'q' to quit the stream
        if cv2.waitKey(1) == ord('q'):
            break

    # Clean up
    cv2.destroyAllWindows()


def video_stream_client(target_ip):
    """Function to capture video and send it to the server."""
    print(f"Sending video stream to {target_ip}:{SERVER_PORT}")

    # Initialize video capture (0 means the default camera)
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        # Read the frame from the webcam
        ret, frame = cap.read()

        # If frame is read successfully
        if ret:
            # Encode the frame as JPEG
            encoded_frame = cv2.imencode('.jpg', frame)[1]

            # Serialize the frame to send over the network
            data = pickle.dumps(encoded_frame)

            # Send the packet to the server
            sock.sendto(data, (target_ip, SERVER_PORT))

        # Press 'q' to quit the stream
        if cv2.waitKey(1) == ord('q'):
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    mode = input("Enter 's' for server or 'c' for client: ").strip().lower()

    if mode == 's':
        video_stream_server()
    elif mode == 'c':
        target_ip = input("Enter the server IP address: ").strip()
        video_stream_client(target_ip)
    else:
        print("Invalid mode. Please enter 's' for server or 'c' for client.")
