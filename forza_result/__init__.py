import os
import argparse
import cv2
import enum
from multiprocessing import Pool
from functools import partial

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


class Color(enum.Enum):
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)
    WHITE = (0, 0, 0)
    BLACK = (255, 255, 255)


pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


###############################################################################
def image_to_string(img, lang='eng'):
    """
    주어진 이미지에서 문자 인식
    :param img: image 객체
    :param lang: 언어
    :return:
    """
    prefix = os.environ.setdefault('TESSDATA_PREFIX', '')
    config = r'--tessdata-dir "{data}"'.format(data=prefix)
    v = pytesseract.image_to_string(img, config=config, lang=lang).strip()
    return v


###############################################################################
def image_processing(img, filters):
    filters = [
        {
            'name': 'threshold',
            'color': 'GRAY',
            'low_tone': 0,
            'high_tone': 255,
            'type': [
                'THRESH_OTSU',
                'THRESH_BINARY_INV'
            ],
        },
        {
            'name': 'gaussian_blur',
            'width': 3,
            'height': 3,
            'sigmax': 0
        },
        {
            'name': 'edge_pre_serv'}
    ]
    for f in filters:
        if f['name'] == 'gaussian_blur':
            w, h, s = f['width'], f['height'], f['sigmax']
            img = cv2.GaussianBlur(img, (w, h), s)

        elif f['name'] == 'threshold':
            l, h = f['low_tone'], f['high_tone']
            _type = sum([getattr(cv2, x) for x in f['type']])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = cv2.threshold(img, l, h, _type)[1]

        elif f['name'] == 'edge_pre_serv':
            img = cv2.edgePreservingFilter(img)
    return img


###############################################################################
def ocr_each_player(img, data):

    order = ['total-record', 'player-name', 'rank', 'car-model', 'best-lab']

    record = dict()
    record['complete'] = True
    record['clean'] = True

    for k in order:
        c = data[k]
        t_img = img[c[1]:c[3], c[0]:c[2]]
        t_img = image_processing(t_img, filters={})
        value = image_to_string(t_img)

        if k == 'total-record' and 'DNF' == value:
            data['player-name'][0] -= 130
            data['car-model'][0] -= 130

        record[k] = value

        if k == 'player-name' and not value:
            return

        if k == 'player-name' and value.endswith(' w'):
            record['player-name'] = value[:-1].strip()

        if k == 'best-lab' and not value:
            record['complete'] = False

        if k == 'best-lab' and -1 != value.find('A'):
            record['best-lab'] = value.replace('A', '').strip()
            record['clean'] = False

    return record


###############################################################################
def ocr(img, data):
    base = data['base']
    count = data['count']
    interval = data['interval']
    order = ['total-record', 'player-name', 'rank', 'car-model', 'best-lab']
    players = dict()

    for i in range(0, count):
        players[i] = dict()
        for item in order:
            players[i][item] = get_coord(
                base, data['coord'][item], interval=interval, count=count)[i]

    with Pool(4) as p:
        v = [d for _, d in players.items()]
        func = partial(ocr_each_player, img)
        ret_value = p.map(func, v)
    return ret_value


###############################################################################
def get_coord(base: tuple, coords: (tuple, list), interval=0, count=1):
    bx, by = base
    x1, y1, x2, y2 = coords

    value = list()
    for v in range(0, count):
        offset = v * interval
        v = [
            x1 + bx,
            y1 + by + offset,
            x2 + bx,
            y2 + by + offset
        ]
        value.append(v)
    return value


###############################################################################
def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('target_image', type=str)
    parser.add_argument('--trained_data', type=str)
    arg_sepc = parser.parse_args()
    return arg_sepc

###############################################################################
def convert(image_file, data):
    # x1, y1, x2, y2
    data = {
        "base": (0, 552),
        "coord": {
            "rank": [105, 25, 195, 85],
            "player-name": [340, 0, 800, 53],
            "car-model": [340, 55, 800, 104],
            "best-lab": [2943, 35, 3243, 83],
            "total-record": [3350, 35, 3700, 83]
        },
        "interval": 120,
        "count": 10

    }
    img = cv2.imread(image_file)
    value = ocr(img, data)
    return value

    # cv2.imwrite('temp.png', img)
    # cv2.imshow('crop', img)
    # cv2.waitKey(0)


