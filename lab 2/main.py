from ctypes import *
from sdl2 import *
from sdl2.keycode import *
from gl import *
from glconstants import *
from Buffer import *
from Program import *


def setup(pointArray):
    glEnable(GL_MULTISAMPLE)
    glClearColor(0, 0, 0, 1.0)

    my_buffer = Buffer(pointArray)#array.array("f", [0, 0]))
    # GenerateVAO
    tmp = array.array("I", [0])
    glGenVertexArrays(1, tmp)
    vao = tmp[0]
    glBindVertexArray(vao)

    # Tell GL about buffer layout and use the buffer
    my_buffer.bind(GL_ARRAY_BUFFER)
    glEnableVertexAttribArray(0)
    # which pipe, items per vertex, type per item, auto-normalize, data size per item in bytes, start in buffer
    # numPoints = len(arrayOfPoints)
    glVertexAttribPointer(0, 2, GL_FLOAT, False, 2 * 4, 0)

    # unbind
    # glBindVertexArray(0)

    prog = Program("vs.txt", "fs.txt")
    prog.use()


def update():
    ev = SDL_Event()
    while 1:
        if not SDL_PollEvent(byref(ev)):
            break
        if ev.type == SDL_QUIT:
            SDL_Quit()
            sys.exit(0)
        elif ev.type == SDL_KEYDOWN:
            k = ev.key.keysym.sym
            print("key down:", k)
            if k == SDLK_q:
                SDL_Quit()
                sys.exit(0)
        elif ev.type == SDL_KEYUP:
            k = ev.key.keysym.sym
            print("key up:", k)
        elif ev.type == SDL_MOUSEBUTTONDOWN:
            print("mouse down:", ev.button.button, ev.button.x, ev.button.y)
        elif ev.type == SDL_MOUSEBUTTONUP:
            print("mouse up:", ev.button.button, ev.button.x, ev.button.y)
        elif ev.type == SDL_MOUSEMOTION:
            print("mouse move:", ev.motion.x, ev.motion.y)


def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawArrays(GL_POINTS, 0, 4)


def main():
    SDL_Init(SDL_INIT_VIDEO)

    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24)
    SDL_GL_SetAttribute(SDL_GL_STENCIL_SIZE, 8)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 4)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 3)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_FLAGS, SDL_GL_CONTEXT_DEBUG_FLAG)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLEBUFFERS, 1)
    SDL_GL_SetAttribute(SDL_GL_MULTISAMPLESAMPLES, 4)

    win = SDL_CreateWindow(b"ETGG", 20, 20, 512, 512, SDL_WINDOW_OPENGL)

    print("running");
    if not win:
        print("Could not create window")
        return

    rc = SDL_GL_CreateContext(win)
    if not rc:
        print("Cannot create GL context")
        raise RuntimeError()

    #Need to randomly add 2d points to array to pass to be buffer and pass num of 2d points to draw
    starArray = array.array("f", [0, 0, 1, 1, .5, .5, -.5, -.5])
    print(len(starArray)/2)

    setup(starArray)

    while 1:
        update()
        draw()
        SDL_GL_SwapWindow(win)

main()