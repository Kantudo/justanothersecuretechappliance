import RPi.GPIO as GPIO
import time
import threading
buzzer_pin = 2

notes = {
	'B0' : 31,
	'C1' : 33, 'CS1' : 35,
	'D1' : 37, 'DS1' : 39,
	'EB1' : 39,
	'E1' : 41,
	'F1' : 44, 'FS1' : 46,
	'G1' : 49, 'GS1' : 52,
	'A1' : 55, 'AS1' : 58,
	'BB1' : 58,
	'B1' : 62,
	'C2' : 65, 'CS2' : 69,
	'D2' : 73, 'DS2' : 78,
	'EB2' : 78,
	'E2' : 82,
	'F2' : 87, 'FS2' : 93,
	'G2' : 98, 'GS2' : 104,
	'A2' : 110, 'AS2' : 117,
	'BB2' : 123,
	'B2' : 123,
	'C3' : 131, 'CS3' : 139,
	'D3' : 147, 'DS3' : 156,
	'EB3' : 156,
	'E3' : 165,
	'F3' : 175, 'FS3' : 185,
	'G3' : 196, 'GS3' : 208,
	'A3' : 220, 'AS3' : 233,
	'BB3' : 233,
	'B3' : 247,
	'C4' : 262, 'CS4' : 277,
	'D4' : 294, 'DS4' : 311,
	'EB4' : 311,
	'E4' : 330,
	'F4' : 349, 'FS4' : 370,
	'G4' : 392, 'GS4' : 415,
	'A4' : 440, 'AS4' : 466,
	'BB4' : 466,
	'B4' : 494,
	'C5' : 523, 'CS5' : 554,
	'D5' : 587, 'DS5' : 622,
	'EB5' : 622,
	'E5' : 659,
	'F5' : 698, 'FS5' : 740,
	'G5' : 784, 'GS5' : 831,
	'A5' : 880, 'AS5' : 932,
	'BB5' : 932,
	'B5' : 988,
	'C6' : 1047, 'CS6' : 1109,
	'D6' : 1175, 'DS6' : 1245,
	'EB6' : 1245,
	'E6' : 1319,
	'F6' : 1397, 'FS6' : 1480,
	'G6' : 1568, 'GS6' : 1661,
	'A6' : 1760, 'AS6' : 1865,
	'BB6' : 1865,
	'B6' : 1976,
	'C7' : 2093, 'CS7' : 2217,
	'D7' : 2349, 'DS7' : 2489,
	'EB7' : 2489,
	'E7' : 2637,
	'F7' : 2794, 'FS7' : 2960,
	'G7' : 3136, 'GS7' : 3322,
	'A7' : 3520, 'AS7' : 3729,
	'BB7' : 3729,
	'B7' : 3951,
	'C8' : 4186, 'CS8' : 4435,
	'D8' : 4699, 'DS8' : 4978
}


super_mario_melody = [
  notes['E7'], notes['E7'], 0, notes['E7'],
  0, notes['C7'], notes['E7'], 0,
  notes['G7'], 0, 0,  0,
  notes['G6'], 0, 0, 0,

  notes['C7'], 0, 0, notes['G6'],
  0, 0, notes['E6'], 0,
  0, notes['A6'], 0, notes['B6'],
  0, notes['AS6'], notes['A6'], 0,

  notes['G6'], notes['E7'], notes['G7'],
  notes['A7'], 0, notes['F7'], notes['G7'],
  0, notes['E7'], 0, notes['C7'],
  notes['D7'], notes['B6'], 0, 0,

  notes['C7'], 0, 0, notes['G6'],
  0, 0, notes['E6'], 0,
  0, notes['A6'], 0, notes['B6'],
  0, notes['AS6'], notes['A6'], 0,

  notes['G6'], notes['E7'], notes['G7'],
  notes['A7'], 0, notes['F7'], notes['G7'],
  0, notes['E7'], 0, notes['C7'],
  notes['D7'], notes['B6'], 0, 0
]
super_mario_tempo = [
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,

  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,

  9, 9, 9,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,

  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,

  9, 9, 9,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
]


