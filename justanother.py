def play(file, position = 0, duration = 10):
    import vlc, time
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(file)
    player.set_media(media)
    player.audio_set_volume(70)
    player.play()
    player.set_position(0.25)


    time.sleep(duration)
    player.stop()

class tts(object):
    def __init__(self, arg):
        import argparse
        args = False
        parser = argparse.ArgumentParser(description='TTS lang and text parser')
        parser.add_argument('-l', '--lang')
        parser.add_argument('-t', '--text', nargs='+')
        parser.add_argument('aux', nargs='+')
        try:
            args = parser.parse_args(arg)
        except:
            raise ValueError('Not the way m8')
            return
        print('args: '+ str(args))
        if args.text:
            self.text = ''.join(e + ' ' for e in args.text)
        else:
            self.text = ''.join(e + ' ' for e in args.aux)
        if args.lang:
            self.lang = args.lang
        else:
            self.lang = 'es'
    def play_text(self):
        from gtts import gTTS
        import threading
        file = 'tts_files/last_played.mp3'
        tts = gTTS(text=str(self.text), lang=self.lang)
        tts.save(file)
        threading.Thread(target=play, args=[file]).start()
