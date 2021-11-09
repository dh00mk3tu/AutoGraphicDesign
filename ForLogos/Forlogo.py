
# Importing the libraries
import requests
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFilter, ImageOps

finalPath = os.getcwd() + '/final/'
if not os.path.exists(finalPath):
    os.makedirs(finalPath)

#Circle cutout of the Logo 
def cutout():
    outputImg = Image.open('3.png')
    mask = Image.open('mask.png').convert('L')
    output = ImageOps.fit(outputImg, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)   

    output.save(f"{finalPath}/output.png")


def addBackground():
    #Open the images
    bg = Image.open('Background.png')
    overlay = Image.open('final/output.png')

    #Convert them to RGBA Color schema
    overlay = overlay.convert("RGBA")
    bg = bg.convert("RGBA")
    
    standardSize = (1016, 1016)
    overlay = overlay.resize(standardSize)

    #Center the image
    width = (bg.width - overlay.width) // 2
    height = (bg.height - overlay.height) // 2
    

    #Pasting the image
    bg.paste(overlay, (width, height), overlay)

    #Saving the image and opening it as output Image
    bg.save("final-logo.png", format="png")


cutout()
addBackground()


