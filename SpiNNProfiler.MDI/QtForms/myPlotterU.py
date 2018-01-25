import struct
from PyQt4 import Qt, QtGui, QtCore, QtNetwork
import PyQt4.Qwt5 as Qwt
#from PyQt4.Qwt5.anynumpy import *
from numpy import *

import constDef as DEF

DEF_SAVE_TO_FILE = False

"""==================================================================================
                                    class Uwidget 
----------------------------------------------------------------------------------"""
class Uwidget(QtGui.QWidget):
    okToClose = False
    pause = False
    def __init__(self, nChip, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.nChips = nChip
        self.saveToFile = DEF_SAVE_TO_FILE
        # Initialize GUI
        CHIPlabel = QtGui.QLabel("Chip", self)
        MODElabel = QtGui.QLabel("Mode", self)

        self.cbChip = QtGui.QComboBox(self)
        self.updateNChips(nChip)
        self.cbChip.setCurrentIndex(0)
        self.cbChip.currentIndexChanged.connect(self.changeChip)
        
        self.cbMode = QtGui.QComboBox(self)
        self.cbMode.addItem("Absolute")
        self.cbMode.addItem("Relative")
        self.modeIdx = 0
        self.cbMode.setCurrentIndex(self.modeIdx)
        self.cbMode.currentIndexChanged.connect(self.changeMode)

        self.pbPause = QtGui.QPushButton("Pause")
        self.pbPause.clicked.connect(self.pbPauseClicked)
        
        self.pList = list()
        for i in range(18):
        #for i in range(20): # Make it more convenient for 4x5 grid
            qwtu = UPlot(nChip, i)
            self.pList.append(qwtu)
            self.pList[i].chipChanged(self.cbChip.currentIndex())
       
        # Let's arrange into 4x5 grid
        vLayout = QtGui.QVBoxLayout()
        #vLayout.addLayout(hLayout)
        idx = 0
        for i in range(4):
            if i<3:
                l = QtGui.QHBoxLayout()
                for j in range(5):
                    l.addWidget(self.pList[idx])
                    idx += 1
                vLayout.addLayout(l)
            else:
                l = QtGui.QHBoxLayout()
                for j in range(3):
                    l.addWidget(self.pList[idx])
                    idx += 1
                l.addSpacing(20)
                l.addWidget(CHIPlabel)
                l.addWidget(self.cbChip)
                l.addSpacing(10)
                l.addWidget(MODElabel)
                l.addWidget(self.cbMode)
                l.addSpacing(30)
                l.addWidget(self.pbPause)
                l.addSpacing(340)
                #l.addStretch()
                vLayout.addLayout(l)
        self.setLayout(vLayout)
        self.setWindowTitle("CPU Utilization Report")

    """
    ######################### GUI callback ########################### 
    """
    def pbPauseClicked(self):
        if not self.pause:
            self.pbPause.setText("Run")
            for i in range(18):
                self.pList[i].pause = True
        else:
            self.pbPause.setText("Pause")
            for i in range(18):
                self.pList[i].pause = False
        self.pause = not self.pause

    def populateChipInfo(self):
        self.cbChip.clear()
        if self.nChips == 4:
            clist = DEF.CHIP_LIST_4
        else:
            clist = DEF.CHIP_LIST_48
        for i in range(self.nChips):
            chipStr = "chip<{},{}>".format(clist[i][0], clist[i][1]) # display: chip<x,y>
            self.cbChip.addItem(chipStr)
        
    def changeChip(self, idx):
        for i in range(18):
            self.pList[i].chipChanged(idx)
        self.updateCurveTitle()
        
    def changeMode(self, idx):
        for i in range(18):
            self.pList[i].modeChanged(idx)

    def newData(self, datagram):
        # Let's parse data here!

        fmt = "<H4BH2B2H3I18I"
        pad, flags, tag, dp, sp, da, say, sax, cmd, freq, temp1, temp2, temp3, \
        cpu0, cpu1, cpu2, cpu3, cpu4, cpu5, cpu6, cpu7, cpu8, cpu9, cpu10, cpu11, \
        cpu12, cpu13, cpu14, cpu15, cpu16, cpu17 = struct.unpack(fmt, datagram)

        chipID = sax*2+say
        cpuVal = [cpu0, cpu1, cpu2, cpu3, cpu4, cpu5, cpu6, cpu7, cpu8, cpu9, cpu10, cpu11, cpu12, cpu13, cpu14, cpu15, cpu16, cpu17]

        #### TODO: map to virtual core please!!! ####
        for i in range(18):
            self.pList[i].newData(chipID, cpuVal[i], freq)

        # save to files
        if self.saveToFile is True:
            seq = sax * 2 + say
            iVal = str(seq)
            for i in range(18):
                cpuStr = ",%d" % cpuVal[i]
                iVal += cpuStr
            iVal += "\n"
            self.Ufiles[seq].write(iVal)

    def saveToFileTriggered(self, state, dirName):
        """
        Will be triggered by Main Window
        """
        if state is True:
            for i in range(self.nChip):
                fName = dirName + '/idle.' + str(i)
                print "Creating file {}".format(fName)
                self.Ufiles[i] = open(fName, 'w')
            self.saveToFile = True

        else:
            self.saveToFile = False
            for i in range(self.nChip):
                if self.Ufiles[i] is not None:
                    self.Ufiles[i].close()
                    self.Ufiles[i] = None

    def updateP2Vmap(self, idx, cpuVal):
        self.p2vMap[idx] = cpuVal
        self.updateCurveTitle()

    def updateNChips(self, nc):
        self.nChips = nc
        self.populateChipInfo()
        # Reset p2vMap
        self.p2vMap = [[c for c in range(18)] for i in range(nc)]

    def updateCurveTitle(self):
        # use self.cbChip.currentIndex() to select the corresponding list
        chipIdx = self.cbChip.currentIndex()
        for i in range(18): # the index here is physical core, not virtual core!!!
            physCore = i
            virtCore = "Core-%d" % (self.p2vMap[chipIdx][physCore])
            self.pList[i].c.setTitle(virtCore)

    def closeEvent(self, event):
        if self.okToClose:
            event.accept()
        else:
            event.ignore()
            
            
            
"""==================================================================================
                                    class UPlot() 
----------------------------------------------------------------------------------"""
class UPlot(Qwt.QwtPlot):
    pause = False
    def __init__(self, nChip, myID, *args):
        Qwt.QwtPlot.__init__(self, *args)

        self.myID = myID
        self.cpuIdx = 0
        self.chipIdx = 0
        self.modeIdx = 0
        self.nChip = nChip
        if myID < 18:        
            self.setCanvasBackground(Qt.Qt.white)
        else:
            self.setCanvasBackground(Qt.QColor(212,212,212))
            self.enableAxis(Qwt.QwtPlot.xBottom, False)
            self.enableAxis(Qwt.QwtPlot.yLeft, False)
            self.canvas().setFrameStyle(Qt.QFrame.NoFrame or Qt.QFrame.Plain)
            #qpl= Qt.QPalette()
            #qpl.setColor(Qt.QPalette.Active,Qt.QPalette.Window,Qt.QColor(212,212,212));
            #qpl.setColor(Qt.QPalette.Inactive,Qt.QPalette.Window,Qt.QColor(212,212,212));
            #qpl.setColor(Qt.QPalette.Disabled,Qt.QPalette.Window,Qt.QColor(212,212,212));
            #self.canvas().setPalette(qpl)

        self.alignScales()

        # Initialize data
        self.x = arange(0.0, 100.1, 0.5)

        # Initialize working parameters
        self.saveToFile = DEF_SAVE_TO_FILE
        # To avoid writing conflict, only core-0 is allowed to save to files
        if self.myID==0:
            self.Ufiles = list()
            for i in range(nChip):
                self.Ufiles.append(None)
       
        self.u = list()     # list of list, contains the utilization value for ALL chips
        #self.c = list()     # contains the curve value
        for i in range(nChip):
            y = zeros(len(self.x), float)
            self.u.append(y)
        #for i in range(18): # for all 18 cores in a chip
        if self.myID < 18:
            cname = "Core-%d" % (self.myID)
        else:
            cname = ""
        self.c = Qwt.QwtPlotCurve(cname)

        ## Color contants
        clr = [Qt.Qt.red, Qt.Qt.green, Qt.Qt.blue, Qt.Qt.cyan, Qt.Qt.magenta, Qt.Qt.yellow, Qt.Qt.black, Qt.Qt.gray, \
               Qt.Qt.darkRed, Qt.Qt.darkGreen, Qt.Qt.darkBlue, Qt.Qt.darkCyan, Qt.Qt.darkMagenta, Qt.Qt.darkYellow, \
               Qt.Qt.darkGray, Qt.Qt.lightGray, \
               Qt.QColor(Qt.qRgb(255,192,203)), Qt.QColor(Qt.qRgb(139,69,19)), Qt.QColor(Qt.qRgb(128, 0, 0)), Qt.Qt.white]
        #Pink: rgb(255,192,203), Brown: rgb(139,69,19), Maron: rgb(128,0,0)
        
        self.c.attach(self)
        if self.myID < 18:
            self.c.setPen(Qt.QPen(clr[self.myID], DEF.PEN_WIDTH))
            self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.BottomLegend);       
        else:
            self.c.setPen(Qt.QPen(Qt.QColor(212,212,212), DEF.PEN_WIDTH))
        
        #self.setTitle("Chip Utilization Report")
        #self.setAxisTitle(Qwt.QwtPlot.xBottom, "Time (seconds)")
        #self.setAxisTitle(Qwt.QwtPlot.yLeft, "Counter Values")
    

    def alignScales(self):
        self.canvas().setFrameStyle(Qt.QFrame.Box | Qt.QFrame.Plain)
        self.canvas().setLineWidth(1)
        for i in range(Qwt.QwtPlot.axisCnt):
            scaleWidget = self.axisWidget(i)
            if scaleWidget:
                scaleWidget.setMargin(0)
            scaleDraw = self.axisScaleDraw(i)
            if scaleDraw:
                scaleDraw.enableComponent(
                    Qwt.QwtAbstractScaleDraw.Backbone, False)

    def newData(self, chipID, cpuVal, freq):    
        self.u[chipID] = concatenate((self.u[chipID][:1], self.u[chipID][:-1]), 1)
        if self.modeIdx==0: #use absolute values
            self.u[chipID][0] = cpuVal
        else:
            ## TODO: change to relative 
            #Due to Timer2 usage, we need to scale the maximum Idle counter
            m = (DEF.MAX_IDLE_CNTR[1] - DEF.MAX_IDLE_CNTR[0]) / (250-10)
            b = DEF.MAX_IDLE_CNTR[1] - m*250
            maxIdleCntr = m*freq+b
            uVal = (maxIdleCntr - cpuVal) * 100 / maxIdleCntr
            if uVal <0:
                uVal = 0
            elif uVal > 100:
                uVal = 100
            self.u[chipID][0] = uVal
        self.c.setData(self.x, self.u[self.chipIdx])
        if not self.pause:
            self.replot()

    def chipChanged(self, idx):
        self.chipIdx = idx
        
    def modeChanged(self, idx):
        self.modeIdx = idx
        if idx==0:
            #self.setAxisTitle(Qwt.QwtPlot.yLeft, "Counter Values")
            self.setAxisAutoScale(Qwt.QwtPlot.yLeft)
        else:
            #self.setAxisTitle(Qwt.QwtPlot.yLeft, "Percent")
            self.setAxisScale(Qwt.QwtPlot.yLeft, 0, 100)
         

# class DataPlot
