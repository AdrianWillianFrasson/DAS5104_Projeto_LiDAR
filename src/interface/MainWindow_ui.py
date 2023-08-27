# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore
from . import assets_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(820, 720)
        MainWindow.setMaximumSize(QSize(820, 16777215))
        icon = QIcon()
        icon.addFile(u":/icon/images/coontrol.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.lbl_splash = QLabel(self.centralwidget)
        self.lbl_splash.setObjectName(u"lbl_splash")
        self.lbl_splash.setPixmap(QPixmap(u":/image/images/splash.png"))
        self.lbl_splash.setScaledContents(False)
        self.lbl_splash.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.lbl_splash)

        self.grb_scansList = QGroupBox(self.centralwidget)
        self.grb_scansList.setObjectName(u"grb_scansList")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grb_scansList.sizePolicy().hasHeightForWidth())
        self.grb_scansList.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.grb_scansList)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.tbw_scans = QTableWidget(self.grb_scansList)
        if (self.tbw_scans.columnCount() < 2):
            self.tbw_scans.setColumnCount(2)
        font = QFont()
        font.setBold(True)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font);
        self.tbw_scans.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font);
        self.tbw_scans.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tbw_scans.setObjectName(u"tbw_scans")
        self.tbw_scans.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tbw_scans.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tbw_scans.setSortingEnabled(False)
        self.tbw_scans.setCornerButtonEnabled(False)

        self.verticalLayout_2.addWidget(self.tbw_scans)


        self.verticalLayout.addWidget(self.grb_scansList)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.grb_scan = QGroupBox(self.centralwidget)
        self.grb_scan.setObjectName(u"grb_scan")
        self.gridLayout = QGridLayout(self.grb_scan)
        self.gridLayout.setObjectName(u"gridLayout")
        self.btp_startScan = QPushButton(self.grb_scan)
        self.btp_startScan.setObjectName(u"btp_startScan")
        self.btp_startScan.setEnabled(True)

        self.gridLayout.addWidget(self.btp_startScan, 0, 0, 1, 1)

        self.btp_stopScan = QPushButton(self.grb_scan)
        self.btp_stopScan.setObjectName(u"btp_stopScan")
        self.btp_stopScan.setEnabled(False)

        self.gridLayout.addWidget(self.btp_stopScan, 1, 0, 1, 1)

        self.btp_showPointCloud = QPushButton(self.grb_scan)
        self.btp_showPointCloud.setObjectName(u"btp_showPointCloud")
        self.btp_showPointCloud.setEnabled(True)

        self.gridLayout.addWidget(self.btp_showPointCloud, 0, 1, 1, 1)

        self.btp_calculateVolume = QPushButton(self.grb_scan)
        self.btp_calculateVolume.setObjectName(u"btp_calculateVolume")
        self.btp_calculateVolume.setEnabled(True)

        self.gridLayout.addWidget(self.btp_calculateVolume, 1, 1, 1, 1)


        self.horizontalLayout.addWidget(self.grb_scan)

        self.grb_liveScan = QGroupBox(self.centralwidget)
        self.grb_liveScan.setObjectName(u"grb_liveScan")
        self.verticalLayout_3 = QVBoxLayout(self.grb_liveScan)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.btp_startLiveScan = QPushButton(self.grb_liveScan)
        self.btp_startLiveScan.setObjectName(u"btp_startLiveScan")

        self.verticalLayout_3.addWidget(self.btp_startLiveScan)

        self.btp_stopLiveScan = QPushButton(self.grb_liveScan)
        self.btp_stopLiveScan.setObjectName(u"btp_stopLiveScan")
        self.btp_stopLiveScan.setEnabled(False)

        self.verticalLayout_3.addWidget(self.btp_stopLiveScan)


        self.horizontalLayout.addWidget(self.grb_liveScan)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName(u"status_bar")
        MainWindow.setStatusBar(self.status_bar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Truckload Volume Calculator", None))
        self.lbl_splash.setText("")
        self.grb_scansList.setTitle(QCoreApplication.translate("MainWindow", u"Scans List", None))
        ___qtablewidgetitem = self.tbw_scans.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Date", None));
        ___qtablewidgetitem1 = self.tbw_scans.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Volume", None));
        self.grb_scan.setTitle(QCoreApplication.translate("MainWindow", u"Scan", None))
        self.btp_startScan.setText(QCoreApplication.translate("MainWindow", u"Start Scan", None))
        self.btp_stopScan.setText(QCoreApplication.translate("MainWindow", u"Stop Scan", None))
        self.btp_showPointCloud.setText(QCoreApplication.translate("MainWindow", u"Show Point Cloud", None))
        self.btp_calculateVolume.setText(QCoreApplication.translate("MainWindow", u"Calculate Volume", None))
        self.grb_liveScan.setTitle(QCoreApplication.translate("MainWindow", u"Live Scan", None))
        self.btp_startLiveScan.setText(QCoreApplication.translate("MainWindow", u"Start Live Scan", None))
        self.btp_stopLiveScan.setText(QCoreApplication.translate("MainWindow", u"Stop Live Scan", None))
    # retranslateUi

