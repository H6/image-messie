# Image Messie

![Image Messie](image-messie.png)

_Messie [ˈmɛsiː]: german word for a compulsive hoarder._

## Overview
Image Messie is a Python tool designed to help organize and manage unsorted image files. It simplifies the process of copying image files from a source folder to a destination folder, making it easier to keep your images well-organized.

## Features
- Copy image files from any source folder to a specified destination folder.
- Group images by year, month and by the camera model used to take the picture.
- Simple and easy-to-use command-line interface.

## Grouping
Image Messie automatically groups images in the destination folder based on the date they were taken and the camera model. This feature organizes the images into subfolders following a Year/Month/Day structure and categorizes them by the camera model, making it easier to find and manage photos from specific dates or taken with specific cameras.

For example, an image taken on March 5, 2023, with a Canon EOS camera will be placed in:
`DESTINATION_FOLDER/2023/03_March/CANON_EOS/`

## Requirements
- Python 3.x

## Setup Virtual Environment
To create a virtual environment for Image Messie, follow these steps:

1. Open your terminal and navigate to the directory where you have the `messie.py` script.
2. Run the following command to create a virtual environment named `.venv`:

python -m venv .venv

3. Activate the virtual environment:
- On Windows, run:
  ```
  .venv\Scripts\activate
  ```
- On macOS and Linux, run:
  ```
  source .venv/bin/activate
  ```
4. Once the virtual environment is activated, you can install any required dependencies using `pip install -r requirements.txt`

Remember to activate the virtual environment every time you work on the project.


## Usage
To use Image Messie, run the following command in your terminal:

```
python messie.py --path SOURCE_FOLDER --destination DESTINATION_FOLDER
```

Replace `SOURCE_FOLDER` with the path to the folder containing the unsorted images, and `DESTINATION_FOLDER` with the path where you want the images to be copied.

## Examples

```
python messie.py --path /path/to/unsorted/images --destination /path/to/sorted/images
```


## Contributing
Contributions to Image Messie are welcome! Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## License

MIT License

Copyright (c) 2024 H6

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## Contact
For any questions or feedback, please contact [Your Contact Information].

