import sys
import yfinance as yf
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QComboBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, timedelta

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
        self.date_range_label = QLabel('Select Date Range:')
        self.date_range_combo = QComboBox()
        self.date_range_combo.addItem('All')
        self.date_range_combo.addItem('5 years')
        self.date_range_combo.addItem('3 years')
        self.date_range_combo.addItem('1 year')
        self.date_range_combo.addItem('YTD')
        layout.addWidget(self.date_range_label)
        layout.addWidget(self.date_range_combo)

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
        selected_range = self.date_range_combo.currentText()
        
        end_date = datetime.today().date()
        
        if selected_range == '5 years':
            start_date = end_date - timedelta(days=365 * 5)
        elif selected_range == '3 years':
            start_date = end_date - timedelta(days=365 * 3)
        elif selected_range == '1 year':
            start_date = end_date - timedelta(days=365)
        elif selected_range == 'YTD':
            start_date = datetime(end_date.year, 1, 1).date()
        else:  # 'All'
            start_date = datetime(1970, 1, 1).date()

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