super_mario_underworld_melody = [
  notes['C4'], notes['C5'], notes['A3'], notes['A4'],
  notes['AS3'], notes['AS4'], 0,
  0,
  notes['C4'], notes['C5'], notes['A3'], notes['A4'],
  notes['AS3'], notes['AS4'], 0,
  0,
  notes['F3'], notes['F4'], notes['D3'], notes['D4'],
  notes['DS3'], notes['DS4'], 0,
  0,
  notes['F3'], notes['F4'], notes['D3'], notes['D4'],
  notes['DS3'], notes['DS4'], 0,
  0, notes['DS4'], notes['CS4'], notes['D4'],
  notes['CS4'], notes['DS4'],
  notes['DS4'], notes['GS3'],
  notes['G3'], notes['CS4'],
  notes['C4'], notes['FS4'], notes['F4'], notes['E3'], notes['AS4'], notes['A4'],
  notes['GS4'], notes['DS4'], notes['B3'],
  notes['AS3'], notes['A3'], notes['GS3'],
  0, 0, 0
]

super_mario_underworld_tempo = [
  12, 12, 12, 12,
  12, 12, 6,
  3,
  12, 12, 12, 12,
  12, 12, 6,
  3,
  12, 12, 12, 12,
  12, 12, 6,
  3,
  12, 12, 12, 12,
  12, 12, 6,
  6, 18, 18, 18,
  6, 6,
  6, 6,
  6, 6,
  18, 18, 18, 18, 18, 18,
  10, 10, 10,
  10, 10, 10,
  3, 3, 3
]

adventure_time_melody = [
    notes['D5'],
    notes['G5'], notes['G5'], notes['G5'], notes['G5'], notes['FS5'],
    notes['FS5'], notes['E5'], notes['D5'], notes['E5'], notes['D5'], notes['D5'],
    notes['C5'], notes['B5'], notes['A5'], notes['G4'],
    0, notes['C5'], notes['B5'], notes['A5'], notes['G4'], 0,
    notes['G5'], 0, notes['G5'], notes['G5'], 0, notes['G5'],
    notes['FS5'], 0, notes['E5'], notes['E5'], notes['D5'], notes['D5'],
    notes['C5'], notes['C5'], notes['C5'], notes['D5'],
    notes['D5'], notes['A5'], notes['B5'], notes['A5'], notes['G4'],
    notes['G5']
  ]
adventure_time_tempo = [
    24,
    24, 12, 12, 12, 24,
    12, 24, 24, 24, 12, 24,
    12, 12, 12, 12,
    24, 12, 24, 24, 12, 24,
    24, 24, 24, 12, 24, 12,
    24, 24, 24, 12, 12, 24,
    8, 24, 24, 8,
    8, 24, 12, 24, 24,
    12
  ]


star_wars_melody = [
					notes['G4'], notes['G4'], notes['G4'],
					notes['EB4'], 0, notes['BB4'], notes['G4'],
					notes['EB4'], 0, notes['BB4'], notes['G4'], 0,

					notes['D4'], notes['D4'], notes['D4'],
					notes['EB4'], 0, notes['BB3'], notes['FS3'],
					notes['EB3'], 0, notes['BB3'], notes['G3'], 0,

					notes['G4'], 0, notes['G3'], notes['G3'], 0,
					notes['G4'], 0, notes['FS4'], notes['F4'],
					notes['E4'], notes['EB4'], notes['E4'], 0,
					notes['GS3'], notes['CS3'], 0,

					notes['C3'], notes['B3'], notes['BB3'], notes['A3'], notes['BB3'], 0,
					notes['EB3'], notes['FS3'], notes['EB3'], notes['FS3'],
					notes['BB3'], 0, notes['G3'], notes['BB3'], notes['D4'], 0,


					notes['G4'], 0, notes['G3'], notes['G3'], 0,
					notes['G4'], 0, notes['FS4'], notes['F4'],
					notes['E4'], notes['EB4'], notes['E4'], 0,
					notes['GS3'], notes['CS3'], 0,

					notes['C3'], notes['B3'], notes['BB3'], notes['A3'], notes['BB3'], 0,

					notes['EB3'], notes['FS3'], notes['EB3'],
					notes['BB3'], notes['G3'], notes['EB3'], 0, notes['BB3'], notes['G3'],
					]


