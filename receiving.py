import socket
import os

save_dir = 'received_files'
os.makedirs(save_dir, exist_ok=True)

port = 5001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen()
    print(f'Receiver running on port {port}. Waiting for files...')
    
    try:
        while True:
            client_socket, addr = server_socket.accept()
            with client_socket:
                print(f'Connection from {addr}')
                
                # Receive filename size and filename
                filename_size = int.from_bytes(client_socket.recv(4), 'big')
                filename = client_socket.recv(filename_size).decode()
                filepath = os.path.join(save_dir, filename)
                
                # Receive filesize
                filesize = int.from_bytes(client_socket.recv(8), 'big')
                
                # Receive file data
                with open(filepath, 'wb') as f:
                    bytes_read = 0
                    while bytes_read < filesize:
                        chunk = client_socket.recv(min(4096, filesize - bytes_read))
                        if not chunk:
                            break
                        f.write(chunk)
                        bytes_read += len(chunk)
                print(f'Saved file {filename} from {addr}')
    except KeyboardInterrupt:
        print('\nReceiver stopped by user.')
