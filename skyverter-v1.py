import numpy as np
from PIL import Image, ImageFilter
import math

### DEFAULT - Image turned to white with gaussian blur with radius of 25, then cut of what is further from true white than true blue
# Color is white
def euclidianDistanceWhite(p): # Euclidian distance from some pixel to white pixel
    return math.sqrt(((255 - p[0]) ** 2 + (255 - p[1]) ** 2 + (255 - p[2]) ** 2))

def euclidianDistanceBlue(p): # Euclidian distance from some pixel to true blue pixel
    return math.sqrt(((0 - p[0]) ** 2 + (0 - p[1]) ** 2 + (255 - p[2]) ** 2))


def processImageDefault():
    image = Image.open('cloud.png').convert('RGBA').filter(ImageFilter.GaussianBlur(25))
    image_matrix = np.array(image)
    
    x_axis = image_matrix.shape[0]
    y_axis = image_matrix.shape[1]
    
    closest = 195076
    for x in range(x_axis):
        for y in range(y_axis):
            pixel = image_matrix[x,y]
            euDisWhite = euclidianDistanceWhite(pixel)
            if euDisWhite < closest:
                closest = euDisWhite

        
    for x in range(x_axis):
        for y in range(y_axis):
            pixel = image_matrix[x,y]
            distanceBlue = euclidianDistanceBlue(pixel)
            distanceWhite = euclidianDistanceWhite(pixel)
            if distanceBlue < distanceWhite:
                pixel[3] = 0
            else:
                alpha = math.ceil(255 * (closest / distanceWhite) * 0.5)
                print(alpha, int(alpha))
                pixel[0] = 255
                pixel[1] = 255
                pixel[2] = 255
                pixel[3] = int(alpha)
                
    converted = Image.fromarray(image_matrix, 'RGBA')
    converted.save('cloud-defualt-50.png')
    
    
### Average - Image turned with alpha using average RGB values, othervise same as default

def average(p):
    return (p[0] / 3) + (p[1] / 3) + (p[2] / 3)

def processImageAverage():
    image = Image.open('cloud.png').convert('RGBA').filter(ImageFilter.GaussianBlur(25))
    image_matrix = np.array(image)
    
    x_axis = image_matrix.shape[0]
    y_axis = image_matrix.shape[1]
    
    biggest = 0
    for x in range(x_axis):
        for y in range(y_axis):
            pixel = image_matrix[x,y]
            avrg = average(pixel)
            if avrg > biggest:
                biggest = avrg

        
    for x in range(x_axis):
        for y in range(y_axis):
            pixel = image_matrix[x,y]
            distanceBlue = euclidianDistanceBlue(pixel)
            distanceWhite = euclidianDistanceWhite(pixel)
            if distanceBlue < distanceWhite:
                pixel[3] = 0
            else:
                avrg = average(pixel)
                alpha = math.ceil(255 * (avrg / biggest) * 0.5)
                pixel[0] = 255
                pixel[1] = 255
                pixel[2] = 255
                pixel[3] = alpha
                
    converted = Image.fromarray(image_matrix, 'RGBA')
    converted.save('cloud-average-50.png')
    
### No alpha gradient
def processImageNoAlphaGradient():
    image = Image.open('cloud.png').convert('RGBA').filter(ImageFilter.GaussianBlur(25))
    image_matrix = np.array(image)
    
    x_axis = image_matrix.shape[0]
    y_axis = image_matrix.shape[1]
    
    for x in range(x_axis):
        for y in range(y_axis):
            pixel = image_matrix[x,y]
            distanceBlue = euclidianDistanceBlue(pixel)
            distanceWhite = euclidianDistanceWhite(pixel)
            if distanceBlue < distanceWhite:
                pixel[3] = 0
            else:
                pixel[0] = 255
                pixel[1] = 255
                pixel[2] = 255
                pixel[3] = math.ceil(255 * 0.5)
                
    converted = Image.fromarray(image_matrix, 'RGBA')
    converted.save('cloud-no-alpha-50.png')

    
######################### MAIN ##########################
def main():
    processImageDefault()
    
if __name__ == '__main__':
    main()