star_wars_tempo = [
					2, 2, 2,
					4, 8, 6, 2,
					4, 8, 6, 2, 8,

					2, 2, 2,
					4, 8, 6, 2,
					4, 8, 6, 2, 8,

					2, 16, 4, 4, 8,
					2, 8, 4, 6,
					6, 4, 4, 8,
					4, 2, 8,
					4, 4, 6, 4, 2, 8,
					4, 2, 4, 4,
					2, 8, 4, 6, 2, 8,

					2, 16, 4, 4, 8,
					2, 8, 4, 6,
					6, 4, 4, 8,
					4, 2, 8,
					4, 4, 6, 4, 2, 8,
					4, 2, 2,
					4, 2, 4, 8, 4, 2,
					]

popcorn_melody = [

	notes['A4'], notes['G4'], notes['A4'], notes['E4'], notes['C4'], notes['E4'], notes['A3'],
	notes['A4'], notes['G4'], notes['A4'], notes['E4'], notes['C4'], notes['E4'], notes['A3'],

	notes['A4'], notes['B4'], notes['C5'], notes['B4'], notes['C5'], notes['A4'], notes['B4'], notes['A4'], notes['B4'], notes['G4'],
	notes['A4'], notes['G4'],notes['A4'], notes['F4'], notes['A4'],


	notes['A4'], notes['G4'], notes['A4'], notes['E4'], notes['C4'], notes['E4'], notes['A3'],
	notes['A4'], notes['G4'], notes['A4'], notes['E4'], notes['C4'], notes['E4'], notes['A3'],

	notes['A4'], notes['B4'], notes['C5'], notes['B4'], notes['C5'], notes['A4'], notes['B4'], notes['A4'], notes['B4'], notes['G4'],
	notes['A4'], notes['G4'],notes['A4'], notes['B4'], notes['C5'],

	notes['E5'], notes['D5'], notes['E5'], notes['C5'], notes['G4'], notes['C5'], notes['E4'],
	notes['E5'], notes['D5'], notes['E5'], notes['C5'], notes['G4'], notes['C5'], notes['E4'],

	notes['E5'], notes['FS5'], notes['G5'], notes['FS5'], notes['G5'], notes['E5'], notes['FS5'], notes['E5'], notes['FS5'], notes['D5'],
	notes['E5'], notes['D5'],notes['E5'], notes['C5'], notes['E5'],

	###

	notes['E5'], notes['D5'], notes['E5'], notes['C5'], notes['G4'], notes['C5'], notes['E4'],
	notes['E5'], notes['D5'], notes['E5'], notes['C5'], notes['G4'], notes['C5'], notes['E4'],

	notes['E5'], notes['FS5'], notes['G5'], notes['FS5'], notes['G5'], notes['E5'], notes['FS5'], notes['E5'], notes['FS5'], notes['D5'],
	notes['E5'], notes['D5'],notes['B4'], notes['D5'], notes['E5'],
]
popcorn_tempo = [
	8,8,8,8,8,8,4,
	8,8,8,8,8,8,4,

	8,8,8,8,8,8,8,8,8,8,
	8,8,8,8,4,

	8,8,8,8,8,8,4,
	8,8,8,8,8,8,4,

	8,8,8,8,8,8,8,8,8,8,
	8,8,8,8,4,

	8,8,8,8,8,8,4,
	8,8,8,8,8,8,4,

	8,8,8,8,8,8,8,8,8,8,
	8,8,8,8,4,

	8,8,8,8,8,8,4,
	8,8,8,8,8,8,4,

	8,8,8,8,8,8,8,8,8,8,
	8,8,8,8,4,
]

twinkle_twinkle_melody = [
	notes['C4'], notes['C4'], notes['G4'], notes['G4'], notes['A4'], notes['A4'], notes['G4'],
	notes['F4'], notes['F4'], notes['E4'], notes['E4'], notes['D4'], notes['D4'], notes['C4'],

	notes['G4'], notes['G4'], notes['F4'], notes['F4'], notes['E4'], notes['E4'], notes['D4'],
	notes['G4'], notes['G4'], notes['F4'], notes['F4'], notes['E4'], notes['E4'], notes['D4'],

	notes['C4'], notes['C4'], notes['G4'], notes['G4'], notes['A4'], notes['A4'], notes['G4'],
	notes['F4'], notes['F4'], notes['E4'], notes['E4'], notes['D4'], notes['D4'], notes['C4'],
]

