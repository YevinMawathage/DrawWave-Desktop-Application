
# DrawWave - AI-Powered Virtual Painter

DrawWave is an interactive desktop application that enables users to draw on a digital canvas using hand gestures or traditional mouse input. The application leverages computer vision and machine learning to track hand movements and convert them into drawing actions, providing an intuitive and engaging drawing experience.

![DrawWave Application](src/DrawWave%20-%20Poster%20-%2010898817.jpg)

## 🌟 Features

### Drawing Modes
- **Gesture Drawing**: Draw using hand gestures captured through your webcam
- **Mouse Drawing**: Traditional drawing using mouse input
- **Eraser Mode**: Easily erase parts of your drawing

### Hand Gesture Recognition
- **Drawing Gesture**: Index finger extended
- **Eraser Gesture**: Index and middle fingers extended
- **Clear Canvas Gesture**: Thumb up with closed fingers

### Canvas Tools
- **Color Selection**: Choose from a wide range of colors
- **Clear Canvas**: Start fresh with a single click
- **Save Functionality**: Export your drawings as images
- **Camera Selection**: Switch between available cameras

### User Interface
- **Split View Interface**: Simultaneous display of webcam feed and canvas
- **Intuitive Controls**: Easy-to-use buttons and keyboard shortcuts
- **Modern UI Design**: Clean and responsive interface

## 🔧 Technologies Used

- **Computer Vision**: OpenCV for image processing
- **Hand Tracking**: MediaPipe for accurate hand landmark detection
- **GUI Framework**: PyQt5 for building the interactive interface
- **Data Storage**: SQLite for saving application settings
- **Image Processing**: NumPy and Pillow for image manipulation
- **Packaging**: PyInstaller for creating standalone executables

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- Webcam (for gesture drawing)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YourUsername/DrawWave-Desktop-Application.git
   cd DrawWave-Desktop-Application
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
# From the project root directory
python src/main.py
```

### Building a Standalone Executable

```bash
pyinstaller DrawWave.spec
```
The executable will be created in the `dist` directory.

## 🎮 How to Use

### Start Screen
When you launch DrawWave, you'll be presented with a start screen where you can begin a new drawing session.

### Drawing Modes
- **Gesture Drawing**: Click the "Gesture Draw" button and use hand gestures in front of your webcam
- **Mouse Drawing**: Click the "Mouse Draw" button and use your mouse to draw on the canvas
- **Eraser**: Click the "Erase" button to switch to eraser mode

### Hand Gestures
- **Draw**: Extend your index finger
- **Erase**: Extend your index and middle fingers
- **Clear Canvas**: Show a thumbs up gesture

### Controls
- **Change Color**: Click the "Change Color" button to open the color picker
- **Clear Canvas**: Click the "Clear" button to erase everything
- **Save Drawing**: Click the "Save" button to export your drawing as an image
- **Switch Camera**: Click the camera icon to switch between available webcams

## 📁 Project Structure

```
DrawWave-Desktop-Application/
├── src/                      # Source code
│   ├── main.py               # Application entry point
│   ├── virtual_painter_gui.py # Main application GUI
│   ├── hand_tracking.py      # Hand tracking and gesture recognition
│   ├── canvas.py             # Canvas drawing logic
│   ├── canvas_widget.py      # Canvas widget implementation
│   ├── database.py           # Database operations
│   ├── start_screen.py       # Start screen implementation
│   └── resource_path.py      # Resource path utilities
├── assests/                  # Images and static resources
├── requirements.txt          # Project dependencies
├── DrawWave.spec            # PyInstaller specification file
└── README.md                # Project documentation
```

## 🤝 Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 🔬 Requirements

The following dependencies are required to run DrawWave:

```
opencv-python     # Computer vision functionality
mediapipe         # Hand tracking and gesture recognition
numpy             # Numerical computing
PyQt5             # GUI framework
Pillow            # Image processing
pyinstaller       # For creating standalone executables
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for the hand tracking framework
- [OpenCV](https://opencv.org/) for computer vision capabilities
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework

---

<p align="center">
  Made with ❤️ for the joy of creative expression through technology
</p>

=======
# AI Virtual Painter

This project enables users to draw on a whiteboard using hand gestures and mouse input. It uses OpenCV, MediaPipe, NumPy, PyQt5, and SQLite to build the application.

## Features:
- Hand gesture recognition
- Color and brush size selection
- Undo/Redo, Save/Export functionality
>>>>>>> bb13ed99570bbb1a47fcbd98e41ca5ac9dc469a0
