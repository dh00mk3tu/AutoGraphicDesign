
# Importing the libraries
import requests
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFilter, ImageOps

finalPath = os.getcwd() + '/final/'
if not os.path.exists(finalPath):
    os.makedirs(finalPath)


#API Call for removing the background
def removeBackground():
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open('3.jpg', 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': 'ue5DscsAx1rtoDxZT2a7a9SU'},
    )
    if response.status_code == requests.codes.ok:
        with open('no-bg.png', 'wb') as out:
            out.write(response.content)
    else:
        print("Error:", response.status_code, response.text)

def addBackground():
    #Open the images
    bg = Image.open('Background.png')
    overlay = Image.open('no-bg.png')

    #Convert them to RGBA Color schema
    overlay = overlay.convert("RGBA")
    bg = bg.convert("RGBA")
    
    x = overlay.width
    y = overlay.height
    if(y<=x):
        standardSize = (1000, int((1000*y)/x))
        overlay = overlay.resize(standardSize)
    else:
        standardSize = (int((1000*x)/y), 1000)
        overlay = overlay.resize(standardSize)

    #Center the image
    width = (bg.width - overlay.width) // 2
    height = (bg.height - overlay.height)
    


    #Pasting the image
    bg.paste(overlay, (width, height), overlay)

    #Saving the image and opening it as output Image
    bg.save("new.png", format="png")


def addMask():
    outputImg = Image.open('new.png')
    mask = Image.open('mask.png').convert('L')
    output = ImageOps.fit(outputImg, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)   

    output.save(f"{finalPath}/output.png")


removeBackground()
addBackground()
addMask()