twinkle_twinkle_tempo = [
	4,4,4,4,4,4,2,
	4,4,4,4,4,4,2,

	4,4,4,4,4,4,2,
	4,4,4,4,4,4,2,

	4,4,4,4,4,4,2,
	4,4,4,4,4,4,2,
]

crazy_frog_melody = [
	notes['A4'], notes['C5'], notes['A4'], notes['A4'], notes['D5'], notes['A4'], notes['G4'],
	notes['A4'], notes['E5'], notes['A4'], notes['A4'], notes['F5'], notes['E5'], notes['C5'],
	notes['A4'], notes['E5'], notes['A5'], notes['A4'], notes['G4'], notes['G4'], notes['E4'], notes['B4'],
	notes['A4'],0,

	notes['A4'], notes['C5'], notes['A4'], notes['A4'], notes['D5'], notes['A4'], notes['G4'],
	notes['A4'], notes['E5'], notes['A4'], notes['A4'], notes['F5'], notes['E5'], notes['C5'],
	notes['A4'], notes['E5'], notes['A5'], notes['A4'], notes['G4'], notes['G4'], notes['E4'], notes['B4'],
	notes['A4'],0,


	notes['A3'], notes['G3'], notes['E3'], notes['D3'],

	notes['A4'], notes['C5'], notes['A4'], notes['A4'], notes['D5'], notes['A4'], notes['G4'],
	notes['A4'], notes['E5'], notes['A4'], notes['A4'], notes['F5'], notes['E5'], notes['C5'],
	notes['A4'], notes['E5'], notes['A5'], notes['A4'], notes['G4'], notes['G4'], notes['E4'], notes['B4'],
	notes['A4'],
]

crazy_frog_tempo = [
	2,4,4,8,4,4,4,
	2,4,4,8,4,4,4,
	4,4,4,8,4,8,4,4,
	1,4,

	2,4,4,8,4,4,4,
	2,4,4,8,4,4,4,
	4,4,4,8,4,8,4,4,
	1,4,

	8,4,4,4,

	2,4,4,8,4,4,4,
	2,4,4,8,4,4,4,
	4,4,4,8,4,8,4,4,
	1,
]

deck_the_halls_melody = [
	notes['G5'], notes['F5'], notes['E5'], notes['D5'],
	notes['C5'], notes['D5'], notes['E5'], notes['C5'],
	notes['D5'], notes['E5'], notes['F5'], notes['D5'], notes['E5'], notes['D5'],
	notes['C5'], notes['B4'], notes['C5'], 0,

	notes['G5'], notes['F5'], notes['E5'], notes['D5'],
	notes['C5'], notes['D5'], notes['E5'], notes['C5'],
	notes['D5'], notes['E5'], notes['F5'], notes['D5'], notes['E5'], notes['D5'],
	notes['C5'], notes['B4'], notes['C5'], 0,

	notes['D5'], notes['E5'], notes['F5'], notes['D5'],
	notes['E5'], notes['F5'], notes['G5'], notes['D5'],
	notes['E5'], notes['F5'], notes['G5'], notes['A5'], notes['B5'], notes['C6'],
	notes['B5'], notes['A5'], notes['G5'], 0,

	notes['G5'], notes['F5'], notes['E5'], notes['D5'],
	notes['C5'], notes['D5'], notes['E5'], notes['C5'],
	notes['D5'], notes['E5'], notes['F5'], notes['D5'], notes['E5'], notes['D5'],
	notes['C5'], notes['B4'], notes['C5'], 0,
]

deck_the_halls_tempo = [
	2, 4, 2, 2,
	2, 2, 2, 2,
	4, 4, 4, 4, 2, 4,
	2, 2, 2, 2,

	2, 4, 2, 2,
	2, 2, 2, 2,
	4, 4, 4, 4, 2, 4,
	2, 2, 2, 2,

	2,4,2,2,
	2,4,2,2,
	4,4,2,4,4,2,
	2,2,2,2,

	2, 4, 2, 2,
	2, 2, 2, 2,
	4, 4, 4, 4, 2, 4,
	2, 2, 2, 2,
]

