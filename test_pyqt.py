import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout, QLineEdit, QTableWidget, QMessageBox, QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import nasdaqdatalink
import matplotlib
import random
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 1400
        self.height = 1000
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()
    
class MyTableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)
        
        self.tabs.addTab(self.tab1,"Graph")
        self.tabs.addTab(self.tab2,"Table")
        
        self.tab1.layout = QVBoxLayout(self)
        self.tab2.layout = QVBoxLayout(self)

        self.textbox = QLineEdit(self)
        self.textbox.move(10, 10)
        self.textbox.resize(280,40)

        self.button = QPushButton('Fetch', self)
        self.button.move(300,10)
        self.button.resize(280,40)

        self.button.clicked.connect(self.on_click)

        self.table = QTableWidget(2, 4, self)
        self.table.resize(1000, 100)

        self.canvas = MplCanvas(self, width=1, height=1, dpi=100)
        toolbar = NavigationToolbar(self.canvas, self)

        self.tab1.layout.addWidget(toolbar)
        self.tab1.layout.addWidget(self.canvas)
        self.tab1.layout.addWidget(self.textbox)
        self.tab1.layout.addWidget(self.button)
        self.tab1.setLayout(self.tab1.layout)

        self.tab2.layout.addWidget(self.table)
        self.tab2.setLayout(self.tab2.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
    @pyqtSlot()
    def on_click(self):
        series_name = self.textbox.text()

        try:
            df = self.fetch_series(series_name)
            df = df.reset_index()
        except Exception as e:
            return

        self.redraw_graph(df, series_name)
        self.repop_table(df)

        self.textbox.setText("")
    
    def fetch_series(self, series_name):
        try:
            return nasdaqdatalink.get(f'FRED/{series_name}')
        except nasdaqdatalink.errors.data_link_error.DataLinkError as e:
            QMessageBox.warning(self, 'Message', "data.nasdaq.com returned an error. Are you sure you "
                + "spelt the ticker correctly and it exists in the FRED database?", QMessageBox.Ok, QMessageBox.Ok)
            raise(e)
        except Exception as e:
            QMessageBox.critical(self, 'Message', "Unknown error. Have you set the NASDAQ_DATA_LINK_API_KEY env variable?", QMessageBox.Ok, QMessageBox.Ok)
            raise(e)

    def redraw_graph(self, df, series_name):
        xdata = df["Date"]

        df['rolling_mean'] = df['Value'].rolling(5).mean()
        df['rolling_median'] = df['Value'].rolling(5).median()
        
        self.canvas.axes.cla()
        self.canvas.axes.plot(xdata, df["Value"], 'r', label="Value")
        self.canvas.axes.plot(xdata, df["rolling_mean"], 'g', label="1-Year Rolling Mean")
        self.canvas.axes.plot(xdata, df["rolling_median"], 'b', label="1-Year Rolling Median")

        self.canvas.axes.legend(loc="upper left")

        self.canvas.axes.set_ylabel("Value")
        self.canvas.axes.set_xlabel("Date")
        self.canvas.axes.set_title(f"FRED/{series_name}")

        self.canvas.draw()


    def repop_table(self, df):

        mean_1 = df[df['Date'].dt.month == 1]["Value"].mean()
        mean_4 = df[df['Date'].dt.month == 4]["Value"].mean()
        mean_7 = df[df['Date'].dt.month == 7]["Value"].mean()
        mean_10 = df[df['Date'].dt.month == 10]["Value"].mean()

        self.table.setItem(0,0, QTableWidgetItem("Jan"))
        self.table.setItem(0,1, QTableWidgetItem("April"))
        self.table.setItem(0,2, QTableWidgetItem("July"))
        self.table.setItem(0,3, QTableWidgetItem("October"))
        
        self.table.setItem(1,0, QTableWidgetItem(str(round(mean_1,2))))
        self.table.setItem(1,1, QTableWidgetItem(str(round(mean_4,2))))
        self.table.setItem(1,2, QTableWidgetItem(str(round(mean_7,2))))
        self.table.setItem(1,3, QTableWidgetItem(str(round(mean_10,2))))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
