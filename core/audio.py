import pygame

class AudioManager():
    sounds = {}

    volume_sfx = 1.0
    volume_bgm = 1.0

    channel_track_1 = None
    channel_track_2 = None
    active_track = 1

    @classmethod
    def init_audio(cls):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        
        pygame.mixer.set_num_channels(16)
        pygame.mixer.set_reserved(2)
        
        cls.channel_track_1 = pygame.mixer.Channel(0)
        cls.channel_track_2 = pygame.mixer.Channel(1)

        cls.sounds["atom_click"] = pygame.mixer.Sound("assets/audio/sfx/sfx_atom_click.ogg")
        cls.sounds["atom_release"] = pygame.mixer.Sound("assets/audio/sfx/sfx_atom_release.ogg")
        cls.sounds["button_click"] = pygame.mixer.Sound("assets/audio/sfx/sfx_button_click.ogg")
        cls.sounds["button_release"] = pygame.mixer.Sound("assets/audio/sfx/sfx_button_release.ogg")
        cls.sounds["game_opening"] = pygame.mixer.Sound("assets/audio/sfx/sfx_game_opening.ogg")
        cls.sounds["game_pause"] = pygame.mixer.Sound("assets/audio/sfx/sfx_game_pause.ogg")
        cls.sounds["game_unpause"] = pygame.mixer.Sound("assets/audio/sfx/sfx_game_unpause.ogg")

    @classmethod
    def play_sfx(cls, sound_name):
        if sound_name in cls.sounds:
            cls.sounds[sound_name].set_volume(cls.volume_sfx)
            cls.sounds[sound_name].play()

    @classmethod
    def stop_sfx(cls, sound_name):
        if sound_name in cls.sounds:
            cls.sounds[sound_name].stop()

    @classmethod
    def play_bgm(cls, filepath: str, loop: bool = True):
        try:
            pygame.mixer.music.load(filepath)
            loops = -1 if loop else 0
            pygame.mixer.music.play(loops=loops)
        except pygame.error as e:
            print(f"Failed to load BGM: {filepath}\nError: {e}")

    @classmethod
    def pause_bgm(cls):
        pygame.mixer.music.pause()

    @classmethod
    def unpause_bgm(cls):
        pygame.mixer.music.unpause()

    @classmethod
    def stop_bgm(cls):
        pygame.mixer.music.stop()

    @classmethod
    def fadeout_bgm(cls, ms: int):
        pygame.mixer.music.fadeout(ms)

    @classmethod
    def play_dynamic_bgm(cls, filepath_1: str, filepath_2: str):
        try:
            track_1 = pygame.mixer.Sound(filepath_1)
            track_2 = pygame.mixer.Sound(filepath_2)
            
            cls.channel_track_1.play(track_1, loops=-1)
            cls.channel_track_2.play(track_2, loops=-1)
            
            cls.active_track = 1
            cls.channel_track_1.set_volume(cls.volume_bgm)
            cls.channel_track_2.set_volume(0.0)
            
        except pygame.error as e:
            print(f"Failed to load dynamic BGM.\nError: {e}")

    @classmethod
    def set_active_dynamic_track(cls, track_num: int):
        cls.active_track = track_num
        
        if cls.active_track == 1:
            cls.channel_track_1.set_volume(cls.volume_bgm)
            cls.channel_track_2.set_volume(0.0)
        elif cls.active_track == 2:
            cls.channel_track_1.set_volume(0.0)
            cls.channel_track_2.set_volume(cls.volume_bgm)
    
    @classmethod
    def stop_dynamic_bgm(cls):
        if cls.channel_track_1:
            cls.channel_track_1.stop()
        if cls.channel_track_2:
            cls.channel_track_2.stop()

    @classmethod
    def set_sfx_volume(cls, volume: float):
        cls.volume_sfx = max(0.0, min(1.0, volume)) 
        for sound in cls.sounds.values():
            sound.set_volume(cls.volume_sfx)

    @classmethod
    def set_bgm_volume(cls, volume: float):
        cls.volume_bgm = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(cls.volume_bgm)

        if cls.channel_track_1 and cls.channel_track_2:
            if cls.active_track == 1:
                cls.channel_track_1.set_volume(cls.volume_bgm)
                cls.channel_track_2.set_volume(0.0)
            else:
                cls.channel_track_1.set_volume(0.0)
                cls.channel_track_2.set_volume(cls.volume_bgm)
