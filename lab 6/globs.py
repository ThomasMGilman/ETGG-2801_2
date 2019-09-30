#Frame rates for drawing
DESIRED_FRAMES_PER_SEC = 60
DESIRED_SEC_PER_FRAME = 0
DESIRED_MSEC_PER_FRAME = 0
TICKS_PER_SECOND = 0
UPDATE_QUANTUM_MSEC = 0

#point count for stars and starObject
numStars = 100
StarBackground = None
MapBackground = None

#textures
mapTextures = []
playerTextures = []
starTextures = []
bulletTextures = []

win = None
objectsToDraw = []

#keys input
keyset = set()

#Sounds
pulseSound          = "Pulse-gun-07.wav"    #http://www.soundescapestudios.com/SESAudio/SES%20Site%20Sounds/Laser%20Sci%20Fi/Pulse-gun-07.wav
pulseSoundTime      = 1000

#Window RGBA
RED     = 0.0
GREEN   = 0.0
BLUE    = 0.0
ALPHA   = 1.0

#Sampler Object
sampler = None

#playerStates
ON_GROUND = 0
RISING = 1
FALLING = 2
FACING_LEFT = 3
FACING_RIGHT = 4

#playerImages parameters
jumpPeak = .3
playerSpeed = .002
playerFireRate = 500

#bullet parameters
bulletSpeed = 0.002 + playerSpeed