import pytest
import numpy as np
import cv2
import pathlib

CURRENT_PATH = pathlib.Path(pathlib.Path(__file__).resolve()).parent
SAMPLE = str(CURRENT_PATH / pathlib.Path('sample_scroll_00.png'))

from forza_result import (
    Color,
    draw_line,
    get_coord
)


def _test_get_relative_coords():
    print(SAMPLE)
    img = cv2.imread(SAMPLE)
    base_y = 552
    for i in range(0, 10):
        x = i * 120
        img = draw_line(img, (0, base_y + x), (img.shape[1], base_y + x),
                        Color.BLUE.value, title='Base_1')
        img = draw_line(img, (0, base_y + 57 + x),
                        (img.shape[1], base_y + 57 + x), Color.RED.value,
                        title='Base_2')
        img = draw_line(img, (0, base_y + 35 + x),
                        (img.shape[1], base_y + 35 + x), Color.GREEN.value,
                        title='Base_3')

    img = draw_line(img, (115, 30), (115, img.shape[0]), Color.RED.value,
                    title='Base_2')
    img = draw_line(img, (340, 30), (340, img.shape[0]), Color.BLUE.value,
                    title='Base_1')
    img = draw_line(img, (2943, 30), (2943, img.shape[0]), Color.GREEN.value,
                    title='Base_3')
    img = draw_line(img, (3350, 30), (3350, img.shape[0]), Color.GREEN.value,
                    title='Base_3')
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyWindow('image')


def test_get_coord():
    expect = [(115, 587, 0, 552), (115, 707, 0, 672), (115, 827, 0, 792),
              (115, 947, 0, 912), (115, 1067, 0, 1032), (115, 1187, 0, 1152),
              (115, 1307, 0, 1272), (115, 1427, 0, 1392), (115, 1547, 0, 1512),
              (115, 1667, 0, 1632)]
    v = get_coord(
        base=(0, 552),
        coords=(115, 35, 0, 0),
        interval=120,
        count=10)
    assert v == expect
