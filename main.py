
# Importing the libraries

import requests
import numpy as np
import os
import glob
from PIL import Image, ImageDraw, ImageFilter, ImageOps

finalPath = os.getcwd() + '/final/'
if not os.path.exists(finalPath):
    os.makedirs(finalPath)

profilePath = []
d = "profiles"
nobg = "nobg"

#Importing all the image files
def getProfilePath(pathValue): 
    profilePath.clear()
    for path in os.listdir(pathValue):
        full_path = os.path.join(pathValue, path)
        if os.path.isfile(full_path):
            profilePath.append(full_path)
            
    print(profilePath)



#API Call for removing the background
def removeBackground(path, index):
    print("remove background called - inside")
    print(path)
    print(index)
    local = "nobg/"+str(index)+".png"
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(path, 'rb')},
        data={'size': 'auto'},
        #X3GeXtGGgT2ZiGovgW56egQd - Harshdeep's API Key
        #ue5DscsAx1rtoDxZT2a7a9SU - Anirudh's API Key
        headers={'X-Api-Key': 'X3GeXtGGgT2ZiGovgW56egQd'},
    )
    if response.status_code == requests.codes.ok:
        with open(local, 'wb') as out:
            out.write(response.content)
    else:
        print("Error:", response.status_code, response.text)
    
def addBackground(index):
    getProfilePath(nobg)
    print(profilePath)

    local = "withbg/"+str(index)+".png"

    #Open the images
    bg = Image.open('Background.png')
    bg = bg.convert("RGBA")

    
    overlay = Image.open(profilePath[index])
    overlay = overlay.convert("RGBA")


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
    bg.save(local, format="png")


def addMask(index):
    local = "finalPath/"+str(index)+".png"
    print("add mask called")
    outputImg = Image.open(profilePath[index])
    mask = Image.open('mask.png').convert('L')
    output = ImageOps.fit(outputImg, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)   
    output.save(local)

#Main Function
def main():
    getProfilePath(d)
    for i in range(len(profilePath)):
        print("remove background called")
        removeBackground(profilePath[i], i)
    getProfilePath(nobg)
    for i in range(len(profilePath)):
        print("add background called")
        addBackground(i)
    for i in range(len(profilePath)):
        addMask(i)
main()
# removeBackground()
# addBackground()
# addMask()



