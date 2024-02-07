
# Suntech Protocol Description
#-----------------------------------------------------------------------------------------
#     a) HDR: Report Header of External Device's Data "ST300UEX" (serial interface)
#     b) DEV_ID: Device ID (9 char)
#     c) MODEL: Device Model (2 char)
#     d) SW_VER: Software Version (3 char)
#     e) DATE: GPS Date (8 char) "20151002"
#     f) TIME: GPS Time (8 char) "16:47:03"
#     g) CELL: Location Code ID (3 hex-digits) + Serving Cell BSIC (2 dec-digits) (string)
#     h) LAT: Latitude (+ or - xx.xxxxxx) (string)
#     i) LON: Longitude (+ or - xxx.xxxxxx) (string)
#     j) SPD: Speed (km/h) (string)
#     k) CRS: Course Overground in Degree (string)
#     l) SATT: Number of Satellites (string)
#     m) FIX: Fixed (1) or Not-Fixed (0) GPS (1 char)
#     n) DIST: Traveled Distance (m) (string)
#     o) PWR_VOLT: Voltage Value of Main Power (string)
#     p) IO: Current IO Status (6 char) (Ign+In1+In2+In3+Out1+Out2)
#     q) LEN: Length of Data (string)
#     r) DATA: Data form External RS232 Device (string up to 500 bytes)
#     s) CHK_SUM: Checksum
#     t) H_METER: Driving Hour-Meter (string)
#     u) BCK_VOLT: Voltage Value of Backup Battery (string)
#     v) MSG_TYPE: Real Time (1) or Storage (0) Report (1 char)

import time

# Integer Rounding Function
def round_int(value, step):
    return int( int((value+step/2 )/step) *step)

# Suntech ST300 Protocol
def protocol_suntech(msg='',sep=';'):
    
    # Initializing
    arr = []
    arr = msg.split(sep)

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
    msg_PB = 'null'    

    #---------------------------------------------------------------------
    # Model:     ST300UEX;205029533;01;395;20151002;16:47:03;629d28;...
    #            -24.997478;-053.295893;000.017;000.00;7;1;2367;12.82;...
    #            000000;20;SMP|A|7|2256|256|1539|717|ID=28;44;014239;4.2;1
    #---------------------------------------------------------------------

    # Validating
    if ((arr[0] == 'ST300UEX') and (len(arr)>=18)):
        msg_devID = arr[1]
        msg_Date = arr[4]
        msg_Time = arr[5]
        msg_Latitude = arr[7]
        msg_Longitude = arr[8]
        msg_Power = arr[14]
        msg_IO = arr[15]
        msg_Length = arr[16]
        msg_Data = arr[17]

        if (len(arr)>=22):
            msg_CheckSum = arr[18]
            msg_Type = arr[21]        

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