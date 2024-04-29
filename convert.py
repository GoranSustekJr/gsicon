import numpy as np
from PIL import Image, ImageFilter
import math
import argparse
from matplotlib import colors
import threading
import sys, time
from yaspin import yaspin



# Class that does operations on a single pixel
class Pixel:
    def __init__(self, p):
        self.p = p
    def euclidianDistanceWhite(self): # Euclidian distance from some pixel to white pixel
        return math.sqrt(((255 - self.p[0]) ** 2 + (255 - self.p[1]) ** 2 + (255 - self.p[2]) ** 2))

    def euclidianDistanceBlue(self): # Euclidian distance from some pixel to true blue pixel
        return math.sqrt(((0 - self.p[0]) ** 2 + (0 - self.p[1]) ** 2 + (255 - self.p[2]) ** 2))

###    def euclidianDistanceSky(self): # Euclidian distance from some pixel to average sky pixel
###        return math.sqrt(((self.s[0] - self.p[0]) ** 2 + (self.s[1] - self.p[1]) ** 2 + (self.s[2] - self.p[2]) ** 2))

    def averageDistanceWhite(self): # Average distance from some pixels RGB to white pixel
        return math.sqrt(((255 - self.p[0]) ** 2 + (255 - self.p[1]) ** 2 + (255 - self.p[2]) ** 2) / 3)

    def averageDistanceBlue(self): # Average distance from some pixels RGB to true blue pixel
        return math.sqrt(((0 - self.p[0]) ** 2 + (0 - self.p[1]) ** 2 + (255 - self.p[2]) ** 2) / 3)
    
    def averageRGB(self): # Average o the RGB values
        return (self.p[0] / 3 + self.p[1] / 3 + self.p[2] / 3)
    
    def updatePixel(self, p):
        self.p[0] = p[0]
        self.p[1] = p[1]
        self.p[2] = p[2]
        self.p[3] = p[3]
        
    def updatePixelAlpha(self, p):
        self.p[3] = p[3]


# Class that does operations on multiple pixels
class Pixels:
    def __init__(self, matrix, color):
        print("     Converting color code format to hex.... ")
        self.color = [int(x * 255) for x in colors.hex2color(f"#{color}")]        
        self.matrix = matrix
        print("     Finding the closest pixel to true white by euclidian distance.... ")
        self.closest = self.closestToWhite()
        

    def skyRGB(self): # Get sky color based on average values of RGB for pixels that have R < 65 and G < 125 //TODO: Fix this function
        x_axis = self.matrix.shape[0]
        y_axis = self.matrix.shape[1]
        check = 0
        red = 0
        green = 0
        blue = 0
        for x in range(x_axis):
            for y in range(y_axis):
                pixel = self.matrix[x, y]
                if (pixel[0] <= 80 and pixel[1] <= 135):
                    check += 1
                    red += pixel[0]
                    green += pixel[1]
                    blue += pixel[2]
        return [(red // check), (green // check), (blue // check)]
    
    def closestToWhite(self): # Max verage o the RGB values
        closest = 0
        x_axis = self.matrix.shape[0]
        y_axis = self.matrix.shape[1]
        for x in range(x_axis):
            for y in range(y_axis):
                pixel = Pixel(self.matrix[x,y])
                euDisWhite = pixel.euclidianDistanceWhite()
                if euDisWhite > closest:
                    closest = euDisWhite
        return closest

    def removeShitWithCAG(self, CAGC): # Name in honor of Thomas; Remove sky elements from the picture by making their alpha value 0 while optimizing for CAG ( Cloud Alpha Gradient Coefficient )
        x_axis = self.matrix.shape[0]
        y_axis = self.matrix.shape[1]
        for x in range(x_axis):
            for y in range(y_axis):
                pixel = Pixel(self.matrix[x, y])
                if pixel.euclidianDistanceBlue() < pixel.euclidianDistanceWhite():
                    self.matrix = [self.color[0], self.color[1], self.color[2], 0]
                else:
                    self.matrix[x,y] = [self.color[0], self.color[1], self.color[2], math.ceil((pixel.averageRGB() / self.closest) * 255 * CAGC)]
                    
    def removeShit(self): # Name in honor of Thomas; Remove sky elements from the picture by making their alpha value 0 without CAG ( Cloud Alpha Gradient )
        x_axis = self.matrix.shape[0]
        y_axis = self.matrix.shape[1]
        for x in range(x_axis):
            for y in range(y_axis):
                pixel = Pixel(self.matrix[x, y])
                if pixel.euclidianDistanceBlue() < pixel.euclidianDistanceWhite():
                    self.matrix[x,y] = [self.color[0], self.color[1], self.color[2], 0]
                else:
                    self.matrix[x,y] = [self.color[0], self.color[1], self.color[2], 255]


def process_image(input, output, blurRadius, cloudAlphaGradientCoefficient, cloudColor):
    print("Opening image and applying blur... ") # Showing user status
    image = Image.open(input).convert('RGBA').filter(ImageFilter.GaussianBlur(blurRadius)) # Open image, convert it to RGBA and add Gaussian blur
    
    print(f"Converting image to 3D pixel array... ")
    image_matrix = Pixels(np.array(image), cloudColor) # Convert that image to pixel array
    
    if (cloudAlphaGradientCoefficient != 0): # If alpha gradient specified
        print(f"Removing shit and adding cloud alpha {cloudAlphaGradientCoefficient}%.... ")
        image_matrix.removeShitWithCAG(cloudAlphaGradientCoefficient) # Run optimized remove sky pixels function with CAG
    else:
        print("Started removing shit")
        image_matrix.removeShit() # Run remove sky pixels function
    
    print("Converting changed 3D pixel array to a new image... ")
    converted = Image.fromarray(image_matrix.matrix, 'RGBA') # Convert the proccessed instance of the image to image file type RGBA 
    
    print("Saving processed image.... ")
    converted.save(output) # Save the converted image to the output file path
    
def main(): # Main function
    # Create arguments for CLI like command
    pars = argparse.ArgumentParser(description="Get cloud icon/image from an image of cloud/sky that does not contain anything except clear sky and clouds ( No land, no mountains... ). Extract cluod from an image of the sky.")
    pars.add_argument("input_image", type=str, help="Input image file path") # Input image parameter
    pars.add_argument("output_image", type=str, help="Output image file path") # Output image parameter
    pars.add_argument("--blur-radius", type=int, default=25, help="Gaussian blur radius, ( default 25 )") # Blur radius parameter
    pars.add_argument("--cloud-alpha-gradient-coefficient", type=int, default=0, help="Should cloud have alpha gradient coefficient in % ( 0 - 100, default 0 = no CAGC )") # Cloud Alpha Gradient Coefficient parameter
    pars.add_argument("--cloud-color", type=str, default="ffffff", help="Output cloud color, ( hex code, default ffffff )") # Cloud color parameter

    args = pars.parse_args() # Parse the CLI arguments
    
    process_image(args.input_image, args.output_image, args.blur_radius , args.cloud_alpha_gradient, args.cloud_color) # Start image proccessing


if __name__ == '__main__':
    spinner = yaspin()
    spinner.start()
    main() # Start the main function
    spinner.stop()