manaderna_melody = [
	notes['E4'],notes['E4'],notes['F4'],notes['G4'],
	notes['G4'],notes['F4'],notes['E4'],notes['D4'],
	notes['C4'],notes['C4'],notes['D4'],notes['E4'],
	notes['E4'],0,notes['D4'],notes['D4'],0,

	notes['E4'],notes['E4'],notes['F4'],notes['G4'],
	notes['G4'],notes['F4'],notes['E4'],notes['D4'],
	notes['C4'],notes['C4'],notes['D4'],notes['E4'],
	notes['D4'],0,notes['C4'],notes['C4'],0,

	notes['D4'],notes['D4'],notes['E4'],notes['C4'],
	notes['D4'],notes['E4'],notes['F4'],notes['E4'],notes['C4'],
	notes['D4'],notes['E4'],notes['F4'],notes['E4'],notes['D4'],
	notes['C4'],notes['D4'],notes['G3'],0,

	notes['E4'],notes['E4'],notes['F4'],notes['G4'],
	notes['G4'],notes['F4'],notes['E4'],notes['D4'],
	notes['C4'],notes['C4'],notes['D4'],notes['E4'],
	notes['D4'],0,notes['C4'],notes['C4'],
]

manaderna_tempo = [
	2,2,2,2,
	2,2,2,2,
	2,2,2,2,
	2,4,4,2,4,

	2,2,2,2,
	2,2,2,2,
	2,2,2,2,
	2,4,4,2,4,

	2,2,2,2,
	2,4,4,2,2,
	2,4,4,2,2,
	2,2,1,4,

	2,2,2,2,
	2,2,2,2,
	2,2,2,2,
	2,4,4,2,
]

bonnagard_melody = [
	notes['C5'],notes['C5'],notes['C5'],notes['G4'],
	notes['A4'],notes['A4'],notes['G4'],
	notes['E5'],notes['E5'],notes['D5'],notes['D5'],
	notes['C5'],0,notes['G4'],

	notes['C5'],notes['C5'],notes['C5'],notes['G4'],
	notes['A4'],notes['A4'],notes['G4'],
	notes['E5'],notes['E5'],notes['D5'],notes['D5'],
	notes['C5'],0,notes['G4'],notes['G4'],

	notes['C5'],notes['C5'],notes['C5'],notes['G4'],notes['G4'],
	notes['C5'],notes['C5'],notes['G4'],
	notes['C5'],notes['C5'],notes['C5'],notes['C5'],notes['C5'],notes['C5'],
	notes['C5'],notes['C5'],notes['C5'],notes['C5'],notes['C5'],notes['C5'],0,

	notes['C5'],notes['C5'],notes['C5'],notes['G4'],
	notes['A4'],notes['A4'],notes['G4'],
	notes['E5'],notes['E5'],notes['D5'],notes['D5'],
	notes['C5'],0,
]

bonnagard_tempo = [
	2,2,2,2,
	2,2,1,
	2,2,2,2,
	1,2,2,

	2,2,2,2,
	2,2,1,
	2,2,2,2,
	1,2,4,4,

	2,2,2,4,4,
	2,2,1,
	4,4,2,4,4,2,
	4,4,4,4,2,2,4,

	2,2,2,2,
	2,2,1,
	2,2,2,2,
	1,1,
]

final_countdown_melody = [
	notes['A3'],notes['E5'],notes['D5'],notes['E5'],notes['A4'],
	notes['F3'],notes['F5'],notes['E5'],notes['F5'],notes['E5'],notes['D5'],
	notes['D3'],notes['F5'],notes['E5'],notes['F5'],notes['A4'],
	notes['G3'],0,notes['D5'],notes['C5'],notes['D5'],notes['C5'],notes['B4'],notes['D5'],
	notes['C5'],notes['A3'],notes['E5'],notes['D5'],notes['E5'],notes['A4'],
	notes['F3'],notes['F5'],notes['E5'],notes['F5'],notes['E5'],notes['D5'],
	notes['D3'],notes['F5'],notes['E5'],notes['F5'],notes['A4'],
	notes['G3'],0,notes['D5'],notes['C5'],notes['D5'],notes['C5'],notes['B4'],notes['D5'],
	notes['C5'],notes['B4'],notes['C5'],notes['D5'],notes['C5'],notes['D5'],
	notes['E5'],notes['D5'],notes['C5'],notes['B4'],notes['A4'],notes['F5'],
	notes['E5'],notes['E5'],notes['F5'],notes['E5'],notes['D5'],
	notes['E5'],
]

