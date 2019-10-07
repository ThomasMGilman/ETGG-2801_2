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
enemyTextures = []

win = None
objectsToDraw = []

#keys input
keyset = set()

#Sounds
pulseSound          = "Pulse-gun-07.wav"    #http://www.soundescapestudios.com/SESAudio/SES%20Site%20Sounds/Laser%20Sci%20Fi/Pulse-gun-07.wav
pulseSoundTime      = 1000

#for debugging use
lastListCount = 0

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
FACING_UP = 5
FACING_DOWN = 6
SHOOTING_UP = 7
SHOOTING_DOWN = 8

#playerImages parameters
jumpPeak = .3
playerSpeed = .002
playerFireRate = 500

#bullet parameters
bulletSpeed = 0.002 + playerSpeed

#enemy parameters
enemySize = .25
enemySpeed = 0.0005
spawnTimer = 2000   #spawn enemy variant every second
lastSpawned = 0

#Entity Life
playerLife = 10
enemyLife = 1
bulletLife = 750        #in mil sec

#Particle parameters
particleLife = 100
particleCount = 50