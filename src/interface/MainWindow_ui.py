# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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

        self.grb_scans = QGroupBox(self.centralwidget)
        self.grb_scans.setObjectName(u"grb_scans")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grb_scans.sizePolicy().hasHeightForWidth())
        self.grb_scans.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.grb_scans)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lbl_search = QLabel(self.grb_scans)
        self.lbl_search.setObjectName(u"lbl_search")

        self.horizontalLayout.addWidget(self.lbl_search)

        self.lne_search = QLineEdit(self.grb_scans)
        self.lne_search.setObjectName(u"lne_search")

        self.horizontalLayout.addWidget(self.lne_search)

        self.btp_refreshTable = QPushButton(self.grb_scans)
        self.btp_refreshTable.setObjectName(u"btp_refreshTable")

        self.horizontalLayout.addWidget(self.btp_refreshTable)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.tbw_scans = QTableWidget(self.grb_scans)
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


        self.verticalLayout.addWidget(self.grb_scans)

        self.grb_operations = QGroupBox(self.centralwidget)
        self.grb_operations.setObjectName(u"grb_operations")
        self.verticalLayout_3 = QVBoxLayout(self.grb_operations)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.btp_startScan = QPushButton(self.grb_operations)
        self.btp_startScan.setObjectName(u"btp_startScan")
        self.btp_startScan.setEnabled(True)

        self.verticalLayout_3.addWidget(self.btp_startScan)

        self.btp_stopScan = QPushButton(self.grb_operations)
        self.btp_stopScan.setObjectName(u"btp_stopScan")
        self.btp_stopScan.setEnabled(False)

        self.verticalLayout_3.addWidget(self.btp_stopScan)

        self.btp_processData = QPushButton(self.grb_operations)
        self.btp_processData.setObjectName(u"btp_processData")
        self.btp_processData.setEnabled(True)

        self.verticalLayout_3.addWidget(self.btp_processData)


        self.verticalLayout.addWidget(self.grb_operations)

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
        self.grb_scans.setTitle(QCoreApplication.translate("MainWindow", u"Scans", None))
        self.lbl_search.setText(QCoreApplication.translate("MainWindow", u"Search:", None))
        self.btp_refreshTable.setText(QCoreApplication.translate("MainWindow", u"Refresh Table", None))
        ___qtablewidgetitem = self.tbw_scans.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"ID", None));
        ___qtablewidgetitem1 = self.tbw_scans.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Volume [cm^3]", None));
        self.grb_operations.setTitle(QCoreApplication.translate("MainWindow", u"Operations", None))
        self.btp_startScan.setText(QCoreApplication.translate("MainWindow", u"Start Scan", None))
        self.btp_stopScan.setText(QCoreApplication.translate("MainWindow", u"Stop Scan", None))
        self.btp_processData.setText(QCoreApplication.translate("MainWindow", u"Process Data", None))
    # retranslateUi

