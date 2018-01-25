# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QtSpiNNProfilerMDI.ui'
#
# Created: Mon Jan 25 15:32:39 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_QtSpiNNProfilerMDI(object):
    def setupUi(self, QtSpiNNProfilerMDI):
        QtSpiNNProfilerMDI.setObjectName(_fromUtf8("QtSpiNNProfilerMDI"))
        QtSpiNNProfilerMDI.resize(1024, 800)
        self.centralwidget = QtGui.QWidget(QtSpiNNProfilerMDI)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.mdiArea = QtGui.QMdiArea(self.centralwidget)
        self.mdiArea.setGeometry(QtCore.QRect(0, 0, 1031, 751))
        self.mdiArea.setObjectName(_fromUtf8("mdiArea"))
        QtSpiNNProfilerMDI.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(QtSpiNNProfilerMDI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_Widgets = QtGui.QMenu(self.menubar)
        self.menu_Widgets.setObjectName(_fromUtf8("menu_Widgets"))
        self.menu_Config = QtGui.QMenu(self.menubar)
        self.menu_Config.setObjectName(_fromUtf8("menu_Config"))
        QtSpiNNProfilerMDI.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(QtSpiNNProfilerMDI)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        QtSpiNNProfilerMDI.setStatusBar(self.statusbar)
        self.action_Tubotron = QtGui.QAction(QtSpiNNProfilerMDI)
        self.action_Tubotron.setCheckable(True)
        self.action_Tubotron.setObjectName(_fromUtf8("action_Tubotron"))
        self.action_Temperature = QtGui.QAction(QtSpiNNProfilerMDI)
        self.action_Temperature.setCheckable(True)
        self.action_Temperature.setObjectName(_fromUtf8("action_Temperature"))
        self.action_Utilization = QtGui.QAction(QtSpiNNProfilerMDI)
        self.action_Utilization.setCheckable(True)
        self.action_Utilization.setObjectName(_fromUtf8("action_Utilization"))
        self.action_Frequency = QtGui.QAction(QtSpiNNProfilerMDI)
        self.action_Frequency.setCheckable(True)
        self.action_Frequency.setObjectName(_fromUtf8("action_Frequency"))
        self.action_Quit = QtGui.QAction(QtSpiNNProfilerMDI)
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))
        self.action_SaveData = QtGui.QAction(QtSpiNNProfilerMDI)
        self.action_SaveData.setCheckable(True)
        self.action_SaveData.setObjectName(_fromUtf8("action_SaveData"))
        self.action_SelectBoard = QtGui.QAction(QtSpiNNProfilerMDI)
        self.action_SelectBoard.setObjectName(_fromUtf8("action_SelectBoard"))
        self.action_CoreSwitcher = QtGui.QAction(QtSpiNNProfilerMDI)
        self.action_CoreSwitcher.setCheckable(True)
        self.action_CoreSwitcher.setObjectName(_fromUtf8("action_CoreSwitcher"))
        self.menu_Widgets.addAction(self.action_Tubotron)
        self.menu_Widgets.addAction(self.action_Temperature)
        self.menu_Widgets.addAction(self.action_Utilization)
        self.menu_Widgets.addAction(self.action_Frequency)
        self.menu_Widgets.addAction(self.action_CoreSwitcher)
        self.menu_Config.addAction(self.action_SaveData)
        self.menu_Config.addAction(self.action_SelectBoard)
        self.menubar.addAction(self.menu_Widgets.menuAction())
        self.menubar.addAction(self.menu_Config.menuAction())

        self.retranslateUi(QtSpiNNProfilerMDI)
        QtCore.QMetaObject.connectSlotsByName(QtSpiNNProfilerMDI)

    def retranslateUi(self, QtSpiNNProfilerMDI):
        QtSpiNNProfilerMDI.setWindowTitle(_translate("QtSpiNNProfilerMDI", "SpiNNaker Profiler", None))
        self.menu_Widgets.setTitle(_translate("QtSpiNNProfilerMDI", "&Widgets", None))
        self.menu_Config.setTitle(_translate("QtSpiNNProfilerMDI", "&Config", None))
        self.action_Tubotron.setText(_translate("QtSpiNNProfilerMDI", "&Tubotron", None))
        self.action_Tubotron.setShortcut(_translate("QtSpiNNProfilerMDI", "F1", None))
        self.action_Temperature.setText(_translate("QtSpiNNProfilerMDI", "Tem&perature", None))
        self.action_Temperature.setShortcut(_translate("QtSpiNNProfilerMDI", "F2", None))
        self.action_Utilization.setText(_translate("QtSpiNNProfilerMDI", "&Utilization", None))
        self.action_Utilization.setShortcut(_translate("QtSpiNNProfilerMDI", "F3", None))
        self.action_Frequency.setText(_translate("QtSpiNNProfilerMDI", "&Frequency", None))
        self.action_Frequency.setShortcut(_translate("QtSpiNNProfilerMDI", "F4", None))
        self.action_Quit.setText(_translate("QtSpiNNProfilerMDI", "&Quit", None))
        self.action_SaveData.setText(_translate("QtSpiNNProfilerMDI", "&Save Data", None))
        self.action_SelectBoard.setText(_translate("QtSpiNNProfilerMDI", "Select &Board", None))
        self.action_SelectBoard.setShortcut(_translate("QtSpiNNProfilerMDI", "F6", None))
        self.action_CoreSwitcher.setText(_translate("QtSpiNNProfilerMDI", "&Core Switcher", None))
        self.action_CoreSwitcher.setShortcut(_translate("QtSpiNNProfilerMDI", "F5", None))

