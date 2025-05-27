import sys
from PyQt5.QtWidgets import QApplication
from start_screen import StartScreen

def main():
    app = QApplication(sys.argv)
    start = StartScreen()  
    start.show() 
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()




