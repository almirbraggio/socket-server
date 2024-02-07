import socket, signal, time, sys
from random import randint

# Print Standard Function
def printf(string='', end='\n'):
    sys.stdout.write(string + end)
    sys.stdout.flush()

while True:
    try:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        port_number = 8081
        server_address = ('localhost', port_number)

        printf('Opening connection')
        sock.connect(server_address)
        
        msg = time.localtime()
        msg =   'ST300UEX;205029533;01;395;%04d%02d%02d;%02d:%02d:%02d;629d03;-24.997469;-053.295893;000.041;000.00;9;1;2367;12.71;000000;27;from rs232;62;014347;4.2;1\r\n' \
                % (msg.tm_year, msg.tm_mon, msg.tm_mday, msg.tm_hour, msg.tm_min, msg.tm_sec)
        printf('Sending message:')
        printf(msg)
        sock.send(msg.encode())
        sock.close()

        time.sleep(5)

    except (KeyboardInterrupt, SystemExit):
        raise
        pass
    except:
        printf('except')
        time.sleep(1)
sys.exit()