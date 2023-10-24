import sys
from PySide6.QtWidgets import QApplication
from src.interface.MainWindow import MainWindow

sys.path.append("src")
sys.path.append("src/interface")


def main():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()

    mainwindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

# Point Cloud Format (xyz):
# [
# (x1, y1, z1)
# (x2, y2, z2)
# ...]
