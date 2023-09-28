import os
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView

from src.ScanManager import ScanManager
from src.Reconstructor3D import Reconstructor3D
from src.VolumeCalculator import VolumeCalculator
from src.PointCloudPlotter import PointCloudPlotter
from src.SensorLiveReceiver import SensorLiveReceiver
from src.PointCloudLivePlotter import PointCloudLivePlotter
from src.interface.MainWindow_ui import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.point_cloud_live_plotter = PointCloudLivePlotter()
        self.sensor_live_receiver = SensorLiveReceiver()
        self.point_cloud_plotter = PointCloudPlotter()
        self.volume_calculator = VolumeCalculator()
        self.reconstructor_3d = Reconstructor3D()
        self.scan_manager = ScanManager()

        self.scans = list()

        # connects
        self.ui.btp_calculateVolume.clicked.connect(self.calculate_volume)
        self.ui.btp_showPointCloud.clicked.connect(self.show_point_cloud)
        self.ui.btp_startLiveScan.clicked.connect(self.start_live_scan)
        self.ui.btp_stopLiveScan.clicked.connect(self.stop_live_scan)
        self.ui.btp_startScan.clicked.connect(self.start_scan)
        self.ui.btp_stopScan.clicked.connect(self.stop_scan)

        # setup
        self.ui.tbw_scans.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.refresh_scan_table()

    def start_scan(self):
        self.ui.btp_startLiveScan.setEnabled(False)
        self.ui.btp_startScan.setEnabled(False)

        output_folder = f"./pointcloud/{datetime.now().strftime('%Y-%m-%d_%Hh%Mmin%Ss')}/"
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        self.scan_manager.start(output_folder)

        self.ui.btp_stopScan.setEnabled(True)

    def stop_scan(self):
        self.ui.btp_stopScan.setEnabled(False)

        self.scan_manager.stop()

        self.ui.btp_startLiveScan.setEnabled(True)
        self.ui.btp_startScan.setEnabled(True)
        self.refresh_scan_table()

    def show_point_cloud(self):
        row_selected = self.ui.tbw_scans.selectedIndexes()

        if not row_selected:
            return

        row_index = row_selected[0].row()
        scan_folder = self.scans[row_index]

        # if not os.path.isfile(f"./pointcloud/{scan_folder}/data.npz"):
        self.reconstructor_3d.create_point_cloud(f"./pointcloud/{scan_folder}/")

        self.point_cloud_plotter.start(f"./pointcloud/{scan_folder}/data.npz")

    def calculate_volume(self):
        row_selected = self.ui.tbw_scans.selectedIndexes()

        if not row_selected:
            return

        row_index = row_selected[0].row()
        scan_folder = self.scans[row_index]

        if not os.path.isfile(f"./pointcloud/{scan_folder}/data.npz"):
            self.reconstructor_3d.create_point_cloud(f"./pointcloud/{scan_folder}/")

        volume = self.volume_calculator.calculate(f"./pointcloud/{scan_folder}/data.npz")

        item = self.ui.tbw_scans.item(row_index, 1)
        item.setText(str(volume))

    def start_live_scan(self):
        self.ui.btp_startLiveScan.setEnabled(False)
        self.ui.btp_startScan.setEnabled(False)

        self.sensor_live_receiver.start()
        self.point_cloud_live_plotter.start(self.sensor_live_receiver.queue)

        self.ui.btp_stopLiveScan.setEnabled(True)

    def stop_live_scan(self):
        self.ui.btp_stopLiveScan.setEnabled(False)

        self.sensor_live_receiver.stop()
        self.point_cloud_live_plotter.stop()

        self.ui.btp_startLiveScan.setEnabled(True)
        self.ui.btp_startScan.setEnabled(True)

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
