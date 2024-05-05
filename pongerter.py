from email.policy import default
from lib2to3.pytree import convert
from sqlite3 import converters
import numpy as np
from PIL import Image, ImageFilter
import math
import argparse
from matplotlib import colors

########################
### Helper functions ###
########################

def euclidianDistanceWhite(p): # Euclidian distance from some pixel to white pixel
    return math.sqrt(((255 - p[0]) ** 2 + (255 - p[1]) ** 2 + (255 - p[2]) ** 2))

def euclidianDistanceBlue(p): # Euclidian distance from some pixel to true blue pixel
    return math.sqrt(((0 - p[0]) ** 2 + (0 - p[1]) ** 2 + (255 - p[2]) ** 2))

def average(p):
    return (p[0] / 3) + (p[1] / 3) + (p[2] / 3)



######################
### Mode functions ###
######################

# Default mode function
def defaultMode(matrix, color, alpha, xAxis, yAxis):
    for x in range(xAxis):
        for y in range(yAxis):
            pixel = matrix[x,y]
            distanceBlue = euclidianDistanceBlue(pixel)
            distanceWhite = euclidianDistanceWhite(pixel)
            if distanceBlue < distanceWhite:
                pixel[3] = 0
            else:
                pixel[0] = color[0]
                pixel[1] = color[1]
                pixel[2] = color[2]
                pixel[3] = math.ceil(255 * alpha)
    return matrix

# Average mode function
def averageMode(matrix, color, alpha, xAxis, yAxis):
    biggest = 0 # Biggest average RGB value
    
    for x in range(xAxis):
        for y in range(yAxis):
            pixel = matrix[x,y]
            avrg = average(pixel)
            if avrg > biggest:
                biggest = avrg

    for x in range(xAxis):
        for y in range(yAxis):
            pixel = matrix[x,y]
            distanceBlue = euclidianDistanceBlue(pixel)
            distanceWhite = euclidianDistanceWhite(pixel)
            if distanceBlue < distanceWhite:
                pixel[3] = 0
            else:
                avrg = average(pixel)
                pixel[0] = color[0]
                pixel[1] = color[1]
                pixel[2] = color[2]
                pixel[3] = math.ceil(255 * (avrg / biggest) * alpha)
    return matrix
                
# Euclidian mode
def euclidianMode(matrix, color, alpha, xAxis, yAxis):
    closest = 195076
    for x in range(xAxis):
        for y in range(yAxis):
            pixel = matrix[x,y]
            euDisWhite = euclidianDistanceWhite(pixel)
            if euDisWhite < closest:
                closest = euDisWhite
                
    for x in range(xAxis):
        for y in range(yAxis):
            pixel = matrix[x,y]
            distanceBlue = euclidianDistanceBlue(pixel)
            distanceWhite = euclidianDistanceWhite(pixel)
            if distanceBlue < distanceWhite:
                pixel[3] = 0
            else:
                pixel[0] = color[0]
                pixel[1] = color[1]
                pixel[2] = color[2]
                pixel[3] = math.ceil(255 * (closest / distanceWhite) * alpha)
    
    return matrix



#################################
### Image Processing Function ###
#################################

def imageProcessing(input, output, mode, color, blurRadius, alpha): # Image processing function, decides by the arguments what will be done
    image = Image.open(input).convert("RGBA").filter(ImageFilter.GaussianBlur(blurRadius))
    imageMatrix = np.array(image)
    
    xAxis = imageMatrix.shape[0]
    yAxis = imageMatrix.shape[1]
    
    colorHex = [int(x * 255) for x in colors.hex2color(f"#{color}")]
    
    if mode == 'default':
        imageMatrix = defaultMode(imageMatrix, colorHex, alpha / 100, xAxis, yAxis)
    elif mode == 'average':
        imageMatrix = averageMode(imageMatrix, colorHex, alpha / 100, xAxis, yAxis)
    elif mode == 'euclidian':
        imageMatrix = euclidianMode(imageMatrix, colorHex, alpha / 100, xAxis, yAxis)
    
    converted = Image.fromarray(imageMatrix, 'RGBA')
    converted.save(output)
    


#################
##### MAIN ######
#################
def main():
    parser = argparse.ArgumentParser(description="Image Processing Tool")
    parser.add_argument("input_file", help="Input file name")
    parser.add_argument("output_file", help="Output file name")
    parser.add_argument("--mode", choices=['euclidian', 'average', 'default'], default='default', help="Processing mode (default: default)")
    parser.add_argument("--color", default='ffffff', help="Color in ffffff format (default: ffffff)")
    parser.add_argument("--blur-radius", type=int, default=25, help="Gaussian blur radius (default: 25)")
    parser.add_argument("--alpha", type=int, default=100, choices=range(1, 101), help="Alpha value (1-100, default: 100)")

    args = parser.parse_args() # Parse the command line arguments
    
    imageProcessing(args.input_file, args.output_file, args.mode, args.color, args.blur_radius, args.alpha) # Call the image processing funciton


# Start the program
if __name__ == '__main__':
    main()