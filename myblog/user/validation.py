#! usr/bin/python
# -*- coding:utf-8 -*-
# @Author: winston he
# @File: validation_pics.py
# @Time: 2020-05-18 09:49
# @Email: winston.wz.he@gmail.com
# @Desc:
import random

from PIL import Image, ImageDraw, ImageFont


def getBGColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


def getFontColor():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


def getChar():
    return chr(random.randint(65, 90))


width = 500
height = 100

font_height = 100
font_width = 100


class ValidationPicGenerator:
    def __init__(self, bg_size, font_size, font_file, char_num):
        self.bg_image = Image.new('RGB', (width, height), (255, 255, 255))
        self.bg_size = bg_size
        self.font = ImageFont.truetype(font_file, 50)
        self.font_size = font_size
        self.draw = ImageDraw.Draw(self.bg_image)
        self.char_num = char_num

    def upside_down_char(self, upside_down_num=1, lang='en'):
        self._draw_back_ground()

        index_set = set()
        while len(index_set) != upside_down_num:
            index = random.randint(0, self.char_num - 1)
            index_set.add(index)

        chars = []
        for i in range(self.char_num):
            curr_char = self._get_chinese_character(encoding='gbk2312')
            chars.append(curr_char)
            print(curr_char)
            font_image = Image.new('RGB', (self.font_size, self.font_size), getBGColor())
            font_draw = ImageDraw.Draw(font_image)
            for x in range(self.font_size):
                for y in range(self.font_size):
                    font_draw.point((x, y), fill=getBGColor())

            font_draw.text((self.font_size / 4, self.font_size / 4), curr_char, fill=getFontColor(), font=self.font,
                           align='left')

            # 160至200 认为是倒转的，-20至20认为是正向的
            rotate_angle = (160, 200) if i in index_set else (-20, 20)
            font_image = font_image.rotate(random.randint(rotate_angle[0], rotate_angle[1]))

            # left, upper, right, and lower
            font_image = font_image.crop([self.font_size * (1 / 4), self.font_size * (1 / 4), self.font_size * (3 / 4),
                                          self.font_size * (3 / 4)])
            self.bg_image.paste(font_image, (i * 100, random.randint(0, 40)))
        # bg_image = self.bg_image.filter(ImageFilter.BLUR)
        self.bg_image.show()
        return [c for idx, c in enumerate(chars) if idx in index_set]

    def regular_char(cls, lang='en'):
        pass

    def _draw_back_ground(self):
        for x in range(self.bg_size[0]):
            for y in range(self.bg_size[1]):
                self.draw.point((x, y), fill=getBGColor())

    @staticmethod
    def _get_chinese_character(encoding='unicode'):
        encoding = encoding.lower()
        if encoding.lower() == 'unicode':
            val = random.randint(0x4e00, 0x9fbf)
            return val
        elif encoding == 'gbk2312':
            head = random.randint(0xb0, 0xf7)
            body = random.randint(0xa1, 0xfe)
            val = f'{head:x}{body:x}'
            s = bytes.fromhex(val).decode('gb2312')
            return s
        else:
            pass


params = [1 - float(random.randint(1, 2)) / 100,
          0, 0, 0,
          1 - float(random.randint(1, 2)) / 100,
          float(random.randint(1, 2)) / 500,
          0.001,
          float(random.randint(1, 1)) / 500,
          ]

if __name__ == '__main__':
    val_pic_gen = ValidationPicGenerator((500, 100), 100, '../fonts/FZHTJW.TTF', 5)
    res = val_pic_gen.upside_down_char(upside_down_num=2)
    print(res)
