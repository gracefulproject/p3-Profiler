import random
import struct
from PyQt4 import Qt, QtGui, QtCore, QtNetwork
import PyQt4.Qwt5 as Qwt
#from PyQt4.Qwt5.anynumpy import *
from numpy import *

import constDef as DEF

"""==================================================================================
                                    class Fwidget 
----------------------------------------------------------------------------------"""
class Fwidget(QtGui.QWidget):
    """
    Temperature plot
    """
    okToClose = False
    pause = False
    saveState = False  # Should we save to disk?
    def __init__(self, nChip, parent=None):
        """
        Layout: top : Dropbox Sensor and Mode
                bottom: QwtPlot 
        """
        QtGui.QWidget.__init__(self, parent)
        self.nChips = nChip
        Clabel = QtGui.QLabel("Chip", self)
        Flabel = QtGui.QLabel("Frequency", self)
        
        self.cbChip = QtGui.QComboBox(self)
        self.cbFreq = QtGui.QComboBox(self)
        fList = list()
        for i in range(260):
            if (i >= 10) and (i % 5 == 0):
                fStr = "%d" % i
                fList.append(fStr)
        self.cbFreq.addItems(fList)
        self.cbFreq.setCurrentIndex(self.getFreqIdx(200))

        self.pbSet = QtGui.QPushButton("Set")
        self.pbPause = QtGui.QPushButton("Pause")
        
        self.qwtFall = FPlot(nChip) # this will display all chips
        self.qwtF1 = FPlot(nChip)   # this will display the first selected chip
        self.qwtF2 = FPlot(nChip)   # this will display the second selected chip

        # Layouting
        vLayout = QtGui.QVBoxLayout()
        # The first row is for controlling frequency for specific chip and displaying all cores
        hLayout = QtGui.QHBoxLayout()
        hLayout.addWidget(Clabel)
        hLayout.addWidget(self.cbChip)
        hLayout.addSpacing(100)
        hLayout.addWidget(Flabel)
        hLayout.addWidget(self.cbFreq)
        hLayout.addSpacing(100)
        hLayout.addWidget(self.pbSet)
        hLayout.addSpacing(100)
        hLayout.addWidget(self.pbPause)
        hLayout.addStretch()
        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.qwtFall)
        # The second row is for displaying the first specific core
        F1Layout = QtGui.QHBoxLayout()
        F1Label = QtGui.QLabel("Select F1", self)
        self.cbChipF1 = QtGui.QComboBox(self)
        #self.updateNChips(nChip)
        F1Layout.addWidget(F1Label)
        F1Layout.addSpacing(20)
        F1Layout.addWidget(self.cbChipF1)
        F1Layout.addStretch()
        vLayout.addLayout(F1Layout)
        vLayout.addWidget(self.qwtF1)
        # The third row is for displaying the second specific core
        F2Layout = QtGui.QHBoxLayout()
        F2Label = QtGui.QLabel("Select F2", self)
        self.cbChipF2 = QtGui.QComboBox(self)
        F2Layout.addWidget(F2Label)
        F2Layout.addSpacing(20)
        F2Layout.addWidget(self.cbChipF2)
        F2Layout.addStretch()
        vLayout.addLayout(F2Layout)
        vLayout.addWidget(self.qwtF2)
        self.setLayout(vLayout)
        self.setWindowTitle("Chip Frequency (MHz)")
        
        # Initial values
        self.updateNChips(nChip)
        
        # SIGNAL-SLOT mechanism
        self.pbSet.clicked.connect(self.pbSetClicked)
        self.pbPause.clicked.connect(self.pbPauseClicked)
        self.cbChipF1.currentIndexChanged.connect(self.selectF1Update)
        self.cbChipF2.currentIndexChanged.connect(self.selectF2Update)
        
        # Trigger for plot F1 and F2
        self.cbChipF1.setCurrentIndex(self.cbChipF1.count()-1)
        self.cbChipF2.setCurrentIndex(self.cbChipF2.count()-1)
        
    """
    ######################### Parameters update ########################### 
    """
    @QtCore.pyqtSlot(int)
    def updateNChips(self, nc):
        self.nChips = nc
        if nc==4:
            cmap = DEF.CHIP_LIST_4
        else:
            cmap = DEF.CHIP_LIST_48
        self.cbChip.clear()
        self.cbChipF1.clear()
        self.cbChipF2.clear()
        for i in range(nc):
            cStr = "chip<{},{}>".format(cmap[i][0], cmap[i][1])
            self.cbChip.addItem(cStr)
            self.cbChipF1.addItem(cStr)
            self.cbChipF2.addItem(cStr)
        self.cbChip.addItem("All")
        self.cbChipF1.addItem("None")
        self.cbChipF2.addItem("None")

        self.qwtFall.selectF = self.cbChip.count() # will display all
        self.qwtF1.selectF = self.cbChipF1.count() # will display none
        self.qwtF2.selectF = self.cbChipF2.count() # will display none

    @QtCore.pyqtSlot(int)
    def selectF1Update(self, id):
        # if ComboBox cbChipF1 is changed
        self.qwtF1.selectF = id
        self.qwtF1.cpuChanged()
        
    @QtCore.pyqtSlot(int)
    def selectF2Update(self, id):
        # if ComboBox cbChipF2 is changed
        self.qwtF2.selectF = id
        self.qwtF2.cpuChanged()
    
    def closeEvent(self, event):
        if self.okToClose:
            event.accept()
        else:
            event.ignore()
            
    """
    ######################### GUI callback ########################### 
    """
    def pbSetClicked(self):
        f, OK = self.cbFreq.currentText().toInt()
        if self.nChips==4:
            cmap = DEF.CHIP_LIST_4
        else:
            cmap = DEF.CHIP_LIST_48

        idx = self.cbChip.currentIndex()
        
        if idx == self.nChips: # send to all chips
            for i in range(self.nChips):
                dax = cmap[i][0]
                day = cmap[i][1]
                self.sendFreqReq(f, dax, day)
        else:                  # send to a particular chip
            dax = cmap[idx][0]
            day = cmap[idx][1]
            self.sendFreqReq(f, dax, day)
        """
        """
        
    def pbPauseClicked(self):
        if not self.pause:
            self.pbPause.setText("Run")
            self.qwtFall.pause = True
            self.qwtF1.pause = True
            self.qwtF2.pause = True
        else:
            self.pbPause.setText("Pause")
            self.qwtFall.pause = False
            self.qwtF1.pause = False
            self.qwtF2.pause = False
        self.pause = not self.pause
                       
    """
    ######################### Data and Saving callback ########################### 
    """
    @QtCore.pyqtSlot(list)
    def newData(self, datagram):
        """
        We will save frequency here
        """
        #if self.saveState:
        fmt = "<H4BH2B2H3I18I"
        pad, flags, tag, dp, sp, da, say, sax, cmd, freq, temp1, temp2, temp3, \
        cpu0, cpu1, cpu2, cpu3, cpu4, cpu5, cpu6, cpu7, cpu8, cpu9, cpu10, cpu11, \
        cpu12, cpu13, cpu14, cpu15, cpu16, cpu17 = struct.unpack(fmt, datagram)

        # TODO: finish it!
        """
        self.Ffiles = list()
        for i in range(nChip):
            self.Tfiles.append(None)

        if self.saveToFile is True:
            seq = sax * 2 + say           
            tVal = "{},{},{},{}\n".format(seq, temp1, temp2, temp3)
            self.Tfiles[seq].write(tVal)
        """
        self.qwtFall.plot(sax, say, freq)
        self.qwtF1.plot(sax, say, freq)
        self.qwtF2.plot(sax, say, freq)

    def saveToFileTriggered(self, state, dirName):
        self.saveState = state
        self.saveDirName = dirName
        if state is True:
            for i in range(self.nChips):
                fName = dirName + '/temp.' + str(i)
                print "Creating file {}".format(fName)
                self.Tfiles[i] = open(fName, 'w')
            self.saveToFile = True

        else:
            self.saveToFile = False
            for i in range(self.nChips):
                if self.Tfiles[i] is not None:
                    self.Tfiles[i].close()
                    self.Tfiles[i] = None

    # We can use sendSDP to control frequency
    def sendFreqReq(self,freq, dax, day):
    #def sendFreqReq(self,flags, tag, dp, dc, dax, day, cmd, seq, arg1, arg2, arg3, bArray):
        """
        The detail experiment with sendSDP() see mySDPinger.py
        """
        da = (dax << 8) + day
        dpc = (DEF.SDP_PORT << 5) + DEF.SDP_CORE
        sa = 0
        spc = 255
        pad = struct.pack('2B',0,0)
        hdr = struct.pack('4B2H', DEF.NO_REPLY, DEF.SEND_IPTAG, dpc, spc, da, sa)
        scp = struct.pack('2H3I', DEF.HOST_SET_FREQ_VALUE, freq, 0, 0, 0)
        sdp = pad + hdr + scp

        CmdSock = QtNetwork.QUdpSocket()
        CmdSock.writeDatagram(sdp, QtNetwork.QHostAddress(DEF.HOST), DEF.SEND_PORT)
        return sdp

    """
    ############################# Helper Functions ##################################
    getP2Vidx()  : get the coreID from CHIP_LIST_4x
    """
    def getFreqIdx(self, f):
        fStr = "%d" % f
        for i in range(self.cbFreq.count()):
            if self.cbFreq.itemText(i)==fStr:
                return i




