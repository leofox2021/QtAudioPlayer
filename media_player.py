import sys, os, time
from mutagen import File
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QAudioOutput
from PyQt5.QtGui import QPixmap
from audio_import import AudioFileImport

class MediaPlayer:

    #Class constructor
    def __init__(self, player, timer_display, play, title, artist, album, slider, volume, volume_value, cover, playlist, all_songs, shuffled):

        #GUI
        self.timer_display = timer_display
        self.play = play
        self.slider = slider
        self.volume = volume
        self.volume_value = volume_value
        self.cover = cover
        self.playlist = playlist
        self.shuffled = shuffled

        #Variables
        self.current_song = None
        self.all_songs = all_songs
        self.media = ''
        self.imp = AudioFileImport(self.all_songs, self.playlist)
        self.player = player
        self.player.setNotifyInterval(1000)
        self.duration_info = None
        self.duration = None
        self.isplayling = False

        #Attributes
        self.title = title
        self.artist = artist
        self.album = album

    #Audio player function
    def playSong(self):
        if self.isplayling == False:
            #If starting to beggining add 20 ms
            #to avoid annoying clicks and audio glitches
            if self.player.position() == 0:
                self.player.setPosition(20)
                self.player.play()

                self.timer_display.setText(str(time.strftime('%M:%S', time.gmtime(0))))
            else:
                self.player.play()

            self.isplayling = True
            self.play.setIcon(QtGui.QIcon('icons/pause.png'))
            self.play.setIconSize(QtCore.QSize(24,24))
            self.volume.setValue(self.player.volume())
            self.volume_value.setText(f'{self.volume.value()}')
        else:
            self.player.pause()
            self.isplayling = False
            self.play.setIcon(QtGui.QIcon('icons/play.png'))
            self.play.setIconSize(QtCore.QSize(24,24))


    #To stop song from playings
    def stopSong(self):
        self.player.stop()
        self.play.setIcon(QtGui.QIcon('icons/play.png'))
        self.play.setIconSize(QtCore.QSize(24,24))
        self.timer_display.setText(str(time.strftime('%M:%S', time.gmtime(0))))


    #Main player initialization
    #Set a song and path by QUrl
    def initializePlayer(self):
        self.media = self.all_songs[self.current_song]
        self.full_path = os.path.join(self.media)
        self.url = QUrl.fromLocalFile(self.full_path)
        self.song = QMediaContent(self.url)
        self.player.setMedia(self.song)
        self.duration_info = File(self.full_path)
        self.duration = int(self.duration_info.info.length * 1000) - 500
        self.isplayling = False
        self.stopSong()
        self.readTags()
        self.playSong()


    #Play current track
    def currentTrack(self):
        self.current_song = self.imp.currentTrack()
        self.initializePlayer()


    #Play next track
    def nextTrack(self):
        if self.shuffled.isChecked() == True:
            self.current_song = self.imp.shuffledMode()
            self.initializePlayer()
        else:
            if self.playlist.currentRow() +1 == len(self.all_songs):
                print('the playlist has FUCKING ENDED!!!!')
                self.stopSong()
            else:
                print(self.playlist.currentRow())
                print(len(self.all_songs))
                self.current_song = self.imp.nextTrack()
                self.initializePlayer()


    #Play previous track
    def prevTrack(self):
        if self.shuffled.isChecked() == True:
            self.current_song = self.imp.shuffledMode()
            self.initializePlayer()
        else:
            self.current_song = self.imp.previousTrack()
            self.initializePlayer()


    #Change volume by tweaking the dial
    def volumeChange(self):
        self.player.setVolume(self.volume.value())
        self.volume_value.setText(f'{self.volume.value()}')


    #Display current position with hotizontal slider
    def displayPosition(self):
        #print(self.player.duration())
        #print(self.slider.value())
        self.slider.setRange(0, self.player.duration())
        self.slider.setValue(self.player.position())


    #Play next song when player reaches the end
    def autoForward(self):
        if self.slider.value() >= self.duration:
            print('Action triggesed!!!!!!!!!!!!')
            #self.duration = 0
            self.nextTrack()
            self.slider.setValue(self.player.position())

        else:
            #print("You're all fucked up")
            pass


    #Display current position in MM:SS
    def showTime(self):
        #One step of a slider is measured in milliseconds (respectively to the player)
        #time.strftime has to receive seconds, thus converting to seconds by dividing
        current_position = round(self.slider.value() / 1000)

        if self.player.position() <= 20:
            self.timer_display.setText(str(time.strftime('%M:%S', time.gmtime(0))))
        else:
            self.timer_display.setText(str(time.strftime('%M:%S', time.gmtime(current_position))))


    #Change position by omving the slider
    def changePosition(self):
        #If moved all the way to the left, song starts again
        if self.slider.value() <= 2000:
            self.stopSong()
            self.playSong()
        #If moved all the way to the right, song stops
        elif self.slider.value() == self.slider.maximum():
            self.nextTrack()
        else:
            self.player.setPosition(self.slider.value() - 1)


    #Read and display all tags
    def readTags(self):
        if self.full_path == '':
            self.title.setText("No song open")

        #Display title, album and artist
        #Using mutagen library
        else:
            #Avoid crashing due to absent title tag
            try:
                audio_file = File(self.full_path)
                title = audio_file["TIT2"].text[0]
            except Exception:
                title = 'Unknown'
            else:
                title = audio_file["TIT2"].text[0]

            #Avoid crashing due to absent album tag
            try:
                audio_file = File(self.full_path)
                album = audio_file["TALB"].text[0]
            except:
                album = 'Unknown'
            else:
                album = audio_file["TALB"].text[0]

            #Avoid crashing due to absent artist tag
            try:
                audio_file = File(self.full_path)
                artist = audio_file['TPE1'].text[0]
            except:
                artist = 'Unknown'
            else:
                artist = audio_file['TPE1'].text[0]

            #Assign all tags
            self.title.setText(f'{title}')
            self.artist.setText(f'{artist}')
            self.album.setText(f'{album}')


            #Display artwork
            #Using mutagen library
            pixmap = QPixmap()

            #Avoid crashing due to absent covers
            try:
                file = File(self.full_path)
                for tag in file.tags.values():
                    if tag.FrameID == 'APIC':
                        pixmap.loadFromData(tag.data)
                        break
            except Exception:
                self.cover.setPixmap(pixmap)
            else:
                for tag in file.tags.values():
                    if tag.FrameID == 'APIC':
                        pixmap.loadFromData(tag.data)
                        break
                self.cover.setPixmap(pixmap)
