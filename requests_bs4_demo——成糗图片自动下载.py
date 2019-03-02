#!python 3
import requests, os, bs4, time

print('开始运行')
time.sleep(1)
url = 'http://www.qiubaichengren.net/1.html'
i , path = 1 , '.\Xbphoto'
if not os.path.exists(path):
    os.makedirs(path)
print('成功接入“成人糗百”主页')
num = int(input('>>>请输入需要下载的页数：'))
print('下载图片将保存到目录： %s' % os.path.abspath(path))
time.sleep(2)
while url:
    print('Downloading ' + str(i) + ' page...' )
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    # print(soup.text)

    photoImg = soup.select('div img')
    # print(type(photo))
    for a in range(len(photoImg)):
        photoUrl = photoImg[a].get('src')
        if photoUrl.endswith('05z75o.jpg'):
            continue
        elif photoUrl.startswith('http://'):
            ph = requests.get(photoUrl)
            ph.raise_for_status()
            print('Downloading ' + str(i) + ' page'+str(a)+'...')

            imageName = str(i) + 'page' + str(a) + os.path.splitext(os.path.basename(photoUrl))[1]
            imageFile = open(os.path.join(path,imageName),'wb')
            for image in ph.iter_content(100000):
                imageFile.write(image)
    i += 1
    url = 'http://www.qiubaichengren.net/%s.html' % (i)

    if i > num:
        break

print('Done')