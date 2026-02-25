import numpy as np
import pygame
import time

pygame.init()                     
sample_rate = pygame.mixer.get_init()[0]  

def singlesine(frequency,amplitude,duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sine_wave = amplitude * 32767 * np.sin(2 * np.pi * frequency * t)
    sine_wave_int = sine_wave.astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack((sine_wave_int, sine_wave_int)))

def multisine(frequency_A,frequency_B,frequency_C,amplitude,duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sine_wave_A = amplitude * 32767 * np.sin(2 * np.pi * frequency_A * t)
    sine_wave_int_A = sine_wave_A.astype(np.int16)
    sine_wave_B = amplitude * 32767 * np.sin(2 * np.pi * frequency_B * t)
    sine_wave_int_B = sine_wave_B.astype(np.int16)
    sine_wave_C = amplitude * 32767 * np.sin(2 * np.pi * frequency_C * t)
    sine_wave_int_C = sine_wave_C.astype(np.int16)
    mixed_wave = (sine_wave_int_A + sine_wave_int_B + sine_wave_int_C)
    mixed_wave = (mixed_wave / 3).astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack((mixed_wave,mixed_wave)))

button_press=singlesine(329.63,0.2,0.1)
button_rel=singlesine(415.3,0.4,0.1)

bullet_charge=singlesine(160,0.06,10/160)
bullet1=multisine(130,175,195,0.5,0.1)
bullet2=multisine(300,240,170,0.5,0.08)
bullet3=multisine(250,270,280,0.4,0.05)

bite=multisine(450,500,550,0.333,0.15)
zomhit1=multisine(100,200,400,0.333,0.3)
zomhit2=singlesine(600,0.2,0.02)
wallhit=singlesine(300,0.2,0.02)

win1=singlesine(440,0.4,0.4)
win2=singlesine(554.37,0.4,0.4)
win3=singlesine(659.25,0.4,0.4)
death1=singlesine(220,0.4,0.4)
death2=singlesine(261.63,0.4,0.4)
death3=singlesine(329.63,0.4,0.4)

charging=multisine(100,120,140,0.345,0.1)
crash1=singlesine(20,1.1,0.2)
crash2=multisine(40,60,900,0.5,0.2)
crash3=singlesine(10,1.5,0.12)
spit=singlesine(700,0.4,0.1)
spit2=singlesine(650,0.4,0.12)
b1death1=singlesine(200,0.8,0.6)
b1death2=singlesine(350,0.8,0.6)
crushing=multisine(95,56,42,0.4,0.1)
b2death=singlesine(600,0.5,0.6)
spawn1=singlesine(150,0.6,0.14)
spawn2=singlesine(180,0.6,0.1)
b3death1=multisine(140,240,340,0.4,0.1)
b3death2=singlesine(4000,0.8,0.08)

