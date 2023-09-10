import sys
import yfinance as yf
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime

class StockPriceGraphApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Stock Price Graph')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Stock symbol input
        self.symbol_label = QLabel('Enter Stock Symbol:')
        self.symbol_input = QLineEdit()
        layout.addWidget(self.symbol_label)
        layout.addWidget(self.symbol_input)

        # Date range selection
        self.start_date_label = QLabel('Start Date:')
        self.start_date_picker = QDateEdit()
        self.start_date_picker.setDate(datetime(2021, 1, 1).date())
        layout.addWidget(self.start_date_label)
        layout.addWidget(self.start_date_picker)

        self.end_date_label = QLabel('End Date:')
        self.end_date_picker = QDateEdit()
        self.end_date_picker.setDate(datetime.today().date())
        layout.addWidget(self.end_date_label)
        layout.addWidget(self.end_date_picker)

        # Fetch and display button
        self.fetch_button = QPushButton('Fetch and Display')
        layout.addWidget(self.fetch_button)

        # Graph display
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.fetch_button.clicked.connect(self.plot_stock_price)

        self.setLayout(layout)

    def plot_stock_price(self):
        symbol = self.symbol_input.text()
        start_date = self.start_date_picker.date().toPyDate()
        end_date = self.end_date_picker.date().toPyDate()

        if symbol:
            df = yf.download(symbol, start=start_date, end=end_date)
            if not df.empty:
                self.figure.clear()
                ax = self.figure.add_subplot(111)
                df['Adj Close'].plot(ax=ax, title=f'Stock Price for {symbol}')
                ax.set_xlabel('Date')
                ax.set_ylabel('Price')
                self.canvas.draw()
            else:
                self.figure.clear()
                self.canvas.draw()
                print("No data found for the selected stock symbol and date range.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StockPriceGraphApp()
    window.show()
    sys.exit(app.exec_())