final_countdown_tempo = [
	1,16,16,4,4,
	1,16,16,8,8,4,
	1,16,16,4,4,
	2,4,16,16,8,8,8,8,
	4,4,16,16,4,4,
	1,16,16,8,8,4,
	1,16,16,4,4,
	2,4,16,16,8,8,8,8,
	4,16,16,4,16,16,
	8,8,8,8,4,4,
	2,8,4,16,16,
	1,
]

smoke_on_the_water_melody = [
	notes['A3'],notes['C4'],notes['D4'],
	notes['A3'],notes['C4'],notes['DS4'],notes['D4'],
	notes['A3'],notes['C4'],notes['D4'],
	notes['C4'],notes['A3']
]

smoke_on_the_water_tempo = [
	4,4,2.667,
	4,4,8,2,
	4,4,2.667,
	4,1.6
]

playlist = {'final_countdown', 'bonnagard', 'manaderna', 'deck_the_halls', 'crazy_frog', 'twinkle_twinkle'
         'popcorn', 'star_wars', 'super_mario', 'super_mario_underworld', 'adventure_time_melody', 'smoke_on_the_water'}

tunes = {'final_countdown':{'pause':0.3, 'pace':1.2, 'melody': final_countdown_melody, 'tempo': final_countdown_tempo},
        'bonnagard': {'pause':0.3, 'pace':0.8, 'melody': bonnagard_melody, 'tempo': bonnagard_tempo},
        'manaderna': {'pause': 0.3, 'pace': 0.8, 'melody': manaderna_melody, 'tempo': manaderna_tempo},
        'deck_the_halls': {'pause':0.3, 'pace':0.8, 'melody': deck_the_halls_melody, 'tempo': deck_the_halls_tempo},
        'crazy_frog': {'pause':0.3, 'pace':0.9, 'melody': crazy_frog_melody, 'tempo': crazy_frog_tempo},
        'twinkle_twinkle': {'pause':0.5, 'pace':1, 'melody': twinkle_twinkle_melody, 'tempo': twinkle_twinkle_tempo},
        'popcorn': {'pause': 0.5, 'pace': 1, 'melody': popcorn_melody, 'tempo': popcorn_tempo},
        'star_wars': {'pause': 0.2, 'pace': 1.2, 'melody': star_wars_melody, 'tempo': star_wars_tempo},
        'super_mario': {'pause': 1.3, 'pace': 0.8, 'melody': super_mario_melody, 'tempo': super_mario_tempo},
        'super_mario_underworld': {'pause': 1.3, 'pace': 0.8, 'melody': super_mario_underworld_melody, 'tempo': super_mario_underworld_tempo},
        'adventure_time_melody': {'pause': 1.3, 'pace': 1.5, 'melody': adventure_time_melody, 'tempo': adventure_time_tempo},
        'smoke_on_the_water' : {'pause': 0.3, 'pace': 1.4, 'melody': smoke_on_the_water_melody, 'tempo': smoke_on_the_water_tempo}
        }

class chiptune_player(object):
    def buzz(self, frequency, length):	 #create the function "buzz" and feed it the pitch and duration)

    	if(frequency==0):
    		time.sleep(length)
    		return
    	else:
    		p.start(50)
    		p.ChangeFrequency(frequency)
    		time.sleep(length)
    		p.stop()

    def setup(self):
    	GPIO.setmode(GPIO.BCM)
    	GPIO.setup(buzzer_pin, GPIO.IN)
    	GPIO.setup(buzzer_pin, GPIO.OUT)
    	global p
    	p = GPIO.PWM(buzzer_pin, 1)

    def destroy(self):
    	GPIO.cleanup()				# Release resource

    def play(self):
        threading.Thread(target=self.play_song, args = ()).start()

    def play_song(self):
    	for i in range(0, len(self.melody)):		# Play song

    		noteDuration = self.pace/self.tempo[i]
    		self.buzz(self.melody[i],noteDuration)	# Change the frequency along the song note

    		pauseBetweenNotes = noteDuration * self.pause
    		time.sleep(pauseBetweenNotes)
    def __init__(self, arg):
        self.setup()
        self.melody = tunes[arg]['melody']
        self.tempo = tunes[arg]['tempo']
        self.pace = tunes[arg]['pace']
        self.pause = tunes[arg]['pause']
