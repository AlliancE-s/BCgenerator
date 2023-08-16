import linecache

import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import random
import radar


def draw_and_write(font, card, p_draw, offset, type, end):
    content = card[type]
    font_size = draw.textsize(content, font=font)
    movement = [font_size[1], font_size[0], 8]

    draw.text((p_draw[0] + offset[0], p_draw[1] + offset[1]), content, font=font, fill=set_color)
    point_all = get_four_point(p_draw[0], p_draw[1], movement, offset)
    writelabel(content, point_all, end)


def get_four_point(point_x, point_y, movement, offset):
    height = movement[0]
    length = movement[1]
    adjust = movement[2]
    point1 = [point_x + offset[0] - adjust, point_y + offset[1] - adjust]
    point2 = [point_x + offset[0] + length + adjust, point_y + offset[1] - adjust]
    point3 = [point_x + offset[0] + length + adjust, point_y + offset[1] + height + adjust]
    point4 = [point_x + offset[0] - adjust, point_y + offset[1] + height + adjust]

    return [point1, point2, point3, point4]


def get_bank_card():
    # 生成卡号

    temp = ['', '', '', '']
    if random.randint(0, 1) == 0:
        temp[0] = str(random.randint(1000, 9999))
        for i in range(1, 4):
            temp[i] = str(random.randint(0, 9999)).zfill(4)
        card_num = str(temp[0] + ' ' + temp[1] + ' ' + temp[2] + ' ' + temp[3])
        numlen = 16
    else:
        temp[0] = str(random.randint(100000, 999999))
        temp[1] = str(random.randint(0, 9999999999999)).zfill(13)
        card_num = str(temp[0] + ' ' + temp[1])
        numlen = 19

    # 生成姓名
    until = radar.random_date("2010-01-01", "2040-12-30").date()
    valid = str(str(until.month).zfill(2) + '/' + str(until.year))

    return card_num, valid, numlen


def get_offset(num):
    # 印刷偏移量
    offset1 = int(random.uniform(-num, num))
    offset2 = int(random.uniform(-num, num))
    return offset1, offset2


