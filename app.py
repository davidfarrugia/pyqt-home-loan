from typing import Tuple
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate

Ui_MainWindow, QtBaseClass = uic.loadUiType("ui/app.ui")


def monthly_loan(loan: float, interest_rate: float, years: int) -> float:
    """
    Calculate monthly loan payment

    :param loan: initial loan amount
    :param interest_rate: interest rate
    :param years: loan term in years
    :return: monthly payment
    """
    n = years * 12
    r = interest_rate / (100 * 12)  # interest per month
    monthly_payment = loan * ((r * ((r + 1) ** n)) / (((r + 1) ** n) - 1))
    return monthly_payment


def remaining_balance(loan: float, interest_rate: float, years: int, payments: int) -> float:
    """
    Calculate the remaining loan balance

    :param loan: initial loan amount
    :param interest_rate: interest rate
    :param years: loan term in years
    :param payments: total number of payments made
    :return: remaning balance
    """
    r = interest_rate / 1200  # monthly interest rate
    m = r + 1
    n = years * 12
    remaining = loan * (((m ** n) - (m ** payments)) / ((m ** n) - 1))
    return remaining


def loan_breakdown(loan: float, ir: float, years: int) -> list:
    """
    Calculate remaining balance per month
    :param loan: initial loan amount
    :param ir: interest rate
    :param years: loan term in years
    :return: remaining loan balance per month
    """
    bal = []
    for i in range((years * 12 + 1)):
        bal.append(remaining_balance(loan, ir, years, i))
    return bal


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # set minimum starting date to today
        self.start_date.setMinimumDate(QDate.currentDate())

        # connect on_click method to push button
        self.calc_push.clicked.connect(self.calculate_clicked)

        # update loan amount
        self.home_value.valueChanged.connect(self.update_loan)
        self.down_payment.valueChanged.connect(self.update_loan)
        self.radio_euro.toggled.connect(self.update_loan)
        self.radio_perc.toggled.connect(self.update_loan)

    def get_home_and_down_value(self) -> Tuple[float, float]:
        """
        Extract home value and down payment value inputted by the user
        :return: home and down payment value
        """

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
        """
        Dynamically update the loan amount
        :return: updates the loan amount field
        """
        home, down = self.get_home_and_down_value()
        self.loan_amount.setValue(int(home - down))

    def calculate_clicked(self):
        """
        On_click method for the calculate push button
        :return:
        """
        years = int(self.spin_years.text())
        loan_amount = float(self.loan_amount.text())
        ir = float(self.interest_spin.text())

        end = self.start_date.date().addYears(years)

        try:
            monthly = monthly_loan(loan_amount, ir, years)
            self.monthly_payments.setText(str(round(monthly, 2)))
            total_paid = monthly*12*years
            self.total_interest.setText(str(round(total_paid-loan_amount, 2)))
            self.total_paid.setText(str(round(total_paid, 2)))

            balance = loan_breakdown(loan_amount, ir, years)
            self.plot(range((years*12)+1), balance)
        except ZeroDivisionError:
            self.monthly_payments.setText("0")
            self.total_interest.setText("0")
            self.total_paid.setText("0")
        finally:
            self.end_date.setText(str(end.toString()))

    def plot(self, month, balance):
        """
        Plots the remaining balance per month

        :param month: month in loan payment
        :param balance: remaining balance per month
        :return:
        """
        self.graphWidget.plot(month, balance)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
