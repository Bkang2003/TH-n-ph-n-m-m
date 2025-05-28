'''
/******************************************************************************
*
* (c) 2025 by FreyrSCADA Embedded Solution Pvt Ltd
*
********************************************************************************
*
* Disclaimer: This program is an example and should be used as such.
*             If you wish to use this program or parts of it in your application,
*             you must validate the code yourself.  FreyrSCADA Embedded Solution Pvt Ltd
*             can not be held responsible for the correct functioning
*             or coding of this example
*******************************************************************************/

/*****************************************************************************/
/*! \file       iec104clienttest.py
 *  \brief      Python Source code file, IEC 60870-5-104 Client library test program - Auto Generation IEC104 Data
 *
 *  \par        FreyrSCADA Embedded Solution Pvt Ltd
 *              Email   : support@freyrscada.com
 */
/*****************************************************************************/
'''

import ctypes 
import time
import struct
import sys

from iec104api import *
from tgtcommon import *

# enbale to view traffic
VIEW_TRAFFIC = 1

# print the struct sIEC104DataAttributeID and sIEC104DataAttributeData
def vPrintDataInformation(psIEC104DataAttributeID , psIEC104DataAttributeData ):
    print(f" IP Address {psIEC104DataAttributeID.contents.ai8IPAddress}")
    print(f" Port Number {psIEC104DataAttributeID.contents.u16PortNumber}")
    print(f" Common Address {psIEC104DataAttributeID.contents.u16CommonAddress}")
    print(f" Typeid ID is {psIEC104DataAttributeID.contents.eTypeID} IOA   {psIEC104DataAttributeID.contents.u32IOA}")
    print(f" Datatype->{psIEC104DataAttributeData.contents.eDataType} Datasize->{ psIEC104DataAttributeData.contents.eDataSize}" )

    if(psIEC104DataAttributeData.contents.tQuality) != eIEC870QualityFlags.GD :
        if(psIEC104DataAttributeData.contents.tQuality & eIEC870QualityFlags.IV) == eIEC870QualityFlags.IV:
            print(" IEC_INVALID_FLAG")
        if(psIEC104DataAttributeData.contents.tQuality & eIEC870QualityFlags.NT) == eIEC870QualityFlags.NT:
             print(" IEC_NONTOPICAL_FLAG")
        if(psIEC104DataAttributeData.contents.tQuality & eIEC870QualityFlags.SB) == eIEC870QualityFlags.SB:
             print(" IEC_SUBSTITUTED_FLAG")
        if(psIEC104DataAttributeData.contents.tQuality & eIEC870QualityFlags.BL) == eIEC870QualityFlags.BL:
             print(" IEC_BLOCKED_FLAG")

    data_type = psIEC104DataAttributeData.contents.eDataType

    if data_type in (eDataTypes.SINGLE_POINT_DATA, eDataTypes.DOUBLE_POINT_DATA, eDataTypes.UNSIGNED_BYTE_DATA):
        data = bytearray(ctypes.string_at(psIEC104DataAttributeData.contents.pvData, 1))
        u8data = struct.unpack('B', data)[0] 
        print(f" Data : {u8data}")

    elif data_type == eDataTypes.SIGNED_BYTE_DATA:
        data = bytearray(ctypes.string_at(psIEC104DataAttributeData.contents.pvData, 1))
        i8data = struct.unpack('b', data)[0]        
        print(f" Data : {i8data}")

    elif data_type == eDataTypes.UNSIGNED_WORD_DATA:
        data = bytearray(ctypes.string_at(psIEC104DataAttributeData.contents.pvData, 2))
        u16data = struct.unpack('H', data)[0]        
        print(f" Data : {u16data}")

    elif data_type == eDataTypes.SIGNED_WORD_DATA:
        data = bytearray(ctypes.string_at(psIEC104DataAttributeData.contents.pvData, 2))
        i16data = struct.unpack('h', data)[0]        
        print(f" Data : {i16data}")

    elif data_type == eDataTypes.UNSIGNED_DWORD_DATA:
        data = bytearray(ctypes.string_at(psIEC104DataAttributeData.contents.pvData, 4))
        u32data = struct.unpack('I', data)[0]        
        print(f" Data : {u32data}")


    elif data_type == eDataTypes.SIGNED_DWORD_DATA:
        data = bytearray(ctypes.string_at(psIEC104DataAttributeData.contents.pvData, 4))
        i32data = struct.unpack('i', data)[0]        
        print(f" Data : {i32data}")

    elif data_type == eDataTypes.FLOAT32_DATA:
        data = bytearray(ctypes.string_at(psIEC104DataAttributeData.contents.pvData, 4))
        f32data = struct.unpack('f', data)[0] 
        print(f" Data : {f32data:.3f}")

    if psIEC104DataAttributeData.contents.sTimeStamp.u16Year != 0:
        print(f" Date : {psIEC104DataAttributeData.contents.sTimeStamp.u8Day:02}-{psIEC104DataAttributeData.contents.sTimeStamp.u8Month:02}-{psIEC104DataAttributeData.contents.sTimeStamp.u16Year:04}  DOW -{psIEC104DataAttributeData.contents.sTimeStamp.u8DayoftheWeek}")
        print(f" Time : {psIEC104DataAttributeData.contents.sTimeStamp.u8Hour:02}:{psIEC104DataAttributeData.contents.sTimeStamp.u8Minute:02}:{psIEC104DataAttributeData.contents.sTimeStamp.u8Seconds:02}:{psIEC104DataAttributeData.contents.sTimeStamp.u16MilliSeconds:03}")