"""==================================================================================
                                    class FPlot() 
-------------------------------------------------------------------------------------"""
class FPlot(Qwt.QwtPlot):
    pause = False
    selectF = -1
    def __init__(self, nChip, *args):
        Qwt.QwtPlot.__init__(self, *args)
       
        self.setCanvasBackground(Qt.Qt.white)
        self.alignScales()

        # Initialize data
        self.x = arange(0.0, 100.1, 0.5)
        self.y = zeros(len(self.x), float)
        self.z = zeros(len(self.x), float)
        self.nChips = nChip
        self.maxScaleY = DEF.MAX_F_SCALE 
        self.minScaleY = DEF.MIN_F_SCALE
        
        self.f = list() # contains the real freq value
        self.c = list() # contains the curve value for self.t
                   
        for i in range(nChip):
            y = zeros(len(self.x), float)
            self.f.append(y)
            sname = "Chip-%d" % (i+1)
            self.c.append(Qwt.QwtPlotCurve(sname))

        ## Color contants
        clr = [Qt.Qt.red, Qt.Qt.green, Qt.Qt.blue, Qt.Qt.cyan, Qt.Qt.magenta, Qt.Qt.yellow, Qt.Qt.black, Qt.Qt.gray, \
               Qt.Qt.darkRed, Qt.Qt.darkGreen, Qt.Qt.darkBlue, Qt.Qt.darkCyan, Qt.Qt.darkMagenta, Qt.Qt.darkYellow, \
               Qt.Qt.darkGray, Qt.Qt.lightGray, \
               Qt.QColor(Qt.qRgb(255,192,203)), Qt.QColor(Qt.qRgb(139,69,19)), Qt.QColor(Qt.qRgb(128, 0, 0)), Qt.Qt.white]
        #Pink: rgb(255,192,203), Brown: rgb(139,69,19), Maron: rgb(128,0,0)
        
        for i in range(nChip):
            self.c[i].setPen(Qt.QPen(clr[i],DEF.PEN_WIDTH))
            self.c[i].attach(self)
            
        
        #self.setTitle("Chip Temperature Report")
        
        self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.BottomLegend);

        """
        self.curveR = Qwt.QwtPlotCurve("Data Moving Right")
        self.curveR.attach(self)
        self.curveL = Qwt.QwtPlotCurve("Data Moving Left")
        self.curveL.attach(self)

        self.curveL.setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.Ellipse,
                                        Qt.QBrush(),
                                        Qt.QPen(Qt.Qt.yellow),
                                        Qt.QSize(7, 7)))
        self.curveR.setPen(Qt.QPen(Qt.Qt.red))
        self.curveL.setPen(Qt.QPen(Qt.Qt.blue))

        mY = Qwt.QwtPlotMarker()
        mY.setLabelAlignment(Qt.Qt.AlignRight | Qt.Qt.AlignTop)
        mY.setLineStyle(Qwt.QwtPlotMarker.HLine)
        mY.setYValue(0.0)
        mY.attach(self)
        """

        self.setAxisScale(Qwt.QwtPlot.yLeft, self.minScaleY, self.maxScaleY)        
        self.setAxisTitle(Qwt.QwtPlot.xBottom, "Time (seconds)")
        self.setAxisTitle(Qwt.QwtPlot.yLeft, "Freq (MHz)")
            
        self.startTimer(50)
        self.phase = 0.0
        

    def getAlignedMaxValue(self):
        mVal = 0
        if self.sensorID == 0:
            mVal = self.currentMaxYVal_S1
        elif self.sensorID == 1:
            mVal = self.currentMaxYVal_S2
        elif self.sensorID == 2:
            mVal = self.currentMaxYVal_S3
        else:
            mVal = int((self.currentMaxYVal_S1 + self.currentMaxYVal_S2) / 2)
        mVal = int(mVal / 1000)
        mVal += 1
        return mVal * 1000
        
    
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

    # alignScales()

    def cpuChanged(self):
        idx = self.selectF
        # detach all
        for i in range(self.nChips):
            self.c[i].detach()
        if idx < self.nChips:
            self.c[idx].attach(self)
    
    def plot(self, sax, say, freq):  
        """     
        fmt = "<H4BH2B2H3I18I"
        pad, flags, tag, dp, sp, da, say, sax, cmd, freq, temp1, temp2, temp3, \
        cpu0, cpu1, cpu2, cpu3, cpu4, cpu5, cpu6, cpu7, cpu8, cpu9, cpu10, cpu11, cpu12, \
        cpu13, cpu14, cpu15, cpu16, cpu17 = struct.unpack(fmt, datagram)
        """
        #chipID = sax*2+say
        if self.nChips==4:
            cmap = DEF.CHIP_LIST_4
        else:
            cmap = DEF.CHIP_LIST_48
        chipID = self.getP2Vidx(cmap, sax, say)
        self.f[chipID] = concatenate((self.f[chipID][:1], self.f[chipID][:-1]), 1)
        
        self.f[chipID][0] = freq
            
        self.c[chipID].setData(self.x, self.f[chipID])

        #self.setAxisAutoScale(Qwt.QwtPlot.yLeft)
        if not self.pause:
            self.replot()
    

    def wheelEvent(self, e):
        numDegrees = e.delta() / 8
        numSteps = numDegrees / 15  # will produce either +1 or -1
        maxY = self.maxScaleY - (numSteps*5)
        if maxY > DEF.MAX_F_SCALE:
            maxY = DEF.MAX_F_SCALE
        if maxY < DEF.MIN_F_SCALE:
            maxY = DEF.MIN_F_SCALE
        self.maxScaleY = maxY
        self.setAxisScale(Qwt.QwtPlot.yLeft, self.minScaleY, self.maxScaleY)

                
    """
    ############################# Helper Functions ##################################
    getP2Vidx()  : get the coreID from CHIP_LIST_4x
    """
    def getP2Vidx(self, cmap, x, y):
        for i in range(self.nChips):
            if cmap[i][0]==x and cmap[i][1]==y:
                return i

# class DataPlot
