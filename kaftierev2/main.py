'''
Created on 5 avr. 2013

@author: moustache
'''

import sys
from PySide.QtGui import QApplication
from qt.fenetres import MainFenetre



if __name__=="__main__":  
    app=QApplication(sys.argv)
    mainFenetre = MainFenetre()
    sys.exit(app.exec_())

    

