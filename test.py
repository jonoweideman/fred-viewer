import pytest

from PyQt5 import QtCore

import fred_viewer


@pytest.fixture
def app(qtbot):
    test_app = fred_viewer.App()
    qtbot.addWidget(test_app)

    return test_app

def test_initialization(app):
    assert app.table_widget.textbox.text() == ""

def test_after_fetch(app, qtbot):
    app.table_widget.textbox.setText("GDP")
    qtbot.mouseClick(app.table_widget.button, QtCore.Qt.LeftButton)
    assert app.table_widget.table.item(0,0).text() == "Jan"
    assert float(app.table_widget.table.item(1,0).text()) > 0 

