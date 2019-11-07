from GameObjects import Player, Enemy, Background, tilemap, Shapes
from utilityLibs import Sampler
from sdl2 import *
from sdl2.sdlmixer import *
from glLibs.gl import *
from glLibs.glconstants import *
from os import listdir
from utilityLibs import glCommands
import os.path, globs, traceback, random, math


def debugCallback( source, msgType, msgId, severity, length, message, param ):
    print(msgId,":",message)
    if severity == GL_DEBUG_SEVERITY_HIGH:
        for x in traceback.format_stack():
            print(x, end="")


def enableDebugging(enabled):
    """Enables debugging, disabled by default for performance"""
    if enabled:
        glDebugMessageCallback(debugCallback, None)
        # Source, type, severity, count, ids, enabled
        glDebugMessageControl(GL_DONT_CARE, GL_DONT_CARE, GL_DONT_CARE,
                              0, None, True)
        glEnable(GL_DEBUG_OUTPUT_SYNCHRONOUS)
        glEnable(GL_DEBUG_OUTPUT)


def setupWindow():
    """Setup and return window object"""
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO)
    Mix_Init(MIX_INIT_OGG | MIX_INIT_MP3)
    Mix_OpenAudio(22050, MIX_DEFAULT_FORMAT, 1, 4096)

    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24)
    SDL_GL_SetAttribute(SDL_GL_STENCIL_SIZE, 8)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 4)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 3)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_FLAGS, SDL_GL_CONTEXT_DEBUG_FLAG)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 1)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 4)

    return SDL_CreateWindow(b"ETGG", 20, 20, 512, 512, SDL_WINDOW_OPENGL)


def setupFrameRateGlobals(fps):
    """Setup Desired FrameRate in Globals"""
    globs.DESIRED_SEC_PER_FRAME = 1 / fps
    globs.DESIRED_MSEC_PER_FRAME = int(globs.DESIRED_SEC_PER_FRAME * 1000)
    globs.TICKS_PER_SECOND = SDL_GetPerformanceFrequency()
    globs.UPDATE_QUANTUM_MSEC = 5


def setTextures(array, folderName):
    TexturesFolder = sorted(listdir(os.path.join("assets", folderName)))
    for texName in TexturesFolder:
        array.append(os.path.join(folderName, texName))


def setupTextures():
    """Setup Textures"""
    setTextures(globs.mapTextures,          "mapTextures")
    setTextures(globs.playerTextures,       "playerTextures")
    setTextures(globs.starTextures,         "starTextures")
    setTextures(globs.bulletTextures,       "bulletTextures")
    setTextures(globs.enemyTextures,        "enemyTextures")
    setTextures(globs.backgroundTextures,   "backgroundTextures")


def setupGlobals():
    """Setup Random, Sounds, FrameRate, Textures, and Sampler"""
    Shapes.seedRandom()
    globs.pulseSound = Mix_LoadWAV(os.path.join("assets", globs.pulseSound).encode())  # load PulseSound file
    setupFrameRateGlobals(globs.DESIRED_FRAMES_PER_SEC)
    setupTextures()

    glEnable(GL_BLEND)
    glEnable(GL_PROGRAM_POINT_SIZE)
    glCommands.setClassicOpacity()

    globs.TWO_PI = 2 * math.pi
    if(globs.sampler == None):
        globs.sampler = Sampler.Sampler()
    globs.sampler.bind(0)


def setupObjects():
    """Setup global objects for drawing"""
    #globs.StarBackground = StarBackground.StarBackground(0, 0, .1, .1)
    globs.MapBackground = tilemap.Map()
    globs.Player = Player.Player(globs.startPosX, globs.startPosY, globs.playerWidth, globs.playerHeight)
    globs.Background = Background.Background()

def setupWorldSpace(worldWidth, worldHeight):
    globs.worldWidth = worldWidth
    globs.worldHeight = worldHeight

def putEnemy(x, y, direction, Width, Height, textureNum):
    #print("spawning enemy: ",x,y,direction, Width, Height,textureNum)
    globs.Enemies.append(Enemy.Enemy(x, y, direction, Width, Height, textureNum))


def spawnEnemy(elapsedMsec):
    if globs.lastSpawned <= 0:
        enemyType = random.randint(0,1)
        tmp = random.randint(-1, 1)
        x = 0
        y = 0
        direction = 0
        if enemyType == 0:
            x = tmp if tmp != 0 else globs.worldWidth
            direction = globs.FACING_RIGHT if x < 0 else globs.FACING_LEFT
        elif enemyType == 1:
            y = globs.worldHeight
            direction = globs.FACING_DOWN
            x = random.uniform(-1, globs.worldWidth)

        x = globs.enemySize+1*x if (x < -1+globs.enemySize or x > 1-globs.enemySize) and y != 0 else x  #keep enemy image in bounds
        texNum = 1 if direction == globs.FACING_DOWN and len(globs.enemyTextures) > 1 else 0            #pick texture

        putEnemy(x, y, direction, globs.enemySize, globs.enemySize, texNum)
        globs.lastSpawned = globs.spawnTimer
    else:
        globs.lastSpawned -= elapsedMsec


def setup(worldWidth, worldHeight):
    enableDebugging(0)  # enables debugging messages, DISABLED BY DEFAULT for performance
    setupGlobals()
    setupObjects()
    setupWorldSpace(worldWidth, worldHeight)
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)