def writelabel(text, point, end=0):
    if end == 0:
        with open("BC_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "' + text + '", "points": ' + str(point) + ', "difficult": false}, ')
    elif end == 1:
        with open("BC_output/Label.txt", "a", encoding='utf-8') as file:
            file.write(
                '{"transcription": "' + text + '", "points": ' + str(point) + ', "difficult": false}')


# def gbk_trans_utf8(file_path):  #存在bug，弃用
#     with open(file_path, 'r', encoding='gbk') as f:
#         content = f.read()
#     with open(file_path, 'w', encoding='utf8') as f:
#         f.write(content)


######################################

# 调试labely和filestate文件
# with open("BC_output/Label.txt", "w") as file:
#     file.write('')
# with open("BC_output/fileState.txt", "w") as file:
#     file.write('')
# with open("BC_output/record.txt", "w") as file:
#     file.write('')
# 生成图片数量
num_pic = 1000

for i in range(num_pic):

    # 图片控件
    typeCode = 22   # 用于不同背景的调整
    bk_img = cv2.imread("backgroud/back" + str(typeCode) + ".jpg")
    offset = get_offset(0)
    temp_filename = str(i + 1 + (typeCode - 11) * num_pic)

    # 读取并初始化
    img_pil = Image.fromarray(bk_img)
    draw = ImageDraw.Draw(img_pil)

    # 保存文件名，四位数
    filename = temp_filename.zfill(8)

    # 随机生成字体样式
    default_font_path = "STHeiti Medium.ttc"

    if i < 25:
        font_type = 1
        font_path = "Farrington-7B.ttf"
    else:
        font_type = 2
        font_path = "STHeiti Medium.ttc"

    if random.randint(0, 1) == 0:
        set_color = (192, 192, 192)
    else:
        set_color = (0, 0, 0)

    # 获取生成内容
    card = get_bank_card()

    # 填充内容

    # label.txt开头初始化
    with open("BC_output/Label.txt", "a", encoding='utf-8') as file:
        file.write("BC_output/" + filename + ".jpg\t[")

    # 生成图片以及坐标
    if typeCode == 1:
        end = 0  # 标记是否为最后一行

        # 卡号
        type = 0
        # movement = [0, 0, 0]---[高度，宽度，调整值]
        # p_draw 是生成文字左上角坐标
        if font_type == 2:  # 黑体
            font = ImageFont.truetype(font_path, 60)
            p_draw = [123, 390]
        elif font_type == 1 & card[2] == 19:  # 银行字体19
            font = ImageFont.truetype(font_path, 45)
            p_draw = [123, 378]
        else:  # 银行字体16
            font = ImageFont.truetype(font_path, 52)
            p_draw = [123, 378]

        draw_and_write(font, card, p_draw, offset, type, end)

        # 日期
        type = 1
        end = 1
        font = ImageFont.truetype(default_font_path, 40)
        p_draw = [316, 482]

        draw_and_write(font, card, p_draw, offset, type, end)

    if typeCode == 2:
        type = 0
        end = 0  # 标记是否为最后一行

        # 卡号
        # movement = [0, 0, 0]---[高度，宽度，调整值]
        # p_draw 是生成文字左上角坐标
        if font_type == 2:  # 黑体
            font = ImageFont.truetype(font_path, 70)
            p_draw = [123, 390]
        elif font_type == 1 & card[2] == 19:  # 银行字体19
            font = ImageFont.truetype(font_path, 52)
            p_draw = [123, 388]
        else:  # 银行字体16
            font = ImageFont.truetype(font_path, 56)
            p_draw = [123, 388]

        draw_and_write(font, card, p_draw, offset, type, end)

        # 日期
        type = 1
        end = 1
        font = ImageFont.truetype(default_font_path, 45)
        p_draw = [410, 520]

        draw_and_write(font, card, p_draw, offset, type, end)

    if typeCode == 3:
        end = 0  # 标记是否为最后一行

        # 卡号
        type = 0
        # movement = [0, 0, 0]---[高度，宽度，调整值]
        # p_draw 是生成文字左上角坐标
        if font_type == 2:  # 黑体
            font = ImageFont.truetype(font_path, 70)
        elif font_type == 1 & card[2] == 19:  # 银行字体19
            font = ImageFont.truetype(font_path, 52)
        else:  # 银行字体16
            font = ImageFont.truetype(font_path, 56)

        p_draw = [180, 420]

        draw_and_write(font, card, p_draw, offset, type, end)

        # 日期
        type = 1
        end = 1
        font = ImageFont.truetype(default_font_path, 45)
        p_draw = [426, 540]

        draw_and_write(font, card, p_draw, offset, type, end)

    if typeCode == 4:
        end = 0  # 标记是否为最后一行
        set_color = (192, 192, 192)

        # 卡号
        type = 0
        # movement = [0, 0, 0]---[高度，宽度，调整值]
        # p_draw 是生成文字左上角坐标
        if font_type == 2:  # 黑体
            font = ImageFont.truetype(font_path, 70)
        elif font_type == 1 & card[2] == 19:  # 银行字体19
            font = ImageFont.truetype(font_path, 52)
        else:  # 银行字体16
            font = ImageFont.truetype(font_path, 56)

        p_draw = [112, 400]

        draw_and_write(font, card, p_draw, offset, type, end)

        # 日期
        type = 1
        end = 1
        font = ImageFont.truetype(default_font_path, 45)
        p_draw = [414, 478]

        draw_and_write(font, card, p_draw, offset, type, end)

    if typeCode == 5:
        end = 0  # 标记是否为最后一行

        # 卡号
        type = 0
        # movement = [0, 0, 0]---[高度，宽度，调整值]
        # p_draw 是生成文字左上角坐标
        if font_type == 2:  # 黑体
            font = ImageFont.truetype(font_path, 70)
        elif font_type == 1 & card[2] == 19:  # 银行字体19
            font = ImageFont.truetype(font_path, 52)
        else:  # 银行字体16
            font = ImageFont.truetype(font_path, 56)

        p_draw = [100, 388]

        draw_and_write(font, card, p_draw, offset, type, end)

        # 日期
        type = 1
        end = 1
        font = ImageFont.truetype(default_font_path, 45)
        p_draw = [496, 540]

        draw_and_write(font, card, p_draw, offset, type, end)

    if typeCode == 6:
        end = 0  # 标记是否为最后一行
        set_color = (192, 192, 192)

        # 卡号
        type = 0
        # movement = [0, 0, 0]---[高度，宽度，调整值]
        # p_draw 是生成文字左上角坐标
        if font_type == 2:  # 黑体
            font = ImageFont.truetype(font_path, 70)
        elif font_type == 1 & card[2] == 19:  # 银行字体19
            font = ImageFont.truetype(font_path, 52)
        else:  # 银行字体16
            font = ImageFont.truetype(font_path, 56)

        p_draw = [280, 372]

        draw_and_write(font, card, p_draw, offset, type, end)

        # 日期
        type = 1
        end = 1
        font = ImageFont.truetype(default_font_path, 45)
        p_draw = [508, 524]

        draw_and_write(font, card, p_draw, offset, type, end)

    if typeCode == 7:
        end = 0  # 标记是否为最后一行

        # 卡号
        type = 0
        # movement = [0, 0, 0]---[高度，宽度，调整值]
        # p_draw 是生成文字左上角坐标
        if font_type == 2:  # 黑体
            font = ImageFont.truetype(font_path, 70)
        elif font_type == 1 & card[2] == 19:  # 银行字体19
            font = ImageFont.truetype(font_path, 52)
        else:  # 银行字体16
            font = ImageFont.truetype(font_path, 56)

        p_draw = [178, 377]

        draw_and_write(font, card, p_draw, offset, type, end)

        # 日期
        type = 1
        end = 1
        font = ImageFont.truetype(default_font_path, 45)
        p_draw = [452, 536]

        draw_and_write(font, card, p_draw, offset, type, end)

    if typeCode == 8:
        end = 0  # 标记是否为最后一行

        # 卡号
        type = 0
        # movement = [0, 0, 0]---[高度，宽度，调整值]
        # p_draw 是生成文字左上角坐标
        if font_type == 2:  # 黑体
            font = ImageFont.truetype(font_path, 70)
        elif font_type == 1 & card[2] == 19:  # 银行字体19
            font = ImageFont.truetype(font_path, 52)
        else:  # 银行字体16
            font = ImageFont.truetype(font_path, 56)

        p_draw = [165, 400]

        draw_and_write(font, card, p_draw, offset, type, end)

        # 日期
        type = 1
        end = 1
        font = ImageFont.truetype(default_font_path, 45)
        p_draw = [534, 522]

        draw_and_write(font, card, p_draw, offset, type, end)

    if typeCode == 9:
        end = 0  # 标记是否为最后一行

        # 卡号
        type = 0
        # movement = [0, 0, 0]---[高度，宽度，调整值]
        # p_draw 是生成文字左上角坐标
        if font_type == 2:  # 黑体
            font = ImageFont.truetype(font_path, 70)
        elif font_type == 1 & card[2] == 19:  # 银行字体19
            font = ImageFont.truetype(font_path, 52)
        else:  # 银行字体16
            font = ImageFont.truetype(font_path, 56)

        p_draw = [157, 394]

        draw_and_write(font, card, p_draw, offset, type, end)

        # 日期
        type = 1
        end = 1
        font = ImageFont.truetype(default_font_path, 45)
        p_draw = [505, 538]

        draw_and_write(font, card, p_draw, offset, type, end)

    if typeCode == 10:
        end = 0  # 标记是否为最后一行
        set_color = (0, 0, 0)

        # 卡号
        type = 0
        # movement = [0, 0, 0]---[高度，宽度，调整值]
        # p_draw 是生成文字左上角坐标
        if font_type == 2:  # 黑体
            font = ImageFont.truetype(font_path, 70)
        elif font_type == 1 & card[2] == 19:  # 银行字体19
            font = ImageFont.truetype(font_path, 52)
        else:  # 银行字体16
            font = ImageFont.truetype(font_path, 56)

        p_draw = [117, 379]

        draw_and_write(font, card, p_draw, offset, type, end)

        # 日期
        type = 1
        end = 1
        font = ImageFont.truetype(default_font_path, 45)
        p_draw = [608, 542]

        draw_and_write(font, card, p_draw, offset, type, end)

    if typeCode > 10 and typeCode <= 22:
        line_num = random.randint(1, 12000)
        card_num_temp = linecache.getline('bank_number.txt', line_num)

        card_type = random.choice([16,18])
        if card_type == 18:
            write_num =card_num_temp[:-2]
            card1 = card_num_temp[0:6]
            card2 = card_num_temp[6:18]
            card_num = f"{card1} {card2}"  # 四个空格
        else:
            write_num = card_num_temp[:-4]
            card1 = card_num_temp[0:4]
            card2 = card_num_temp[4:8]
            card3 = card_num_temp[8:12]
            card4 = card_num_temp[12:16]
            card_num = f"{card1}  {card2}  {card3}  {card4}"

        color_list = ['white','black', 'blue', 'red', 'green', (192, 192, 192)]
        if typeCode == 11: color_list = ['white', 'blue', 'red', 'green', (192, 192, 192)]
        if typeCode == 15: color_list = ['black', 'blue', 'red', 'green', (192, 192, 192)]
        if typeCode == 17: color_list = ['white', 'blue', 'red', 'green', (192, 192, 192)]
        if typeCode == 20: color_list = ['white', 'blue', 'red', 'green', 'black']
        if typeCode == 22: color_list = ['white', (192, 192, 192), 'red', 'green', 'black']
        set_color = random.choice(color_list)

        font_path = "Farrington-7B.ttf"
        font = ImageFont.truetype(font_path, 62)

        p_draw = [5, 5]

        content = str(card_num)
        font_size = draw.textsize(content, font=font)
        movement = [font_size[1], font_size[0], 8]

        draw.text((p_draw[0] + offset[0], p_draw[1] + offset[1]), content, font=font, fill=set_color)
        point_all = get_four_point(p_draw[0], p_draw[1], movement, offset)
        writelabel(write_num, point_all)

        with open("BC_output/record.txt", "a", encoding='utf-8') as file:
            file.write(
                filename + '.jpg\t' + write_num + '\n')

    # 不知道这行干啥的，留着
    bk_img = np.array(img_pil)

    # 输出

    # label.txt结尾
    with open("BC_output/Label.txt", "a", encoding='utf-8') as file:
        file.write("]\n")

    # 写入确认信息
    with open("BC_output/fileState.txt", "a", encoding='utf-8') as file:
        file.write('BC_output\\' + filename + ".jpg\t1\n")

    # cv2.imshow(filename, bk_img)
    # cv2.waitKey()
    cv2.imwrite("BC_output/" + filename + ".jpg", bk_img)
    print(filename + '完成-背景' + str(typeCode))

# gbk_trans_utf8('DL_output/Label.txt')
# gbk_trans_utf8('DL_output/fileState.txt')
