import PIL
from PIL import Image       #用于图像生成、读取、保存、调整尺寸等
from PIL import ImageDraw   #用于绘图
from PIL import ImageFont   #用于调节字体样式
import urllib.request       #用于下载图片
import pandas as pd
import json                 #用于解析JSON
import sys                  #用于取当前运行目录
import os                   #用于取系统字体文件夹目录

#下载图片
def download_image(img_url, api_token = 'a'):
    header = {"Authorization": "Bearer " + api_token}
    request = urllib.request.Request(img_url,headers = header)

    try:
        response = urllib.request.urlopen(request)
        filename = r'D:\Programimg\Python\Python3\PIL练习\副榜生成\download.jpg'
        if (response.getcode() == 200):
            with open(filename, "wb") as f:
                f.write(response.read())
    except:
        print ("下载图片失败，错误发生在\n" + img_url)

def get_image_by_bid(bid):
    apiUrl = 'http://api.bilibili.com/x/web-interface/view?bvid=' + bid
    html = urllib.request.urlopen(apiUrl).read().decode("utf-8")
    jsonData = json.loads(html)
    picUrl = jsonData['data']['pic']
    download_image(picUrl)


df = pd.read_excel(r'D:\Programimg\Python\Python3\PIL练习\副榜生成\原始数据.xlsx')
font_folder_path = os.environ['LOCALAPPDATA'] + r'\Microsoft\Windows\Fonts'

#遍历数据框的前若干行
for index, row in df.iterrows():
    if row['rank'] <= 60:
        continue
    elif row['rank'] > 300:
        break

    img = Image.open(sys.path[0] + r'\背景图.png')
    draw = ImageDraw.Draw(img)

    #标题
    font_path = font_folder_path + r'SourceHanSansCN-Bold.otf' #思源黑体 粗
    font = ImageFont.truetype(font = font_path, size = 60) #调整字体大小
    title = row['title']
    length, hight = draw.textsize(str(title), font)
    if length > 1188:
        while length > 1188:
            title = title[:-1]
            length, hight = draw.textsize(str(title + '...'), font)
        title = title + '...'

    if title[0] == '【':
        draw.text((627, 86), title, font = font, fill = (50,50,50)) 
    elif title[0] == '《':
        draw.text((636, 86), title, font = font, fill = (50,50,50)) 
    else:
        draw.text((666, 86), title, font = font, fill = (50,50,50)) 

    #排名
    rank = str(int(row['rank']))
    if len(rank) == 2:
        font = ImageFont.truetype(font = font_path, size = 122) #调整字体大小
    else:
        font = ImageFont.truetype(font = font_path, size = 100) #调整字体大小
    
    length, hight = draw.textsize(rank, font)
    draw.text((200 - length, 50), rank, font = font, fill = (255,255,255)) 
 
    #BV号、时间、UP主
    font_path = font_folder_path + r'\SourceHanSansCN-Normal.otf' #思源黑体 普通
    font = ImageFont.truetype(font = font_path, size = 32) #调整字体大小
    stringDate = str(row['pubdate'])
    draw.text((676, 177), row['bid'], font = font, fill = (255,255,255)) 
    draw.text((956, 177), stringDate, font = font, fill = (76,123,179)) 
    length, hight = draw.textsize(row['name'], font)
    draw.text((1854 - length, 177), row['name'], font = font, fill = (100,100,100)) 

    #数据
    font_path = font_folder_path + r'\SourceHanSansCN-Light.otf' #思源黑体 细
    font = ImageFont.truetype(font = font_path, size = 32) #调整字体大小
    length, hight = draw.textsize(str(row['view']), font)
    draw.text((830 - length, 253), str(row['view']), font = font, fill = (155,155,155)) 
    length, hight = draw.textsize(str(row['favorite']), font)
    draw.text((1110 - length, 253), str(row['favorite']), font = font, fill = (155,155,155)) 
    length, hight = draw.textsize(str(row['likes']), font)
    draw.text((1390 - length, 253), str(row['likes']), font = font, fill = (155,155,155)) 
        
    #得分
    font_path = font_folder_path + r'\SourceHanSansCN-Bold.otf' #思源黑体 粗
    font = ImageFont.truetype(font = font_path, size = 48)
    favoPoint = round(row['favorite'] / 0.06228082026935366)
    likePoint = round(row['likes'] / 0.08916704112307915)
    point = str(row['view'] + favoPoint + likePoint) #分数现场计算
    length, hight = draw.textsize(point, font)
    draw.text((1854 - length, 250), point, font = font, fill = (103,168,245)) 

    get_image_by_bid(row['bid'])
    videoPic = Image.open(r'D:\Programimg\Python\Python3\PIL练习\副榜生成\download.jpg')
    videoPic = videoPic.resize((416,260))
    img.paste(videoPic,(207,50))

    #img.show()
    img.save(sys.path[0] + r'\副榜\img_' + rank + '.png')
    print(rank)