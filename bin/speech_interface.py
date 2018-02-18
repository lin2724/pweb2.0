# coding=utf-8
import time
from baidu_speech_test import get_mp3_by_text
from pygame import mixer # Load the required library


class SpeechText:
    def __init__(self):
        self.m_set_folder_path = 'audio'

        self.do_init()
        pass

    def do_init(self):
        mixer.init(frequency=15050)
        pass

    def set_store_folder(self, folder_path):
        self.m_set_folder_path = folder_path
        pass

    def get_mp3(self, text):
        return get_mp3_by_text(text, self.m_set_folder_path)
        pass

    def play_mp3(self, mp3_file_path):
        mixer.music.load(mp3_file_path)
        mixer.music.play()
        pass

    def do_speech(self, text):
        mp3_file_path = self.get_mp3(text)
        self.play_mp3(mp3_file_path)
        pass

gSpeechHandler = None


def do_speech(text, folder=None):
    global gSpeechHandler
    if not gSpeechHandler:
        gSpeechHandler = SpeechText()
    if folder:
        gSpeechHandler.set_store_folder(folder)
    return gSpeechHandler.do_speech(str(text.encode('utf-8')))
    pass

