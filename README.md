# Infant-Danger-Detection-using-OpenCV
This project is designed to track the movements of an infant in a room using a webcam. The system allows you to select the infant using a rectangular box and mark dangerous areas in the room, such as switch boxes. If the infant moves near a marked danger zone, the system will alert the parents by playing a warning sound or voice alert.

## Features
- **Real-Time Object Tracking:** The system tracks the infant's movements in real-time using a webcam.
- **Customizable Danger Zones:** Users can manually mark dangerous areas in the room.
- **Proximity Alerts:** The system alerts parents if the infant is detected near any of the marked danger zones.
- **Audio Alerts:** Uses text-to-speech and sound alerts to notify parents of potential danger.

## Installation
1. **Clone the Repository**
    ```bash
    git clone https://github.com/yourusername/infant-danger-detection-opencv.git
    cd infant-danger-detection-opencv
    ```

2. **Install Dependencies**
    Make sure you have Python 3.x installed. Then, install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application**
    Start the application by running:
    ```bash
    python main.py
    ```

## Usage
1. **Selecting the Infant:**
   - When the video stream starts, draw a rectangular box around the infant to initiate tracking.

2. **Marking Danger Zones:**
   - After selecting the infant, you can click on the video feed to mark dangerous areas. These areas will be monitored continuously.

3. **Monitoring and Alerts:**
   - The system will track the infant’s position relative to the danger zones. If the infant gets too close to a marked area, an alert will be triggered to notify the parents.

## Dependencies
- **Python 3.x**
- **OpenCV** (`cv2`)
- **imutils**
- **scipy**
- **pyttsx3**
- **playsound**
- **tkinter** (for GUI elements)

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request or open an issue if you find any bugs or have suggestions for improvements.
