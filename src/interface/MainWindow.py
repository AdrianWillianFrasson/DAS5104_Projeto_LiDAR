import os
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView

from src.ScanManager import ScanManager
from src.DataManager import DataManager
from src.Constants import Constants
from src.interface.MainWindow_ui import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.data_manager = DataManager()
        self.scan_manager = ScanManager()

        self.scanList = list()

        # connects
        self.ui.btp_refreshTable.clicked.connect(self.refresh_table)
        self.ui.btp_processData.clicked.connect(self.process_data)
        self.ui.btp_startScan.clicked.connect(self.start_scan)
        self.ui.btp_stopScan.clicked.connect(self.stop_scan)

        # setup
        self.ui.tbw_scans.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.refresh_table()

    def start_scan(self):
        self.ui.btp_startScan.setEnabled(False)

        date = datetime.now().strftime("%Y-%m-%d_%Hh%Mmin%Ss")
        output_folder = f"{Constants.SCANS_DIRECTORY}{date}/"

        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        self.scan_manager.start_scan(output_folder)

        self.ui.btp_stopScan.setEnabled(True)

    def stop_scan(self):
        self.ui.btp_stopScan.setEnabled(False)

        self.scan_manager.stop_scan()

        self.ui.btp_startScan.setEnabled(True)
        self.refresh_table()

    def process_data(self):
        row_selected = self.ui.tbw_scans.selectedIndexes()

        if not row_selected:
            return

        row_index = row_selected[0].row()
        scan_folder = self.scanList[row_index]

        volume = self.data_manager.process_data(f"{Constants.SCANS_DIRECTORY}{scan_folder}/")

        item = self.ui.tbw_scans.item(row_index, 1)
        item.setText(str(volume))

    def refresh_table(self):
        self.scanList = [scan for scan in os.listdir(
            Constants.SCANS_DIRECTORY) if not os.path.isfile(f"{Constants.SCANS_DIRECTORY}{scan}")]
        self.scanList.reverse()

        self.ui.tbw_scans.setRowCount(0)

        for scan in self.scanList:
            row = self.ui.tbw_scans.rowCount()
            self.ui.tbw_scans.insertRow(row)

            item_id = QTableWidgetItem(scan.replace("-", "/").replace("_", " "))
            item_volume = QTableWidgetItem("-")

            item_id.setTextAlignment(Qt.AlignCenter)
            item_volume.setTextAlignment(Qt.AlignCenter)
            item_id.setFlags(item_id.flags() ^ Qt.ItemIsEditable)
            item_volume.setFlags(item_volume.flags() ^ Qt.ItemIsEditable)

            self.ui.tbw_scans.setItem(row, 0, item_id)
            self.ui.tbw_scans.setItem(row, 1, item_volume)
