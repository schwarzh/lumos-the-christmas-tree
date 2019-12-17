import time
import random
import opc
import os
import subprocess
import signal

fadecandyUrl = 'localhost:7890'

# Create a client object
client = opc.Client(fadecandyUrl)
numLEDs = 50

# playable animation sequences
LUMOS = "lumos" 
AGUAMENTI = "aguamenti"
INCENDIO = "incendio"
BROKEN = "broken"

# broke = False
current_spell = ''

dir_path = os.path.dirname(os.path.realpath(__file__))
mp3Dir = dir_path + "/mp3s/"
media_prefix= "file://" + mp3Dir
vlc_path = "/usr/bin/cvlc"
incendio_command = f"{dir_path}/incendio/strip50_flames" # replace with your command for playing these light animations
aguamenti_command = f"{dir_path}/aguamenti/strip50_water"
broken_command = f"{dir_path}/broken/strip50_spazzy"
lumos_command = f"{dir_path}/lumos/strip50_light"

def killMusic():
    print("killing music")
    if 'musicPlayer' in vars() or 'musicPlayer' in globals():
        musicPlayer.kill()

def playMusic(file): 
    global musicPlayer
    print(f"playing music {file}")
    killMusic()
    musicPlayer = subprocess.Popen(f"exec {vlc_path} {media_prefix + file}", shell=True)

def killLights():
    print("killing lights")
    pauseLights()
    pixels = [ (0,0,0) ] * numLEDs
    client.put_pixels(pixels)

def pauseLights():
    print("pausing lights")
    if 'lightPlayer' in vars() or 'lightPlayer' in globals():
        print(f"killing pid: {lightPlayer.pid}")
        os.killpg(os.getpgid(lightPlayer.pid), signal.SIGTERM)

def setNewSpell(spell):
    global current_spell, previous_spell, paused
    print("setting new spell: " + spell)
    previous_spell = current_spell
    current_spell = spell
    killMusic()
    killLights()
    paused = False

def playLights(command):
    global lightPlayer
    print(f"playing lights")
    killLights()
    lightPlayer = subprocess.Popen(f"exec {command}", stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid)

def lumos():
    print("Lumos called")
    setNewSpell(LUMOS)

    playLights(lumos_command)

def nox():
    print("Nox called")
    killLights()

def aguamenti():
    print("Aguamenti called")
    setNewSpell(AGUAMENTI)

    #run water animation and sounds
    playMusic("zapsplat_nature_ocean_waves_medium_splash_rocks_distance_water_rushes_around_rocks_shallow_close_43574.mp3")
    playLights(aguamenti_command)

def finite_incantatem():
    print("Finite Incantatem called")
    killMusic()
    killLights()
    
def arresto_momentum():
    print("Arresto Momentum called")
    global paused
    #play record scratch
    playMusic("hptheme.mp3")
    # don't need to stop the player, it shold only be a couple of seconds long
    #pause current animation and music
    pauseLights()

def silencio():
    print("Silencio called")
    killMusic()

def incendio():
    print("Incendio called")
    #play fire animation and sounds
    setNewSpell(INCENDIO)
    playMusic("audio_hero_FireMediumRoarHiss_PE052201_358.mp3")
    playLights(incendio_command)

def reparo():
    print("reparo called")
    #resume previous animation
    
    # play starting up sound then restart previous spell
    playMusic("hptheme.mp3")
    if previous_spell:
        if previous_spell == LUMOS:
                lumos()
        elif previous_spell == AGUAMENTI:
                aguamenti()
        elif previous_spell == INCENDIO:
                incendio()
    else: 
        finite_incantatem()

def broken():
    print("broken called")
    setNewSpell(BROKEN)
    #play spazzy electric sounds
    playMusic("sound_design_effect_electricity_electric_arc.mp3")
    playLights(broken_command)