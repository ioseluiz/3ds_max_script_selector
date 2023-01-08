from PySide2 import QtCore
from PySide2 import QtGui
from PySide2.QtWidgets import (
	QMainWindow,
	QDockWidget,
	QWidget,
	QLabel,
	QComboBox,
	QPushButton,
	QRadioButton,
    QVBoxLayout
)
import shiboken2
from pymxs import runtime as rt
import csv



class PyMaxDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super(PyMaxDockWidget, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle('Script for Lift Selection - Construction Defects')
        self.initUI()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #qtmax.DisableMaxAcceleratorsOnFocus(self, True)
        
    def initUI(self):
        main_layout = QVBoxLayout()
        title_label = QLabel("Select lifts according to:")
        main_layout.addWidget(title_label)
        
        self.combo = QComboBox()
        self.combo.setObjectName("Structure")
        self.combo.addItems(["UE", "UW", "ME", "MW", "LE", "LW"])
        main_layout.addWidget(self.combo)
        
        self.rb_nodefects = QRadioButton("No Defects", self)
        main_layout.addWidget(self.rb_nodefects)
        
        self.rb_onedefect = QRadioButton("1 Defect", self)
        main_layout.addWidget(self.rb_onedefect)
        
        self.rb_twodefects = QRadioButton("2 Defects", self)
        main_layout.addWidget(self.rb_twodefects)
        
        self.rb_threeplusdefects = QRadioButton("> 3 Defects", self)
        main_layout.addWidget(self.rb_threeplusdefects)
        
        self.rb_ncrcod = QRadioButton("Has NCR or COD", self)
        main_layout.addWidget(self.rb_ncrcod)
        
        btn_select = QPushButton("SELECT LIFTS")
        btn_select.clicked.connect(self.probar_boton)
        main_layout.addWidget(btn_select)
        
        
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setWidget(widget)
        self.resize(250, 100)
        
    def probar_boton(self):
        # Obtner info de estructura (combobox)
        datos = self.read_file()
        print(len(datos))
        
        
        structure = self.combo.currentText()
        if self.rb_nodefects.isChecked():
            print("No Defects")
            lifts_nodefects = [x['name'].replace(" ","") for x in datos if int(x['defects']) == 0]
            print(len(lifts_nodefects))
            print(lifts_nodefects)
            self.select_lifts(lifts_nodefects)
            
        if self.rb_onedefect.isChecked():
            print("One Defect")
            lifts_onedefect = [x['name'].replace(" ","") for x in datos if int(x['defects']) == 1]
            print(len(lifts_onedefect))
            print(lifts_onedefect)
            self.select_lifts(lifts_onedefect)
            
        if self.rb_twodefects.isChecked():
            print("Two Defects")
            lifts_twodefects = [x['name'].replace(" ","") for x in datos if int(x['defects']) == 2]
            print(len(lifts_twodefects))
            print(lifts_twodefects)
            self.select_lifts(lifts_twodefects)
            
        if self.rb_threeplusdefects.isChecked():
            print("More than 3 defects")
            lifts_threeplusdefects = [x['name'].replace(" ","") for x in datos if int(x['defects']) >= 3]
            print(len(lifts_threeplusdefects))
            print(lifts_threeplusdefects)
            self.select_lifts(lifts_threeplusdefects)
            
            
        if self.rb_ncrcod.isChecked():
            print("NCR/COD")
            
    def read_file(self):
        data = []
        with open('defects_pacific.txt', mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data.append(row)
            return data
            
    def filter_ncr(self, data):
        pass
        
    def select_lifts(self,selection_list):
        existing_names = []
        existing_objs = rt.objects
        objects_for_selection = []
        for x in existing_objs:
            existing_names.append(x.name)
        for o in selection_list:
            if o in existing_names:
                objects_for_selection.append(rt.getNodeByName(o))
        rt.select(objects_for_selection)
        
        
    
        
        
def main():
    main_window_qwdgt = QWidget.find(rt.windows.getMAXHWND())
    main_window = shiboken2.wrapInstance(shiboken2.getCppPointer(main_window_qwdgt)[0], QMainWindow)
    w = PyMaxDockWidget(parent=main_window)
    w.setFloating(True)
    w.show()
    
if __name__ == '__main__':
    main()
    