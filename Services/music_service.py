import pygame


def init_music(self, path):
    """
    Initialize the music service with the given path.
    
    :param path: The path to the music directory.
    """
    pygame.mixer.init()
    pygame.mixer.music.load("www/mm.mp3")
    pygame.mixer.music.play(loops=-1)
    self.music_on = True


def toggle_music(self, event=None):
    self.music_canvas.delete("all")
    if self.music_on:
        pygame.mixer.music.stop()
        self.music_icon_loader.draw_icon("sound_off", self.music_canvas.winfo_height()/2, self.music_canvas.winfo_height()/2)
        self.music_on = False
    else:
        pygame.mixer.music.play(loops=-1)
        self.music_icon_loader.draw_icon("sound_on", self.music_canvas.winfo_height()/2, self.music_canvas.winfo_height()/2)
        self.music_on = True