from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QMessageBox, QPushButton
from PyQt5.QtCore import pyqtSlot
import sys
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


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(0, 0, 600, 600)
        self.setWindowTitle("FRED Viewer")
        self.initUI()

    def initUI(self):
        # self.label = QtWidgets.QLabel(self)
        # self.label.setText("")
        # self.label.move(300,10)
        
        
        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(10, 10)
        self.textbox.resize(280,40)

        # Create a button in the window
        self.button = QPushButton('Fetch', self)
        self.button.move(300,10)
        
        # # connect button to function on_click
        self.button.clicked.connect(self.on_click)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.axes.plot([0,1,2,3,4], [10,1,20,3,40])
        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.canvas, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)

        layout.addWidget(self.textbox)
        layout.addWidget(self.button)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()

    def update_plot(self):
        # Drop off the first y element, append a new one.
        self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.xdata, self.ydata, 'r')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    
    @pyqtSlot()
    def on_click(self):
        series_name = self.textbox.text()
        print("Attempting to fetch data")
        try:
            df = nasdaqdatalink.get(f'FRED/{series_name}')
            df = df.reset_index()
            xdata = df["Date"]

            df['rolling_mean'] = df['Value'].rolling(5).mean()
            df['rolling_median'] = df['Value'].rolling(5).median()
            
            self.canvas.axes.cla()
            self.canvas.axes.plot(xdata, df["Value"], 'r', label="Value")
            self.canvas.axes.plot(xdata, df["rolling_mean"], 'g', label="1-Year Rolling Mean")
            self.canvas.axes.plot(xdata, df["rolling_median"], 'b', label="1-Year Rolling Median")

            print(df.head(20))
            self.canvas.axes.legend(loc="upper left")

            self.canvas.draw()

        except nasdaqdatalink.errors.data_link_error.DataLinkError as e:
            QMessageBox.critical(self, 'Message', "data.nasdaq.com returned an error. Are you sure you "
                + "spelt the ticker correctly and it exists in the FRED database?", QMessageBox.Ok, QMessageBox.Ok)
        except Exception as e:
            QMessageBox.critical(self, 'Message', "Unknown error. Have you set the NASDAQ_DATA_LINK_API_KEY env variable?", QMessageBox.Ok, QMessageBox.Ok)
            print(e)
            raise(e)

        self.textbox.setText("")

        


def window():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

window()