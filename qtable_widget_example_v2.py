from PyQt4 import QtGui
from PyQt4.QtGui import QFont, QStyleFactory

app = QtGui.QApplication([])
# app.setStyle (QStyleFactory.create ('Fusion'))

columns = ['Column 0', 'Column 1', 'Column 2']
items = [['Row%s Col%s' % (row, col) for col in range(len(columns))] for row in range(1)]

view = QtGui.QTableWidget()

view.setColumnCount(len(columns))
view.setHorizontalHeaderLabels(columns)
view.setRowCount(len(items))
for row, item in enumerate(items):
    for col, column_name in enumerate(item):
        item = QtGui.QTableWidgetItem("%s" % column_name)
        view.setItem(row, col, item)
    view.setRowHeight(row, 16)

fnt = QFont()
fnt.setPointSize(15)
fnt.setBold(True)
fnt.setFamily("Arial")

item1 = view.horizontalHeaderItem(0)
item1.setForeground(QtGui.QColor(255, 0, 0))
item1.setBackground(QtGui.QColor(0, 0, 0))  # Black background! does not work!!
item1.setFont(fnt)

item2 = view.horizontalHeaderItem(1)
item2.setForeground(QtGui.QColor(0, 255, 0))
item2.setFont(fnt)

item3 = view.horizontalHeaderItem(2)
item3.setForeground(QtGui.QColor(255, 0, 255))

view.setHorizontalHeaderItem(0, item1)
view.setHorizontalHeaderItem(1, item2)
view.setHorizontalHeaderItem(2, item3)

view.show()
app.exec_()
