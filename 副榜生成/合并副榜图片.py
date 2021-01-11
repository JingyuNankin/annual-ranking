import PIL
from PIL import Image
from PIL import ImageDraw
import os  

rawPicturePath = sys.path[0] + r'\副榜\img_'
i = 60
for page in range(80):
    img = Image.new('RGB',(1920,1080))
    for part in range (3):
        i = i + 1
        address = rawPicturePath + str(i) + '.png'
        subImg = Image.open(address)
        img.paste(subImg, (0, int(1080 * part / 3)))
    img.save(sys.path[0] + r'\整合副榜\img_page' + str(page + 1) + '.png')
    print(page) 
