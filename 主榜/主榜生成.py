import PIL
from PIL import Image       #用于图像生成、读取、保存、调整尺寸等
from PIL import ImageDraw   #用于绘图
from PIL import ImageFont   #用于调节字体样式
import sys                  #用于取当前运行目录
import os                   #用于取系统字体文件夹目录
import pandas as pd

df = pd.read_excel(sys.path[0] + r'\原始数据.xlsx')
font_folder_path = os.environ['LOCALAPPDATA'] + r'\Microsoft\Windows\Fonts'

#遍历数据框的前若干行
for index, row in df.iterrows():
    if int(row['rank']) > 60: #主榜的的条件是前60项
        break

    img = Image.open(sys.path[0] + r'\背景图.png')
    draw = ImageDraw.Draw(img)

    #标题
    font_path = font_folder_path + r'\SourceHanSansCN-Bold.otf' #思源宋体 粗
    font = ImageFont.truetype(font = font_path, size = 60) #调整字体大小
    title = row['title']
    length, hight = draw.textsize(str(title), font)
    if length > 1854: #如果长度过长，使用省略号“...”来缩短长度
        while length > 1854:
            title = title[:-1]
            length, hight = draw.textsize(str(title + '...'), font)
        title = title + '...'


    if title[0] == '【':
        draw.text((-9, 25), title, font = font, fill = (10,10,10)) 
    elif title[0] == '《':
        draw.text((0, 25), title, font = font, fill = (10,10,10)) 
    else:
        draw.text((30, 25), title, font = font, fill = (10,10,10)) 

    #排名
    
    rank = str(int(row['rank']))
    if len(rank) == 1:
        rank = '0' + rank
    if len(rank) == 2:
        font = ImageFont.truetype(font = font_path, size = 220) #调整字体大小
        length, hight = draw.textsize(rank, font)
        draw.text((1900 - length, 261), rank, font = font, fill = (255,255,255)) 
    else:
        font = ImageFont.truetype(font = font_path, size = 145) #调整字体大小
        length, hight = draw.textsize(rank, font)
        draw.text((1900 - length, 311), rank, font = font, fill = (255,255,255)) 

    #BV号、时间、UP主
    font_path = font_folder_path + r'\SourceHanSansCN-Normal.otf' #思源宋体 普通
    font = ImageFont.truetype(font = font_path, size = 32) #调整字体大小
    stringDate = str(row['pubdate'])
    draw.text((40, 108), row['bid'], font = font, fill = (255,255,255)) 
    draw.text((320, 108), stringDate, font = font, fill = (76,123,179)) 
    draw.text((30, 154), row['staff'], font = font, fill = (45,45,45)) 
    if row['copyright'] == 2:
        draw.text((640, 108), '搬运', font = font, fill = (45,45,45)) 

    #数据
    length, hight = draw.textsize(str(row['view']), font)
    draw.text((1880 - length, 645 + 90 * 0), str(row['view']), font = font, fill = (255,255,255)) 
    length, hight = draw.textsize(str(row['favorite']), font)
    draw.text((1880 - length, 645 + 90 * 1), str(row['favorite']), font = font, fill = (255,255,255)) 
    favoPoint = round(row['favorite'] / 0.06228082026935366)
    length, hight = draw.textsize(str(favoPoint), font)
    draw.text((1880 - length, 645 + 90 * 2), str(favoPoint), font = font, fill = (255,255,255)) 
    length, hight = draw.textsize(str(row['likes']), font)
    draw.text((1880 - length, 645 + 90 * 3), str(row['likes']), font = font, fill = (255,255,255)) 
    likePoint = round(row['likes'] / 0.08916704112307915)
    length, hight = draw.textsize(str(likePoint), font)
    draw.text((1880 - length, 645 + 90 * 4), str(likePoint), font = font, fill = (255,255,255)) 

    #得分
    font_path = font_folder_path + r'\SourceHanSansCN-Bold.otf' #思源宋体 粗
    font = ImageFont.truetype(font = font_path, size = 48)
    point = str(row['view'] + favoPoint + likePoint) #分数现场计算
    length, hight = draw.textsize(point, font)
    draw.text((1875 - length, 550), point, font = font, fill = (103,168,245)) 

    #img.show()
    img.save(sys.path[0] + r'\主榜\img_' + rank + '.png')
    print(rank)
