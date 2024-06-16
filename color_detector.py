import argparse
import cv2
import numpy as np
import pandas as pd
import sys
import os

# Function to handle argument parsing
def parse_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required=True, help="Image Path")
    ap.add_argument('-c', '--colors', required=False, help="Colors CSV Path", default='colors.csv')
    return vars(ap.parse_args())

# Function to get color name
def getColorName(R, G, B, csv):
    minimum = 10000
    cname = ""
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# Mouse callback function
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

# Main function
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
