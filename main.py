#!/usr/bin/python3
# Encoding: utf8

# Author: Almir A Braggio
# Date: 30 nov. 2015

# Socket Info.
port_number = 8081
host_name = ''
server_address = ('', port_number)

# Socket Timeout
sock_open_wait = 5  # Try to open the socket, if socket busy
sock_timeout = 600  # To close connection, if lose communication

# MongoDB
mongodb_host = 'mongodb://localhost:27017/'
mongodb_name = 'database'
mongodb_collection = 'posts'
mongoflag = False   # Send to database

# Others
printflag = True    # Write to standard output

# Library
import sys, time
import json
from gevent import socket
from gevent.server import StreamServer
from pymongo import MongoClient

# Continental VDO Protocol
from protocol_vdo import *
# Suntech ST300 Protocol
from protocol_suntech import *

# Print Standard Function
def printf(string='', end='\n'):
    if printflag:
        sys.stdout.write(string + end)
        sys.stdout.flush()

# Integer Rounding Function
def round_int(value, step):
    return int( int((value+step/2 )/step) *step)

# Saving on the database
def db(post={}):
    if mongoflag:
        # MongoDB connection
        db_client = MongoClient(mongodb_host)
        # Select database and collection
        db = db_client[mongodb_name]
        db_posts = db[mongodb_collection]
        # Post!
        post_id = db_posts.insert(post)
        if printflag:
            post_id_str = str(post_id)
            printf('Post Id Count... "%s"' % db_posts.count())
        db_client.close()
    return;

# Handle Function
def handle_conn(sock, address):

    post = 0
    client_ip = address[0]
    client_port = address[1]
    client_id = id(sock)
    printf('New connection from %s:%d (%d)' % (client_ip, client_port, client_id))

    # Timeout too close connection, if lose communication
    sock.settimeout(sock_timeout)
    try:
        while True:

            msg = ''
            msg = sock.recv(4096).decode()

            # Null message?
            if (len(msg) == 0):
                break

            try:
                # Receiving new message
                if msg:
                    #printf('Message: %s' % msg)
                    # Suntech Protocol
                    if (msg.split(';')[0] == 'ST300UEX'):
                        printf('Suntech ST300R Protocol')
                        post = protocol_suntech(msg)
                    elif (msg.split(';')[0] == 'ST300STT'):
                        printf('Suntech ST300R Default GPS Data')
                        post = 0 # ignore
                    # VDO Protocol
                    elif (msg[0:2] == 'SV'):
                        printf('Continental VDO Protocol')
                        post = protocol_vdo(msg)
                    # Undefined Protocol
                    else:
                        printf('Undefined Protocol')
                        post = 0

                    # Its a valid data
                    if (post):
                        print('Message:')
                        print(json.dumps(post,sort_keys=True,indent=4,separators=(',',':')))
                        # Save in database
                        db(post)
                    else:
                        printf('Invalid Data')
                else:
                    printf('No more data from %s:%d (%d)' % (client_ip, client_port, client_id))
                    break
            except KeyboardInterrupt:
                raise
            except IndexError as err:
                printf('Exception IndexError %s' % (str(err),))
            except:
                printf('Exception %s' % ('unknown',))
                raise

    except socket.timeout:
        printf('Connection timed out')

    printf('Closing connection from %s:%d (%d)' % (client_ip, client_port, client_id))
    sock.shutdown(socket.SHUT_WR)
    sock.close()

while True:
    try:
        # Create a TCP Socket Server
        # Limit to 1,000 simultaneous connections
        server = StreamServer(server_address, handle_conn, spawn=1000)
        printf('Socket successfully created on port: %s' % port_number)
        # Run forever
        server.serve_forever()
    except KeyboardInterrupt:
        break
    except:
        printf('Socket could not be created')
        printf('Waiting for %d seconds' % sock_open_wait)
        time.sleep(sock_open_wait)

sys.exit()