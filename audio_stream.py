import socket
import pyaudio
import threading

# Audio streaming settings
CHUNK = 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 1  # Mono audio
RATE = 44100  # 44.1kHz sampling rate
BUFFER_SIZE = 4096  # Buffer size for receiving audio frames

# UDP settings
SERVER_IP = '0.0.0.0'
SERVER_PORT = 9998
CLIENT_PORT = 9999


def audio_stream_server():
    """Function to receive and play audio stream."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, SERVER_PORT))

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open stream for playing audio
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

    print(f"Audio stream server started on {SERVER_IP}:{SERVER_PORT}")

    while True:
        # Receive audio data from client
        data, addr = sock.recvfrom(BUFFER_SIZE)
        stream.write(data)  # Play the received audio data


def audio_stream_client(target_ip):
    """Function to capture and send audio stream."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (target_ip, SERVER_PORT)

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open stream for capturing audio
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print(f"Sending audio stream to {target_ip}:{SERVER_PORT}")

    while True:
        # Read audio data from the microphone
        data = stream.read(CHUNK)
        # Send audio data to the server
        sock.sendto(data, server_address)


if __name__ == "__main__":
    mode = input("Enter 's' for server or 'c' for client: ").strip().lower()

    if mode == 's':
        audio_stream_server()
    elif mode == 'c':
        target_ip = input("Enter the server IP address: ").strip()
        audio_stream_client(target_ip)
    else:
        print("Invalid mode. Please enter 's' for server or 'c' for client.")
