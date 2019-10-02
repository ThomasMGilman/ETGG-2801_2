from GameObjects import Player, StarBackground, tilemap, Shapes
from utilityLibs import Sampler
from sdl2 import *
from sdl2.sdlmixer import *
from glLibs.gl import *
from glLibs.glconstants import *
from os import listdir
import os.path, globs, traceback


def debugCallback( source, msgType, msgId, severity, length, message, param ):
    print(msgId,":",message)
    if severity == GL_DEBUG_SEVERITY_HIGH:
        for x in traceback.format_stack():
            print(x, end="")


def enableDebugging(enabled = False):
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
    TexturesFolder = listdir(os.path.join("assets", folderName))
    for texName in TexturesFolder:
        array.append(os.path.join(folderName, texName))


def setupTextures():
    """Setup Textures"""
    setTextures(globs.mapTextures,      "mapTextures")
    setTextures(globs.playerTextures,   "playerTextures")
    setTextures(globs.starTextures,     "starTextures")
    setTextures(globs.bulletTextures,   "bulletTextures")


def setupGlobals():
    """Setup Random, Sounds, FrameRate, Textures, and Sampler"""
    Shapes.seedRandom()
    globs.pulseSound = Mix_LoadWAV(os.path.join("assets", globs.pulseSound).encode())  # load PulseSound file
    setupFrameRateGlobals(globs.DESIRED_FRAMES_PER_SEC)
    setupTextures()
    if(globs.sampler == None):
        globs.sampler = Sampler.Sampler()
    globs.sampler.bind(0)


def setupObjects():
    """Setup global objects for drawing"""
    globs.StarBackground = StarBackground.StarBackground(0, 0)
    globs.MapBackground = tilemap.Map()
    globs.objectsToDraw.append(Player.Player(0, 0, .25))