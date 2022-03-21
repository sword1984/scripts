"""
@author: Sword
@email: 173963781@qq.com
@site: www.winkawaks.org
@file: winkawaks.py
@time: 2022/3/17 21:37
"""

"""
批量下载ROMS
"""

import os
import requests
import bs4

DOWN_PATH = "C:\\WinKawaks\\"


# 获取ROMS合部游戏列表源码
def open_website(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 '
                      'Safari/537.36'}

    response = requests.get(url=url, headers=headers)

    return response


def get_games(source):
    soup = bs4.BeautifulSoup(source.text, 'html.parser')
    items = soup.find_all('div', class_="rom-system-index-entry-full")
    result = list()

    for item in items:
        kind = item.get('name')
        name = item.find('a').get('name')
        result.append({'kind': kind, 'name': name})

    return result


def download_link(game_info):
    url = "https://www.winkawaks.org/roms/{}/{}-download.htm".format(game_info['kind'], game_info['name'])
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    link = 'https:' + soup.find('div', id='rom-url').find('a').get('href')

    return link


def download_rom(url, path):
    print('下载文件（{}）中'.format(path))
    response = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        print('正在写入文件...')
        for ch in response:
            f.write(ch)


def download_screen_shot(rom_name, pic_path):
    url = "https://www.winkawaks.org/org/roms/{}/{}-01.jpg".format(rom_name, rom_name)
    response = requests.get(url, stream=True)

    with open(pic_path, 'wb') as f:
        for ch in response:
            f.write(ch)


def main():
    url = "https://www.winkawaks.org/roms/full-rom-list.htm"
    content = open_website(url)
    games_info = get_games(source=content)

    for each in games_info:
        file_path = DOWN_PATH + 'roms\\' + each['kind'] + '\\' + each['name'] + '.zip'
        if os.path.exists(file_path):
            print('{}已存在'.format(file_path))
        else:
            link = download_link(each)
            download_rom(link, file_path)

        picture_path = DOWN_PATH + 'sshots\\{}.bmp'.format(each['name'])
        if os.path.exists(picture_path):
            print('{}已存在'.format(picture_path))
        else:
            download_screen_shot(each['name'], picture_path)


if __name__ == '__main__':
    main()



