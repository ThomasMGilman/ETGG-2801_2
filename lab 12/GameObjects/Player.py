from sdl2.keycode import *
from GameObjects import Bullet, Camera
from GameObjects.Entity import *
import globs

class Player(Entity):
    tex = None
    def __init__(self, x, y, z, Width, Height, Depth):
        self.halfHeight = Width / 2

        if Player.tex == None:
            Player.tex = ImageTexture2DArray(globs.Textures["player"][0], path=globs.Textures["player"][-1]);

        super().__init__(x, y, z, Width, Height, Depth, globs.playerLife, globs.playerSpeed, "Player")
        self.CameraObj = Camera.Camera(self.pos)

    def draw(self):
        self.CameraObj.setUniforms()
        super().draw(Player.tex, 0)

    def updatePos(self, delta):
        super().updatePos(delta)
        self.CameraObj.strafe(delta.x, delta.y, delta.z)

    def update(self, elapsedTime):
        if SDLK_d in globs.keyset or SDLK_RIGHT in globs.keyset:        #Move Right
            self.updatePos(vec3(-self.speed * elapsedTime, 0, 0))

        if SDLK_a in globs.keyset or SDLK_LEFT in globs.keyset:         #Move Left
            self.updatePos(vec3(self.speed * elapsedTime, 0, 0))

        if SDLK_w in globs.keyset or SDLK_UP in globs.keyset:           #Move Forward
            self.updatePos(vec3(0, 0, self.speed * elapsedTime))

        if SDLK_s in globs.keyset or SDLK_DOWN in globs.keyset:         #Move Backwards
            self.updatePos(vec3(0, 0, -self.speed * elapsedTime))

        if SDLK_r in globs.keyset or SDLK_o in globs.keyset:            #tilt clockwise
            self.CameraObj.tilt(self.speed * elapsedTime)

        if SDLK_e in globs.keyset or SDLK_u in globs.keyset:            #tilt counter-clockwise
            self.CameraObj.tilt(-self.speed * elapsedTime)

        if SDLK_RIGHT in globs.keyset or SDLK_l in globs.keyset:        #turn right
            self.CameraObj.turn(self.speed * elapsedTime)

        if SDLK_LEFT in globs.keyset or SDLK_j in globs.keyset:         #turn left
            self.CameraObj.turn(-self.speed * elapsedTime)

        if SDLK_UP in globs.keyset or SDLK_i in globs.keyset:           #look up
            self.CameraObj.pitch(self.speed * elapsedTime)

        if SDLK_DOWN in globs.keyset or SDLK_k in globs.keyset:         #look down
            self.CameraObj.pitch(-self.speed * elapsedTime)

        if SDLK_g in globs.keyset or SDLK_y in globs.keyset:            #roll right
            self.CameraObj.roll(self.speed * elapsedTime)

        if SDLK_f in globs.keyset or SDLK_t in globs.keyset:            #roll left
            self.CameraObj.roll(-self.speed * elapsedTime)


        if SDLK_r in globs.keyset:
            print(self.pos)