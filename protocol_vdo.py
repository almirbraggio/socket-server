import time

# Defines
get_IMEI = False
printflag = True    # Write to standard output

tcp_msgtypes = (
    0x06,   # 3.1 ACK
    0x15,   # 3.2 NACK
    0x00,   # 3.3 Keep alive
    #0x02,  # 4.2 Classic status table
    #0x09,  # 4.3 Bulk classic status table
    0x22,   # 4.4 Advanced status table
    #0x29,  # 4.5 Bulk advanced status table
    #0x1F,  # 4.6.3 Response to default configuration request
    #0x33,  # 4.6.6 Response to status table configuration request
    #0x03,  # 5.3 Input parameter response
    #0x05,  # 6.3 Response to the request for output parameters
    #0x86,  # 7.1 Set application parameters configuration
    #0x87,  # 7.2 Request application parameters
    #0x07,  # 7.3 Response to request application parameters
    #0x07,  # 7.3 Response to request application parameters
    0x10,   # 7.6 Response to request IMEI+Card number
    0x40,   # 12.1 Snapshot record  

    0xFA,   # Transparent data
)

# Print Standard Function
def printf(string='', end='\n'):
    if printflag:
        sys.stdout.write(string + end)
        sys.stdout.flush()

# Integer Rounding Function
def round_int(value, step):
    return int( int((value+step/2 )/step) *step)

# Convert list to string
def conv_vec2str(data):
    if type(data) != list:
        raise Exception('Type must be list')
    s = ''
    for ch in data:
        s += chr(ch)
    return s

# Convert string to vector
def conv_str2vec(s):
    if type(s) != str:
        raise Exception('Type must be str')
    v = []
    for ch in s:
        v.append(ord(ch))
    return v

# Class Message
class cMessage:
    pass

# Class Define
class cDefine:
    DLE = 0x10
    STX = 0x02
    ETX = 0x03
    MAX_DATA_SIZE = 228
    MAX_MSG_SIZE  = 2 + MAX_DATA_SIZE

# Continental VDO Protocol
def protocol_vdo(msg='',sep=';'):
    # Initializing
    msg_VDO = cMessage()
    msg_VDO.ConnSN = False
    msg_VDO.ConnIMEI = None
    msg_VDO.Serialnum = 'null'
    
    # Init data post
    msg_asctime = 'null'
    msg_devID = 'null'
    msg_Date = 'null'
    msg_Time = 'null'
    msg_Latitude = 'null'
    msg_Longitude = 'null'
    msg_Power = 'null'
    msg_IO = 'null'
    msg_Data = 'null'
    msg_Length = 'null'
    msg_CheckSum = 'null'
    msg_Type = 'null'

    # First validation
    if (len(msg) < 11):
        printf('Not enough data')
        return 0

    # Header
    msg_VDO.Protoheader = msg[0:2]
    # Invalid header
    if (msg_VDO.Protoheader != 'SV'):
        printf('Invalid protocol header')
        return 0

    msg_VDO.StrData = msg[10:]
    msg_VDO.StrSwversion = msg[4]
    msg_VDO.StrSerialnum = msg[5:9]
    msg_VDO.StrProduct = msg[9]
    
    # Convert string to vector of integers
    msg = conv_str2vec(msg)

    msg_VDO.Len = (msg[2]<<8) | msg[3]
    # Invalid lenght?
    if (msg_VDO.Len != len(msg)):
        printf('Invalid lenght')
        return 0

    msg_VDO.Swversion = msg[4]
    msg_VDO.Serialnum = (msg[5]<<24) | (msg[6]<<16) | (msg[7]<<8) | msg[8]
    msg_VDO.Product = msg[9]
    msg_VDO.Type = msg[10]
    
    # Valid command type?
    if (msg_VDO.Type not in tcp_msgtypes):
        printf('Unexpected command')
        return 0

    msg_VDO.Data = msg[10:]

    if msg_VDO.Type == 0xFA:
        # Transparent data
        if msg_VDO.Data[0] == 0xFA and msg_VDO.Data[1] == 0x00:
            # Type = 'TRANSPDATA'
            msg_Status = msg_VDO.StrData[:2]
            msg_Data = msg_VDO.StrData[2:]
            msg_Date = ''
            msg_Time = ''
            msg_Latitude = ''
            msg_Longitude = ''
        # Transparent data with status
        elif msg_VDO.Data[0] == 0xFA and msg_VDO.Data[1] == 0x01:
            # Type = 'TRANSPDATA+STATUS'
            msg_Status = msg_VDO.StrData[:37]
            msg_Data = msg_VDO.StrData[37:]

            GPSTime = time.gmtime((msg_VDO.Data[2] << 24) | (msg_VDO.Data[3] << 16) |
                    (msg_VDO.Data[4] << 8) | (msg_VDO.Data[5] << 0))
            DateTime = "%d-%02d-%02d %02d:%02d:%02d" % (GPSTime.tm_year, GPSTime.tm_mon, GPSTime.tm_mday,
                    GPSTime.tm_hour, GPSTime.tm_min, GPSTime.tm_sec)

            # Date and time
            msg_Date = '%04d%02d%02d' % (GPSTime.tm_year, GPSTime.tm_mon, GPSTime.tm_mday)
            msg_Time = '%02d:%02d:%02d' % (GPSTime.tm_hour, GPSTime.tm_min, GPSTime.tm_sec)

            # Latitude
            msg_Latitude = (msg_VDO.Data[6] << 24) | (msg_VDO.Data[7] << 16) | (msg_VDO.Data[8] << 8) | (msg_VDO.Data[9] << 0)
            if msg_Latitude > 0x7FFFFF:
                msg_Latitude -= 0x1000000
            msg_Latitude /= 3600.0
            msg_Latitude = '%.6f' % msg_Latitude

            # Longitude
            msg_Longitude = (msg_VDO.Data[10] << 24) | (msg_VDO.Data[11] << 16) | (msg_VDO.Data[12] << 8) | (msg_VDO.Data[13] << 0)
            if msg_Longitude > 0x7FFFFF:
                msg_Longitude -= 0x1000000
            msg_Longitude /= 3600.0
            msg_Longitude = '%.6f' % msg_Longitude

        msg_devID = str(msg_VDO.Serialnum)
        msg_Length = str(len(msg_Data))

        msg_asctime = str(time.asctime())

        final = {
        "ASCTIME" : msg_asctime,
        "DEV_ID" : msg_devID,
        "DATE" : msg_Date, "TIME" : msg_Time,
        "LAT" : msg_Latitude, "LON" : msg_Longitude,
        "PWR" : msg_Power, "IO" : msg_IO,
        "DATA" : msg_Data,
        "LEN" : msg_Length, "CHK_SUM" : msg_CheckSum,
        "MSG_TYPE": msg_Type
        }

        return final
    else:
        return 0

#EOF