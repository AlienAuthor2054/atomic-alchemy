from pygame import mixer

class Audio:
    def __init__(self):
        self.mixer = mixer
        self.mixer.pre_init(44100, -16, 2, 512)
        self.mixer.init()