import pyglet

from pyromancy.core.sprite.zsprite import ZSprite


class ZExSprite(ZSprite):
    def __init__(self, tileset, x=0, y=0, z=0, start_frame=0, batch=None, group=None):
        self.__tileset = tileset
        super(ZExSprite, self).__init__(x=x, y=y, z=z,
                                        img=self.__tileset["frames"][start_frame],
                                        batch=batch,
                                        group=group)

    @property
    def center(self):
        return self.x + self.__tileset["tilewidth"] * 0.5, self.y + self.__tileset["tileheight"] * 0.5

    @property
    def group(self):
        return self._get_group()

    def set_animation(self, frame_list, speed, loop=True):
        self.image = pyglet.image.Animation.from_image_sequence([self.__tileset["frames"][i] for i in frame_list],
                                                                speed, loop)

    def set_frame(self, frame_idx):
        if 0 <= frame_idx < len(self.__tileset["frames"]):
            self.set_animation([frame_idx, ], None)

    def set_relative_position(self, dx, dy, dz):
        self.x += dx
        self.y += dy
        self.z += dz

    def set_absolute_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
