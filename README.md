# Knotz Image Zoom-Out Video Generator

This application allows users to create a zoom-out effect on an image and generate a video from the effect. It provides a simple and user-friendly interface where users can select an image, specify the video duration and the frames per second, and choose an output directory for the video.

## Features

- User-friendly GUI
- Generates a video with a zoom-out effect from a selected image
- Allows user to specify the video duration and the frames per second
- Outputs the video to a user-specified directory

## Future Enhancements

- Support for multiple files
- Allow user to specify the starting point of the zoom-out effect on the image
- Other effects like panning, blur, and fade

## Installation

### Prerequisites

Before you start, ensure you have met the following requirements:

* You have installed Python 3.9 or later. If you haven't installed Python yet, you can download it from [here](https://www.python.org/downloads/). The Python package includes the Tkinter module by default. If you're using a Python version earlier than 3.9, you might need to install Tkinter separately.

* You have a Windows/Linux/Mac machine that can run Python and Tkinter.

### Installing Image Zoom-Out Video Generator

To install Image Zoom-Out Video Generator, follow these steps:

1. Clone the repository or download the source code.
2. Navigate to the project directory in your terminal or command prompt.
3. Install the required Python packages using pip:

   ```
   pip install -r requirements.txt
   ```

   If you have both Python 2.x and Python 3.x installed, you might need to use `pip3` instead of `pip`.

4. Run the application:

   ```
   python zoomui.py
   ```

   If you have both Python 2.x and Python 3.x installed, you might need to use `python3` instead of `python`.

If you encounter any problems during the installation, feel free to open an issue on this GitHub repository.

## Usage

1. Click the 'Browse' button next to 'Image File' to select an image
2. Enter the desired video duration in seconds
3. Enter the desired frames per second
4. Click the 'Browse' button next to 'Output Directory' to select a directory where the video will be saved
5. Click the 'Generate Video' button to start the processing. A message saying 'Processing...' will appear
6. Once the video has been generated, a message saying 'Processing complete!' will appear

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
