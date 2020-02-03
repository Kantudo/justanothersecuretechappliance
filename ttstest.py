from gtts import gTTS
import vlc
import time
tts = gTTS('hello')
tts.save('hello.mp3')

instance = vlc.Instance()
player = instance.media_player_new()
media = instance.media_new('./hello.mp3')
player.set_media(media)
player.audio_set_volume(70)
player.set_position(0)

player.play()
time.sleep(10)
