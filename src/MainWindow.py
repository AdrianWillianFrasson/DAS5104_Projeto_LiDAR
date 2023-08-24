from PySide6.QtWidgets import QMainWindow
from src.interface.main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # connects
        self.ui.btp_startScan.clicked.connect(self.start_scan)
        self.ui.btp_stopScan.clicked.connect(self.stop_scan)
        self.ui.btp_showPC.clicked.connect(self.show_PC)

    def start_scan(self):
        print("start_scan")

    def stop_scan(self):
        print("stop_scan")

    def show_PC(self):
        print("show_PC")
