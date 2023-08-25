from src.ScanManager import ScanManager


class VolumeCalculator():

    def __init__(self):
        self.scan_manager = ScanManager()

    def start(self):
        self.scan_manager.start()

    def stop(self):
        self.scan_manager.stop()
