from PyQt4 import QtGui, QtNetwork
from PyQt4.QtCore import *
import QtCoreSwitch
import constDef as DEF
import struct


"""===============================================================================================
                                      Wrapper for CoreSwitch
-----------------------------------------------------------------------------------------------"""
class Swidget(QtGui.QWidget, QtCoreSwitch.Ui_CoreSwitch):
    okToClose = False
    def __init__(self, nChips, parent=None):
        super(Swidget, self).__init__(parent)
        self.setupUi(self)
        #self.c1.setChecked(True) -> just for test if my logic is correct :)
        self.nChips = nChips
        self.p2vMap = [[c for c in range(18)] for i in range(nChips)]
        self.activeCore = [i for i in range(18)] # initially, let's assume all cores are alive
        # Then populate comboBox
        for i in range(nChips):
            x, y = self.getChipP2P(i)
            cStr = "chip<{},{}>".format(x, y)
            self.cbChips.addItem(cStr)

        # SIGNAL-SLOTS mechanism 
        self.cbChips.currentIndexChanged.connect(self.chipChanged)
        self.changeConnection(True)
        
        # Final step: find out which cores are active initially
        self.askActiveCore()

    def changeConnection(self, state):
        if state:
            self.c0.clicked.connect(self.coreToggled)
            self.c1.clicked.connect(self.coreToggled)
            self.c2.clicked.connect(self.coreToggled)
            self.c3.clicked.connect(self.coreToggled)
            self.c4.clicked.connect(self.coreToggled)
            self.c5.clicked.connect(self.coreToggled)
            self.c6.clicked.connect(self.coreToggled)
            self.c7.clicked.connect(self.coreToggled)
            self.c8.clicked.connect(self.coreToggled)
            self.c9.clicked.connect(self.coreToggled)
            self.c10.clicked.connect(self.coreToggled)
            self.c11.clicked.connect(self.coreToggled)
            self.c12.clicked.connect(self.coreToggled)
            self.c13.clicked.connect(self.coreToggled)
            self.c14.clicked.connect(self.coreToggled)
            self.c15.clicked.connect(self.coreToggled)
            self.c16.clicked.connect(self.coreToggled)
            self.c17.clicked.connect(self.coreToggled)
        else:
            self.c0.clicked.disconnect(self.coreToggled)
            self.c1.clicked.disconnect(self.coreToggled)
            self.c2.clicked.disconnect(self.coreToggled)
            self.c3.clicked.disconnect(self.coreToggled)
            self.c4.clicked.disconnect(self.coreToggled)
            self.c5.clicked.disconnect(self.coreToggled)
            self.c6.clicked.disconnect(self.coreToggled)
            self.c7.clicked.disconnect(self.coreToggled)
            self.c8.clicked.disconnect(self.coreToggled)
            self.c9.clicked.disconnect(self.coreToggled)
            self.c10.clicked.disconnect(self.coreToggled)
            self.c11.clicked.disconnect(self.coreToggled)
            self.c12.clicked.disconnect(self.coreToggled)
            self.c13.clicked.disconnect(self.coreToggled)
            self.c14.clicked.disconnect(self.coreToggled)
            self.c15.clicked.disconnect(self.coreToggled)
            self.c16.clicked.disconnect(self.coreToggled)
            self.c17.clicked.disconnect(self.coreToggled)
        
    @pyqtSlot(int)
    def chipChanged(self, idx):
        dax, day = self.getChipP2P(idx)
        self.askActiveCore(sax, say)
        
    def closeEvent(self, event):
        if self.okToClose:
            event.accept()
        else:
            event.ignore()

    """
    updateNChips() will be triggered by main QtForms
    """
    @pyqtSlot(int)
    def updateNChips(self, nc):
        self.nChips = nc
        self.p2vMap = [[c for c in range(18)] for i in range(nc)]
        self.askActiveCore()

    def updateP2Vmap(self, idx, cpuVal):
        self.p2vMap[idx] = cpuVal

    @pyqtSlot()
    def coreToggled(self):
        """
        At the moment, we just kill the core. In the future, we might add some functionalities:
        1. Test if that "dead" core can be reactivated, run simple test
        2. Put the PM-agent on that core
        3. Label that core to be available again (and notify host as well)
        """
        # First, detect who send the signal (which core is toggled)
        sender = self.sender()
        
        if sender == self.c1:
            print "Button c1 is pressed"
            if self.c1.isChecked():
                print "Now it's checked"
                self.askToDeactiveCore(1)
            else:
                #keep it low at the moment!
                #self.c1.setChecked(True)
                self.askToActivateCore(1)
                #print "Now it's unchecked"
        elif sender == self.c2:
            print "Button c2 is pressed"
            if self.c2.isChecked():
                print "Now it's checked"
                self.askToDeactiveCore(2)
            else:
                #keep it low at the moment!
                #self.c2.setChecked(True)
                self.askToActivateCore(2)
                #print "Now it's unchecked"
        elif sender == self.c3:
            print "Button c3 is pressed"
            if self.c3.isChecked():
                print "Now it's checked"
                self.askToDeactiveCore(3)
            else:
                #keep it low at the moment!
                #self.c3.setChecked(True)
                self.askToActivateCore(3)
                #print "Now it's unchecked"
        elif sender == self.c4:
            print "Button c4 is pressed"
            if self.c4.isChecked():
                print "Now it's checked"
                self.askToDeactiveCore(4)
            else:
                #keep it low at the moment!
                #self.c4.setChecked(True)
                self.askToActivateCore(4)
                #print "Now it's unchecked"
        elif sender == self.c5:
            print "Button c5 is pressed"
            if self.c5.isChecked():
                print "Now it's checked"
                self.askToDeactiveCore(5)
            else:
                #keep it low at the moment!
                #self.c5.setChecked(True)
                self.askToActivateCore(5)
                #print "Now it's unchecked"
        elif sender == self.c6:
            print "Button c6 is pressed"
            if self.c6.isChecked():
                print "Now it's checked"
                self.askToDeactiveCore(6)
            else:
                #keep it low at the moment!
                #self.c6.setChecked(True)
                self.askToActivateCore(6)
                #print "Now it's unchecked"
        elif sender == self.c7:
            print "Button c7 is pressed"
            if self.c7.isChecked():
                print "Now it's checked"
                self.askToDeactiveCore(7)
            else:
                #keep it low at the moment!
                #self.c7.setChecked(True)
                self.askToActivateCore(7)
                #print "Now it's unchecked"
        elif sender == self.c8:
            print "Button c8 is pressed"
            if self.c8.isChecked():
                print "Now it's checked"
                self.askToDeactiveCore(8)
            else:
                #keep it low at the moment!
                #self.c8.setChecked(True)
                self.askToActivateCore(8)
                #print "Now it's unchecked"
        elif sender == self.c9:
            print "Button c9 is pressed"
            if self.c9.isChecked():
                print "Now it's checked"
                self.askToDeactiveCore(9)
            else:
                #keep it low at the moment!
                #self.c9.setChecked(True)
                self.askToActivateCore(9)
                #print "Now it's unchecked"
        elif sender == self.c10:
            print "Button c10 is pressed"
            if self.c10.isChecked():
                print "Now it's checked"
                self.askToDeactiveCore(10)
            else:
                #keep it low at the moment!
                #self.c10.setChecked(True)
                self.askToActivateCore(10)
                #print "Now it's unchecked"
        elif sender == self.c11:
            print "Button c11 is pressed"
            if self.c11.isChecked():
                print "Now it's checked"
                self.askToDeactiveCore(11)
            else:
                #keep it low at the moment!
                #self.c11.setChecked(True)
                self.askToActivateCore(11)
                #print "Now it's unchecked"
        elif sender == self.c12:
            print "Button c12 is pressed"
            if self.c12.isChecked():
                print "Now it's checked"
                self.askToDeactiveCore(12)
            else:
                #keep it low at the moment!
                #self.c12.setChecked(True)
                self.askToActivateCore(12)
                #print "Now it's unchecked"
        elif sender == self.c13:
            print "Button c13 is pressed"
            if self.c13.isChecked():
                print "Now it's checked"
                self.askToDeactiveCore(13)
            else:
                #keep it low at the moment!
                #self.c13.setChecked(True)
                self.askToActivateCore(13)
                #print "Now it's unchecked"
        elif sender == self.c14:
            print "Button c14 is pressed"
            if self.c14.isChecked():
                print "Now it's checked"
                self.askToDeactiveCore(14)
            else:
                #keep it low at the moment!
                #self.c14.setChecked(True)
                self.askToActivateCore(14)
                #print "Now it's unchecked"
        elif sender == self.c15:
            print "Button c15 is pressed"
            if self.c15.isChecked():
                print "Now it's checked"
                self.askToDeactiveCore(15)
            else:
                #keep it low at the moment!
                #self.c15.setChecked(True)
                self.askToActivateCore(15)
                #print "Now it's unchecked"
        elif sender == self.c16:
            print "Button c16 is pressed"
            if self.c6.isChecked():
                print "Now it's checked"
                self.askToDeactiveCore(16)
            else:
                #keep it low at the moment!
                #self.c16.setChecked(True)
                self.askToActivateCore(16)
                #print "Now it's unchecked"
        elif sender == self.c17:
            print "Button c17 is pressed"
            if self.c17.isChecked():
                print "Now it's checked"
                self.askToDeactiveCore(17)
            else:
                #keep it low at the moment!
                #self.c17.setChecked(True)
                self.askToActivateCore(17)
                #print "Now it's unchecked"
        else:
            print "Something else..."
        
    @pyqtSlot(list)
    def newData(self, datagram):
        """
        Can be used to read which core is dead
        Remember to disable the signal-slot connection before making push button toggling visualisation
        """
        # Do we receive active cores reply?
        if len(datagram)==DEF.HOST_REQ_ACTIVE_CORES_REPLY_SIZE:
            fmt = "<H4BH2B2H3I" # ingat: say dulu baru sax, karena....
            pad, flags, tag, dp, sp, da, say, sax, \
            cmd, seq, arg1, arg2, arg3 = struct.unpack(fmt, datagram)

            if cmd==DEF.HOST_REQ_ACTIVE_CORES:
                # the profiler should send sc[SC_CPU_DIS], where '1' indicates disabled core
                # Just update according to current selected chip
                chipIdx = self.getChipIdx(sax, say)
                if self.cbChips.currentIndex()==chipIdx:
                    # Disconnect signal-slot
                    self.changeConnection(False)
                    # Get the p2v core map
                    cList = arg1 # seq will contain physical core IDs
                    # then for all buttons, do flip
                    for i in range(18):
                        pCore = i
                        vCore = self.p2vMap[chipIdx][pCore]
                        #print "Current found vCore = {}".format(vCore)
                        if vCore != 0: # No monitor core!
                            mask = (1 << i) # if a core is OK, then its bit is '1'
                            if vCore==1: # process for pushButton-c0
                                if (cList & mask) > 0: # the core is functional
                                    self.c1.setChecked(True)
                                else:                  # the core is "shut-down"
                                    self.c1.setChecked(False)
                            elif vCore==2:
                                if (cList & mask) > 0:
                                    self.c2.setChecked(True)
                                else:
                                    self.c2.setChecked(False)
                            elif vCore==3:
                                if (cList & mask) > 0:
                                    self.c3.setChecked(True)
                                else:
                                    self.c3.setChecked(False)
                            elif vCore==4:
                                if (cList & mask) > 0:
                                    self.c4.setChecked(True)
                                else:
                                    self.c4.setChecked(False)
                            elif vCore==5:
                                if (cList & mask) > 0:
                                    self.c5.setChecked(True)
                                else:
                                    self.c5.setChecked(False)
                            elif vCore==6:
                                if (cList & mask) > 0:
                                    self.c6.setChecked(True)
                                else:
                                    self.c6.setChecked(False)
                            elif vCore==7:
                                if (cList & mask) > 0:
                                    self.c7.setChecked(True)
                                else:
                                    self.c7.setChecked(False)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                            elif vCore==8:
                                if (cList & mask) > 0:
                                    self.c8.setChecked(True)
                                else:
                                    self.c8.setChecked(False)
                            elif vCore==9:
                                if (cList & mask) > 0:
                                    self.c9.setChecked(True)
                                else:
                                    self.c9.setChecked(False)
                            elif vCore==10:
                                if (cList & mask) > 0:
                                    self.c10.setChecked(True)
                                else:
                                    self.c10.setChecked(False)
                            elif vCore==11:
                                if (cList & mask) > 0:
                                    self.c11.setChecked(True)
                                else:
                                    self.c11.setChecked(False)
                            elif vCore==12:
                                if (cList & mask) > 0:
                                    self.c12.setChecked(True)
                                else:
                                    self.c12.setChecked(False)
                            elif vCore==13:
                                if (cList & mask) > 0:
                                    self.c13.setChecked(True)
                                else:
                                    self.c13.setChecked(False)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
                            elif vCore==14:
                                if (cList & mask) > 0:
                                    self.c14.setChecked(True)
                                else:
                                    self.c14.setChecked(False)
                            elif vCore==15:
                                if (cList & mask) > 0:
                                    self.c15.setChecked(True)
                                else:
                                    self.c15.setChecked(False)
                            elif vCore==16:
                                if (cList & mask) > 0:
                                    self.c16.setChecked(True)
                                else:
                                    self.c16.setChecked(False)
                            else: # vCore==17
                                if (cList & mask) > 0:
                                    self.c17.setChecked(True)
                                else:
                                    self.c17.setChecked(False)
                                    
                    # Finally, reconnect signal-slot
                    self.changeConnection(True)
                        
    def askActiveCore(self, sax=None, say=None):
        if sax is not None and say is not None:
            self.sendSDP(DEF.NO_REPLY, DEF.SEND_IPTAG, DEF.SDP_PORT, DEF.SDP_CORE, \
                         sax, say, DEF.HOST_REQ_ACTIVE_CORES, 0, 0, 0, 0, None)
            return

        for i in range(self.nChips):
            dax, day = self.getChipP2P(i)
            #print "Asking p2v core map for chip<{},{}>".format(Coremap[i][0], Coremap[i][1])
            self.sendSDP(DEF.NO_REPLY, DEF.SEND_IPTAG, DEF.SDP_PORT, DEF.SDP_CORE, \
                         dax, day, DEF.HOST_REQ_ACTIVE_CORES, 0, 0, 0, 0, None)

    def askToDeactiveCore(self, vCore):
        chipIdx = self.cbChips.currentIndex()
        dax, day = self.getChipP2P(chipIdx)
        self.sendSDP(DEF.NO_REPLY, DEF.SEND_IPTAG, DEF.SDP_PORT, DEF.SDP_CORE, \
                     dax, day, DEF.HOST_REQ_TO_DEACTIVATE_CORE, vCore, 0, 0, 0, None)

    def askToActivateCore(self, vCore):
        chipIdx = self.cbChips.currentIndex()
        dax, day = self.getChipP2P(chipIdx)
        self.sendSDP(DEF.NO_REPLY, DEF.SEND_IPTAG, DEF.SDP_PORT, DEF.SDP_CORE, \
                     dax, day, DEF.HOST_REQ_TO_ACTIVATE_CORE, vCore, 0, 0, 0, None)

    """
    Sepertinya urutan chip-x dan chip-y terbalik selama ini!
    Mungkin karena word dipecah jadi 2 byte
    """
    def sendSDP(self, flags, tag, dp, dc, dax, day, cmd, seq, arg1, arg2, arg3, bArray):
        da = (dax << 8) + day
        dpc = (dp << 5) + dc
        sa = 0
        spc = 255
        pad = struct.pack('2B',0,0)
        hdr = struct.pack('4B2H',flags,tag,dpc,spc,da,sa)
        scp = struct.pack('2H3I',cmd,seq,arg1,arg2,arg3)
        if bArray is not None:
            sdp = pad + hdr + scp + bArray
        else:
            sdp = pad + hdr + scp

        CmdSock = QtNetwork.QUdpSocket()
        CmdSock.writeDatagram(sdp, QtNetwork.QHostAddress(DEF.HOST), DEF.SEND_PORT)
        return sdp

    """
    ############################# Helper Functions ##################################
    """            
    def getChipIdx(self, sax, say):
        if self.nChips==4:
            cmap = DEF.CHIP_LIST_4
        else:
            cmap = DEF.CHIP_LIST_48
        for i in range(self.nChips):
            if sax==cmap[i][0] and say==cmap[i][1]:
                return i 
            
    def getChipP2P(self, chipIdx):
        if self.nChips==4:
            cmap = DEF.CHIP_LIST_4
        else:
            cmap = DEF.CHIP_LIST_48
        return cmap[chipIdx][0], cmap[chipIdx][1]
            
        
    def getP2V(self, chipIdx, pCore):
        """
        get virtual core Id from the given pCore within the chipIdx
        """
        return self.p2vMap[chipIdx][pCore]

#class Swidget
