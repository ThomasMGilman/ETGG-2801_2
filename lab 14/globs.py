#CONSTANTS
TWO_PI = 0
WIN_WIDTH = 512
WIN_HEIGHT = 512
FOV = 90

#Frame rates for drawing
DESIRED_FRAMES_PER_SEC = 60
DESIRED_SEC_PER_FRAME = 0
DESIRED_MSEC_PER_FRAME = 0
TICKS_PER_SECOND = 0
UPDATE_QUANTUM_MSEC = 0

#point count for stars and starObject
numStars = 100
starSize = 2
StarBackground = None
MapBackground = None

#Textures
Textures = {}

#Sounds
Sounds = {}

#Meshes
Meshes = {}

win = None
Player = None
Background = None

MeshObjects = []
Bullets = []
Enemies = []
Particles = []

#keys input
keyset = set()

#Sounds
pulseSoundTime      = 1000

#for debugging use
lastListCount = 0

#Window RGBA
RED     = 0.0
GREEN   = 0.0
BLUE    = 0.0
ALPHA   = 1.0

#States
DEAD = 0
ALIVE = 1
DYING = 2

#World Space parameters
minWorldX = -1
minWorldY = -1
worldWidth  = 4
worldHeight = 4

#Background
backgroundRotationSpeed = .0002

#Sampler Object
sampler = None

#player parameters
playerStartPos = None
playerScale = None
jumpPeak = .3
playerSpeed = .001
playerFireRate = 2000

#bullet parameters
bulletSpeed = 0.002
bulletScale = None

#enemy parameters
enemySize = .25
bossSize = .75
enemySpeed = 0.0005
spawnTimer = 1000   #spawn enemy variant every second
lastSpawned = 0
bossFilePath = "boss2.obj"
bossInGame = False

bossSpawnXOffset = .5
bossSpawnYOffset = -.05
bossSpawnZOffset = 0
bossSpawnX = (worldWidth - minWorldX) / 2
bossSpawnY = (worldHeight - minWorldY) / 2
bossSpawnZ = 0

#Entity Life
playerLife = 10
enemyLife = 1
bulletLife = 1000        #in mil sec

#Particle parameters
particleLife = 1000
particleCount = 100
particleSize = 20
speedDivisor = .001

particleAlpha = 1

