#! /usr/bin/python
import os, sys, time, getopt
import numpy
import serial

# Default constants used by Arduino
ADC_Bits = 4096 # 12-bit ADC
V_ref = 2.5
R_shunt = [0.005*50, 0.005*50, 0.005*50, 0.010*50, 0.005*50, 0.010*50, 0.005*50]
#V_div = [1, 1, 1, 1, 1, 1.5, 6]
V_div = [1, 1, 1, 1, 1, 1.5, 6*0.75]
pwr_label = ["BankA","BankB","BankC","FPGA","SDRAM","BMP","Mains"]

# Get log default directory
SERIAL_PORT = '/dev/ttyACM0'
DEF_LOG_DIR = './'
logFile = None
sPort = None
tStart = 0
dump = False

def displayHelp():
    print 'Usage:'
    print '\tprofiler_cli -h'
    print '\tprofiler_cli -d'
    print '\tprofiler_cli --dump'
    print 'Use the -d (or --dump) option to dump the reading on the screen'

def readCLI(argv):
   global dump
   try:
      opts, args = getopt.getopt(argv,"hd",["dump"])
   except getopt.GetoptError:
      displayHelp()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
	 displayHelp()
	 sys.exit()
      elif opt in ("-d", "--dump"):
	 dump = True

def sOpen():
    global sPort
    sPort = serial.Serial()
    sPort.port = SERIAL_PORT
    sPort.baudrate = 115200
    sPort.bytesize = 8
    sPort.parity = 'N'
    sPort.stopbits = 1
    sPort.timeout = None
    print "[INFO] Try to open the port...",
    sPort.open()
    if sPort.is_open is True:
        print "done!"
    else:
        print "fail!"
    return sPort.is_open

def convert(val):
    """
    Convert raw data into power values. The raw data has 15 elements (including timestamp at last position)

    """
    res = None
    try:
        rawData = map(int, val)
        # rawData has the following format:
        # I_BankA, V_BankA, I_BankB, V_BankB, I_BankC, V_BankC, I_FPGA, V_FPGA, I_SDRAM,
        # V_SDRAM, I_BMP, V_ALL, V_BMP, I_All -> then it needs to be modified!!!

        pwrData = [0 for _ in range(7)]
        #modData = numpy.concatenate((rawData[:11], rawData[13:], rawData[11:13]))
        modData = numpy.concatenate((rawData[:11], rawData[12:13], rawData[11:12], rawData[13:14]))
        for i in range(7):
            pwrData[i] = (modData[i*2]*V_ref/(ADC_Bits*R_shunt[i])) *\
                         (modData[i*2+1]*V_ref*V_div[i]/(ADC_Bits))

        res = "{},{},{},{},{},{},{}".format(pwrData[0],pwrData[1],pwrData[2],pwrData[3],\
                                            pwrData[4],pwrData[5],pwrData[6])
    except ValueError as ve:
        print "Value error on arduinoData:", ve
    return res

def readP():
    """
    Read the SpiNN-4 power through serial port
    """
    global tStart
    l = sPort.readline()
    v = l.split(',')
    if len(v) is not 15:
        return
    else:
        if dump is True:
            print l,
        tNow = time.time()
        t = time.strftime('%H,%M,%S')
        if tStart is 0:
            tStart = tNow
        tms = int((tNow - tStart)*1000)

        #s = "{},{}".format(time.time() - tStart, l)
        #t = time.strftime('%H:%M:%S:')
        #s = "{}{}-->{}".format(t,int((time.time()-tStart)*1000), l)

        pwr = convert(v)
        if pwr is not None:
            s = "{},{},{}\n".format(tms,t, pwr)
            logFile.write(s)

def main():
    readCLI(sys.argv[1:])

    # check if we have access to the port
    print "[INFO] Will be using {} for power reading".format(SERIAL_PORT)
    ok = os.access(SERIAL_PORT, os.R_OK)
    if ok is False:
        print "[ERR!] Cannot access the serial port!"
        print "[INFO] Try change the access permision of {} !!!".format(SERIAL_PORT)
        sys.exit(-1)

    global logFile

    # Open serial port
    if sOpen() is False:
        print "[ERR!] Cannot open the serial port!"
        sys.exit(-1)

    # Open logfile
    fname = DEF_LOG_DIR + "profiling_at_" + time.strftime("%b_%d_%Y-%H.%M.%S", time.gmtime()) + ".log"
    logFile = open(fname, "w")
    print "[INFO] Start recording in {}...".format(fname)
    while True:
        try:
            readP()
        except KeyboardInterrupt:
            break
    print "\n[INFO] Closing the serial port...",
    print "done!"
    if logFile is not None:
        print "Closing log file {}...".format(fname),
        logFile.close()
        print "done!"
        print "The format of the data is:"
        print "millisecond, hour, minute, second, BankA , BankB, BankC, FPGA, SDRAM, BMP, Total power"

    print "Finished!"

if __name__=='__main__':
    main()

