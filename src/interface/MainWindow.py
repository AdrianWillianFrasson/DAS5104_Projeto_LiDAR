import os
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView

from src.ScanManager import ScanManager
from src.VolumeCalculator import VolumeCalculator
from src.interface.MainWindow_ui import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.volume_calculator = VolumeCalculator()
        self.scan_manager = ScanManager()
        self.scans = list()

        # connects
        self.ui.btp_calculateVolume.clicked.connect(self.calculate_volume)
        self.ui.btp_startScan.clicked.connect(self.start_scan)
        self.ui.btp_stopScan.clicked.connect(self.stop_scan)
        self.ui.btp_showPC.clicked.connect(self.show_PC)

        # setup
        self.ui.tbw_scans.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.refresh_scan_table()

    def start_scan(self):
        output_folder = f"./pointcloud/{datetime.now().strftime('%Y-%m-%d_%Hh%Mmin%Ss')}/"

        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        self.ui.btp_startScan.setEnabled(False)
        self.scan_manager.start(output_folder)
        self.ui.btp_stopScan.setEnabled(True)

    def stop_scan(self):
        self.ui.btp_stopScan.setEnabled(False)
        self.scan_manager.stop()
        self.ui.btp_startScan.setEnabled(True)

        self.refresh_scan_table()

    def show_PC(self):
        pass

    def calculate_volume(self):
        row_selected = self.ui.tbw_scans.selectedIndexes()

        if not row_selected:
            return

        self.volume_calculator.calculate(f"./pointcloud/{self.scans[row_selected[0].row()]}/")

    def refresh_scan_table(self):
        self.scans = [scan for scan in os.listdir("./pointcloud/") if not os.path.isfile(f"./pointcloud/{scan}")]
        self.scans.reverse()
        self.ui.tbw_scans.setRowCount(0)

        for scan in self.scans:
            row = self.ui.tbw_scans.rowCount()
            self.ui.tbw_scans.insertRow(row)

            item_date = QTableWidgetItem(scan.replace("-", "/").replace("_", " "))
            item_volume = QTableWidgetItem("-")

            item_date.setTextAlignment(Qt.AlignCenter)
            item_volume.setTextAlignment(Qt.AlignCenter)
            item_date.setFlags(item_date.flags() ^ Qt.ItemIsEditable)
            item_volume.setFlags(item_volume.flags() ^ Qt.ItemIsEditable)

            self.ui.tbw_scans.setItem(row, 0, item_date)
            self.ui.tbw_scans.setItem(row, 1, item_volume)
