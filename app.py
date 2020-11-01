from typing import Tuple

from PyQt5 import QtWidgets, uic

qtcreator_file = "ui/app.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.calc_push.clicked.connect(self.calculate_clicked)

        # update loan amount
        self.home_value.valueChanged.connect(self.update_loan)
        self.down_payment.valueChanged.connect(self.update_loan)
        self.radio_euro.toggled.connect(self.update_loan)
        self.radio_perc.toggled.connect(self.update_loan)

    def get_home_and_down_value(self) -> Tuple[float, float]:
        home = float(self.home_value.text())

        if self.radio_euro.isChecked():
            down = float(self.down_payment.text())
        elif self.radio_perc.isChecked():
            down_perc = float(self.down_payment.text())
            down = (down_perc / 100) * home
        else:
            down = 0

        return home, down

    def update_loan(self):
        home, down = self.get_home_and_down_value()
        self.loan_amount.setValue(int(home - down))
        print(down)

    def calculate_clicked(self):
        years = float(self.spin_years.text())
        loan_amount = float(self.loan_amount.text())
        ir = float(self.interest_spin.text())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
