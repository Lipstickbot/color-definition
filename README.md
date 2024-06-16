# color-definition
Importing necessary libraries
python

import argparse
import cv2
import numpy as np
import pandas as pd
import sys
import os
argparse: library for handling command-line arguments.
cv2: OpenCV library for image processing.
numpy: library for working with arrays.
pandas: library for working with tabular data (e.g., CSV files).
sys: library for interacting with system parameters and functions.
os: library for interacting with the file system.
Function for handling command-line arguments
python

def parse_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required=True, help="Image Path")
    ap.add_argument('-c', '--colors', required=False, help="Colors CSV Path", default='colors.csv')
    return vars(ap.parse_args())
Creates an ArgumentParser object for handling command-line arguments.
Adds two arguments: path to the image (--image) and path to the colors CSV file (--colors).
Returns a dictionary with the arguments.
Function to get the color name
python
def getColorName(R, G, B, csv):
    minimum = 10000
    cname = ""
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname
Takes the R, G, B values and a DataFrame csv containing the colors.
Calculates the distance between the given color and the colors in the CSV.
Returns the name of the color with the minimum distance.
Mouse callback function
python

def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked, img
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)
Defines actions to be taken on a double left-click.
Saves the coordinates of the click and the B, G, R values of the pixel.
Main function
python

def main(img_path, colors_path):
    global img, clicked, b, g, r, xpos, ypos

    clicked = False
    r = g = b = xpos = ypos = 0

    # Read image with OpenCV
    img = cv2.imread(img_path)

    if img is None:
        print(f"Error: The image at {img_path} could not be read.")
        sys.exit()

    # Read the CSV file with pandas
    if not os.path.isfile(colors_path):
        print(f"Error: The colors CSV file at {colors_path} could not be found.")
        sys.exit()

    index = ["color", "color_name", "hex", "R", "G", "B"]
    csv = pd.read_csv(colors_path, names=index, header=None)

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_function)

    while True:
        cv2.imshow("image", img)
        if clicked:
            # Draw a rectangle filled with the color
            cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

            # Create text string to display (color name and RGB values)
            text = getColorName(r, g, b, csv) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

            # Display the text
            cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            
            # For very light colors, display text in black
            if r + g + b >= 600:
                cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

            clicked = False

        # Break the loop when the user hits 'esc' key
        if cv2.waitKey(20) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
Initializes global variables.
Loads the image using OpenCV.
Checks for the existence and loads the CSV file with colors.
Sets up the OpenCV window and binds it to the mouse event handler.
In a loop, displays the image and handles double-clicks to show the color name.
Breaks the loop when the "Esc" key is pressed.
Entry point of the program
python

if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = parse_arguments()
        img_path = args['image']
        colors_path = args['colors']
    else:
        # Hard-code the image path and colors CSV path here for testing purposes
        img_path = r'C:\Users\vovot\Downloads\python-project-color-detection\colorpic.jpg'  # Use raw string
        colors_path = r'C:\Users\vovot\Downloads\python-project-color-detection\colors.csv'  # Use raw string

    main(img_path, colors_path)
Checks if command-line arguments are provided.
If arguments are provided, uses them. Otherwise, uses hard-coded paths for testing.
Calls the main function main() with the image and CSV file paths.
This code allows you to determine and display the name of the color of any pixel on the image upon double-clicking with the mouse.
