import socket
import os

# Get IP and file path from user
target_ip = input('Enter the receiver IP address: ').strip()
file_path = input('Enter the full path of the file to send: ').strip()

# Basic validation
if not os.path.isfile(file_path):
    print('File does not exist.')
    exit(1)

port = 5001  # Choose a port

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((target_ip, port))
        # Send filename size and filename first
        filename = os.path.basename(file_path)
        s.send(len(filename).to_bytes(4, 'big'))
        s.send(filename.encode())
        
        # Send file size
        filesize = os.path.getsize(file_path)
        s.send(filesize.to_bytes(8, 'big'))
        
        # Send the file content in chunks
        with open(file_path, 'rb') as f:
            while (chunk := f.read(4096)):
                s.sendall(chunk)
    print('File sent successfully.')
except Exception as e:
    print(f'Error: {e}')
