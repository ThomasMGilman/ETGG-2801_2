from GameObjects import Player, Enemy, Background, tilemap, Shapes, Map
from utilityLibs import Sampler, glCommands
from sdl2 import *
from sdl2.sdlmixer import *
from glLibs.gl import *
from glLibs.glconstants import *
from os import listdir
from toolLibs import math3d
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

def set_glEnables():
    glEnable(GL_BLEND)                  #Enable Alpha
    glEnable(GL_PROGRAM_POINT_SIZE)     #Enable Point sizing
    glEnable(GL_DEPTH_TEST)             #Enable Depth Testing
    glDepthFunc(GL_LEQUAL)              #Set Depth Test Function
    glCommands.setClassicOpacity()


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

    return SDL_CreateWindow(b"ETGG", 20, 20, globs.WIN_WIDTH, globs.WIN_HEIGHT, SDL_WINDOW_OPENGL)


def setupFrameRateGlobals(fps):
    """Setup Desired FrameRate in Globals"""
    globs.DESIRED_SEC_PER_FRAME = 1 / fps
    globs.DESIRED_MSEC_PER_FRAME = int(globs.DESIRED_SEC_PER_FRAME * 1000)
    globs.TICKS_PER_SECOND = SDL_GetPerformanceFrequency()
    globs.UPDATE_QUANTUM_MSEC = 5


def setupResourcesDict(Dict, FolderPath):
    """Append the specified Resources Dictionary with the contents found inside the folder passed along with its path,
        Follows the structure of folder of folders"""
    ResourceFolder = sorted(listdir(FolderPath))
    if len(ResourceFolder) > 0:
        for dir in ResourceFolder:
            Dict[dir] = []
            location = os.path.join(FolderPath, dir)
            resourcesDir = sorted(listdir(location))
            for resource in resourcesDir:
                Dict[dir].append(resource)
            Dict[dir].append(location)
    #print("Dict setup: ",Dict)


def setupResources():
    setupResourcesDict(globs.Textures, os.path.join("assets", "Textures"))
    setupResourcesDict(globs.Meshes, os.path.join("assets", "Meshes"))
    setupResourcesDict(globs.Sounds, os.path.join("assets", "Audio"))


def setupGlobals():
    """Setup Random, Sounds, FrameRate, Textures, and Sampler"""
    Shapes.seedRandom()
    setupFrameRateGlobals(globs.DESIRED_FRAMES_PER_SEC)
    setupResources()
    set_glEnables()

    globs.playerStartPos = math3d.vec3(0,.5,0)
    globs.playerScale = math3d.vec3(1, 1, 1)
    globs.bulletScale = math3d.vec3(.25, .25, .25)
    globs.TWO_PI = 2 * math.pi
    if(globs.sampler == None):
        globs.sampler = Sampler.Sampler()
    globs.sampler.bind(0)


def setupObjects():
    """Setup global objects for drawing"""
    globs.Player = Player.Player(globs.playerStartPos, globs.playerScale)
    globs.MeshObjects.append(Map.MapRoom(math3d.vec3(0,0,0), "dungeon", 2))


def setup():
    enableDebugging(0)  # enables debugging messages, DISABLED BY DEFAULT for performance
    setupGlobals()
    setupObjects()
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)