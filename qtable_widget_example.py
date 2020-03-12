import PyQt4
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFont

app = QtGui.QApplication([])

columns = ['Column 0', 'Column 1', 'Column 2']
items = [['Row%s Col%s' % (row, col) for col in range(len(columns))] for row in range(100)]

view = QtGui.QTableWidget()

afont = PyQt4.QtGui.QFont()
afont.setFamily("Arial Black")
afont.setPointSize(30)

# styleSheet = "QHeaderView {" \
#              "spacing: 10px;" \
#              "background-color: yellow;" \
#              "color: white;" \
#              "border: 1px solid red;" \
#              "margin: 1px;" \
#              "text-align: right;" \
#              "font-family: arial;" \
#              "font-size: 12px; }" \
# bFont=PyQt4.QtGui.QFont("Arial", 20, QFont.Bold)
# view.horizontalHeader().setStyleSheet("QHeaderView {font-size: 30pt; color: blue; background-color:lightblue;}")
# view.horizontalHeader().setStyleSheet(styleSheet)

# styleSheet =

font_type = 'bold'
background_color = 'blue'
font_size = 15
foreground_color = 'white'
font_weight = 'bold'

# str_sub = "font-weight: %s; color: %s; font-size: %dpx; background-color: %s;" % (font_weight, foreground_color, font_size, background_color)
str_sub = ""
if font_type is not None:
    str_sub = "font-weight: {};".format(str.lower(font_type))
if foreground_color is not None:
    str_sub += "color: {};".format(str.lower(foreground_color))
if background_color is not None:
    str_sub += "background-color: {};".format(str.lower(background_color))
if font_size is not None:
    str_sub += "font-size: {}pt;".format(font_size)
ss = "QHeaderView::section {%s}" % str_sub

# ss = "QHeaderView::section {color: white;font-size: 30pt; background-color: red;}"

# ss = "QHeaderView::section {font-weight: %s; color: %s; font-size: %dpx; background-color: %s;}" % \
#      (font_weight, foreground_color, font_size, background_color)
view.horizontalHeader().setStyleSheet(ss)

# view.horizontalHeader().setFont(bFont)
# view.horizontalHeader().setStyleSheet("QHeaderView { font-size: 30pt; }")
# view.horizontalHeader().setFont(afont)
# view.horizontalHeader().setStyleSheet("color: blue;")

view.setColumnCount(len(columns))
view.setHorizontalHeaderLabels(columns)
view.setRowCount(len(items))
for row, item in enumerate(items):
    for col, column_name in enumerate(item):
        item = QtGui.QTableWidgetItem("%s" % column_name)
        view.setItem(row, col, item)
    view.setRowHeight(row, 16)

view.show()
app.exec_()
