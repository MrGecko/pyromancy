__author__ = 'Gecko'

from random import randint as rdi

from noise import pnoise3


def create_2d_texture_random(width, height, d, scaleB, z=None):
    y_coords = range(height)
    x_coords = range(width)

    texel_final = []

    if z is None:
        z = rdi(-10000, 10000)
    scaleA = 1

    half = 0
    for y in y_coords:
        for x in x_coords:
            pixel = 150 * pnoise3(x * scaleA - half, y * scaleA - half, z, octaves=10, persistence=0.10)
            pixel += 40 * pnoise3(x * scaleB - half, y * scaleB - half, z, octaves=5, persistence=0.25)
            pixel += 120 * pnoise3(x * scaleB * 0.6 - half, y * scaleB * 0.6 - half, z, octaves=5, persistence=0.4)
            texel_final.append(pixel)

    # transform to a 0..255 range
    m = abs(min(texel_final))
    texel_final = [p + m for p in texel_final]
    _max = max(texel_final)
    if _max == 0:
        _max = 1
    coeff = float(d) / _max
    texel_final = [int(coeff * p) for p in texel_final]
    return z, texel_final


if __name__ == '__main__':
    w, h, d = 100, 100, 30
    create_2d_texture_random(w, h, d, 1.0 / 10)
    pass