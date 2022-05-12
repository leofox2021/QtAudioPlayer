import sys, os, numpy, audio_import, media_player
from mutagen.id3 import ID3
from mutagen import File
from PyQt5 import QtGui, QtCore, uic
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QApplication, QMenuBar
from PyQt5.QtMultimedia import QMediaPlayer
from media_player import MediaPlayer
from audio_import import AudioFileImport
from playlist_import import PlaylistImport


Form, Window = uic.loadUiType("gui/audio_player.ui")


#Set up window
app = QApplication(sys.argv)
window = Window()
form = Form()
form.setupUi(window)
name = form.label


#QT elements
slider = form.horizontalSlider #Position slider
play = form.pushButton #Play button
stop = form.pushButton_2 #Stop button
openfile = form.pushButton_3 #Open file dialog button
prev = form.pushButton_4 #Play previous track
next = form.pushButton_5 #Play next track
open_playlist = form.pushButton_6 #Open playlist button
save_to_playlist = form.pushButton_7 #Create a new playlist
clear = form.pushButton_8 #Clear button
shuffled = form.pushButton_9 #Shuffle button
cover = form.label_3 #Album art
title = form.label #Song title
artist = form.label_4 #Song artist
album = form.label_5 #Song album
timer_display = form.label_6 #Show time
info_bar = form.label_7 #Info bar
volume = form.dial #Volume dial
playlist = form.listWidget #Playlist window
all_playlists = form.listWidget_2
volume_value = form.label_2 #Volume value label
player = QMediaPlayer() #Player


#Menu
preferences = form.actionPreferences

#Variables
all_songs = []


#Assigning icons
#PLAY
play.setIcon(QtGui.QIcon('icons/play.png'))
play.setIconSize(QtCore.QSize(12,12))

#STOP
stop.setIcon(QtGui.QIcon('icons/stop.png'))
stop.setIconSize(QtCore.QSize(12,12))

#PREVIOUS
prev.setIcon(QtGui.QIcon('icons/backward.png'))
prev.setIconSize(QtCore.QSize(24,24))

#NEXT
next.setIcon(QtGui.QIcon('icons/forward.png'))
next.setIconSize(QtCore.QSize(24,24))

#SHUFFLE
shuffled.setIcon(QtGui.QIcon('icons/shuffle.png'))
shuffled.setIconSize(QtCore.QSize(24,24))


#Initial values when the player is started
volume.setRange(0, 100)
volume_value.setText(f'{volume.value()}')
title.setText('Open a music file')
artist.setText('-')
album.setText('-')
slider.setTickInterval(1000)


#Media player class
#  INCLUDES:
#  Play, pause, stop functions
#  Tracking player position, changing volume
#  Displayling tags, displaying time
x = MediaPlayer(player, timer_display, play, title, artist, album, slider, volume, volume_value, cover, playlist, all_songs, shuffled)

#Audio File Import class
#  INCLUDES:
#  Importing files to the 'all_songs' list, using QFileDialog
#  Displaying imported songs in the 'playlist' ListView
#  Current track, next track, previous track methods
#  (each of them returns a 'current song' value that represents an exact path to respective track)
y = AudioFileImport(all_songs, playlist)

#Playlist Import class
#  INCLUDES:
#  Creating a playlist, opening a playlist,
#  Display all playlists in the 'playlists' folder in working directory
z = PlaylistImport(all_playlists, all_songs, playlist, info_bar)


#Load all existing playlists into GUI
z.displayPlaylists()


preferences.triggered.connect(lambda: print('Testing'))

#Buttons
play.clicked.connect(x.playSong)
stop.clicked.connect(x.stopSong)
prev.clicked.connect(x.prevTrack)
next.clicked.connect(x.nextTrack)
openfile.clicked.connect(y.importFromFiles)
save_to_playlist.clicked.connect(z.createPlaylist)
clear.clicked.connect(z.clearPlaylist)


#Playlist
playlist.itemDoubleClicked.connect(x.currentTrack)
all_playlists.itemDoubleClicked.connect(z.openPlaylist)


#Volume slider
volume.sliderMoved.connect(x.volumeChange)
volume.sliderPressed.connect(x.volumeChange)


#Player position and slider
player.positionChanged.connect(x.displayPosition)
slider.valueChanged.connect(x.autoForward)
slider.valueChanged.connect(x.showTime)
slider.sliderReleased.connect(x.changePosition)
slider.sliderMoved.connect(x.showTime)


#App execution
window.show()
app.exec()
