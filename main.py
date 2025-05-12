import sys
from PyQt5.QtWidgets import QApplication
from start_screen import StartScreen

def main():
    app = QApplication(sys.argv)
    start = StartScreen()  # Instantiate VirtualPainterGUI instead of StartScreen
    start.show() # Show the canvas window directly
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
