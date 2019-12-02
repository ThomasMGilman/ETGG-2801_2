from utilityLibs.glCommands import *
from Setup import *
import globs, sys

def buryTheDead(List):
    index = 0
    while index < len(List):
        if not List[index].alive():
            x = List.pop()
            if index < len(List):
                List[index] = x
        else:
            index += 1

    #for debugging
    '''if len(List) != globs.lastListCount:
        print(str(len(List)))
        globs.lastListCount = len(List)'''
    return List


def updateAndDraw(objList, elapsedMsec):
    for obj in objList:
        obj.update(elapsedMsec)
        obj.draw()


def draw(elapsedMSec):
    clear()

    for mesh in globs.MeshObjects:
        mesh.draw()

    globs.Player.draw()

    SDL_GL_SwapWindow(globs.win)


def update(elapsedMsec):
    ev = SDL_Event()
    while 1:
        if not SDL_PollEvent(byref(ev)):
            break
        if ev.type == SDL_QUIT:
            SDL_Quit()
            sys.exit(0)
        elif ev.type == SDL_KEYDOWN:
            k = ev.key.keysym.sym
            globs.keyset.add(k)
            if k == SDLK_q:
                SDL_Quit()
                sys.exit(0)

        elif ev.type == SDL_KEYUP:
            k = ev.key.keysym.sym
            globs.keyset.discard(k)

        elif ev.type == SDL_MOUSEBUTTONDOWN:
            print("mouse down:", ev.button.button, ev.button.x, ev.button.y)

        elif ev.type == SDL_MOUSEBUTTONUP:
            print("mouse up:", ev.button.button, ev.button.x, ev.button.y)

        #elif ev.type == SDL_MOUSEMOTION:
            #print("mouse move:", ev.motion.x, ev.motion.y)

    globs.Player.update(elapsedMsec)


def main():
    globs.win = setupWindow()                 #Setup SDL_GL_Attributes and get SDL_Window
    print("running");
    if not globs.win:
        print("Could not create window")
        return

    rc = SDL_GL_CreateContext(globs.win)
    if not rc:
        print("Cannot create GL context")
        raise RuntimeError()

    setup()

    lastTicks = SDL_GetPerformanceCounter()
    accumElapsedMsec = 0
    while 1:
        nowTicks = SDL_GetPerformanceCounter()                                      #Get ticks at start of loop
        elapsedTicks = nowTicks - lastTicks                                         #Ticks since lastTick
        lastTicks = nowTicks                                                        #lastTick is now
        elapsedMsec = int(1000 * elapsedTicks / globs.TICKS_PER_SECOND)             #convert lastTicks to Msec
        accumElapsedMsec += elapsedMsec
        while accumElapsedMsec >= globs.UPDATE_QUANTUM_MSEC:
            update(elapsedMsec)
            accumElapsedMsec -= globs.UPDATE_QUANTUM_MSEC

        draw(elapsedMsec)

        endTicks = SDL_GetPerformanceCounter()                                      #Get finale tick
        frameTicks = endTicks - nowTicks                                            #Get num ticks for frame
        frameMsec = int(frameTicks / globs.TICKS_PER_SECOND * 1000)                 #convert ticks for frame to Msec
        leftoverMsec = globs.DESIRED_MSEC_PER_FRAME - frameMsec                     #calculate numTicks for desired frameRate left
        if leftoverMsec > 0:
            SDL_Delay(leftoverMsec)                                                 #delay to meet frameRate if frame doesnt take to long

main()