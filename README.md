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

1. Clone this repository
2. Navigate to the cloned repository
3. Install the required packages by running `pip install -r requirements.txt`
4. Run `python zoom.py` to start the application (zoomui.py is for testing)

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