# update callback
def cbUpdate(u16ObjectId, psIEC104DataAttributeID, psIEC104DataAttributeData, psIEC104UpdateParameters, ptErrorValue):
    i16rErrorCode = ctypes.c_short()
    i16rErrorCode = 0   
    print(" cbUpdate() called ")
    print(" Client ID : %u" % u16ObjectId)
    vPrintDataInformation(psIEC104DataAttributeID, psIEC104DataAttributeData)
    message = f" COT {psIEC104UpdateParameters.contents.eCause}"
    print(message)
    
    return i16rErrorCode

# Client connection Status Callback
def cbClientStatus(u16ObjectId, psIEC104ClientConnectionID , peSat, ptErrorValue):

    i16rErrorCode = ctypes.c_short()
    i16rErrorCode = 0   
    print(" cbClientStatus called -  from IEC104 client")

    print(" Server ID : %u" % u16ObjectId)
    print(" IP Address %s Port %u " % (psIEC104ClientConnectionID.contents.ai8IPAddress, psIEC104ClientConnectionID.contents.u16PortNumber))
    print(" Server CA : %u" % psIEC104ClientConnectionID.contents.u16CommonAddress)

    if peSat.contents.value == eStatus.CONNECTED:
        print(" Status - Connected")
    else:
        print(" Status - Disconnected")
    
   
    return i16rErrorCode

