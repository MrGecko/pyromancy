__author__ = 'Gecko'

from random import randint as rdi

from noise import pnoise3


def create_2d_texture_random(width, height, d, scaleB):
    y_coords = range(height)
    x_coords = range(width)

    texel_final = []

    z = rdi(-10000, 10000)
    scaleA = 1

    half = 0
    for y in y_coords:
        for x in x_coords:
            v = pnoise3(x * scaleA - half, y * scaleA - half, z,  octaves=10, persistence=0.10)
            v = int(v * 150)
            pixel = int(v)

            v = pnoise3(x * scaleB - half, y * scaleB - half, z, octaves=5, persistence=0.25)
            v = int(v * 40)
            pixel += int(v)

            v = pnoise3(x * scaleB*0.6 - half, y * scaleB*0.6 - half, z, octaves=5, persistence=0.4)
            v = int(v * 60)
            v *= 2

            pixel += int(v)
            texel_final.append(pixel)

    m = abs(min(texel_final))
    texel_final = [p + m for p in texel_final]
    coeff = float(d) / max(texel_final)
    texel_final = [int(coeff * p) for p in texel_final]
    return texel_final


if __name__ == '__main__':

    w, h, d = 100, 100, 30
    create_2d_texture_random(w, h, d, 1.0/10)
    pass