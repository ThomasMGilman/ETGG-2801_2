from math3d import *
from sdl2.keycode import *
from sdl2.sdlmixer import *
from ImageTexture2DArray import *
from Program import *
import utils, math

class Car:
    
    def __init__(self):
        self.body = CarBody()
        self.tire = CarTire()
        self.speed = .001
        self.tireSpeed = .005
        self.carAngle = 0
        self.pos = vec2(0, 0)
        self.frontTirePos = vec2(.345, -.12)
        self.backTirePos = vec2(-.3, -.12)
        self.twoPi = 2 * math.pi
        self.horn = Mix_LoadWAV(os.path.join("assets", "dixie-horn_daniel-simion.wav").encode())
        self.hornTime = 3000
        self.driving = Mix_LoadWAV(os.path.join("assets", "old-car-engine-edit.wav").encode())
        self.driveTime = 4000
        self.playingHorn = False
        self.soundTimer = 0
        self.tireRot = 0

    def checkAngle(self, angle):
        if(angle > self.twoPi):
            angle -= self.twoPi

    def updatePos(self, amount):
        self.pos.x += amount
        self.tireRot -= amount
        if not Mix_Playing(-1) and self.playingHorn == False and self.soundTimer <= 0:
            print("play VroomVRoom",Mix_Playing(-1))
            Mix_FadeInChannelTimed(-1, self.driving, 0, 0, self.driveTime)
            self.soundTimer = self.driveTime

    def update(self, elapsed, keyset):
        print("SoundPlaying", Mix_Playing(-1))

        if SDLK_w in keyset:
            self.updatePos(self.speed * elapsed)
        elif SDLK_s in keyset:
            self.updatePos(-self.speed * elapsed)
        elif self.playingHorn == False and Mix_Playing(-1) and self.playingHorn == False:
            self.soundTimer = 0
            Mix_HaltChannel(-1)
        if SDLK_SPACE in keyset:
            self.soundTimer = 0
            self.playingHorn = True
            Mix_FadeInChannelTimed(-1, self.horn, 0, 0, 3000)
        if SDLK_d in keyset:
            self.carAngle -= self.speed * elapsed
        if SDLK_a in keyset:
            self.carAngle += self.speed * elapsed

        if self.soundTimer > 0:
            self.soundTimer -= elapsed

        if not Mix_Playing(-1) and self.playingHorn == True:
            self.playingHorn = False

        self.checkAngle(self.carAngle)
        self.checkAngle(self.tireRot)

    def draw(self):
        angleOfmov = vec2(math.cos(self.carAngle), math.sin(self.carAngle))
        transPos    = translation2(self.pos)
        rotAngle    = rotation2(self.carAngle)
        carAnglePos = rotAngle * transPos
        Program.setUniform("worldMatrix", carAnglePos)
        Program.updateUniforms()
        self.body.draw()

        #draw the front tire
        frontTirePos    = translation2(self.frontTirePos)
        tireAngle       = rotation2(self.tireRot)
        Program.setUniform("worldMatrix", tireAngle * frontTirePos * carAnglePos)
        Program.updateUniforms()
        self.tire.draw()
        
        #draw the rear tire
        backTirePos = translation2(self.backTirePos)
        Program.setUniform("worldMatrix", tireAngle * backTirePos * carAnglePos)
        Program.updateUniforms()
        self.tire.draw()

class CarBody:
    def __init__(self):
        self.tex = ImageTexture2DArray("car.png")
        self.vao = utils.makeSquare( 0.5,0.13,False)
    def draw(self):
        glBindVertexArray(self.vao)
        self.tex.bind(0)
        glDrawElements(GL_TRIANGLES,6,GL_UNSIGNED_INT,0)
        
class CarTire:
    def __init__(self):
        self.tex = ImageTexture2DArray("tire.png")
        self.vao = utils.makeSquare( 0.075,0.075,False)
        self.tireAngle = 0
    def draw(self):
        glBindVertexArray(self.vao)
        self.tex.bind(0)
        glDrawElements(GL_TRIANGLES,6,GL_UNSIGNED_INT,0)