# Debug callback
def cbDebug(u16ObjectId,  psIEC104DebugData , ptErrorValue):
    
    i16rErrorCode = ctypes.c_short()
    i16rErrorCode = 0 

    # u16nav = ctypes.c_ushort()
    u16nav = 0
   
    #print(" cbDebug() called")
    
    print(f" {psIEC104DebugData.contents.sTimeStamp.u8Hour}:{psIEC104DebugData.contents.sTimeStamp.u8Minute}:{psIEC104DebugData.contents.sTimeStamp.u8Seconds} Server ID: {u16ObjectId}",end='')
    
    if (psIEC104DebugData.contents.u32DebugOptions & eDebugOptionsFlag.DEBUG_OPTION_TX) == eDebugOptionsFlag.DEBUG_OPTION_TX:
        print(f" send IP {psIEC104DebugData.contents.ai8IPAddress} Port {psIEC104DebugData.contents.u16PortNumber}", end='')
        print(" ->", end='')
        
        u16nav = 0
        for u16nav in range(int(psIEC104DebugData.contents.u16TxCount)):
            #print(f" {psIEC104DebugData.contents.au8TxData[u16nav]:02x}", end='')
            try:
                print(f" {psIEC104DebugData.contents.au8TxData[u16nav]:02x}", end='')
            except TypeError:
                print("TypeError: Check list of indices")
        
    
        
    if (psIEC104DebugData.contents.u32DebugOptions & eDebugOptionsFlag.DEBUG_OPTION_RX) == eDebugOptionsFlag.DEBUG_OPTION_RX:
        print(f" receive IP {psIEC104DebugData.contents.ai8IPAddress} Port {psIEC104DebugData.contents.u16PortNumber}", end='')
        print(" <-", end='')

        #print(f"u16RxCount - {psIEC104DebugData.contents.u16RxCount} len aaray - {len(psIEC104DebugData.contents.au8RxData)}")

        
        for u16nav in range(int(psIEC104DebugData.contents.u16RxCount)):
            print(f" {psIEC104DebugData.contents.au8RxData[u16nav]:02x}", end='')
      

        
    if (psIEC104DebugData.contents.u32DebugOptions & eDebugOptionsFlag.DEBUG_OPTION_ERROR) == eDebugOptionsFlag.DEBUG_OPTION_ERROR:
        print(f" Error message {psIEC104DebugData.contents.au8ErrorMessage}")
        print(f" ErrorCode {psIEC104DebugData.contents.iErrorCode}")
        print(f" ErrorValue {psIEC104DebugData.contents.tErrorvalue}")

    print("", flush=True)

    return i16rErrorCode

# print error code and description
def errorcodestring(errorcode):
    sIEC104ErrorCodeDes = sIEC104ErrorCode()
    sIEC104ErrorCodeDes.iErrorCode = errorcode
    iec104_lib.IEC104ErrorCodeString(sIEC104ErrorCodeDes)
    return sIEC104ErrorCodeDes.LongDes.decode("utf-8")

# print error value and description
def errorvaluestring(errorvalue):
    sIEC104ErrorValueDes = sIEC104ErrorValue()
    sIEC104ErrorValueDes.iErrorValue = errorvalue   
    iec104_lib.IEC104ErrorValueString(sIEC104ErrorValueDes)
    return sIEC104ErrorValueDes.LongDes.decode("utf-8")
def autoSendDistance(myClient):
    import random
    while True:
        f32value = ctypes.c_float(random.uniform(10, 100))  # khoảng cách giả lập

        psDAID = sIEC104DataAttributeID()
        psNewValue  = sIEC104DataAttributeData()
        psIEC104CommandParameters = sIEC104CommandParameters()

        psDAID.ai8IPAddress = "127.0.0.1".encode('utf-8')
        psDAID.u16PortNumber = 2404
        psDAID.u16CommonAddress = 1
        psDAID.eTypeID = eIEC870TypeID.M_ME_NC_1  # kiểu đo analog
        psDAID.u32IOA = 100  # IOA bạn quy định
        psDAID.pvUserData = None

        psNewValue.tQuality = eIEC870QualityFlags.GD
        psNewValue.pvData = ctypes.c_void_p(ctypes.addressof(f32value))
        psNewValue.eDataType = eDataTypes.FLOAT32_DATA
        psNewValue.eDataSize = eDataSizes.FLOAT32_SIZE

        now = time.localtime()
        psNewValue.sTimeStamp.u8Day = now.tm_mday
        psNewValue.sTimeStamp.u8Month = now.tm_mon
        psNewValue.sTimeStamp.u16Year = now.tm_year
        psNewValue.sTimeStamp.u8Hour = now.tm_hour
        psNewValue.sTimeStamp.u8Minute = now.tm_min
        psNewValue.sTimeStamp.u8Seconds = now.tm_sec
        psNewValue.sTimeStamp.u16MilliSeconds = 0
        psNewValue.bTimeInvalid = False

        tErrorValue = ctypes.c_short()
        result = iec104_lib.IEC104UpdateData(myClient, ctypes.byref(psDAID), ctypes.byref(psNewValue), ctypes.byref(psIEC104CommandParameters), ctypes.byref(tErrorValue))

        if result != 0:
            print(f"[ERROR] Send failed → {errorcodestring(result)} / {errorvaluestring(tErrorValue.value)}")
        else:
            print(f"[INFO] Distance sent: {f32value.value:.2f} cm")

        time.sleep(1)


# main program
def main():
    
    print(" \t\t**** IEC 60870-5-104 Protocol Client Library Test ****")
    
    # Check library version against the library header file
    if iec104_lib.IEC104GetLibraryVersion().decode("utf-8") != IEC104_VERSION:
        print(" Error: Version Number Mismatch")
        print(" Library Version is  : {}".format(iec104_lib.IEC104GetLibraryVersion().decode("utf-8")))
        print(" The Header Version used is : {}".format(IEC104_VERSION))
        print("")
        input(" Press Enter to free IEC 104 client object")
        exit(0)

    print(" Library Version is : {}".format(iec104_lib.IEC104GetLibraryVersion().decode("utf-8")))
    print(" Library Build on   : {}".format(iec104_lib.IEC104GetLibraryBuildTime().decode("utf-8")))
    print(" Library License Information   : {}".format(iec104_lib.IEC104GetLibraryLicenseInfo().decode("utf-8")))

    i16ErrorCode = ctypes.c_short()
    tErrorValue =  ctypes.c_short()

    sParameters = sIEC104Parameters()

   

    # Initialize IEC 60870-5-104 Server object parameters
    sParameters.eAppFlag          =  eApplicationFlag.APP_CLIENT        # This is a IEC104 Server      
    sParameters.ptReadCallback    = IEC104ReadCallback(0)               # Read Callback
    sParameters.ptWriteCallback   = IEC104WriteCallback(0)                # Write Callback
    sParameters.ptUpdateCallback  = IEC104UpdateCallback(cbUpdate)                 # Update Callback
    sParameters.ptSelectCallback  = IEC104ControlSelectCallback(0)               # Select Callback
    sParameters.ptOperateCallback = IEC104ControlOperateCallback(0)              # Operate Callback
    sParameters.ptCancelCallback  = IEC104ControlCancelCallback(0)              # Cancel Callback
    sParameters.ptFreezeCallback  = IEC104ControlFreezeCallback(0)              # Freeze Callback
    sParameters.ptDebugCallback   = IEC104DebugMessageCallback(cbDebug)                # Debug Callback
    sParameters.ptPulseEndActTermCallback = IEC104ControlPulseEndActTermCallback(0)    # pulse end callback
    sParameters.ptParameterActCallback = IEC104ParameterActCallback(0)   # Parameter activation callback
    sParameters.ptServerStatusCallback = IEC104ServerStatusCallback(0)   # server status callback
    sParameters.ptDirectoryCallback    = IEC104DirectoryCallback(0)              # Directory Callback
    sParameters.ptClientStatusCallback   = IEC104ClientStatusCallback(cbClientStatus)           # client connection status Callback
    sParameters.u32Options        = 0
    sParameters.u16ObjectId				= 1				#Server ID which used in callbacks to identify the iec 104 server object   


    # Create a CLIENT object

    myClient =  iec104_lib.IEC104Create(ctypes.byref(sParameters), ctypes.byref((i16ErrorCode)), ctypes.byref((tErrorValue)))
    if i16ErrorCode.value != 0:
        message = f"IEC 60870-5-104 Library API Function - IEC104Create() failed: {i16ErrorCode.value} - {errorcodestring(i16ErrorCode)}, {tErrorValue.value} - {errorvaluestring(tErrorValue)}"
        print(message)    
        exit(0) 
    else:
        message = f"IEC 60870-5-104 Library API Function - IEC104Create() success"
        print(message) 

    while(True):

        sIEC104Config = sIEC104ConfigurationParameters()

        # Client load configuration - communication and protocol configuration parameters
        sIEC104Config.sClientSet.ai8SourceIPAddress ="0.0.0.0".encode('utf-8')	# client own IP Address , use 0.0.0.0 / network ip address for binding socket*/   
		
        sIEC104Config.sClientSet.benabaleUTCtime    =   False
        
        
        # Debug option settings
        if  'VIEW_TRAFFIC' in globals():
            sIEC104Config.sClientSet.sDebug.u32DebugOptions   =   (eDebugOptionsFlag.DEBUG_OPTION_RX | eDebugOptionsFlag.DEBUG_OPTION_TX)
        else:
            sIEC104Config.sClientSet.sDebug.u32DebugOptions  =   0
        



        sIEC104Config.sClientSet.u16TotalNumberofConnection =   1

        arraypointer = (sClientConnectionParameters * sIEC104Config.sClientSet.u16TotalNumberofConnection)()
        sIEC104Config.sClientSet.psClientConParameters  = ctypes.cast(arraypointer, ctypes.POINTER(sClientConnectionParameters))

        #client 1 configuration Starts
		#check server configuration - TCP/IP Address
	    
        arraypointer[0].ai8DestinationIPAddress="127.0.0.1".encode('utf-8')  #iec 104 server ip address
        arraypointer[0].u16PortNumber             =   2404  # iec 104 server port number


        arraypointer[0].i16k                      =   12
        arraypointer[0].i16w                      =   8
        arraypointer[0].u8t0                      = 30
        arraypointer[0].u8t1                      = 15
        arraypointer[0].u8t2                      = 10
        arraypointer[0].u16t3                     = 20

        arraypointer[0].eState =  eConnectState.DATA_MODE
        arraypointer[0].u8TotalNumberofStations           =   1
        arraypointer[0].au16CommonAddress[0]          =   1
        arraypointer[0].au16CommonAddress[1]          =   0
        arraypointer[0].au16CommonAddress[2]          =   0
        arraypointer[0].au16CommonAddress[3]          =   0
        arraypointer[0].au16CommonAddress[4]          =   0
        arraypointer[0].u8OriginatorAddress           =   0


        arraypointer[0].u32GeneralInterrogationInterval   =   0    # in sec if 0 , gi will not send in particular interval
        arraypointer[0].u32Group1InterrogationInterval    =   0    # in sec if 0 , group 1 interrogation will not send in particular interval*/
        arraypointer[0].u32Group2InterrogationInterval    =   0    # in sec if 0 , group 1 interrogation will not send in particular interval*/
        arraypointer[0].u32Group3InterrogationInterval    =   0    # in sec if 0 , group 1 interrogation will not send in particular interval*/
        arraypointer[0].u32Group4InterrogationInterval    =   0    # in sec if 0 , group 1 interrogation will not send in particular interval*/
        arraypointer[0].u32Group5InterrogationInterval    =   0    # in sec if 0 , group 1 interrogation will not send in particular interval*/
        arraypointer[0].u32Group6InterrogationInterval    =   0    # in sec if 0 , group 1 interrogation will not send in particular interval*/
        arraypointer[0].u32Group7InterrogationInterval    =   0    # in sec if 0 , group 1 interrogation will not send in particular interval*/
        arraypointer[0].u32Group8InterrogationInterval    =   0    # in sec if 0 , group 1 interrogation will not send in particular interval*/
        arraypointer[0].u32Group9InterrogationInterval    =   0    # in sec if 0 , group 1 interrogation will not send in particular interval*/
        arraypointer[0].u32Group10InterrogationInterval   =   0    # in sec if 0 , group 1 interrogation will not send in particular interval*/
        arraypointer[0].u32Group11InterrogationInterval   =   0    # in sec if 0 , group 1 interrogation will not send in particular interval*/
        arraypointer[0].u32Group12InterrogationInterval   =   0    # in sec if 0 , group 1 interrogation will not send in particular interval*/
        arraypointer[0].u32Group13InterrogationInterval   =   0    # in sec if 0 , group 1 interrogation will not send in particular interval*/
        arraypointer[0].u32Group14InterrogationInterval   =   0    # in sec if 0 , group 1 interrogation will not send in particular interval*/
        arraypointer[0].u32Group15InterrogationInterval   =   0    # in sec if 0 , group 1 interrogation will not send in particular interval*/
        arraypointer[0].u32Group16InterrogationInterval   =   0    # in sec if 0 , group 1 interrogation will not send in particular interval*/
        arraypointer[0].u32CounterInterrogationInterval   =   0    # in sec if 0 , ci will not send in particular interval*/
        arraypointer[0].u32Group1CounterInterrogationInterval =   0    # in sec if 0 , group 1 counter interrogation will not send in particular interval*/
        arraypointer[0].u32Group2CounterInterrogationInterval =   0    # in sec if 0 , group 1 counter interrogation will not send in particular interval*/
        arraypointer[0].u32Group3CounterInterrogationInterval =   0    # in sec if 0 , group 1 counter interrogation will not send in particular interval*/
        arraypointer[0].u32Group4CounterInterrogationInterval =   0    # in sec if 0 , group 1 counter interrogation will not send in particular interval*/
        arraypointer[0].u32ClockSyncInterval  =   0              # in sec if 0 , clock sync, will not send in particular interval */

        arraypointer[0].u32CommandTimeout =   10000
        arraypointer[0].u32FileTransferTimeout    =   50000
        arraypointer[0].bCommandResponseActtermUsed   =   True


        arraypointer[0].bEnablefileftransfer = False
        arraypointer[0].ai8FileTransferDirPath = "C:\\".encode('utf-8') 
        arraypointer[0].bUpdateCallbackCheckTimestamp = False
        arraypointer[0].eCOTsize = eCauseofTransmissionSize.COT_TWO_BYTE
        
        sIEC104Config.sClientSet.bAutoGenIEC104DataObjects = True
        # Define number of objects
        arraypointer[0].u16NoofObject             =   0
        # Allocate memory for objects
        arraypointer[0].psIEC104Objects = None

        # client 1 configuration ends

       
        i16ErrorCode =  iec104_lib.IEC104LoadConfiguration(myClient, ctypes.byref(sIEC104Config), ctypes.byref((tErrorValue)))
        if i16ErrorCode != 0:
            message = f"IEC 60870-5-104 Library API Function - IEC104LoadConfiguration() failed: {i16ErrorCode} - {errorcodestring(i16ErrorCode)}, {tErrorValue.value} - {errorvaluestring(tErrorValue)}"
            print(message)    
            break

        else:
            message = f"IEC 60870-5-104 Library API Function - IEC104LoadConfiguration() success"
            print(message) 



        i16ErrorCode =  iec104_lib.IEC104Start(myClient, ctypes.byref((tErrorValue)))
        if i16ErrorCode != 0:
            message = f"IEC 60870-5-104 Library API Function - IEC104Start() failed: {i16ErrorCode} - {errorcodestring(i16ErrorCode)}, {tErrorValue.value} - {errorvaluestring(tErrorValue)}"
            print(message)    
            break

        else:
            message = f"IEC 60870-5-104 Library API Function - IEC104Start() success"
            print(message) 

        print("press x to exit")

        print("Client running... sending sensor data every second")
        autoSendDistance(myClient)


        break
            
            

      



    i16ErrorCode =  iec104_lib.IEC104Stop(myClient, ctypes.byref((tErrorValue)))
    if i16ErrorCode != 0:
        message = f"IEC 60870-5-104 Library API Function - IEC104Stop() failed: {i16ErrorCode} - {errorcodestring(i16ErrorCode)}, {tErrorValue.value} - {errorvaluestring(tErrorValue)}"
        print(message)        
    else:
        message = f"IEC 60870-5-104 Library API Function - IEC104Stop() success"
        print(message) 



    i16ErrorCode =  iec104_lib.IEC104Free(myClient, ctypes.byref((tErrorValue)))
    if i16ErrorCode != 0:
        message = f"IEC 60870-5-104 Library API Function - IEC104Free() failed: {i16ErrorCode} - {errorcodestring(i16ErrorCode)}, {tErrorValue.value} - {errorvaluestring(tErrorValue)}"
        print(message)    
    else:
        message = f"IEC 60870-5-104 Library API Function - IEC104Free() success"
        print(message) 


    print("Exiting the program...")
      

if __name__ == "__main__":
    main()
